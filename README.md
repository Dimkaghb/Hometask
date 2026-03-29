# Hometask: Structured Output Generation

**[Русский](README_ru.md) | [Қазақша](README_kz.md)**

Train a small language model to convert natural language descriptions into structured data formats.

## Task Overview

Given **Qwen 3.5-0.8B** and a training dataset, fine-tune the model (via LoRA) to produce correct structured output in **5 formats**: JSON, YAML, XML, CSV, and TOML.

**Input example:**
```
JSON; name is Alice Smith, age is 25, city is Berlin
```

**Expected output:**
```json
{"name": "Alice Smith", "age": 25, "city": "Berlin"}
```

## Quick Start

```bash
# 1. Install dependencies
uv sync  # or: pip install -r requirements.txt

# 2. Generate the dataset
uv run python -m data.generate_dataset

# 3. Train the baseline LoRA adapter (requires GPU)
uv run python -m train.baseline_train

# 4. Run inference
uv run python -m inference.baseline_generate --lora_path output/baseline_lora

# 5. Evaluate
uv run python -m evaluate.run_eval \
    --submission_dir output/baseline_lora \
    --test_path data/test.jsonl \
    --ground_truth_path data/test_ground_truth.jsonl
```

## Output Formats

### JSON
```
Input:  JSON; name is Alice Smith, age is 25, city is Berlin
Output: {"name": "Alice Smith", "age": 25, "city": "Berlin"}
```

### YAML
```
Input:  Convert to YAML: name is Bob Jones, email is bob@example.com, occupation is teacher
Output: name: Bob Jones
        email: bob@example.com
        occupation: teacher
```

### XML
```
Input:  XML format. Name: Carol White. Country: Japan. Score: 92.5
Output: <record><name>Carol White</name><country>Japan</country><score>92.5</score></record>
```

### CSV
```
Input:  Output as CSV: name Dave Brown, phone +1-555-0123, age 40
Output: name,phone,age
        Dave Brown,+1-555-0123,40
```

### TOML
```
Input:  TOML — name is Eve Green, score is 88.3, city is Tokyo
Output: name = "Eve Green"
        score = 88.3
        city = "Tokyo"
```

## Fields

Each sample uses a random subset of 2-6 fields from:

| Field | Type | Example |
|-------|------|---------|
| name | string | "Alice Smith" |
| age | integer | 25 |
| email | string | "alice@gmail.com" |
| city | string | "Berlin" |
| country | string | "Germany" |
| occupation | string | "Software Engineer" |
| phone | string | "+1-555-012-3456" |
| score | float | 92.5 |

## Scoring

Each sample is scored with:

```
score = 0.5 * format_valid + 0.5 * field_accuracy
```

- **format_valid** (0 or 1): Can the output be parsed by the standard parser for that format?
- **field_accuracy** (0.0 to 1.0): Of the expected fields, what fraction have the correct value?

**Final score** = mean of all sample scores (0.0 to 1.0).

### Example

If the expected output is `{"name": "Alice", "age": 30}` and the model outputs `{"name": "Alice", "age": 25}`:
- format_valid = 1 (valid JSON)
- field_accuracy = 0.5 (name correct, age wrong)
- score = 0.5 * 1 + 0.5 * 0.5 = **0.75**

## Submission

Submit a directory containing:
1. **LoRA weights** (optional): `adapter_config.json` + `adapter_model.safetensors`
2. **Custom generation code** (optional): `generate.py` with a `generate(model, tokenizer, prompt, format_name) -> str` function

See [submission/README_SUBMISSION.md](submission/README_SUBMISSION.md) for details.

## Baseline

The provided baseline uses:
- LoRA with r=16, targeting only `q_proj` and `v_proj`
- 3 training epochs
- Generic system prompt
- Greedy decoding

Expected baseline score: **~0.55-0.65**

## Rules

- Max adapter size: 100 MB
- Generation timeout: 5 seconds per sample
- No internet access during evaluation
- You must use the Qwen 3.5-0.8B base model (no model substitution)
