"""Command line interface for :mod:`llm_prompts`."""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable, Sequence

import yaml
from config_resolver import get_file_content, parse_data

from .builder import build_prompt, read_prompt
from .extract import extract_yaml
from .prompts import load_auto_generation_config, prompt_cv, prompt_cover_letter


def _read_text(value: str | None, file_path: str | None, default_stdin: bool = False) -> str | None:
    if value is not None:
        return value
    if file_path:
        return get_file_content(file_path)
    if default_stdin and not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def _add_generation_args(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("--config", default=None, help="Auto-generation config YAML (default: auto-generation.config.yaml).")
    sub.add_argument("--prompt", dest="prompt_path", default=None, help="Prompt template file.")
    sub.add_argument("--notes", default=None, help="Extra user notes for the prompt.")
    sub.add_argument("--job-description", dest="job_description_file", default=None, help="Job description file.")
    sub.add_argument("--job-description-text", default=None, help="Inline job description.")
    sub.add_argument("-o", "--output", default=None, help="Write the generated YAML to this file.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-prompts",
        description="Build prompts, extract YAML and generate tailored CV/cover-letter data.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract-yaml", help="Extract YAML from an LLM response (reads stdin by default).")
    extract.add_argument("text", nargs="?", default=None, help="Response text (reads stdin when omitted).")

    build = subparsers.add_parser("build", help="Fill a prompt template with variables.")
    build.add_argument("--template", required=True, help="Prompt template file.")
    build.add_argument("--var", action="append", default=None, metavar="KEY=VALUE", help="Template variable (repeatable).")
    build.add_argument("--var-file", default=None, help="YAML/JSON file with variables.")

    cv = subparsers.add_parser("cv", help="Generate a tailored CV YAML.")
    _add_generation_args(cv)
    cv.add_argument("--cv-example", required=True, help="Template CV data file (YAML).")

    cover = subparsers.add_parser("cover-letter", help="Generate a tailored cover-letter YAML.")
    _add_generation_args(cover)
    cover.add_argument("--cv", required=True, help="The CV data used for this application.")
    cover.add_argument("--cover-letter-example", required=True, help="Cover-letter example file (YAML).")

    return parser


def _collect_vars(args: argparse.Namespace) -> dict[str, Any]:
    variables: dict[str, Any] = {}
    if args.var_file:
        variables.update(parse_data(args.var_file) or {})
    for pair in args.var or []:
        if "=" not in pair:
            raise SystemExit(f"Invalid --var '{pair}', expected KEY=VALUE")
        key, value = pair.split("=", 1)
        try:
            variables[key] = parse_data(value)
        except Exception:
            variables[key] = value
    return variables


def _emit(output_path: str | None, content: str) -> None:
    if output_path:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(content)
        print(f"Wrote {output_path}")
    else:
        print(content)


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "extract-yaml":
        text = args.text if args.text is not None else sys.stdin.read()
        print(extract_yaml(text))
        return 0

    if args.command == "build":
        variables = _collect_vars(args)
        print(build_prompt(read_prompt(args.template), variables))
        return 0

    config_path = args.config or "auto-generation.config.yaml"
    config = load_auto_generation_config(config_path)
    job_description = _read_text(args.job_description_text, args.job_description_file, default_stdin=True)
    if job_description is None:
        raise SystemExit("Provide --job-description, --job-description-text or pipe stdin.")

    if args.command == "cv":
        result = prompt_cv(
            get_file_content(args.cv_example),
            args.notes,
            job_description,
            config=config,
            prompt_path=args.prompt_path or "prompt-cv.txt",
        )
    else:
        result = prompt_cover_letter(
            get_file_content(args.cv),
            args.notes,
            get_file_content(args.cover_letter_example),
            job_description,
            config=config,
            prompt_path=args.prompt_path or "prompt-cover-letter.txt",
        )

    _emit(args.output, result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
