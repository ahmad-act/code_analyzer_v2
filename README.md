# code_analyzer_v2

**code_analyzer_v2** is a modular Python package that helps you analyze **code quality**, **style**, **naming**, **security**, **test coverage**, **complexity**, and **documentation** — all from a single CLI or Python API interface.

---

## 📚 Table of Contents

- [✅ Features](#-features)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
  - [🐍 Python API](#-python-api)
  - [💻 Command-Line Interface (CLI)](#-command-line-interface-cli)
- [📁 Project Structure](#-project-structure)
- [🧠 Code Review Summary](#-code-review-summary)
  - [1️⃣ Code Quality](#1️⃣-code-quality)
  - [2️⃣ Naming Conventions](#2️⃣-naming-conventions)
  - [3️⃣ Spelling & Grammar](#3️⃣-spelling--grammar)
  - [4️⃣ Clarity & Maintainability](#4️⃣-clarity--maintainability)
  - [5️⃣ Testing & Coverage](#5️⃣-testing--coverage)
  - [6️⃣ Security & Safety](#6️⃣-security--safety)
  - [7️⃣ Dependency Management](#7️⃣-dependency-management)
  - [8️⃣ Performance Profiling](#8️⃣-performance-profiling)
  - [9️⃣ Formatting & Style](#9️⃣-formatting--style)
  - [🔟 Documentation](#🔟-documentation)
- [🤝 Contributing](#-contributing)

---

## ✅ Features

Supports analysis through a range of popular Python tools:

- 🔍 Static analysis: `Pylint`, `Flake8`, `mypy`
- 📊 Code complexity & maintainability: `Radon`, `Refactor`
- 🧾 Naming conventions: `pep8-naming`
- ✍️ Spelling & grammar: `pyspellchecker`
- 📦 Dependency issues: `pipreqs`, `deptry`, `pip-audit`
- 🔐 Security analysis: `Bandit`
- 🧪 Test coverage: `pytest`, `coverage.py`, `hypothesis`
- 🚀 Performance profiling: `cProfile`, `line_profiler`, `memory_profiler`, `Scalene`
- 🧹 Auto-formatting & documentation: `docformatter`, `darglint`, `pdoc`, `Sphinx`

---

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ahmad-act/code_analyzer_v2.git
   cd code_analyzer_v2
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package locally**

   ```bash
   pip install -e .
   ```

---

## 🚀 Usage

### 🐍 Python API

Import and use the analyzer in your own Python project:

```python
from code_analyzer_v2 import analyze_project

report = analyze_project('/path/to/project')
print(report)
```

### 💻 Command-Line Interface (CLI)

Run the analysis from your terminal:

```bash
code-analyzer-v2 "<path/to/project>" --output "<path/to/output/report.json>"
```

Example:

```bash
code-analyzer-v2 "D:\My Study\Coding\code_analyzer_v2\TestProject" --output "D:\My Study\Coding\code_analyzer_v2\report.json"
```

---

## 📁 Project Structure

```plaintext
├── requirements.txt                    # Project dependencies
├── setup.py                            # Legacy setup script
├── setup.cfg                           # Config for linters and tools
├── CodeReview/                         # Modules for code analysis
│   ├── ClarityAndMaintainability/
│   │   ├── radon_runner.py
│   │   └── refactor_runner.py
│   ├── CodeQuality/
│   │   ├── flake8_runner.py
│   │   ├── mypy_runner.py
│   │   └── pylint_runner.py
│   ├── DependencyManagement/
│   │   ├── deptry_runner.py
│   │   └── pipreqs_runner.py
│   ├── NamingConvention/
│   │   └── pep8_naming_runner.py
│   ├── SecurityAndSafety/
│   │   └── bandit_runner.py
│   ├── SpellingAndGrammar/
│   │   ├── codespell_runner.py
│   │   ├── misspell_runner.py
│   │   └── pyspellchecker_runner.py
│   ├── TestingAndTestCoverage/
│   │   ├── coverage_runner.py
│   │   ├── hypothesis_runner.py
│   │   └── pytest_runner.py
├── code_analyzer/                      # Core analysis engine
│   ├── analyzer.py
│   └── cli.py
├── TestProject/                        # Sample project for testing
│   └── src/
│       ├── example.py
│       └── tests/
│           └── test_example.py
```

---

## 🧠 Code Review Summary

### 1️⃣ Code Quality

| Tool     | Description                                               | License           | Language     |
|----------|-----------------------------------------------------------|--------------------|--------------|
| Pylint   | Bug detection, code smells, anti-patterns                 | GPLv2             | Python       |
| Flake8   | Combines pyflakes, pycodestyle, McCabe                    | MIT               | Python       |
| mypy     | Static type checker for Python                            | MIT               | Python       |

### 2️⃣ Naming Conventions

| Tool           | Description                                      | License   | Language |
|----------------|--------------------------------------------------|-----------|----------|
| pep8-naming    | Enforces PEP8 naming conventions via Flake8      | MIT       | Python   |

### 3️⃣ Spelling & Grammar

| Tool               | Description                                      | License | Language        |
|--------------------|--------------------------------------------------|---------|------------------|
| pyspellchecker     | Basic spellchecking using word frequency        | MIT     | English          |

### 4️⃣ Clarity & Maintainability

| Tool        | Description                                   | License | Language |
|-------------|-----------------------------------------------|---------|----------|
| Radon       | Complexity and maintainability metrics        | MIT     | Python   |
| refactor    | Safe automated refactoring                    | MIT     | Python   |

### 5️⃣ Testing & Coverage

| Tool         | Description                               | License   | Language |
|--------------|-------------------------------------------|-----------|----------|
| pytest       | Testing framework                         | MIT       | Python   |
| coverage.py  | Measures code coverage                    | Apache 2.0| Python   |
| hypothesis   | Property-based testing                    | MPL 2.0   | Python   |

### 6️⃣ Security & Safety

| Tool     | Description                                | License    | Language |
|----------|--------------------------------------------|------------|----------|
| bandit   | Static analysis for security vulnerabilities| Apache 2.0 | Python   |

### 7️⃣ Dependency Management

| Tool        | Description                                 | License     | Language |
|-------------|---------------------------------------------|-------------|----------|
| pipreqs     | Generates requirements.txt automatically    | MIT         | Python   |
| deptry      | Detects unused/missing dependencies         | MIT         | Python   |
| pip-audit   | Audits packages for known vulnerabilities   | Apache 2.0  | Python   |

### 8️⃣ Performance Profiling

| Tool             | Description                            | License     | Language |
|------------------|----------------------------------------|-------------|----------|
| cProfile         | Built-in profiler                      | Python std  | Python   |
| line_profiler    | Line-by-line CPU profiler              | BSD         | Python   |
| memory_profiler  | Line-by-line memory usage              | BSD         | Python   |
| Scalene          | CPU/GPU/memory profiler                | Apache 2.0  | Python   |

### 9️⃣ Formatting & Style

| Tool         | Description                              | License | Language |
|--------------|------------------------------------------|---------|----------|
| Black        | Opinionated code formatter               | MIT     | Python   |
| isort        | Sorts and formats import statements      | MIT     | Python   |
| autopep8     | Fixes PEP8 violations                    | MIT     | Python   |

### 🔟 Documentation

| Tool         | Description                                      | License     | Language |
|--------------|--------------------------------------------------|-------------|----------|
| pdoc         | Lightweight docs from type hints/docstrings     | Unlicense   | Python   |
| Sphinx       | Full-featured doc generator                      | BSD         | Python (extensible) |
| docformatter | Formats docstrings per PEP 257                   | MIT         | Python   |
| darglint     | Ensures docstring matches function signatures   | MIT         | Python   |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request to discuss improvements or bugs.

---

