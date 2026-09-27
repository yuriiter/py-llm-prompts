"""High-level CV / cover-letter prompt workflows.

These functions glue together prompt building, the OpenAI-compatible client and
YAML extraction. Configuration is passed in explicitly so the package has no
hidden dependency on a project-specific file.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Mapping

from config_resolver import parse_data

from .builder import build_prompt, read_prompt
from .client import get_openai_cb
from .extract import extract_yaml

__all__ = ["load_auto_generation_config", "prompt_cv", "prompt_cover_letter"]

DEFAULT_CONFIG_PATH = "auto-generation.config.yaml"


def load_auto_generation_config(path: str = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Load the auto-generation config (base_url, api_key, models)."""

    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Auto-generation config '{path}' not found. Copy "
            "auto-generation.config.example.yaml and set your API key."
        )
    return parse_data(path)


def _resolve(
    config: Mapping[str, Any] | None,
    get_response: Callable[..., str] | None,
) -> tuple[Mapping[str, Any], Callable[..., str]]:
    config = config or load_auto_generation_config()
    client = get_response or get_openai_cb(config.get("base_url"), config.get("api_key"))
    return config, client


def prompt_cv(
    changable_cv_data_example: str,
    user_notes: str | None,
    job_description: str,
    config: Mapping[str, Any] | None = None,
    prompt_path: str = "prompt-cv.txt",
    get_response: Callable[..., str] | None = None,
) -> str:
    """Generate tailored CV YAML from a CV example and a job description."""

    config, client = _resolve(config, get_response)

    prompt_template = read_prompt(prompt_path)
    prompt = build_prompt(
        prompt_template,
        {
            "changable_cv_data_example": changable_cv_data_example,
            "user_notes": user_notes,
            "job_description": job_description,
        },
    )

    response = extract_yaml(client(prompt, model=config.get("models")[0], temperature=0.1))
    parse_data(response)
    return response


def prompt_cover_letter(
    used_cv_data: str,
    user_notes: str | None,
    cover_letter_example: str,
    job_description: str,
    config: Mapping[str, Any] | None = None,
    prompt_path: str = "prompt-cover-letter.txt",
    get_response: Callable[..., str] | None = None,
) -> str:
    """Generate a tailored cover-letter YAML from a job description."""

    config, client = _resolve(config, get_response)

    prompt_template = read_prompt(prompt_path)
    prompt = build_prompt(
        prompt_template,
        {
            "used_cv_data": used_cv_data,
            "user_notes": user_notes,
            "job_description": job_description,
            "cover_letter_example": cover_letter_example,
        },
    )

    response = extract_yaml(client(prompt, model=config.get("models")[0], temperature=0.1))
    parse_data(response)
    return response
