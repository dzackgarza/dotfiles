# Sage Filter Torture Test

## 1. Basic Mathematical Operations

```sage
1 + 1
```

```sage
2 * (3 + 4) / 5
```

```sage
2**100
```

## 2. Symbolic Mathematics

```sage
var('x y')
(x + y)^3
```

```sage
diff(sin(x) * cos(x), x)
```

## 3. Plot Types

### 3.1 Basic 2D Plot
```sage
plot(x^2, (x, -2, 2))
```

### 3.2 3D Plot
```sage
plot3d(x^2 + y^2, (x, -2, 2), (y, -2, 2))
```

### 3.3 Graph Theory Plot
```sage
G = graphs.PetersenGraph()
G.show()
```

## 4. Matplotlib Integration

```sage
import matplotlib.pyplot as plt
plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt
```

## 5. LaTeX Output

```sage
latex(integrate(1/(1+x^2), x))
```

## 6. Error Cases

### 6.1 Syntax Error
```sage
1 +
```

### 6.2 Runtime Error
```sage
1/0
```

## 7. System Commands

```sage
!echo "Hello from shell"
```

## 8. Multiple Code Blocks with Variables

```sage
a = 5
b = 7
a * b
```

```sage
a + b  # Should raise NameError if no persistence
```

## 9. Plot with Custom Options

```sage
plot(x^2, (x, -2, 2), axes_labels=['$x$', '$y$'], 
     title='$y = x^2$', figsize=4, gridlines=True)
```
