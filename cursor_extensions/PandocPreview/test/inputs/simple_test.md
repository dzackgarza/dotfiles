# A small, simple test

:::{.lemma title="Correspondence between bilinear and quadratic forms"}
Every $\QQ$-valued bilinear module $(L, \beta)$ (not necessarily symmetric) determines a $\QQ$-valued quadratic module $(L, q_\beta)$
\begin{align*}
q_\beta: L &\to \QQ \\
v &\mapsto q_\beta(v) \da \beta(v,v)
,\end{align*}
which only depends on the symmetric part of $\beta$, given by ${1\over 2}(\beta^t + \beta)$.
Conversely, every $\QQ$-valued quadratic module $(L, q)$ determines a *symmetric* module $(L, \beta_q)$ where
\begin{align*}
\beta_q: L\tensor_\ZZ L &\to \QQ \\
v \tensor w &\mapsto \beta_q(v) \da q(v + w) - q(v) - q(w)
\end{align*}
is the polar form of $q$.
Thus there are maps
\begin{align*}
T^2_\ZZ(L\dual) &\to \Quad_\ZZ(L)   \to \Sym^2_\ZZ(L) \\
\beta   &\mapsto q_\beta             \\
        &\qquad\qquad\qquad\qquad      q        \mapsto \beta_q
.\end{align*}
Moreover, by ???, the map $\beta\mapsto q_\beta$ is surjective, i.e. every $\ZZ$-valued quadratic form $q$ can be written as the quadratic form $\beta(v,v)$ associated to a bilinear form $\beta$.
However, note that the lift of $q$ to $\beta$ need not be unique.
:::