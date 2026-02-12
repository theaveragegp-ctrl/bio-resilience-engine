# Contributing to Bio-Resilience Engine

We welcome contributions to the Bio-Resilience Engine project! This document provides guidelines for contributing.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/bio-resilience/bio-resilience-engine.git
cd bio-resilience-engine
```

2. Create a virtual environment:
```bash
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Code Style

- Follow PEP 8 for Python code
- Use Black for code formatting (line length: 100)
- Use Ruff for linting
- Add type hints to all function signatures
- Write docstrings in Google style

## Testing

Run the test suite:
```bash
pytest tests/ -v --cov=src
```

Run only fast tests:
```bash
pytest tests/ -v -m "not slow"
```

## Pull Request Process

1. Create a feature branch from `main`:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Description of changes"
```

3. Push to your fork and create a pull request

4. Ensure all tests pass and coverage remains above 95%

5. Request review from maintainers

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(fusion): add adaptive Kalman filter tuning

Implement online Q-matrix adaptation based on innovation
statistics for improved state estimation during activity
transitions.

Closes #123
```

## Documentation

- Update documentation for any API changes
- Add docstrings to all public functions/classes
- Update README.md if adding new features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
