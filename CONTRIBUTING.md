# Contributing to NoteCal

Thank you for your interest in contributing to NoteCal!

## Development Setup

1. Clone the repository
2. Use the project virtual environment for all dependency installation and commands
3. Install dependencies:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Run the application:

   ```powershell
   .\.venv\Scripts\python.exe run.py
   ```

## Quality Checks

Run these commands before opening a pull request:

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q run.py src tests
```

To verify the Windows packaging configuration:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean NoteCal.spec
```

`build/`, `dist/`, `.venv/`, and runtime data files are local artifacts and should not be committed.

## How to Contribute

### Bug Reports
Please open an issue with a clear description of the problem, including:
- Your operating system
- Steps to reproduce
- Expected vs actual behavior

### Feature Requests
Open an issue with the label "enhancement" and describe:
- The problem you are trying to solve
- How you envision the solution
- Any alternatives you have considered

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with clear commit messages
4. Submit a pull request against the `main` branch

## Code Style
- Follow the configured Ruff rules
- Add type annotations to new functions
- Update docstrings for public APIs
- Keep UI-facing behavior covered by focused tests when logic is extracted from PyQt widgets

## License
By contributing, you agree that your contributions will be licensed under the MIT License.
