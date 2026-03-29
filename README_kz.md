# үй тапсырмасы: Құрылымдық шығыс генерациясы

**[English](README.md) | [Русский](README_ru.md)**

Кіші тілдік модельді табиғи тілдегі сипаттамаларды құрылымдық деректер форматтарына түрлендіруге үйретіңіз.

## Тапсырма сипаттамасы

**Qwen 3.5-0.8B** моделі мен оқу деректер жиынтығын пайдаланып, модельді (LoRA арқылы) **5 форматта** дұрыс құрылымдық шығыс шығаруға дәл баптаңыз: JSON, YAML, XML, CSV және TOML.

**Кіріс мысалы:**
```
JSON; name is Alice Smith, age is 25, city is Berlin
```

**Күтілетін шығыс:**
```json
{"name": "Alice Smith", "age": 25, "city": "Berlin"}
```

## Жылдам бастау

```bash
# 1. Тәуелділіктерді орнатыңыз
uv sync  # немесе: pip install -r requirements.txt

# 2. Деректер жиынтығын генерациялаңыз
uv run python -m data.generate_dataset

# 3. Базалық LoRA адаптерін оқытыңыз (GPU қажет)
uv run python -m train.baseline_train

# 4. Инференсті іске қосыңыз
uv run python -m inference.baseline_generate --lora_path output/baseline_lora

# 5. Бағалау
uv run python -m evaluate.run_eval \
    --submission_dir output/baseline_lora \
    --test_path data/test.jsonl \
    --ground_truth_path data/test_ground_truth.jsonl
```

## Шығыс форматтары

### JSON
```
Кіріс:  JSON; name is Alice Smith, age is 25, city is Berlin
Шығыс: {"name": "Alice Smith", "age": 25, "city": "Berlin"}
```

### YAML
```
Кіріс:  Convert to YAML: name is Bob Jones, email is bob@example.com, occupation is teacher
Шығыс: name: Bob Jones
       email: bob@example.com
       occupation: teacher
```

### XML
```
Кіріс:  XML format. Name: Carol White. Country: Japan. Score: 92.5
Шығыс: <record><name>Carol White</name><country>Japan</country><score>92.5</score></record>
```

### CSV
```
Кіріс:  Output as CSV: name Dave Brown, phone +1-555-0123, age 40
Шығыс: name,phone,age
       Dave Brown,+1-555-0123,40
```

### TOML
```
Кіріс:  TOML — name is Eve Green, score is 88.3, city is Tokyo
Шығыс: name = "Eve Green"
       score = 88.3
       city = "Tokyo"
```

## Өрістер

Әр мысал 2-6 өрістен тұратын кездейсоқ жиынтықты пайдаланады:

| Өріс | Түрі | Мысал |
|------|------|-------|
| name | жол | "Alice Smith" |
| age | бүтін сан | 25 |
| email | жол | "alice@gmail.com" |
| city | жол | "Berlin" |
| country | жол | "Germany" |
| occupation | жол | "Software Engineer" |
| phone | жол | "+1-555-012-3456" |
| score | бөлшек сан | 92.5 |

## Бағалау

Әр мысал келесі формула бойынша бағаланады:

```
score = 0.5 * format_valid + 0.5 * field_accuracy
```

- **format_valid** (0 немесе 1): Шығысты сол форматтың стандартты парсерімен талдауға болады ма?
- **field_accuracy** (0.0-ден 1.0-ге дейін): Күтілетін өрістердің қанша бөлігінде дұрыс мән бар?

**Қорытынды балл** = барлық мысалдардың орташа мәні (0.0-ден 1.0-ге дейін).

### Мысал

Егер күтілетін шығыс — `{"name": "Alice", "age": 30}`, ал модель `{"name": "Alice", "age": 25}` шығарса:
- format_valid = 1 (жарамды JSON)
- field_accuracy = 0.5 (name дұрыс, age дұрыс емес)
- score = 0.5 * 1 + 0.5 * 0.5 = **0.75**

## Шешімді тапсыру

Мыналарды қамтитын директорияны тапсырыңыз:
1. **LoRA салмақтары** (міндетті емес): `adapter_config.json` + `adapter_model.safetensors`
2. **Генерация коды** (міндетті емес): `generate(model, tokenizer, prompt, format_name) -> str` функциясы бар `generate.py`

Толығырақ: [submission/README_SUBMISSION.md](submission/README_SUBMISSION.md)

## Базалық шешім

Ұсынылған базалық шешім мыналарды пайдаланады:
- r=16 параметрлі LoRA, тек `q_proj` және `v_proj` мақсатты
- 3 оқу дәуірі (epoch)
- Жалпы жүйелік промпт
- Ашкөз декодтау (greedy decoding)

Күтілетін базалық балл: **~0.55-0.65**

## Ережелер

- Адаптердің макс. өлшемі: 100 МБ
- Генерация тайм-ауты: бір мысалға 5 секунд
- Бағалау кезінде интернетке рұқсат жоқ
- Qwen 3.5-0.8B базалық моделін пайдалану қажет (модельді ауыстыруға тыйым салынады)
