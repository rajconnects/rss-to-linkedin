# Contributing to RSS to LinkedIn

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/rss-to-linkedin.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright for browser automation
npx playwright install chromium

# Copy example configs
cp examples/config.example.yaml config.yaml
cp examples/style_guide.example.md STYLE_GUIDE.md
cp examples/feeds.example.csv data/feeds.csv
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

## Testing

Before submitting a PR, ensure:

1. RSS feed fetching works: `python fetch_feeds.py`
2. Memory system works: `python memory.py`
3. Image generation works: Test with `generate_image.py`

## Pull Request Process

1. Update the README.md if you're adding features
2. Add any new dependencies to requirements.txt
3. Ensure your code doesn't break existing functionality
4. Write a clear PR description explaining your changes

## Feature Ideas

Looking for ways to contribute? Here are some ideas:

- [ ] Add support for more RSS feed formats
- [ ] Improve image generation templates
- [ ] Add support for scheduling posts
- [ ] Create a web interface
- [ ] Add support for other social platforms (Twitter/X, etc.)
- [ ] Improve article scoring algorithms
- [ ] Add sentiment analysis for article filtering

## Reporting Bugs

When reporting bugs, please include:

1. Your Python version
2. Your operating system
3. Steps to reproduce the issue
4. Expected vs actual behavior
5. Any error messages

## Questions?

Feel free to open an issue for questions or discussions about potential contributions.
