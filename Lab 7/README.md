# Lab 7 — Fuzz Testing with Hypothesis

**Student SRN:** PES1UG24CS553

## Contents
- `processor.py` — hardened shipping input-processing functions.
- `test_processor.py` — Hypothesis property-based fuzz tests and regression tests.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest hypothesis
```

## Run the application
```bash
python processor.py
```

Example inputs:
```text
20x30x10
E123
{"weight": 12.5}
```

## Run tests
```bash
python -m pytest -v test_processor.py
```

## Input handling policy
- Invalid dimensional measurements return `0.0`.
- Invalid tracking codes return `INVALID-000000`.
- Invalid manifest payloads or weights return `0.0`.
- Valid inputs retain the expected calculation and formatting behavior.

The test suite uses Hypothesis to generate arbitrary text and `None` values for all three functions, and includes regression tests for valid inputs and important malformed-input boundaries.
