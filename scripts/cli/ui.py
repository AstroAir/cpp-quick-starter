"""
Beautiful CLI UI utilities - colors, spinners, prompts, and more.
Inspired by npm/yarn CLI experience.
"""

import os
import sys
import time
import threading
from typing import Optional, List, Callable, Any, TypeVar
from dataclasses import dataclass
from enum import Enum

T = TypeVar("T")


class Colors:
    """ANSI color codes for terminal output."""

    # Basic colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"

    # Reset
    RESET = "\033[0m"

    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports colors."""
        if os.environ.get("NO_COLOR"):
            return False
        if os.environ.get("FORCE_COLOR"):
            return True
        if not hasattr(sys.stdout, "isatty"):
            return False
        if not sys.stdout.isatty():
            return False
        if sys.platform == "win32":
            try:
                import ctypes

                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except Exception:
                return os.environ.get("TERM") is not None
        return True


# Global color support flag
_color_enabled = Colors.supports_color()


def set_color_enabled(enabled: bool) -> None:
    """Enable or disable colors globally."""
    global _color_enabled
    _color_enabled = enabled


def c(text: str, *styles: str) -> str:
    """Apply color/style to text."""
    if not _color_enabled or not styles:
        return text
    return "".join(styles) + text + Colors.RESET


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    import re

    return re.sub(r"\033\[[0-9;]*m", "", text)


# Convenience color functions
def red(text: str) -> str:
    return c(text, Colors.RED)


def green(text: str) -> str:
    return c(text, Colors.GREEN)


def yellow(text: str) -> str:
    return c(text, Colors.YELLOW)


def blue(text: str) -> str:
    return c(text, Colors.BLUE)


def magenta(text: str) -> str:
    return c(text, Colors.MAGENTA)


def cyan(text: str) -> str:
    return c(text, Colors.CYAN)


def white(text: str) -> str:
    return c(text, Colors.WHITE)


def dim(text: str) -> str:
    return c(text, Colors.DIM)


def bold(text: str) -> str:
    return c(text, Colors.BOLD)


def success(text: str) -> str:
    return c(text, Colors.GREEN, Colors.BOLD)


def error(text: str) -> str:
    return c(text, Colors.RED, Colors.BOLD)


def warning(text: str) -> str:
    return c(text, Colors.YELLOW, Colors.BOLD)


def info(text: str) -> str:
    return c(text, Colors.CYAN)


def highlight(text: str) -> str:
    return c(text, Colors.MAGENTA, Colors.BOLD)


# Symbols
class Symbols:
    """Unicode symbols for CLI output."""

    # Status
    SUCCESS = "✔" if _color_enabled else "[OK]"
    ERROR = "✖" if _color_enabled else "[X]"
    WARNING = "⚠" if _color_enabled else "[!]"
    INFO = "ℹ" if _color_enabled else "[i]"
    QUESTION = "?" if _color_enabled else "[?]"

    # Arrows
    ARROW_RIGHT = "→" if _color_enabled else "->"
    ARROW_LEFT = "←" if _color_enabled else "<-"
    ARROW_UP = "↑" if _color_enabled else "^"
    ARROW_DOWN = "↓" if _color_enabled else "v"
    POINTER = "❯" if _color_enabled else ">"

    # Progress
    BULLET = "●" if _color_enabled else "*"
    CIRCLE = "○" if _color_enabled else "o"
    SQUARE = "■" if _color_enabled else "#"
    STAR = "★" if _color_enabled else "*"

    # Misc
    LINE = "─" if _color_enabled else "-"
    VERTICAL = "│" if _color_enabled else "|"
    CORNER_TL = "┌" if _color_enabled else "+"
    CORNER_TR = "┐" if _color_enabled else "+"
    CORNER_BL = "└" if _color_enabled else "+"
    CORNER_BR = "┘" if _color_enabled else "+"


class Spinner:
    """Animated spinner for long-running operations."""

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    FRAMES_SIMPLE = ["|", "/", "-", "\\"]

    def __init__(self, message: str = "", use_simple: bool = False):
        self.message = message
        self.frames = self.FRAMES_SIMPLE if use_simple or not _color_enabled else self.FRAMES
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.current_frame = 0

    def _spin(self) -> None:
        while self.running:
            frame = self.frames[self.current_frame % len(self.frames)]
            sys.stdout.write(f"\r{cyan(frame)} {self.message}")
            sys.stdout.flush()
            self.current_frame += 1
            time.sleep(0.08)

    def start(self, message: Optional[str] = None) -> "Spinner":
        if message:
            self.message = message
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()
        return self

    def stop(self, final_message: Optional[str] = None, symbol: str = "") -> None:
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.2)
        # Clear spinner line
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        if final_message:
            print(f"{symbol} {final_message}" if symbol else final_message)
        sys.stdout.flush()

    def succeed(self, message: Optional[str] = None) -> None:
        self.stop(message or self.message, green(Symbols.SUCCESS))

    def fail(self, message: Optional[str] = None) -> None:
        self.stop(message or self.message, red(Symbols.ERROR))

    def warn(self, message: Optional[str] = None) -> None:
        self.stop(message or self.message, yellow(Symbols.WARNING))

    def info(self, message: Optional[str] = None) -> None:
        self.stop(message or self.message, blue(Symbols.INFO))

    def __enter__(self) -> "Spinner":
        return self.start()

    def __exit__(self, *args: Any) -> None:
        if self.running:
            self.succeed()


class ProgressBar:
    """Progress bar for operations with known length."""

    def __init__(
        self,
        total: int,
        width: int = 40,
        prefix: str = "",
        fill: str = "█",
        empty: str = "░",
    ):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.fill = fill if _color_enabled else "#"
        self.empty = empty if _color_enabled else "-"
        self.current = 0

    def update(self, current: Optional[int] = None, message: str = "") -> None:
        if current is not None:
            self.current = current
        else:
            self.current += 1

        percent = self.current / self.total if self.total > 0 else 1
        filled = int(self.width * percent)
        bar = self.fill * filled + self.empty * (self.width - filled)

        percent_str = f"{percent * 100:5.1f}%"
        line = f"\r{self.prefix}[{cyan(bar)}] {percent_str}"
        if message:
            line += f" {dim(message)}"

        sys.stdout.write(line)
        sys.stdout.flush()

        if self.current >= self.total:
            print()

    def __enter__(self) -> "ProgressBar":
        return self

    def __exit__(self, *args: Any) -> None:
        if self.current < self.total:
            print()


def print_banner(title: str, subtitle: str = "", version: str = "") -> None:
    """Print a beautiful ASCII banner."""
    banner = r"""
  _____ _____  _____     _____ _             _
 / ____|  __ \|  __ \   / ____| |           | |
