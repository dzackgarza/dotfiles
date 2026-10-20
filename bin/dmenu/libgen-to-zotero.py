#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4>=4.12,<5", "requests>=2.32,<3"]
# ///
"""Search LibGen in rofi and store a selected PDF in live Zotero."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://libgen.li/index.php"
ZOTERO_URL = "http://127.0.0.1:23119"
MD5_PATTERN = re.compile(r"md5=([0-9a-f]{32})")
URL_PATTERN = re.compile(r"Here is the direct download link:\s*(https?://\S+)")


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    size: str
    md5: str

    @property
    def label(self) -> str:
        return f"{self.title} | {self.author} | PDF {self.size} | {self.md5[:8]}"


def menu(prompt: str, choices: list[str] | None = None) -> str | None:
    result = subprocess.run(
        ["rofi", "-dmenu", "-i", "-p", prompt, "-l", "15"],
        input="\n".join(choices) if choices is not None else "",
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def search(query: str) -> list[Book]:
    response = requests.get(
        SEARCH_URL,
        params={"req": query, "page": 1, "res": 100},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()
    page = BeautifulSoup(response.text, "html.parser")
    books: list[Book] = []
    table = page.select_one("#tablelibgen")
    if table is None:
        raise RuntimeError("LibGen returned no results table")
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
            )
        )
    return books


def resolve(md5: str) -> str:
    result = subprocess.run(
        ["bunx", "--yes", "libgen-downloader@3.4.0", "-u", md5],
        text=True,
        capture_output=True,
        check=True,
        timeout=120,
    )
    match = URL_PATTERN.search(result.stdout)
    if match is None:
        raise RuntimeError(f"LibGen did not resolve {md5}: {result.stdout.strip()}")
    return match.group(1)


def check_zotero() -> None:
    response = requests.get(f"{ZOTERO_URL}/version", timeout=10)
    response.raise_for_status()
    status = response.json()
    if not status.get("healthy") or "attach_standalone" not in status.get("capabilities", []):
        raise RuntimeError("The live Zotero add-on does not support standalone attachments")


def download(url: str, md5: str, path: Path) -> None:
    digest = hashlib.md5()
    with requests.get(url, stream=True, timeout=(15, 60)) as response:
        response.raise_for_status()
        with path.open("wb") as output:
            first = True
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                if first and not chunk.startswith(b"%PDF-"):
                    raise RuntimeError("The download URL returned a file that is not a PDF")
                first = False
                output.write(chunk)
                digest.update(chunk)
    if digest.hexdigest() != md5:
        raise RuntimeError(f"Downloaded PDF does not match catalog MD5 {md5}")


def attach(book: Book, path: Path) -> str:
    response = requests.post(
        f"{ZOTERO_URL}/attach",
        json={"title": book.title, "file_path": str(path)},
        timeout=120,
    )
    response.raise_for_status()
    result = response.json()
    if result.get("success") is not True or not result.get("attachment_key"):
        raise RuntimeError(f"Zotero did not confirm the attachment: {result}")
    return result["attachment_key"]


def notify(title: str, message: str) -> None:
    subprocess.run(["notify-send", title, message], check=False)


def main() -> None:
    query = menu("LibGen search")
    if query is None:
        return
    books = search(query)
    if not books:
        notify("LibGen", "No PDF results")
        return
    chosen = menu("Send PDF to Zotero", [book.label for book in books])
    if chosen is None:
        return
    book = next((book for book in books if book.label == chosen), None)
    if book is None:
        raise RuntimeError("Choose a listed PDF")
    check_zotero()
    url = resolve(book.md5)
    with tempfile.NamedTemporaryFile(prefix="libgen-", suffix=".pdf", dir="/tmp", delete=False) as staged:
        path = Path(staged.name)
    try:
        download(url, book.md5, path)
        key = attach(book, path)
    finally:
        subprocess.run(["trash", str(path)], check=True)
    notify("Zotero PDF added", f"{book.title}\n{key}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, requests.RequestException, subprocess.SubprocessError, RuntimeError) as error:
        print(error, file=sys.stderr)
        notify("LibGen to Zotero failed", str(error)[:300])
        sys.exit(1)
