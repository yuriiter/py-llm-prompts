"""Extract structured data from LLM responses."""

from __future__ import annotations

import re

__all__ = ["extract_yaml"]

_FENCE = re.compile(r"```(?:yaml)?\n(.*?)\n```", re.DOTALL)


def extract_yaml(response: str) -> str:
    """Return the YAML body of a fenced code block, or the input unchanged."""

    match = _FENCE.search(response)
    return match.group(1) if match else response
