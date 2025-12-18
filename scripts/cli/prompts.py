"""
Interactive prompts for CLI - beautiful input collection.
"""

import sys
import re
from typing import Optional, List, Callable, Any, TypeVar, Dict

from .ui import (
    Colors,
    Symbols,
    c,
    cyan,
    green,
    yellow,
    red,
    dim,
    bold,
    magenta,
    clear_line,
    move_cursor_up,
    _color_enabled,
)

T = TypeVar("T")


def _getch() -> str:
    """Get a single character from stdin without echo."""
    if sys.platform == "win32":
        import msvcrt

        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):  # Special keys
            ch = msvcrt.getwch()
            return f"\x00{ch}"
        return ch
    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":  # Escape sequence
                ch += sys.stdin.read(2)
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def _is_enter(ch: str) -> bool:
    return ch in ("\r", "\n")


def _is_backspace(ch: str) -> bool:
    return ch in ("\x7f", "\x08")


def _is_up(ch: str) -> bool:
    return ch in ("\x1b[A", "\x00H")


def _is_down(ch: str) -> bool:
    return ch in ("\x1b[B", "\x00P")


def _is_ctrl_c(ch: str) -> bool:
    return ch == "\x03"


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


def text(
    message: str,
    default: str = "",
    placeholder: str = "",
    validate: Optional[Callable[[str], bool]] = None,
    validate_message: str = "Invalid input",
    required: bool = True,
) -> str:
    """
    Prompt for text input.

    Args:
        message: The prompt message
        default: Default value if empty
        placeholder: Placeholder text (shown dimmed)
        validate: Validation function
        validate_message: Message shown on validation failure
        required: Whether input is required
    """
    suffix = f" {dim(f'({default})')}" if default else ""
    prompt = f"{green(Symbols.QUESTION)} {bold(message)}{suffix} {dim(Symbols.POINTER)} "

    while True:
        sys.stdout.write(prompt)
        if placeholder and not default:
            sys.stdout.write(dim(placeholder))
            sys.stdout.write("\b" * len(placeholder))
        sys.stdout.flush()

        try:
            value = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            raise KeyboardInterrupt()

        if not value:
            if default:
                value = default
            elif required:
                clear_line()
                move_cursor_up()
                clear_line()
                print(f"{red(Symbols.ERROR)} {red('This field is required')}")
                continue

        if validate and value:
            try:
                if not validate(value):
                    raise ValidationError(validate_message)
            except ValidationError as e:
                clear_line()
                move_cursor_up()
                clear_line()
                print(f"{red(Symbols.ERROR)} {red(str(e))}")
                continue

        # Show final value
        move_cursor_up()
        clear_line()
        display_value = value if value else dim("(empty)")
        print(f"{green(Symbols.SUCCESS)} {bold(message)} {dim(Symbols.ARROW_RIGHT)} {cyan(display_value)}")
        return value


