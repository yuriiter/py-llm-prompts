import pytest

from llm_prompts import (
    build_prompt,
    extract_yaml,
    prompt_cv,
    read_prompt,
    split_description_and_notes,
    try_till_no_exception,
)


def test_extract_yaml_fenced():
    response = "Here you go:\n```yaml\nname: Ada\n```\n"
    assert extract_yaml(response) == "name: Ada"


def test_extract_yaml_plain():
    assert extract_yaml("name: Ada") == "name: Ada"


def test_build_prompt_substitutes():
    out = build_prompt("Hello {{ name }} ({{ missing }})", {"name": "Ada", "missing": None})
    assert out == "Hello Ada (<Not defined>)"


def test_read_prompt_strips_comments(tmp_path):
    prompt = tmp_path / "p.txt"
    prompt.write_text("line one // inline\n// full line\nline two\n")
    assert read_prompt(str(prompt)) == "line one\n\nline two"


def test_split_description_and_notes():
    assert split_description_and_notes("job\n===\nnotes") == ["job", "notes"]
    assert split_description_and_notes("job") == ["job"]


def test_try_till_no_exception():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("boom")
        return "ok"

    assert try_till_no_exception(flaky, max_retries=5) == "ok"
    assert calls["n"] == 3

    with pytest.raises(ValueError):
        try_till_no_exception(lambda: (_ for _ in ()).throw(ValueError("nope")), max_retries=2, on_error=lambda e, a: None)


def test_prompt_cv_with_fake_client(tmp_path):
    (tmp_path / "prompt-cv.txt").write_text("CV:{{ changable_cv_data_example }} JD:{{ job_description }}")
    calls = {}

    def fake_get_response(prompt, **params):
        calls["prompt"] = prompt
        calls["params"] = params
        return "```yaml\nname: Ada\n```"

    result = prompt_cv(
        "cv",
        "notes",
        "job",
        config={"base_url": "", "api_key": None, "models": ["test-model"]},
        prompt_path=str(tmp_path / "prompt-cv.txt"),
        get_response=fake_get_response,
    )

    assert result == "name: Ada"
    assert "CV:cv" in calls["prompt"]
    assert calls["params"]["model"] == "test-model"
