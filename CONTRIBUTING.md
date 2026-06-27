# Contributing to AegisXAI

Thank you for considering contributing! We welcome issues, feature requests, documentation improvements, and pull requests.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/AegisXAI.git`
3. Install dependencies: `pip install -r aegisxai/requirements.txt`
4. Generate dataset: `python generate_large_dataset.py`
5. Run: `streamlit run app.py`

## Development Workflow

- Create a branch: `git checkout -b feature/your-feature`
- Make changes and verify with `python -m py_compile app.py`
- Run tests: `cd aegisxai && pytest tests/ -v`
- Ensure all 84+ pages load without StreamlitDuplicateElementKey errors
- Commit with a descriptive message
- Push and open a pull request

## Code Style

- Follow PEP 8 (use `ruff` or `black` if available)
- No TODOs, placeholders, or pseudocode in production files
- Use f-strings, type hints where practical
- Keep `app.py` lean — add new pages as module functions in the dashboards/ package

## Pull Request Checklist

- [ ] Code compiles (`python -m py_compile app.py`)
- [ ] No duplicate element key errors in Streamlit
- [ ] New pages registered in `PAGE_FUNCTIONS` dict
- [ ] Tests pass for any modified logic
- [ ] `.gitignore` updated if new generated files added

## Reporting Issues

Include the full error traceback, Streamlit version, and steps to reproduce.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
