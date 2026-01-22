This document describes the coding standards, tooling, and best practices. All contributors are expected to follow these rules to ensure consistency, maintainability, and high code quality.

---

## 1. General Principles

* **Readability first**: Code is read more often than it is written. Optimize for clarity.
* **Explicit is better than implicit** (PEP 20).
* **Correctness > performance** unless performance is explicitly critical.
* **Small, composable units**: Prefer small functions and classes with a single responsibility.
* **Consistency over personal preference**: Follow existing patterns in the codebase.

---

## 2. Project Tooling

### Python

* Target Python version must match the one specified in `pyproject.toml`.
* Use standard library features where possible before adding new dependencies.

### Dependency Management (Poetry)

* Use **Poetry** for dependency management and packaging.
* All dependencies must be declared in `pyproject.toml`.
* Separate dependencies clearly:

  * `dependencies` — runtime requirements
  * `group.dev.dependencies` — development tools (mypy, ruff, pytest, etc.)
* Lock file (`poetry.lock`) **must be committed**.

Common commands:

```bash
poetry install
poetry add <package>
poetry add --group dev <package>
poetry run <command>
```

---

## 3. Static Typing (mypy — strict mode)

We use **mypy in strict mode**. This is non-optional.

### Rules

* All functions and methods **must have explicit type annotations**.
* Avoid using `Any`. If unavoidable, document why.
* Prefer precise types over broad ones.
* Use `typing` and `collections.abc` appropriately.
* Public APIs must be fully typed.

### Best Practices

* Use `Protocol` instead of concrete classes when defining interfaces.
* Prefer `TypedDict` for structured dictionaries.
* Use `@dataclass` for simple data containers.
* Narrow types early (e.g., with `if x is None:`).

Example:

```python
from typing import Iterable

def normalize(values: Iterable[int]) -> list[int]:
    return [v for v in values if v >= 0]
```

---

## 4. Linting & Formatting (ruff)

We use **ruff** for linting and formatting.

### Rules

* Code must pass `ruff check` with no warnings.
* Do not disable rules globally unless there is a strong reason.
* If a rule is suppressed locally, add a short comment explaining why.

### Style Guidelines

* Follow PEP 8 unless ruff enforces a stricter or clearer rule.
* Prefer explicit imports over wildcard imports.
* Remove unused imports, variables, and dead code.

Run locally:

```bash
poetry run ruff check .
poetry run ruff format .
```

---

## 5. Project Structure

* Organize code by **domain**, not by technical layers when possible.
* Avoid deeply nested modules.
* Keep `__init__.py` files minimal.

---

## 6. Functions & Classes

### Functions

* Should do **one thing**.
* Prefer pure functions when possible.
* Avoid side effects unless clearly documented.
* Keep functions short (generally < 40 lines).

### Classes

* Represent meaningful domain concepts.
* Avoid "god objects".
* Prefer composition over inheritance.
* Make state explicit and minimal.

---

## 7. Error Handling

* Never silently ignore exceptions.
* Catch exceptions **only** when you can handle them meaningfully.
* Prefer custom exception types for domain-specific errors.

Example:

```python
class InvalidConfigurationError(Exception):
    pass
```

---

## 8. Testing

* Write tests for all non-trivial logic.
* Prefer **pytest**.
* Tests should be deterministic and isolated.
* Avoid relying on external services in unit tests.

### Testing Guidelines

* One logical behavior per test.
* Use clear and descriptive test names.
* Arrange → Act → Assert structure.

---

## 9. Documentation

* Public modules must have docstrings.
* Functions, classes, and methods DON'T have docstrings (docstrings - bud pructic, method name has to be self-doc.).
* Keep documentation up to date with code changes.

---

## 10. Git & Code Review

* Keep commits small and focused.
* Write meaningful commit messages.
* Avoid mixing refactors and behavior changes in one commit.
* All code must pass tests, mypy, ruff before merging.

During code review, focus on:

* Correctness
* Simplicity
* Readability
* Type safety

---

## 11. Final Checklist Before PR

* [ ] Code passes `ruff` with no issues (check and fromat)
* [ ] Code passes `mypy --strict`
* [ ] Tests are added or updated

---
