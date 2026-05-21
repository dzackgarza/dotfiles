# Component Catalog

Config sources: `~/.config/hypr/`, `~/.config/waybar/`, `~/.config/ags/`,
`~/.config/rofi/`, `dotfiles/.config-sync/`, `dotfiles/bin/`.

## Window Manager

- **Hyprland 0.55.0** — Primary compositor.
  Config: `~/.config/hypr/hyprland.conf`, `~/.config/hypr/confs/*.conf`. Plugins:
  hyprfocus, dynamic-cursors.
  Utilities: hyprctl, hyprpm, hypridle, hyprlock, hyprsunset, hyprscratch.
- **SwayFX 0.5.3** — Fallback Wayland compositor.
  Config: `dotfiles/.config-sync/sway/config`.

## Bar

- **Waybar** — Status bar.
  Config: `~/.config/waybar/config.jsonc`. Style: `~/.config/waybar/style/full-top.css`.
  Left modules: sway/workspaces, sway/scratchpad, custom/books (opens PDF finder),
  custom/apps (nwggrid), custom/osk, custom/printscreen (grim+slurp to clipboard).
  Center: clock, custom/claude-usage (AGS toggle).
  Right: pulseaudio, cpu, memory, temperature, battery, tray.

## Widgets / Popups

- **AGS (Astal GTK Shell)** — Widget system.
  Powers claude-usage popover in Waybar.
  Config: `~/.config/ags/`. Entry: `app.tsx`. Source: `src/`.

  **Usage tracking (independent of `usage-limits`):** The AGS widget fetches Claude
  usage via its own OAuth pipeline (`services/claude-usage-fetcher.ts`) and Codex usage
  via a standalone curl script (`get_codex_usage.sh`). Results feed the Waybar
  `custom/claude-usage` module (center), which toggles a popover.

## Launchers

- **Rofi** — App launcher and menu system.
  Config: `~/.config/rofi/`.
  - `Mod+D` -> rofi drun (GUI apps) via `~/.config/hypr/scripts/menu.sh`
  - `Mod+A` -> rofi PDF browser from Dropbox/Library via
    `dotfiles/bin/dmenu/dmenuAllPDFs.sh`
  - `Mod+Shift+D` -> emoji picker
  - `Mod+Shift+B` -> website launcher
- **Rofi/dmenu scripts** in `dotfiles/bin/dmenu/` — dmenuAllPDFs, dmenuAnnotatedPDFs,
  dmenuRecentPDFs, dmenu_locate, dmenu_Oldest_Notes, faves_term, faves_wm.

## Notifications

- **dunst** — Notification daemon.
  Config: `dotfiles/.config-sync/dunst/dunstrc`.

## Terminals

- **kitty** — Primary terminal emulator.
- **alacritty** — Used for btop scratchpad.

## Shell

- **Zsh** — Login shell.
  Configs: `dotfiles/zsh/zshrc.symlink`, `~/.config/zsh/*.zsh`. Zinit plugins:
  - zsh-autosuggestions — Fish-like inline autosuggestions from history.
  - zsh-history-substring-search — History search by typing a prefix then up/down.
  - zsh-completions — Extra completion definitions.
  - zsh-syntax-highlighting — Command-line syntax coloring as you type.
  - fzf (junegunn/fzf) — Fuzzy finder; provides `Ctrl+R` history search, `Ctrl+T` file
    search.
  - zsh-z (agkozak/zsh-z) — Frecency-based directory jumping (`z` command).
  - fzf-z-jump (custom) — Interactive `z` directory jump with fzf preview.
- **Starship** — Prompt.
  Config: `~/.config/starship.toml`.
- **atuin** — Shell history search with contextual filtering and sync.
- **zoxide** — Smarter `cd` with frecency ranking.
- **direnv** — Per-directory environment variable loading.
- **exa** — Modern `ls` replacement with icons and git status.
- **base16-shell** — Terminal color scheme framework (managed via tinty).
- **fzf** — Fuzzy finder used for history search, file search, directory jumping.
- **ripgrep** / **ag** — Code search tools used in shell and Neovim.
## Editor

