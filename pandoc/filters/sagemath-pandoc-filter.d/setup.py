from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sagemath-pandoc-filter",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Pandoc filter for processing SageMath code in Markdown documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sagemath-pandoc-filter",
    packages=find_packages(),
    package_data={
        'sagemath_pandoc_filter': ['*.py', 'utils/*.py'],
    },
    install_requires=[
        'panflute>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'sagemath-pandoc-filter=sagemath_pandoc_filter.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
