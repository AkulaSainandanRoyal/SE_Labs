# Lab 5 — Static Code Analysis Issues

## Initial findings

| Issue | Type / Severity | Location | Description | Fix applied |
|---|---|---|---|---|
| Shell command execution | Security — High | `clear_old_exports()` | `os.system()` combined with a constructed command can allow command injection. | Replaced shell execution with `pathlib.Path.glob()` and `unlink()`; validated the prefix. |
| Mutable default argument | Code quality — Medium | `book_class()` | A default list can be shared between calls, producing unexpected state. | Changed the default to `None` and initialized a new list inside the function. |
| Bare exception | Code quality — Medium | `cancel_booking()` | A bare `except` can hide unrelated errors. | Catch only `KeyError` and `ValueError`. |
| Capacity boundary error | Logic — Medium | `book_class()` | Using `>` instead of `>=` allows a booking beyond the configured capacity. | Reject a booking when the current roster length is greater than or equal to capacity. |
| Invalid capacity | Logic — Medium | `set_capacity()` | Zero or negative seat counts are invalid. | Raise `ValueError` when capacity is not positive. |
| File resource handling | Code quality — Low | `export_roster()` | Opening a file without a context manager can leave resource cleanup unclear. | Use `with open(..., encoding="utf-8")`. |
| Naming and formatting | Style — Low | Multiple functions | Non-snake_case naming, old-style formatting, missing docstrings, and spacing violations reduce readability. | Use snake_case, f-strings, docstrings, and consistent formatting. |
| Unsafe input assumptions | Robustness — Medium | `main()` / `add_members()` | Negative guest counts and invalid input should not be accepted silently. | Validate the count and handle invalid integer input. |

## Final analysis results

- Pylint: **10.00/10**
- Bandit: **0 reported security issues**
- Flake8: **No reported violations**
- Python compilation: **Passed**

The findings above summarize the original code and the fixes made. The before-and-after report files provide the detailed tool output.