- **Neovim** — Config: `dotfiles/.config-sync/nvim/init.vim`. Plugin manager: vim-plug.
  Plugins:
  - vim-pandoc-syntax — Highlights Pandoc-specific Markdown (embedded LaTeX, citations,
    table alignment, fenced code annotations) that standard Markdown syntax misses.
  - vim-voom — Two-pane outliner synced with document headings; tree-based fold
    navigation and section reordering.
  - quicktex (dzackgarza) — Space-triggered keyword replacement with separate
    dictionaries for math mode vs prose (e.g. `\cl` -> `\mathcal{L}`).
  - vimtex — Continuous background LaTeX compilation (latexmk), forward/inverse search
    with PDF viewer, document outline, motions/completions for labels, citations, and
    commands.
  - fzf / fzf.vim — `:Files`, `:Ag`, `:Rg`, `:Buffers` backed by the fzf native binary.
  - vim-checklist — Toggles `[ ]` / `[x]` checkboxes and tracks completion counts.
  - coc.nvim — LSP client providing autocompletion, diagnostics, code actions.
    Extensions: coc-vimtex, coc-dictionary, coc-word, coc-spell-checker.
  - nerdcommenter — `gc` / `gcc` mappings to comment/uncomment lines in any language.
  - tabular — Align text on delimiter patterns (`:`, `=`, `|`, etc.)
    into aligned columns.
  - vim-table-mode — `:Tableize` converts delimited text into aligned Markdown/Org
    tables with live formatting.
  - nerdtree — Sidebar file explorer with bookmarks, file operations, and git status.
  - vim-nerdtree-syntax-highlight — Colors NERDTree entries by file type.
  - vim-devicons — Adds file-type icon glyphs to NERDTree and other plugins.
  - delimitMate — Inserts matching closing delimiters and wraps selected text.
  - ack.vim — `:Ack` / `:Ag` project search with quickfix-style results.
    Color schemes: flazz/vim-colorschemes, papercolor-theme, flattened (solarized),
    vim-one, mustang-vim.

## File Managers

- **dolphin** — GUI (KDE).
- **yazi** — Terminal (via kitty).
- **ranger** — Terminal.
  Config: `dotfiles/.config-sync/ranger/`.

## Documents / PDFs

- **zotero** — Reference manager (workspace 10).
- **zathura**, **okular** — PDF viewers.

## Media

- **mpv** — Media player.
  Config: `dotfiles/.config-sync/mpv/`.

## Screenshots

- **grimblast + satty** — Print key workflow: select area via rofi, annotate, save.
  Script: `~/.config/hypr/scripts/screenshot.sh`.
- Waybar "Screen Clip" button uses `grim -g "$(slurp)" - | wl-copy` (clipboard only).

## Display

- **hyprsunset** — Blue light filter.
- **autorandr** — Display profiles (home, justhdmi, mobile).

## Input

- **evremap** — Keyboard remapping (systemd user service).

## Systemd User Services

- evremap.service, gitwatch@.service, jupyter-sagemath.service, network-monitor.service

## Startup (from `~/.config/hypr/confs/startup.conf`)

- waybar, hypridle, hyprsunset, nm-applet, copyq, dropbox, bitwarden-desktop, polkit
  agent, AGS (`ags run ~/.config/ags`), zotero (workspace 10), hyprscratch.

## Scripts (dotfiles/bin/)

### Document finders (`dmenu/`)

- `dmenuAllPDFs.sh` — Browse and open PDFs from Dropbox/Library via rofi.
- `dmenuAnnotatedPDFs.sh` — Browse PDFs with existing annotations.
- `dmenuRecentPDFs.sh` — Browse recently modified PDFs.
- `dmenu_locate.sh` — File search via locate with rofi.
- `dmenu_Oldest_Notes.sh` — Browse notes by oldest modification time.
- `faves_term.sh` / `faves_wm.sh` — Launch favorite terminal / GUI apps.

### Utility scripts (`launcher/`)

- `clean-history` — Remove duplicate/trivial entries from Zsh history.
- `cursor-clean` — Clear Cursor editor cache files.
- `llm-rofi` — Browse and select LLM prompt templates via rofi.
- `sysinfo` — Display comprehensive system diagnostics.
- `theme-switcher` — Preview and switch base16-shell themes.

### LLM integration (`llm-scripts/`)

- `askterm` — Convert natural language to shell commands via Groq API.
- `amplify-prompt` — Opens a dialog to expand a short prompt into detailed instructions.
- `llm-query` — Send a one-shot query to an LLM from the command line.
- `llm-repl` — REPL chat interface for Gemini/other LLMs with history.
- `bash-code-review.py` — Review shell scripts for errors and style issues.
- `python-code-review.py` — Review Python code for bugs and style via Groq.
- `math-reviewer` — Review mathematical thesis content via LLM.
- `doc-expander.py` — Expand compressed notes into full prose.

### Pandoc / Document conversion (`pandoc/`)

- `pandoc_paper_totex.sh` — Convert Markdown paper to LaTeX.
- `pandoc_totex_orpdf.sh` — Convert Markdown to LaTeX or PDF.
- `pandoc_tohtml.sh` — Convert Markdown to HTML.
- `pandoc_stripmacros.sh` — Strip LaTeX macro definitions from files.
- `pdfpreview.sh` — Open PDF preview in zathura.
- `vimpreview.sh` — Open HTML preview in qutebrowser.
- `tikz_to_svg.sh` — Convert TikZ diagrams to SVG.
- `ankdown.py` / `ankdown_bk.py` — Generate Anki flashcards from Markdown.

### Flashcard tools (`flashcards/`)

- `flashcards_unified.py` — Unified Anki flashcard generator with configurable
  templates.

### Note-taking (`notes/`)

- `newnote.sh` — Create a new dated note file.
- `newcard.sh` — Create a new Anki card.
- `newzet.sh` — Create a new Zettelkasten note.
- `inkscape-figures.sh` — Insert Inkscape figure into document.
- `stylus_autosave_file.sh` — Trigger save in stylus writing app.

