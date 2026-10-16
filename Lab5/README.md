# Lab 5 — Static Code Analysis

**Project:** Fitness Club Class Booking Ledger

## Deliverables

- `gym_system.py` — cleaned implementation
- `gym_system_original.py` — preserved original implementation
- `issues.md` — initial findings and fixes
- `Lab5_Issues_Table.docx` — formatted issue table
- `reflection.md` — lab reflection
- `pylint_report_before.txt` and `pylint_report_after.txt`
- `bandit_report_before.txt` and `bandit_report_after.txt`
- `flake8_report_before.txt` and `flake8_report_after.txt`

## Tools

Pylint, Bandit, Flake8, and Python bytecode compilation.

## Final results

| Check | Result |
|---|---|
| Pylint | 10.00/10 |
| Bandit | No issues identified |
| Flake8 | No violations |
| Python compilation | Passed |

## Run the program

```bash
python gym_system.py
```

Enter a non-negative whole number when prompted for walk-in HIIT guests.

## Re-run static analysis

```bash
python -m py_compile gym_system.py
pylint gym_system.py
bandit -r gym_system.py
flake8 gym_system.py
```

The detailed before-and-after outputs are preserved in the report files.