| |    | |__) | |__) | | (___ | |_ __ _ _ __| |_ ___ _ __
| |    |  ___/|  ___/   \___ \| __/ _` | '__| __/ _ \ '__|
| |____| |    | |       ____) | || (_| | |  | ||  __/ |
 \_____|_|    |_|      |_____/ \__\__,_|_|   \__\___|_|
"""
    print(cyan(banner))
    print(f"  {bold(title)}")
    if subtitle:
        print(f"  {dim(subtitle)}")
    if version:
        print(f"  {dim(f'v{version}')}")
    print()


def print_box(content: List[str], title: str = "", width: int = 60) -> None:
    """Print content in a box."""
    s = Symbols

    # Calculate width
    max_len = max(len(strip_ansi(line)) for line in content) if content else 0
    width = max(width, max_len + 4, len(title) + 4)

    # Top border
    if title:
        title_str = f" {title} "
        padding = width - len(title_str) - 2
        print(f"{s.CORNER_TL}{s.LINE}{title_str}{s.LINE * padding}{s.CORNER_TR}")
    else:
        print(f"{s.CORNER_TL}{s.LINE * (width - 2)}{s.CORNER_TR}")

    # Content
    for line in content:
        visible_len = len(strip_ansi(line))
        padding = width - visible_len - 4
        print(f"{s.VERTICAL} {line}{' ' * padding} {s.VERTICAL}")

    # Bottom border
    print(f"{s.CORNER_BL}{s.LINE * (width - 2)}{s.CORNER_BR}")


def print_list(items: List[str], bullet: str = "", indent: int = 2) -> None:
    """Print a formatted list."""
    bullet = bullet or Symbols.BULLET
    for item in items:
        print(f"{' ' * indent}{green(bullet)} {item}")


def print_step(step: int, total: int, message: str) -> None:
    """Print a step indicator."""
    print(f"\n{dim(f'[{step}/{total}]')} {bold(message)}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{green(Symbols.SUCCESS)} {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{red(Symbols.ERROR)} {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{yellow(Symbols.WARNING)} {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{blue(Symbols.INFO)} {message}")


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def move_cursor_up(lines: int = 1) -> None:
    """Move cursor up n lines."""
    sys.stdout.write(f"\033[{lines}A")
    sys.stdout.flush()


def clear_line() -> None:
    """Clear current line."""
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
