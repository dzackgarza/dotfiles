#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4>=4.12,<5", "requests>=2.32,<3"]
# ///
"""Search LibGen and Anna's Archive in rofi and store a selected PDF in live Zotero."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Self

import requests
from bs4 import BeautifulSoup

MIRRORS_CONFIG_URL = "https://raw.githubusercontent.com/obsfx/libgen-downloader/configuration/config.v3.json"
ANNAS_CLI = ["uvx", "--from", "annas-archive-cli==0.2.0rc4", "anna"]
ANNAS_RESULT_LIMIT = 50
ANNAS_MAX_WAIT_SECONDS = 300
LIBGEN = "LibGen"
ANNAS = "Anna's"
ZOTERO_URL = "http://127.0.0.1:23119"
MD5_PATTERN = re.compile(r"md5=([0-9a-f]{32})")
URL_PATTERN = re.compile(r"Here is the direct download link:\s*(https?://\S+)")
LOG_PATH = Path.home() / ".local/state/libgen-to-zotero.log"
LOG = logging.getLogger("libgen-to-zotero")


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    size: str
    md5: str
    sources: frozenset[str]

    @property
    def label(self) -> str:
        sources = "+".join(sorted(self.sources))
        return f"[{sources}] {self.title} | {self.author} | PDF {self.size} | {self.md5[:8]}"


class Progress:
    """Keep a visible stage indicator open during network and Zotero work."""

    def __init__(self, title: str, stage: str) -> None:
        self.title = title
        self.stage = stage
        self.process: subprocess.Popen[str] | None = None

    def __enter__(self) -> Self:
        self.process = subprocess.Popen(
            [
                "zenity",
                "--progress",
                "--pulsate",
                "--no-cancel",
                "--auto-close",
                "--title",
                self.title,
                "--text",
                self.stage,
                "--width",
                "440",
            ],
            stdin=subprocess.PIPE,
            text=True,
        )
        self.update(self.stage)
        return self

    def update(self, stage: str) -> None:
        LOG.info(stage)
        if (
            self.process is None
            or self.process.stdin is None
            or self.process.poll() is not None
        ):
            raise RuntimeError(
                "The progress window closed before the operation finished"
            )
        self.process.stdin.write(f"# {stage}\n")
        self.process.stdin.flush()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.process is None or self.process.stdin is None:
            return
        if self.process.poll() is None:
            self.process.stdin.write("100\n")
            self.process.stdin.close()
        status = self.process.wait(timeout=5)
        if status != 0 and exc is None:
            raise RuntimeError(f"The progress window exited with status {status}")


def message(kind: str, title: str, body: str) -> None:
    notification = subprocess.run(
        [
            "notify-send",
            "-a",
            "PDF to Zotero",
            "-u",
            "critical" if kind == "error" else "normal",
            title,
            body,
        ],
        check=False,
    )
    if notification.returncode != 0:
        LOG.error(
            "Could not show %s notification: exit status %s",
            kind,
            notification.returncode,
        )
    result = subprocess.run(
        ["zenity", f"--{kind}", "--title", title, "--text", body, "--width", "440"],
        check=False,
    )
    if result.returncode != 0:
        LOG.error("Could not show %s dialog: exit status %s", kind, result.returncode)


def menu(prompt: str, choices: list[str] | None = None) -> str | None:
    result = subprocess.run(
        ["rofi", "-dmenu", "-i", "-p", prompt, "-l", "15"],
        input="\n".join(choices) if choices is not None else "",
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 1 and not result.stderr.strip():
        return None
    if result.returncode != 0:
        raise RuntimeError(
            f"The search menu failed: {result.stderr.strip() or result.returncode}"
        )
    return result.stdout.strip() or None


def search_libgen(query: str) -> list[Book]:
    config_response = requests.get(MIRRORS_CONFIG_URL, timeout=15)
    config_response.raise_for_status()
    mirrors = config_response.json()["mirrors"]
    table = None
    for mirror in mirrors:
        LOG.info("Searching mirror: %s", mirror["src"])
        try:
            response = requests.get(
                f"{mirror['src'].rstrip('/')}/index.php",
                params={"req": query, "page": 1, "res": 100},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            LOG.warning("Search mirror failed: %s", error)
            continue
        page = BeautifulSoup(response.text, "html.parser")
        error_banner = page.select_one(".alert-danger")
        if error_banner is not None:
            LOG.warning(
                "Search mirror reported an error: %s",
                error_banner.get_text(" ", strip=True),
            )
            continue
        table = page.select_one("#tablelibgen")
        if table is not None:
            break
        submitted_query = page.select_one('form[action="index.php"] input[name="req"]')
        if submitted_query is not None and submitted_query.get("value") == query:
            return []
        LOG.warning("Search mirror returned no results table: %s", mirror["src"])
    if table is None:
        raise RuntimeError("No LibGen search mirror returned a results table")
    books: list[Book] = []
    for row in table.select("tr"):
        cells = row.find_all("td", recursive=False)
        if len(cells) < 9 or cells[7].get_text(" ", strip=True).lower() != "pdf":
            continue
        title = cells[0].select_one('a[href^="edition.php"]')
        mirror = cells[8].select_one('a[href*="md5="]')
        if title is None or mirror is None:
            continue
        match = MD5_PATTERN.search(mirror.get("href", ""))
        if match is None:
            continue
        books.append(
            Book(
                title=title.get_text(" ", strip=True),
                author=cells[1].get_text(" ", strip=True),
                size=cells[6].get_text(" ", strip=True),
                md5=match.group(1),
                sources=frozenset({LIBGEN}),
            )
        )
    return books


def search_annas(query: str) -> list[Book]:
    LOG.info("Searching Anna's Archive")
    result = subprocess.run(
        [
            *ANNAS_CLI,
            "search",
            query,
            "--ext",
            "pdf",
            "--limit",
            str(ANNAS_RESULT_LIMIT),
            "--json",
        ],
        text=True,
        capture_output=True,
        check=False,
        timeout=180,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Anna's Archive search failed: {(result.stderr or result.stdout).strip()[-500:]}"
        )
    records = json.loads(result.stdout)
    return [
        Book(
            title=record["title"],
            author=record["author"],
            size=record["size"],
            md5=record["md5"],
            sources=frozenset({ANNAS}),
        )
        for record in records
        if record["format"] == "pdf"
    ]


def search(query: str) -> list[Book]:
    """LibGen results first, then Anna's; one entry per MD5 naming every source."""
    with ThreadPoolExecutor(max_workers=2) as pool:
        libgen = pool.submit(search_libgen, query)
        annas = pool.submit(search_annas, query)
        books = [*libgen.result(), *annas.result()]
    merged: dict[str, Book] = {}
    for book in books:
        seen = merged.get(book.md5)
        if seen is None:
            merged[book.md5] = book
            continue
        merged[book.md5] = Book(
            title=seen.title,
            author=seen.author,
            size=seen.size,
            md5=seen.md5,
            sources=seen.sources | book.sources,
        )
    return list(merged.values())


