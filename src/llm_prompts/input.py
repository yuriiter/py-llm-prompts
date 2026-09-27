"""Interactive input helpers."""

from __future__ import annotations

__all__ = ["multiline_input", "split_description_and_notes"]


def multiline_input(prompt: str) -> str:
    """Read multiple lines from stdin until EOF (Ctrl-D / Ctrl-Z)."""

    print(prompt)
    print("[Ctrl-D or Ctrl-Z to submit]")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    return "\n".join(contents)


def split_description_and_notes(
    description_and_notes: str,
    delimiter: str = "\n===\n",
) -> list[str]:
    """Split a combined job-description/notes blob on ``delimiter``."""

    return description_and_notes.split(delimiter)