def password(message: str, mask: str = "*") -> str:
    """
    Prompt for password input (masked).
    """
    prompt = f"{green(Symbols.QUESTION)} {bold(message)} {dim(Symbols.POINTER)} "
    sys.stdout.write(prompt)
    sys.stdout.flush()

    value = ""
    while True:
        ch = _getch()
        if _is_ctrl_c(ch):
            print()
            raise KeyboardInterrupt()
        elif _is_enter(ch):
            break
        elif _is_backspace(ch):
            if value:
                value = value[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
        elif len(ch) == 1 and ch.isprintable():
            value += ch
            sys.stdout.write(mask)
            sys.stdout.flush()

    print()
    move_cursor_up()
    clear_line()
    masked = mask * min(len(value), 8) if value else dim("(empty)")
    print(f"{green(Symbols.SUCCESS)} {bold(message)} {dim(Symbols.ARROW_RIGHT)} {dim(masked)}")
    return value


def confirm(message: str, default: bool = True) -> bool:
    """
    Prompt for yes/no confirmation.
    """
    hint = "Y/n" if default else "y/N"
    prompt = f"{green(Symbols.QUESTION)} {bold(message)} {dim(f'({hint})')} {dim(Symbols.POINTER)} "

    while True:
        sys.stdout.write(prompt)
        sys.stdout.flush()

        try:
            value = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            raise KeyboardInterrupt()

        if not value:
            result = default
        elif value in ("y", "yes", "是"):
            result = True
        elif value in ("n", "no", "否"):
            result = False
        else:
            move_cursor_up()
            clear_line()
            continue

        move_cursor_up()
        clear_line()
        answer = green("Yes") if result else red("No")
        print(f"{green(Symbols.SUCCESS)} {bold(message)} {dim(Symbols.ARROW_RIGHT)} {answer}")
        return result


def select(
    message: str,
    choices: List[str],
    default: int = 0,
    descriptions: Optional[List[str]] = None,
) -> tuple[int, str]:
    """
    Prompt for single selection from list.
    Returns (index, value).
    """
    if not choices:
        raise ValueError("Choices cannot be empty")

    current = default
    descriptions = descriptions or [""] * len(choices)

    def render() -> None:
        print(f"{green(Symbols.QUESTION)} {bold(message)}")
        for i, (choice, desc) in enumerate(zip(choices, descriptions)):
            if i == current:
                pointer = cyan(Symbols.POINTER)
                label = cyan(choice)
            else:
                pointer = " "
                label = choice
            desc_str = f" {dim(f'- {desc}')}" if desc else ""
            print(f"  {pointer} {label}{desc_str}")

    render()

    while True:
        ch = _getch()
        if _is_ctrl_c(ch):
            raise KeyboardInterrupt()
        elif _is_enter(ch):
            break
        elif _is_up(ch):
            current = (current - 1) % len(choices)
        elif _is_down(ch):
            current = (current + 1) % len(choices)
        else:
            continue

        # Re-render
        for _ in range(len(choices) + 1):
            move_cursor_up()
            clear_line()
        render()

    # Clear and show result
    for _ in range(len(choices) + 1):
        move_cursor_up()
        clear_line()
    print(f"{green(Symbols.SUCCESS)} {bold(message)} {dim(Symbols.ARROW_RIGHT)} {cyan(choices[current])}")

    return current, choices[current]


def multiselect(
    message: str,
    choices: List[str],
    defaults: Optional[List[int]] = None,
    min_selections: int = 0,
    max_selections: Optional[int] = None,
) -> List[tuple[int, str]]:
    """
    Prompt for multiple selections from list.
    Returns list of (index, value) tuples.
    """
    if not choices:
        raise ValueError("Choices cannot be empty")

    current = 0
    selected = set(defaults or [])

    def render() -> None:
        print(f"{green(Symbols.QUESTION)} {bold(message)} {dim('(space to toggle, enter to confirm)')}")
        for i, choice in enumerate(choices):
            if i == current:
                pointer = cyan(Symbols.POINTER)
            else:
                pointer = " "

            if i in selected:
                checkbox = green(Symbols.SUCCESS)
            else:
                checkbox = dim(Symbols.CIRCLE)

            label = cyan(choice) if i == current else choice
            print(f"  {pointer} {checkbox} {label}")

    render()

    while True:
        ch = _getch()
        if _is_ctrl_c(ch):
            raise KeyboardInterrupt()
        elif _is_enter(ch):
            if len(selected) < min_selections:
                continue
            break
        elif _is_up(ch):
            current = (current - 1) % len(choices)
        elif _is_down(ch):
            current = (current + 1) % len(choices)
        elif ch == " ":
            if current in selected:
                selected.remove(current)
            else:
                if max_selections is None or len(selected) < max_selections:
                    selected.add(current)
            # Stay at current position after toggle
        else:
            continue

        # Re-render
        for _ in range(len(choices) + 1):
            move_cursor_up()
            clear_line()
        render()

    # Clear and show result
    for _ in range(len(choices) + 1):
        move_cursor_up()
        clear_line()

    selected_names = [choices[i] for i in sorted(selected)]
    result_str = ", ".join(selected_names) if selected_names else dim("(none)")
    print(f"{green(Symbols.SUCCESS)} {bold(message)} {dim(Symbols.ARROW_RIGHT)} {cyan(result_str)}")

    return [(i, choices[i]) for i in sorted(selected)]


def number(
    message: str,
    default: Optional[int] = None,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    """
    Prompt for numeric input.
    """

    def validate(val: str) -> bool:
        try:
            n = int(val)
            if min_value is not None and n < min_value:
                raise ValidationError(f"Value must be at least {min_value}")
            if max_value is not None and n > max_value:
                raise ValidationError(f"Value must be at most {max_value}")
            return True
        except ValueError:
            raise ValidationError("Please enter a valid number")

    default_str = str(default) if default is not None else ""
    result = text(
        message,
        default=default_str,
        validate=validate,
        validate_message="Please enter a valid number",
    )
    return int(result)


def path(
    message: str,
    default: str = "",
    must_exist: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
) -> str:
    """
    Prompt for file/directory path.
    """
    import os

    def validate(val: str) -> bool:
        expanded = os.path.expanduser(val)
        if must_exist and not os.path.exists(expanded):
            raise ValidationError(f"Path does not exist: {val}")
        if os.path.exists(expanded):
            if os.path.isfile(expanded) and not file_okay:
                raise ValidationError("Expected a directory, not a file")
            if os.path.isdir(expanded) and not dir_okay:
                raise ValidationError("Expected a file, not a directory")
        return True

    return text(message, default=default, validate=validate)


# Convenience function for project name validation
def project_name(message: str = "Project name", default: str = "") -> str:
    """
    Prompt for project name with validation.
    """

    def validate(val: str) -> bool:
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_\- ]*$", val):
            raise ValidationError(
                "Name must start with a letter and contain only letters, numbers, underscores, hyphens, or spaces"
            )
        return True

    return text(message, default=default, validate=validate)
