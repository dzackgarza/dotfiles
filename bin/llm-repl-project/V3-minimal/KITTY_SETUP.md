# Kitty Terminal Setup for LLM REPL

LLM REPL V3-minimal works best with [Kitty terminal](https://sw.kovidgoyal.net/kitty/) for proper Shift+Enter key detection.

## Why Kitty?

Most terminal emulators cannot distinguish between `Enter` and `Shift+Enter` - they send the same key codes to applications. Kitty has advanced keyboard protocol support that allows applications like Textual to detect modifier keys properly.

## Installation

### Arch Linux / Arch-based
```bash
sudo pacman -S kitty
```

### Ubuntu/Debian
```bash
sudo apt install kitty
```

### macOS
```bash
brew install kitty
```

### From source
```bash
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
```

## Configuration

1. **Use the provided config**: Copy `kitty-llm-repl.conf` to your kitty config:
   ```bash
   cp kitty-llm-repl.conf ~/.config/kitty/kitty.conf
   ```

2. **Or add these key lines to your existing kitty.conf**:
   ```conf
   # Ensure Shift+Enter is passed through to applications
   map shift+enter no_op
   
   # Optional: Enable enhanced keyboard protocol
   # (helps with advanced key detection)
   ```

## Key Behavior in LLM REPL

With Kitty properly configured:

- **Enter**: Send message to LLM
- **Shift+Enter**: Insert newline in input field
- **Ctrl+C**: Quit application

## Testing Key Detection

Run the key debugging tool to verify your setup:

```bash
pdm run python test_kitty_keys.py
```

This will show you exactly what key events are being detected. You should see:
- `'enter'` when pressing Enter
- `'shift+enter'` when pressing Shift+Enter

## Fallback for Other Terminals

If you cannot use Kitty, the application provides these alternatives:

1. **Alt+Enter**: Send message (works in most terminals)
2. **Enter**: Insert newline (natural behavior)

To enable Alt+Enter mode, uncomment the Alt+Enter handler in `src/widgets/prompt_input.py`.

## Troubleshooting

### Shift+Enter not working?

1. **Check your terminal**: Run `echo $TERM` - should show `xterm-kitty` or similar
2. **Test key detection**: Use the debug tool above
3. **Check config**: Ensure no conflicting keybindings in your kitty.conf
4. **Try debug mode**: Start kitty with `kitty --debug-input` to see raw key events

### Still having issues?

1. **Verify Kitty version**: `kitty --version` (needs 0.19+)
2. **Reset config**: Try with minimal kitty.conf
3. **Check environment**: Some terminal multiplexers (screen, tmux) can interfere

## Advanced Configuration

For power users, you can customize the key behavior by modifying `kitty-llm-repl.conf`:

```conf
# Send specific escape sequences for better detection
map shift+enter send_text all \x1b[13;2u

# Disable conflicting shortcuts
map ctrl+shift+enter no_op
map ctrl+enter no_op
```

## Performance Tips

The provided config includes optimizations for terminal applications:

- Reduced input delay (3ms)
- Optimized repaint timing
- Disabled audio bells
- Proper scrollback settings

This ensures smooth operation of the LLM REPL interface.