# Sage Filter for Pandoc

A Pandoc filter for processing SageMath code blocks and inline expressions in Markdown documents.

## Features

- Process Sage code blocks and inline expressions in Markdown
- Support for both 2D and 3D plots
- LaTeX output for mathematical expressions
- Error handling and reporting

## Installation

```bash
pip install -e .
```

## Usage

```bash
pandoc input.md -F sagemath-pandoc-filter -o output.html
```

## Development

### Running Tests

```bash
python -m sagemath_pandoc_filter.tests.test_plot_generation
```

### Building the Package

```bash
python setup.py sdist bdist_wheel
```
