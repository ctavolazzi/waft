# Contributing to Waft

Thank you for your interest in contributing to Waft! 🌊

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/waft.git
   cd waft
   ```
3. **Set up the development environment**:
   ```bash
   uv sync
   uv tool install --editable .
   ```

   **Important**: Use `--editable` mode so code changes are immediately reflected.
   If you've already installed without `--editable`, reinstall with:
   ```bash
   uv tool install --editable .
   ```

   Or use the convenience script:
   ```bash
   ./scripts/dev-reinstall.sh
   ```

## Development Workflow

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test them:
   ```bash
   # After making code changes, reinstall if not using --editable:
   uv tool install --editable .

   # Run tests
   uv run pytest

   # Run linting
   uv run ruff check .

   # Format code
   uv run ruff format .
   ```

   **Note**: If you installed with `--editable`, code changes are automatically
   reflected. If you installed without `--editable`, you must reinstall after
   each change.

3. **Commit your changes**:
   ```bash
   git commit -m "Description of your changes"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request** on GitHub

## Code Style

- Follow PEP 8 style guidelines
- Use `ruff` for linting and formatting
- Keep functions focused and small
- Add docstrings to public functions and classes
- Write tests for new features

## Testing

- Run tests with: `uv run pytest`
- Ensure all tests pass before submitting a PR
- Add tests for new features

## Pull Request Guidelines

- Provide a clear description of your changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep PRs focused on a single feature or fix

## Questions?

Feel free to open an issue for questions or discussions!

