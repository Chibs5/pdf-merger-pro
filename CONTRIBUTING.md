# Contributing to PDF Merger Pro

Thank you for considering contributing to PDF Merger Pro! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Python version)
- Screenshots if applicable

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Why this feature would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test the GUI if you modified GUI code
   - Test the CLI if you modified CLI code
   - Ensure existing functionality still works

5. **Commit your changes**
   ```bash
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues

## Development Setup

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/pdf-merger-pro.git
   cd pdf-merger-pro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate      # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   # GUI
   python main.py
   
   # CLI
   python cli.py --help
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Add type hints where appropriate

## Testing

Before submitting a PR, please test:
- GUI functionality (if modified)
- CLI commands (if modified)
- Error handling
- Edge cases

## Documentation

If you add new features:
- Update README.md
- Update CLI_GUIDE.md (for CLI features)
- Add docstrings to new functions
- Update the changelog in README.md

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
