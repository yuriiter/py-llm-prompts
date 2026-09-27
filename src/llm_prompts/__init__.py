"""LLM prompt building, client helpers, YAML extraction and CV workflows."""

from .builder import build_prompt, read_prompt, remove_comment
from .client import get_openai_cb
from .extract import extract_yaml
from .input import multiline_input, split_description_and_notes
from .prompts import load_auto_generation_config, prompt_cv, prompt_cover_letter
from .retry import try_till_no_exception

__version__ = "0.1.0"

__all__ = [
    "build_prompt",
    "extract_yaml",
    "get_openai_cb",
    "load_auto_generation_config",
    "multiline_input",
    "prompt_cv",
    "prompt_cover_letter",
    "read_prompt",
    "remove_comment",
    "split_description_and_notes",
    "try_till_no_exception",
    "__version__",
]
