# Minimal Python Static Analysis Project

This is a minimal Python project designed to demonstrate and test static analysis tools:

- **Pylint**: Detects logical flaws, code smells, anti-patterns.
- **Flake8**: Combines PyFlakes, pycodestyle, and McCabe complexity checks.
- **SonarQube**: Performs deeper static code analysis (external setup required).
- **mypy**: Performs static type checking.

---

## Project Structure

```plaintext
TestProject/
├── src/
│ └── example.py        # Sample code with intentional issues
├── tests/
│ └── test_example.py   # Basic tests
├── pyproject.toml      # Flake8 & Pylint configuration
├── mypy.ini            # mypy configuration
└── requirements.txt    # Python dependencies
```