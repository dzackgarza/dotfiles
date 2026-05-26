A regular code block (should pass through unchanged):

```python
def hello():
    print("world")
```

A tikz code block (full document):

```tikz
\documentclass[tikz,border=2pt]{standalone}
\begin{document}
\begin{tikzpicture}
\draw (0,0) -- (1,0);
\node at (0.5,0.5) {hello};
\end{tikzpicture}
\end{document}
```
