"""Retry helpers for flaky LLM calls."""

from __future__ import annotations

from typing import Any, Callable

__all__ = ["try_till_no_exception"]


def try_till_no_exception(
    func: Callable[..., Any],
    *args: Any,
    max_retries: int = 5,
    on_error: Callable[[Exception, int], None] | None = None,
    **kwargs: Any,
) -> Any:
    """Call ``func`` until it succeeds, retrying up to ``max_retries`` times."""

    last_exception: Exception = Exception("Unknown error")
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            last_exception = exc
            if on_error is not None:
                on_error(exc, attempt + 1)
            else:
                print(f"Attempt {attempt + 1} failed with exception: {exc}")
                print("Trying again...")

    print("Max retries exceeded.")
    raise last_exception
