---
title: Sage Test Document
header-includes:
  - \usepackage{graphicx}
  - \graphicspath{{./sage-images/}}
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \usepackage{hyperref}
papersize: letter
geometry: margin=1in
---

# Sage Test Document

## Basic Computation

```sage
x = 2
y = 3
z = x + y
print(f"The sum of {x} and {y} is {z}")
```

## Plot Example

```sage
# Create a plot of sine and cosine functions
p = plot(sin(x), (x, -pi, pi), color='red', legend_label='$\\sin(x)$')
p += plot(cos(x), (x, -pi, pi), color='blue', legend_label='$\\cos(x)$')
p.set_legend_background_color('#FFFFFF')
# The plot will be displayed automatically in the output
p
```

## Factorial Function

```sage
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
    
fact_5 = factorial(5)
print(f"5! = {fact_5}")
```

## Inline Math

You can use Sage for inline calculations, for example, $2^{10} = 1024$.

## Matrix Example

```sage
# Create and display a matrix
A = matrix([[1, 2], [3, 4]])
print("Matrix A:")
A

# Calculate determinant
print(f"\nDeterminant of A: {A.det()}")
```
