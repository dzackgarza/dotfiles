---
title: Comprehensive Sage Test Document
author: Sage Test Suite
date: 2025-06-20
header-includes:
  - |
    ```{=latex}
    \usepackage{amsmath}
    \usepackage{graphicx}
    \usepackage{xcolor}
    \usepackage{hyperref}
    \usepackage{listings}
    \usepackage{tcolorbox}
    \usepackage{float}
    \usepackage{booktabs}
    \usepackage{siunitx}
    \sisetup{group-digits=false}
    \usepackage[margin=1in]{geometry}
    \lstset{basicstyle=\ttfamily\small, breaklines=true, frame=single, backgroundcolor=\color{gray!10}}
    ```
---

# Comprehensive Sage Test Document

This document combines multiple Sage test documents to verify the functionality of the Sage filter.

## Table of Contents
- [Basic Sage Test](#basic-sage-test)
- [Mathematics and Plotting](#mathematics-and-plotting)
- [Advanced Examples](#advanced-examples)

## Basic Sage Test

### Simple Calculation

```sagesilent
a = 5
b = 7
```

### Display Result

The sum of a and b is: $5 + 7 = 12$

### Code Example

```sage
# This is a simple Sage code block
print("The sum of a and b is:", a + b)
print("The product is:", a * b)
```

## Mathematics and Plotting

### Basic Computation

```{.sageblock}
x = 2
y = 3
z = x + y
```

### Plot Example

```sage
# Create a simple plot
plot(sin(x), (x, 0, 2*pi), title='Sine Wave')
```

### Matrix Operations

```sage
# Matrix operations
A = matrix([[1, 2], [3, 4]])
B = matrix([[0, 1], [1, 0]])
print("A + B = ", A + B)
print("A * B = ", A * B)
```

## Advanced Examples

### 3D Plotting

```sage
# 3D surface plot
var('x,y')
plot3d(sin(pi*(x^2+y^2))/2, (x,-1,1), (y,-1,1), color='rainbow')
```

### Symbolic Mathematics

```sage
# Symbolic integration and differentiation
var('x')
f = x^3 + 2*x^2 - 5*x + 6
print("f(x) =") 
show(f)
print("f'(x) =") 
show(diff(f, x))
print("∫f(x)dx =") 
show(integral(f, x))
```

### Interactive Widgets

```sage
# Interactive plot (won't work in static PDF, but good for testing)
@interact
def f(n=(1..10)):
    show(plot(sin(n*x), (x, 0, 2*pi), title=f'sin({n}x)'))
```

## Conclusion

This document serves as a comprehensive test of Sage functionality in Markdown documents. It includes:
- Basic calculations and variable assignments
- Mathematical expressions and plots
- Matrix operations
- 3D visualizations
- Symbolic mathematics
- Interactive elements (for testing in non-PDF contexts)

To compile this document to PDF with Sage code execution, use:

```bash
pandoc --filter sage_filter_package -o combined_sage_tests.pdf combined_sage_tests.md
```