def resolve(md5: str) -> str:
    result = subprocess.run(
        ["bunx", "--yes", "libgen-downloader@3.4.0", "-u", md5],
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"LibGen could not resolve {md5}: {(result.stderr or result.stdout).strip()[-500:]}"
        )
    match = URL_PATTERN.search(result.stdout)
    if match is None:
        raise RuntimeError(f"LibGen did not resolve {md5}: {result.stdout.strip()}")
    return match.group(1)


def check_zotero() -> None:
    response = requests.get(f"{ZOTERO_URL}/version", timeout=10)
    response.raise_for_status()
    status = response.json()
    if not status.get("healthy") or "attach_standalone" not in status.get(
        "capabilities", []
    ):
        raise RuntimeError(
            "The live Zotero add-on does not support standalone attachments"
        )


def download(url: str, md5: str, path: Path, progress: Progress) -> None:
    digest = hashlib.md5()
    downloaded = 0
    reported = 0
    with requests.get(url, stream=True, timeout=(15, 60)) as response:
        response.raise_for_status()
        with path.open("wb") as output:
            first = True
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                if first and not chunk.startswith(b"%PDF-"):
                    raise RuntimeError(
                        "The download URL returned a file that is not a PDF"
                    )
                first = False
                output.write(chunk)
                digest.update(chunk)
                downloaded += len(chunk)
                if downloaded - reported >= 1048576:
                    progress.update(
                        f"Downloading PDF: {downloaded / 1048576:.1f} MB received"
                    )
                    reported = downloaded
    if digest.hexdigest() != md5:
        raise RuntimeError(f"Downloaded PDF does not match catalog MD5 {md5}")
    progress.update(f"PDF verified: {downloaded / 1048576:.1f} MB, MD5 matches")


def attach(book: Book, path: Path) -> str:
    response = requests.post(
        f"{ZOTERO_URL}/attach",
        json={"title": book.title, "file_path": str(path)},
        timeout=120,
    )
    if not response.ok:
        raise RuntimeError(
            f"Zotero rejected the PDF (HTTP {response.status_code}): {response.text[:500]}"
        )
    result = response.json()
    if result.get("success") is not True or not result.get("attachment_key"):
        raise RuntimeError(f"Zotero did not confirm the attachment: {result}")
    return result["attachment_key"]


def main() -> None:
    query = menu("LibGen search")
    if query is None:
        LOG.info("Search canceled")
        return
    LOG.info("Search requested: %s", query)
    with Progress("LibGen search", "Searching LibGen mirrors"):
        books = search(query)
    if not books:
        LOG.info("No PDF results for %s", query)
        message("info", "LibGen search", f"No PDF results for: {query}")
        return
    LOG.info("PDF results: %d", len(books))
    chosen = menu("Send PDF to Zotero", [book.label for book in books])
    if chosen is None:
        LOG.info("Result selection canceled")
        return
    book = next((book for book in books if book.label == chosen), None)
    if book is None:
        raise RuntimeError("Choose a listed PDF")
    LOG.info("Selected PDF: %s [%s]", book.title, book.md5)
    with Progress("LibGen to Zotero", "Checking live Zotero") as progress:
        check_zotero()
        progress.update("Finding a working PDF link")
        url = resolve(book.md5)
        progress.update("Downloading PDF")
        with tempfile.NamedTemporaryFile(
            prefix="libgen-", suffix=".pdf", dir="/tmp", delete=False
        ) as staged:
            path = Path(staged.name)
        try:
            download(url, book.md5, path, progress)
            progress.update("Adding PDF as a standalone Zotero item")
            key = attach(book, path)
            LOG.info("Zotero stored item: %s [%s]", key, book.md5)
        finally:
            subprocess.run(["trash", str(path)], check=True)
        progress.update(f"Zotero item added: {key}")
    LOG.info("Completed Zotero item: %s [%s]", key, book.md5)
    message("info", "PDF added to Zotero", f"{book.title}\nZotero item: {key}")


if __name__ == "__main__":
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        main()
    except (
        OSError,
        requests.RequestException,
        subprocess.SubprocessError,
        RuntimeError,
        KeyError,
        ValueError,
    ) as error:
        LOG.exception("Workflow failed")
        print(f"LibGen to Zotero failed: {error}. Log: {LOG_PATH}", file=sys.stderr)
        message("error", "LibGen to Zotero failed", f"{error}\n\nLog: {LOG_PATH}")
        sys.exit(1)
