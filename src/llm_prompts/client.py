"""OpenAI-compatible chat client helpers."""

from __future__ import annotations

import os
from typing import Any, Callable

import openai

__all__ = ["get_openai_cb"]


def get_openai_cb(base_url: str | None = None, api_key: str | None = None) -> Callable[..., str]:
    """Return a ``get_response(prompt, **params)`` callable bound to a client.

    The API key falls back to the ``OPENAI_API_KEY`` environment variable.
    """

    openai.base_url = base_url
    openai.api_key = api_key or os.environ.get("OPENAI_API_KEY")

    def get_response(prompt: str, **params: Any) -> str:
        chat_completion = openai.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            **params,
        )
        return chat_completion.choices[0].message.content.strip()

    return get_response
