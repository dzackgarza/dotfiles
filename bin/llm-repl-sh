from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
import re

class ChatREPL:
    def __init__(self):
        self.console = Console()

    def render_markdown_with_code(self, text: str):
        """Render markdown with syntax-highlighted code blocks using rich."""
        # Split text into markdown and code blocks
        code_block_pattern = re.compile(r'```(\w+)?\n([\s\S]*?)```', re.MULTILINE)
        last_end = 0
        for match in code_block_pattern.finditer(text):
            # Print markdown before the code block
            if match.start() > last_end:
                md_chunk = text[last_end:match.start()]
                if md_chunk.strip():
                    self.console.print(Markdown(md_chunk))
            lang = match.group(1) or "python"
            code = match.group(2)
            self.console.print(Syntax(code, lang, theme="monokai", line_numbers=False))
            last_end = match.end()
        # Print any remaining markdown after the last code block
        if last_end < len(text):
            md_chunk = text[last_end:]
            if md_chunk.strip():
                self.console.print(Markdown(md_chunk))

    def display_messages(self):
        """Display all messages in the chat, with markdown/code formatting for assistant."""
        print("\n" + "="*60)
        for message in self.messages[-20:]:  # Show last 20 messages
            if message.type == MessageType.ASSISTANT:
                timestamp = message.timestamp.strftime("%H:%M:%S")
                self.console.print(f"[bold blue][{timestamp}] Assistant:[/bold blue]")
                self.render_markdown_with_code(message.content)
            else:
                print_formatted_text(self.format_message(message), style=self.style)
        print("="*60 + "\n") 