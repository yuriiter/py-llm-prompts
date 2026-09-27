"""Prompt template loading and variable substitution."""

from __future__ import annotations

import re
from typing import Mapping

from config_resolver import get_file_content

__all__ = ["remove_comment", "read_prompt", "build_prompt"]

_COMMENT = re.compile(r"//.*")
_PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


def remove_comment(line: str) -> str:
    """Strip a trailing ``//`` comment from a prompt line."""

    return _COMMENT.sub("", line).strip()


def read_prompt(path: str) -> str:
    """Read a prompt file, dropping ``//`` comment lines."""

    prompt_content = get_file_content(path)
    prompt_lines = prompt_content.splitlines()
    return "\n".join(remove_comment(line) for line in prompt_lines)


def build_prompt(prompt_template: str, data: Mapping[str, object]) -> str:
    """Substitute ``{{ key }}`` placeholders with values from ``data``.

    Placeholders without spaces are supported too. ``None`` values are rendered
    as ``<Not defined>``; unknown placeholders are left untouched.
    """

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in data:
            return match.group(0)
        value = data[key]
        return "<Not defined>" if value is None else str(value)

    return _PLACEHOLDER.sub(replace, prompt_template)