### Media control (`mpv_scripts/`)

- `mpv_toggle.sh` — Play/pause mpv via socat.
- `mpv_ff.sh` / `mpv_rw.sh` — Seek forward/backward 3 seconds.
- `mpv_speedup.sh` / `mpv_slowdown.sh` — Increase/decrease playback speed.

### Window management (`i3_and_wm_scripts/`)

- `slurpshot` / `slurpshot2` — Screenshot scripts using grim, slurp, bemenu (legacy).
- `recentlyAnnotatedPDFs.sh` / `recentlyOpenedPDFs.sh` — Browse recent PDFs (legacy).
- `change_wallpaper_reddit.py` — Pull wallpapers from Reddit.
- `popup-calendar.sh` — Calendar popup for polybar.
- `mic_muted.sh` — Check microphone mute status.
- `vim_anywhere.sh` — Open a temporary Vim/Neovim buffer for quick editing.
- `i3-get-window-criteria` — Get i3 window criteria for config rules.
- `polybar.sh` — Launch polybar.

### Misc utilities (`misc_utils/`)

- `compresspdf` — Compress PDFs using Ghostscript.
- `calibre-convert.sh` / `convert-epub-to-pdf` — E-book format conversion.
- `diffwrap` — External diff tool wrapper for Git.
- `fixbluetooth.sh` — Restart Bluetooth service.
- `insblank.sh` — Insert blank pages into a PDF.
- `biblatex_check.py` — Check BibLaTeX entries for missing fields.
- `aurtab.py` — Tab-completion cache generator for `yay`/AUR packages.
- `palette_generator.sh` — Generate terminal color palettes.
- `unicode_strip` — Strip non-ASCII characters from text.
- `tewisay` — Cowsay-style speaking cow (compiled binary).
- `256color` / `colortest` — Display terminal color charts.

### Top-level scripts

- `clip` — Clipboard management utility.
- `combiner` — Merge paragraphs separated by blank lines.
- `cpu-info-print` — Print detailed CPU information.
- `dedup-fuzzy-history` — Deduplicate Zsh history using fuzzy matching.
- `dot-to-cytoscape` / `dot-to-vis` — Convert Graphviz DOT to Cytoscape/Vis.js JSON.
- `extract-singleline-history` — Extract single-line commands from Zsh history.
- `fast-cursor` — Toggle cursor speed settings.
- `fdd` — Fuzzy directory changer (like zoxide/fasd).
- `fetch-pandoc-mcp` — MCP server for URL-to-Markdown conversion via Pandoc.
- `find-all-latex-labels` / `find-project-labels` / `find-project-labels-py` — Extract
  LaTeX `\label`/`\cref` references.
- `fix-details` — Fix file metadata/details.
- `i3-setup` — Apply X11 keyboard settings (legacy).
- `initNotes` — Initialize a Markdown paper directory with Makefile.
- `lock` / `unlock` — Recursively set files read-only / writable.
- `mathpix-convert` / `mathpix-snip` — Math OCR via Mathpix API.
- `md-pandoc` — Compile Markdown to PDF via Pandoc.
- `newpaper` — Scaffold a new academic paper directory.
- `open-with-nvim` — Open file in Neovim from external launcher.
- `qual-update` — Update qualification exam progress tracker.
- `remarkable-put` — Upload file to reMarkable tablet via rmapi.
- `sage-capability-assertions` — Verify SageMath capabilities.
- `script-launcher` — Rofi-based script launcher with descriptions.
- `smart-pandoc-debugger` — Diagnose Pandoc build errors in Markdown+LaTeX.
- `starship-style` — Switch between Starship prompt themes.
- `stt` / `stt-hold` — Real-time speech-to-text via Vosk with grammar correction.
- `sway-random-bg` — Set random wallpaper from a directory.
- `system-info` — Display system information snapshot.
- `toggle-osk` — Toggle on-screen keyboard (wvkbd).
- `unresolved-links` — Scan Obsidian vault for unresolved `[[wikilinks]]`.
- `update-max-upload` — Update max upload size for Waybar display.
- `watch-changes` — Watch directory for changes and run a command.
- `wkill` — Click on a window to kill it (slurp + wmctrl/hyprctl).
- `xpand-paper` — Expand/compile a paper from Markdown sources.
- `xpandlatex` / `xpandlatex-new` — Expand LaTeX macros/includes into single file.

## Historical Configs

Configs still in the repo from before the switch to Wayland:

- **i3** — X11 window manager.
  Config: `dotfiles/.config-sync/i3/config`.
- **polybar** — X11 status bar.
  Config: `dotfiles/.config-sync/polybar/config`.
- **picom** — X11 compositor.
  Config: `dotfiles/.config-sync/picom.conf`.
- **eww** — Widget system (previously used, superseded by AGS).
- **termite** — Terminal emulator.
- **twmn** — Notification system (previously used, superseded by dunst).
