# Sage Filter Test Document

## 1. Basic Arithmetic

``` sage
# Simple arithmetic operations
a = 2 + 2
b = 5 * 3
c = 2 ** 10
```

\_\_builtins\_\_ = {\'\_\_name\_\_\': \'builtins\', \'\_\_doc\_\_\': \"Built-in functions, exceptions, and other objects.\\n\\nNoteworthy: None is the \`nil\' object; Ellipsis represents \`\...\' in slices.\", \'\_\_package\_\_\': \'\', \'\_\_loader\_\_\': \<class \'\_frozen_importlib.BuiltinImporter\'\>, \'\_\_spec\_\_\': ModuleSpec(name=\'builtins\', loader=\<class \'\_frozen_importlib.BuiltinImporter\'\>, origin=\'built-in\'), \'\_\_build_class\_\_\': \<built-in function \_\_build_class\_\_\>, \'\_\_import\_\_\': \<built-in function \_\_import\_\_\>, \'abs\': \<built-in function abs\>, \'all\': \<built-in function all\>, \'any\': \<built-in function any\>, \'ascii\': \<built-in function ascii\>, \'bin\': \<built-in function bin\>, \'breakpoint\': \<built-in function breakpoint\>, \'callable\': \<built-in function callable\>, \'chr\': \<built-in function chr\>, \'compile\': \<built-in function compile\>, \'delattr\': \<built-in function delattr\>, \'dir\': \<built-in function dir\>, \'divmod\': \<built-in function divmod\>, \'eval\': \<built-in function eval\>, \'exec\': \<built-in function exec\>, \'format\': \<built-in function format\>, \'getattr\': \<built-in function getattr\>, \'globals\': \<built-in function globals\>, \'hasattr\': \<built-in function hasattr\>, \'hash\': \<built-in function hash\>, \'hex\': \<built-in function hex\>, \'id\': \<built-in function id\>, \'input\': \<built-in function input\>, \'isinstance\': \<built-in function isinstance\>, \'issubclass\': \<built-in function issubclass\>, \'iter\': \<built-in function iter\>, \'aiter\': \<built-in function aiter\>, \'len\': \<built-in function len\>, \'locals\': \<built-in function locals\>, \'max\': \<built-in function max\>, \'min\': \<built-in function min\>, \'next\': \<built-in function next\>, \'anext\': \<built-in function anext\>, \'oct\': \<built-in function oct\>, \'ord\': \<built-in function ord\>, \'pow\': \<built-in function pow\>, \'print\': \<built-in function print\>, \'repr\': \<built-in function repr\>, \'round\': \<built-in function round\>, \'setattr\': \<built-in function setattr\>, \'sorted\': \<built-in function sorted\>, \'sum\': \<built-in function sum\>, \'vars\': \<built-in function vars\>, \'None\': None, \'Ellipsis\': Ellipsis, \'NotImplemented\': NotImplemented, \'False\': False, \'True\': True, \'bool\': \<class \'bool\'\>, \'memoryview\': \<class \'memoryview\'\>, \'bytearray\': \<class \'bytearray\'\>, \'bytes\': \<class \'bytes\'\>, \'classmethod\': \<class \'classmethod\'\>, \'complex\': \<class \'complex\'\>, \'dict\': \<class \'dict\'\>, \'enumerate\': \<class \'enumerate\'\>, \'filter\': \<class \'filter\'\>, \'float\': \<class \'float\'\>, \'frozenset\': \<class \'frozenset\'\>, \'property\': \<class \'property\'\>, \'int\': \<class \'int\'\>, \'list\': \<class \'list\'\>, \'map\': \<class \'map\'\>, \'object\': \<class \'object\'\>, \'range\': \<class \'range\'\>, \'reversed\': \<class \'reversed\'\>, \'set\': \<class \'set\'\>, \'slice\': \<class \'slice\'\>, \'staticmethod\': \<class \'staticmethod\'\>, \'str\': \<class \'str\'\>, \'super\': \<class \'super\'\>, \'tuple\': \<class \'tuple\'\>, \'type\': \<class \'type\'\>, \'zip\': \<class \'zip\'\>, \'\_\_debug\_\_\': True, \'BaseException\': \<class \'BaseException\'\>, \'BaseExceptionGroup\': \<class \'BaseExceptionGroup\'\>, \'Exception\': \<class \'Exception\'\>, \'GeneratorExit\': \<class \'GeneratorExit\'\>, \'KeyboardInterrupt\': \<class \'KeyboardInterrupt\'\>, \'SystemExit\': \<class \'SystemExit\'\>, \'ArithmeticError\': \<class \'ArithmeticError\'\>, \'AssertionError\': \<class \'AssertionError\'\>, \'AttributeError\': \<class \'AttributeError\'\>, \'BufferError\': \<class \'BufferError\'\>, \'EOFError\': \<class \'EOFError\'\>, \'ImportError\': \<class \'ImportError\'\>, \'LookupError\': \<class \'LookupError\'\>, \'MemoryError\': \<class \'MemoryError\'\>, \'NameError\': \<class \'NameError\'\>, \'OSError\': \<class \'OSError\'\>, \'ReferenceError\': \<class \'ReferenceError\'\>, \'RuntimeError\': \<class \'RuntimeError\'\>, \'StopAsyncIteration\': \<class \'StopAsyncIteration\'\>, \'StopIteration\': \<class \'StopIteration\'\>, \'SyntaxError\': \<class \'SyntaxError\'\>, \'SystemError\': \<class \'SystemError\'\>, \'TypeError\': \<class \'TypeError\'\>, \'ValueError\': \<class \'ValueError\'\>, \'Warning\': \<class \'Warning\'\>, \'FloatingPointError\': \<class \'FloatingPointError\'\>, \'OverflowError\': \<class \'OverflowError\'\>, \'ZeroDivisionError\': \<class \'ZeroDivisionError\'\>, \'BytesWarning\': \<class \'BytesWarning\'\>, \'DeprecationWarning\': \<class \'DeprecationWarning\'\>, \'EncodingWarning\': \<class \'EncodingWarning\'\>, \'FutureWarning\': \<class \'FutureWarning\'\>, \'ImportWarning\': \<class \'ImportWarning\'\>, \'PendingDeprecationWarning\': \<class \'PendingDeprecationWarning\'\>, \'ResourceWarning\': \<class \'ResourceWarning\'\>, \'RuntimeWarning\': \<class \'RuntimeWarning\'\>, \'SyntaxWarning\': \<class \'SyntaxWarning\'\>, \'UnicodeWarning\': \<class \'UnicodeWarning\'\>, \'UserWarning\': \<class \'UserWarning\'\>, \'BlockingIOError\': \<class \'BlockingIOError\'\>, \'ChildProcessError\': \<class \'ChildProcessError\'\>, \'ConnectionError\': \<class \'ConnectionError\'\>, \'FileExistsError\': \<class \'FileExistsError\'\>, \'FileNotFoundError\': \<class \'FileNotFoundError\'\>, \'InterruptedError\': \<class \'InterruptedError\'\>, \'IsADirectoryError\': \<class \'IsADirectoryError\'\>, \'NotADirectoryError\': \<class \'NotADirectoryError\'\>, \'PermissionError\': \<class \'PermissionError\'\>, \'ProcessLookupError\': \<class \'ProcessLookupError\'\>, \'TimeoutError\': \<class \'TimeoutError\'\>, \'IndentationError\': \<class \'IndentationError\'\>, \'IndexError\': \<class \'IndexError\'\>, \'KeyError\': \<class \'KeyError\'\>, \'ModuleNotFoundError\': \<class \'ModuleNotFoundError\'\>, \'NotImplementedError\': \<class \'NotImplementedError\'\>, \'RecursionError\': \<class \'RecursionError\'\>, \'UnboundLocalError\': \<class \'UnboundLocalError\'\>, \'UnicodeError\': \<class \'UnicodeError\'\>, \'BrokenPipeError\': \<class \'BrokenPipeError\'\>, \'ConnectionAbortedError\': \<class \'ConnectionAbortedError\'\>, \'ConnectionRefusedError\': \<class \'ConnectionRefusedError\'\>, \'ConnectionResetError\': \<class \'ConnectionResetError\'\>, \'TabError\': \<class \'TabError\'\>, \'UnicodeDecodeError\': \<class \'UnicodeDecodeError\'\>, \'UnicodeEncodeError\': \<class \'UnicodeEncodeError\'\>, \'UnicodeTranslateError\': \<class \'UnicodeTranslateError\'\>, \'ExceptionGroup\': \<class \'ExceptionGroup\'\>, \'EnvironmentError\': \<class \'OSError\'\>, \'IOError\': \<class \'OSError\'\>, \'open\': \<built-in function open\>, \'quit\': Use quit() or Ctrl-D (i.e. EOF) to exit, \'exit\': Use exit() or Ctrl-D (i.e. EOF) to exit, \'copyright\': Copyright (c) 2001-2022 Python Software Foundation.
All Rights Reserved.

Copyright (c) 2000 BeOpen.com.
All Rights Reserved.

Copyright (c) 1995-2001 Corporation for National Research Initiatives.
All Rights Reserved.

Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam.
All Rights Reserved., \'credits\':     Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands
    for supporting Python development.  See www.python.org for more information., \'license\': Type license() to see the full license text, \'help\': Type help() for interactive help, or help(object) for help about object.}

a = 4

b = 15

c = 1024

Results: - $2 + 2 = 4$ - $5 \times 3 = 15$ - $2^{10} = 1024$

## 2. Mathematical Functions

``` sage
# Mathematical functions
x = var('x')
f = sin(x) + cos(x)
df = diff(f, x)
integral_f = integrate(f, x)
```

Function: $f(x) = \cos\left(x\right) + \sin\left(x\right)$\
Derivative: $f'(x) = \cos\left(x\right) - \sin\left(x\right)$\
Integral: $\int f(x)\,dx = -\cos\left(x\right) + \sin\left(x\right) + C$

## 3. Plotting

### 3.1 Basic Plot

\[Error generating plot: name \'torus\' is not defined
Traceback (most recent call last):
  File \"/home/dzack/notes/teaching/sagemath_pandoc_filter.sage\", line 212, in process_sage_plot
    \'disk\': disk, \'sphere\': sphere, \'torus\': torus, \'parametric_plot3d\': parametric_plot3d,
                                             \^\^\^\^\^
NameError: name \'torus\' is not defined
\]

### 3.2 3D Plot

\[Error generating plot: name \'torus\' is not defined
Traceback (most recent call last):
  File \"/home/dzack/notes/teaching/sagemath_pandoc_filter.sage\", line 212, in process_sage_plot
    \'disk\': disk, \'sphere\': sphere, \'torus\': torus, \'parametric_plot3d\': parametric_plot3d,
                                             \^\^\^\^\^
NameError: name \'torus\' is not defined
\]

## 4. Linear Algebra

``` sage
# Matrix operations
A = matrix([[1, 2], [3, 4]])
B = matrix([[0, 1], [1, 0]])
C = A * B  # Matrix multiplication
D = A.inverse()
```

Matrix multiplication: $A \times B = \left(\begin{array}{rr}
2 & 1 \\
4 & 3
\end{array}\right)$\
Inverse of A: $A^{-1} = \left(\begin{array}{rr}
-2 & 1 \\
\frac{3}{2} & -\frac{1}{2}
\end{array}\right)$

## 5. Number Theory

``` sage
# Number theory functions
n = 123456789
is_prime_n = is_prime(n)
factors = factor(n)
```

is_prime_n = False

-   Is $123456789$ prime? $\mathrm{False}$
-   Prime factorization: $123456789 = 3^{2} \cdot 3607 \cdot 3803$

## 6. Silent Computation

The 10th Fibonacci number is $55$.

## 7. Error Handling

### 7.1 Syntax Error

``` sage
# This will cause a syntax error
x = 
```

\[Syntax Error: invalid syntax (\<string\>, line 2)\]

### 7.2 Runtime Error

``` sage
# This will cause a runtime error
1/0
```

\[Error executing code: division by zero\]

## 8. LaTeX Output

``` sage
# Generate LaTeX output
A = matrix(2, 2, [1, 2, 3, 4])
latex_A = A._latex_()
```

latex_A = \\left(\\begin{array}{rr}
1 & 2 \\\\
3 & 4
\\end{array}\\right)

LaTeX output: $\left(\begin{array}{rr}
1 & 2 \\
3 & 4
\end{array}\right)$

## 9. Conclusion

This document tests various Sage features including: - Basic arithmetic
and variables - Mathematical functions and calculus - 2D and 3D
plotting - Linear algebra - Number theory - Silent computation - Error
handling - LaTeX output generation
