# Sage Filter Examples

This directory contains example Markdown files that demonstrate the usage of the Sage filter. These examples are part of the `sagemath_pandoc_filter` Python package.

## Example Files

1. `basic_sage_test.md` - A simple test file with basic Sage calculations
2. `combined_sage_test.md` - A comprehensive test document with various Sage examples
3. `combined_sage_tests.md` - The main combined test document
4. `sage_pdf_test.md` - Test file for PDF generation with Sage code
5. `test_output.md` - Example output from running the Sage filter

## How to Use

### From the Project Root

```bash
# Generate all example PDFs
./generate_test_pdfs.sh

# Or process a single file
pandoc --filter ./sage_filter_runner.py \
    -o sage_filter_package/examples/pdfs/output.pdf \
    sage_filter_package/examples/combined_sage_tests.md
```

### From Within the Package

If you're working within the package directory:

```bash
# Navigate to the package directory
cd sage_filter_package

# Run a single example
pandoc --filter ../sage_filter_runner.py \
    -o examples/pdfs/output.pdf \
    examples/combined_sage_tests.md
```

## Generated PDFs

Generated PDFs are stored in the `pdfs/` subdirectory. These are not version controlled as they are generated files.

## Requirements

- Python 3.6+
- SageMath
- Pandoc
- panflute Python package
- The Sage filter package (installed in development mode)
