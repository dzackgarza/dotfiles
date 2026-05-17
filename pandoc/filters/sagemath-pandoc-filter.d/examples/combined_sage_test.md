---
title: Sage Filter Test Document
author: Sage Test Suite
date: 2025-06-20
papersize: letter
geometry: margin=1in
header-includes:
  - \usepackage{amsmath}
  - \usepackage{graphicx}
  - \usepackage{xcolor}
  - \usepackage{hyperref}
  - \usepackage{listings}
  - \usepackage{tcolorbox}
  - \usepackage{float}
  - \usepackage{booktabs}
  - \usepackage{siunitx}
  - \sisetup{group-digits=false}
  - \lstset{basicstyle=\ttfamily\small, breaklines=true, frame=single, backgroundcolor=\color{gray!10}}
---

# Sage Filter Test Document

## 1. Basic Arithmetic

```sage
# Simple arithmetic operations
a = 2 + 2
b = 5 * 3
c = 2 ** 10
print(f"Results:")
print(f"- 2 + 2 = {a}")
print(f"- 5 × 3 = {b}")
print(f"- 2^10 = {c}")
```

## 2. Mathematical Functions

```sage
# Mathematical functions
x = var('x')
f = sin(x) + cos(x)
df = diff(f, x)
int_f = integral(f, x)

print("Function:")
print(f"f(x) = {f}")
print("\nDerivative:")
print(f"f'(x) = {df}")
print("\nIntegral:")
print(f"∫f(x)dx = {int_f} + C")
```

## 3. Plotting

### 3.1 Basic Plot

```sage
# Create a simple plot
p = plot(sin(x), (x, 0, 2*pi), color='red', legend_label='$\\sin(x)$')
p += plot(cos(x), (x, 0, 2*pi), color='blue', legend_label='$\\cos(x)$')
p.set_legend_background_color('#FFFFFF')
# The plot will be displayed automatically
p
```

### 3.2 3D Plot

```sage
# 3D surface plot
var('x,y')
plot3d(sin(pi*(x^2+y^2))/2, (x,-1,1), (y,-1,1), color='rainbow')
```

## 4. Linear Algebra

```sage
# Matrix operations
A = matrix([[1, 2], [3, 4]])
B = matrix([[0, 1], [1, 0]])
C = A * B
D = A.inverse()

print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)
print("\nMatrix multiplication A × B:")
print(C)
print("\nInverse of A:")
print(D)
```

## 5. Number Theory

```sage
# Number theory functions
n = 123456789
is_prime_n = is_prime(n)
factors = factor(n)

print(f"Is {n} prime? {is_prime_n}")
print(f"Prime factors of {n}:")
print(factors)
```

## 6. Fibonacci Sequence

```sage
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


fib_10 = fibonacci(10)
print(f"The 10th Fibonacci number is {fib_10}")
```

## 7. Error Handling

### 7.1 Syntax Error

```sage
# This will cause a syntax error
# Uncomment to test:
# x = 
print("This line demonstrates where a syntax error would occur")
```

### 7.2 Runtime Error

```sage
# This will cause a runtime error
try:
    result = 1/0
except Exception as e:
    print(f"Caught an error: {e}")
```

## 8. LaTeX Output

```sage
# Generate LaTeX output
A = matrix(2, 2, [1, 2, 3, 4])
print("Matrix A:")
print(A)
print("\nLaTeX representation:")
print(A._latex_())
```

## 9. Conclusion

This document tests various Sage features including:
- Basic arithmetic and variables
- Mathematical functions and calculus
- 2D and 3D plotting
- Linear algebra
- Number theory
- Silent computation
- Error handling
- LaTeX output generation
