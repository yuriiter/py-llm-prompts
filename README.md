# py-llm-prompts

LLM prompt building, an OpenAI-compatible chat client helper, YAML extraction,
retry/input helpers and high-level CV / cover-letter generation workflows.
Extracted from the `mcv` (advanced-templating) project.

## Library

```python
from llm_prompts import build_prompt, extract_yaml, prompt_cv

prompt = build_prompt("Hello {{ name }}", {"name": "Ada"})
cv_yaml = prompt_cv(cv_example, notes, job_description, config=my_config)
```

## CLI

```bash
# Extract YAML from an LLM response on stdin.
echo '```yaml
name: Ada
```' | llm-prompts extract-yaml

# Fill a prompt template.
llm-prompts build --template prompt-cv.txt --var name=Ada --var-file extra.yaml

# Generate tailored YAML (requires auto-generation.config.yaml + prompt files).
llm-prompts cv --cv-example cv.data.yaml --job-description job.txt --config auto-generation.config.yaml
llm-prompts cover-letter --cv cv.yaml --cover-letter-example cover-letter.example.yaml --job-description job.txt
```
