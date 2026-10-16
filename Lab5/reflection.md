# Lab 5 — Reflection

## 1. Why is static code analysis useful?

Static code analysis checks source code without requiring the complete program to run. It helps identify potential security weaknesses, coding errors, maintainability problems, and style violations early in development. Using multiple tools provides different perspectives on code quality.

## 2. What important issues were found in the original program?

The original program used `os.system()` to delete files through a shell command, a mutable default argument, a bare exception handler, and an incorrect capacity boundary condition. It also had missing docstrings, inconsistent naming, formatting violations, and file-handling issues.

## 3. How did the fixes improve the program?

Shell-based file deletion was replaced with `pathlib` operations, the mutable default was replaced with `None`, and exception handling was narrowed to expected exceptions. Capacity and guest-count validation were added, file operations use a context manager, and naming and documentation were improved.

## 4. What did the final analysis show, and what did you learn?

The final checks reported a Pylint score of 10.00/10, no Bandit findings, no Flake8 violations, and successful Python compilation. This exercise showed that security, correctness, readability, and maintainability all matter. It also demonstrated the value of running analysis tools again after changes instead of assuming that a fix is correct.
