# Contributing to Mocchibird

Thank you for your interest in contributing to Mocchibird! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/mocchi-chat.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Set up your development environment (see below)

## Development Environment Setup

1. **Install Python 3.8+**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your test Discord bot token and API keys
   ```

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Testing Your Changes

1. **Syntax check**
   ```bash
   python -m py_compile bot.py training.py
   ```

2. **Import test**
   ```bash
   python -c "import bot; import training; print('OK')"
   ```

3. **Functional testing**
   - Create a test Discord server
   - Run the bot and test your changes
   - Verify the bot responds to @mentions correctly

## Making Changes

### Adding New Features

1. Update the relevant Python files (bot.py, training.py)
2. Update config.yaml if new configuration is needed
3. Update README.md with documentation
4. Test your changes thoroughly

### Fixing Bugs

1. Create a test case that reproduces the bug
2. Fix the bug
3. Verify the fix works
4. Add comments explaining the fix if needed

### Updating Documentation

1. Keep README.md up to date with any changes
2. Update code comments and docstrings
3. Add examples when helpful

## Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Describe your changes clearly
   - Link any related issues

## Pull Request Guidelines

- Keep pull requests focused on a single feature or fix
- Write clear commit messages
- Update documentation as needed
- Respond to review feedback promptly
- Be respectful and constructive

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Questions?

If you have questions or need help:
- Open an issue on GitHub
- Check existing issues and documentation
- Ask in the pull request comments

Thank you for contributing to Mocchibird! 🎉
