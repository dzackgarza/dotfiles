tests = []

before = r"""
Wikilinks [[like this]] must be ignored.
"""
after = before
tests += (before, after)

before = r"""
Preserve [[strange wikilinks | wikilinks]] as well.
"""
after = before
tests += (before, after)


before = r"""
Leave correct math alone
\begin{align*}
f(x) = 2
\end{align*}
"""
after = before
tests += (before, after)

before = r"""
Format incorrect math \begin{align*}
f(x) = 2
\end{align*}
"""

after = r"""
Format incorrect math 
\begin{align*}
f(x) = 2
\end{align*}
"""
tests += (before, after)

before = r""" 
Correct math must be preserved.
\[
f(x) = 2
.\]
"""
after = before
tests += (before, after)

before = r""" 
Displaymath should be bumped to a new line \[
f(x) = 2
\]
"""
after = r"""
Displaymath should be bumped to a new line 
\[
f(x) = 2
\]
"""

before = r"""
:::{.example title="Algebraic Spaces"}
[[algebraic space|Algebraic spaces]], e.g. $\PP^n$.
Think of these as [étale sheaves](étale sheaves) of sets (think functor of points), identified as discrete spaces:
\[  
\mathcal{S}_{\leq 0} \da \ts{\text{Discrete spaces}}
.\]

"""
after = before
tests += (before, after)

before = r"""
:::{.example title="Algebraic Spaces"} Some text on the wrong line.
[[algebraic space|Algebraic spaces]], e.g. $\PP^n$.
Think of these as [étale sheaves](étale sheaves) of sets (think functor of points), identified as discrete spaces:
\[  
\mathcal{S}_{\leq 0} \da \ts{\text{Discrete spaces}}
.\]

Every component is contractible, so there are no higher homotopy groups and we think of these as 0-truncated spaces.
:::
"""

# Should not introduce hyperlink encoding
after = r"""
:::{.example title="Algebraic Spaces"}
Some text on the wrong line.
[[algebraic space|Algebraic spaces]], e.g. $\PP^n$.
Think of these as [étale sheaves](étale sheaves) of sets (think functor of points), identified as discrete spaces:
\[  
\mathcal{S}_{\leq 0} \da \ts{\text{Discrete spaces}}
.\]

Every component is contractible, so there are no higher homotopy groups and we think of these as 0-truncated spaces.
:::
"""
tests += (before, after)

before = r"""
::: {.remark}
Some strange spacing.
:::
"""

after = r"""
:::{.remark}
Some strange spacing.
:::
"""
