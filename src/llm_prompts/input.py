"""Interactive input helpers."""

from __future__ import annotations

import os
import shlex
import subprocess
import tempfile

__all__ = ["multiline_input", "editor_input", "split_description_and_notes"]


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


def editor_input(
    instruction: str | None = None,
    initial_text: str = "",
    suffix: str = ".txt",
) -> str:
    """Open ``$EDITOR`` on a temporary file and return its contents.

    The editor is resolved from ``EDITOR``, then ``VISUAL``, then ``vi``. The
    ``initial_text`` is pre-filled so it can serve as a template.
    """

    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"

    with tempfile.NamedTemporaryFile(
        "w", suffix=suffix, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(initial_text)
        path = handle.name

    try:
        if instruction:
            print(instruction)
        print(f"Opening editor: {editor}")
        subprocess.run([*shlex.split(editor), path], check=True)

        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    finally:
        if os.path.exists(path):
            os.remove(path)


def split_description_and_notes(
    description_and_notes: str,
    delimiter: str = "\n===\n",
) -> list[str]:
    """Split a combined job-description/notes blob on ``delimiter``."""

    return description_and_notes.split(delimiter)
