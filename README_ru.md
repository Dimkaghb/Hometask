# Домашнее задание: Генерация структурированного вывода

**[English](README.md) | [Қазақша](README_kz.md)**

Обучите малую языковую модель преобразовывать описания на естественном языке в структурированные форматы данных.

## Обзор задачи

Имея **Qwen 3.5-0.8B** и обучающий набор данных, дообучите модель (через LoRA) для создания корректного структурированного вывода в **5 форматах**: JSON, YAML, XML, CSV и TOML.

**Пример входных данных:**
```
JSON; name is Alice Smith, age is 25, city is Berlin
```

**Ожидаемый вывод:**
```json
{"name": "Alice Smith", "age": 25, "city": "Berlin"}
```

## Быстрый старт

```bash
# 1. Установите зависимости
uv sync  # или: pip install -r requirements.txt

# 2. Сгенерируйте набор данных
uv run python -m data.generate_dataset

# 3. Обучите базовый LoRA адаптер (требуется GPU)
uv run python -m train.baseline_train

# 4. Запустите инференс
uv run python -m inference.baseline_generate --lora_path output/baseline_lora

# 5. Оценка
uv run python -m evaluate.run_eval \
    --submission_dir output/baseline_lora \
    --test_path data/test.jsonl \
    --ground_truth_path data/test_ground_truth.jsonl
```

## Форматы вывода

### JSON
```
Вход:  JSON; name is Alice Smith, age is 25, city is Berlin
Выход: {"name": "Alice Smith", "age": 25, "city": "Berlin"}
```

### YAML
```
Вход:  Convert to YAML: name is Bob Jones, email is bob@example.com, occupation is teacher
Выход: name: Bob Jones
       email: bob@example.com
       occupation: teacher
```

### XML
```
Вход:  XML format. Name: Carol White. Country: Japan. Score: 92.5
Выход: <record><name>Carol White</name><country>Japan</country><score>92.5</score></record>
```

### CSV
```
Вход:  Output as CSV: name Dave Brown, phone +1-555-0123, age 40
Выход: name,phone,age
       Dave Brown,+1-555-0123,40
```

### TOML
```
Вход:  TOML — name is Eve Green, score is 88.3, city is Tokyo
Выход: name = "Eve Green"
       score = 88.3
       city = "Tokyo"
```

## Поля

Каждый пример использует случайный набор из 2-6 полей:

| Поле | Тип | Пример |
|------|-----|--------|
| name | строка | "Alice Smith" |
| age | целое число | 25 |
| email | строка | "alice@gmail.com" |
| city | строка | "Berlin" |
| country | строка | "Germany" |
| occupation | строка | "Software Engineer" |
| phone | строка | "+1-555-012-3456" |
| score | дробное число | 92.5 |

## Оценка

Каждый пример оценивается по формуле:

```
score = 0.5 * format_valid + 0.5 * field_accuracy
```

- **format_valid** (0 или 1): Можно ли разобрать вывод стандартным парсером для данного формата?
- **field_accuracy** (от 0.0 до 1.0): Какая доля ожидаемых полей имеет правильное значение?

**Итоговый балл** = среднее по всем примерам (от 0.0 до 1.0).

### Пример

Если ожидаемый вывод — `{"name": "Alice", "age": 30}`, а модель выдала `{"name": "Alice", "age": 25}`:
- format_valid = 1 (валидный JSON)
- field_accuracy = 0.5 (name верно, age неверно)
- score = 0.5 * 1 + 0.5 * 0.5 = **0.75**

## Отправка решения

Отправьте директорию, содержащую:
1. **Веса LoRA** (опционально): `adapter_config.json` + `adapter_model.safetensors`
2. **Код генерации** (опционально): `generate.py` с функцией `generate(model, tokenizer, prompt, format_name) -> str`

Подробнее: [submission/README_SUBMISSION.md](submission/README_SUBMISSION.md)

## Базовое решение

Предоставленное базовое решение использует:
- LoRA с r=16, нацеленный только на `q_proj` и `v_proj`
- 3 эпохи обучения
- Общий системный промпт
- Жадное декодирование

Ожидаемый базовый балл: **~0.55-0.65**

## Правила

- Макс. размер адаптера: 100 МБ
- Тайм-аут генерации: 5 секунд на пример
- Без доступа к интернету во время оценки
- Необходимо использовать базовую модель Qwen 3.5-0.8B (замена модели запрещена)
