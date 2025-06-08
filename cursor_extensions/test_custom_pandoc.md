# Lattice Theory

:::{.remark}
Throughout this section, $R$ is an integral domain which we often take to be $\ZZ$.
We write $k$ for its field of fractions, often taken to be $\QQ$.
We write the group of units as $R\units$, and $L, M$ are generally finitely generated projective $R$-modules.
Over $R=\ZZ$, these will be regarded as free modules of finite $\ZZ$-rank.
We write $\ZZpadic$ for the ring of $p$-adic integers, and $\QQpadic$ for its field of fractions.
We write $\beta$ for a general symmetric bilinear form.
If $S$ is an $\ZZ$-module, we write $L_S \da L \tensor_\ZZ S$ for the base change of $L$ to an $S$-module.
In particular, if $L$ is a $\ZZ$-module, there are naturally defined extensions $L_\QQ, L_\RR, L_\CC$, as well as $L_{\ZZpadic}$ for any prime $p$.
We write $\FF_p$ for the finite field with $p$ elements, and $C_n$ for the cyclic group of order $n$.
:::

## Bilinear/Quadratic Modules and Lattices

From here onward, $L$ will be a free $\ZZ$-module of finite rank $n$.

:::{.definition title="Bilinear modules/forms"}
Let $L$ be a $\ZZ$-module.
A **bilinear form** $\beta$ on $L$ is a morphism 
\begin{align*}
\beta \in \Hom_\ZZ( L \tensor_\ZZ L, &\ZZ) \\
v\tensor w &\mapsto \beta(v, w)
,\end{align*}
which can be regard as an element of $\Sym^2_\ZZ(L\dual)$.
We often omit $\beta$ from the notation and simply write $vw$ or $v\cdot w$ for $\beta(v, w)$.
We refer to a general pair $(L, \beta)$ as a **bilinear $\ZZ$-module**.
We write $T^2_\ZZ(L\dual)$ or simply $\Bil_\ZZ(L)$ for the set of bilinear forms on a fixed module $L$.

More generally, we may allow bilinear forms to be $\QQ$-valued, in which case we say $\beta$ is **integral** if its image $\beta(L, L)$ is contained in $\ZZ$.
:::

:::{.definition title="Symmetric/skew-symmetric bilinear forms"}
A bilinear form $\beta: L\tensor_\ZZ L\to \QQ$ is **$\eps$-symmetric** for $\eps\in \QQ$ if 
\[
\beta(a, b) = \eps. \beta(b, a)
.\]

- If $\eps = 1$, we say $\beta$ is **symmetric**.
- If $\eps = -1$ we say $\beta$ is **skew-symmetric**.
- $\beta$ is **alternating** if $\beta(a,a) = 0$ for all $a\in L$.
:::

:::{.remark}
Note that any bilinear form $\omega$ gives rise to a symmetric form defined by $\beta \da {1\over 2}(\omega^t + \omega)$, where $\omega^t(a,b) \da \omega(b,a)$.
If $\omega$ is skew-symmetric, then the associated symmetric form is zero.
:::

:::{.definition title="Quadratic modules/forms"}
A **quadratic form** on $L$ is a morphism of sets $q: L\to S$ such that

- $q(\lambda . v) = \lambda^2 .q(v)\in \QQ$ for all $v\in L$ and all $\lambda \in \QQ$, and
- Its **polar form**
\begin{align*}
\beta_q: L \tensor_\ZZ L &\to \QQ \\
(v, w) &\mapsto \beta_q(v,w)\da q(v + w) - q(v) - q(w)
\end{align*}
is a symmetric bilinear form on $L$.

We similarly say $q$ is **integral** if $q(L) \subseteq \ZZ$, and refer to the pair $(L, q)$ as a **quadratic $\ZZ$-module**.
We write $\Quad_\ZZ(L)$ or simply $\Quad_\ZZ(L)$ for the set of all quadratic forms on a fixed module $L$.
:::

:::{.definition title="Lattices"}
A **lattice** is a pair $(L, \beta)$ where $L$ is a free $\ZZ$-module of finite rank and $\beta$ is a (possibly $\QQ$-valued) nondegenerate symmetric bilinear form.
We often require $\beta$ to be integral, but occasionally also refer to modules with $\QQ$-valued forms as lattices by abuse of language.

Similarly, we refer to a pair $(L, q)$ as a **quadratic lattice** if $q$ is a nondegenerate quadratic form, again possibly $\QQ$-valued, which is often required to be integral.
:::

:::{.definition title="Even/odd lattices"}
If $(L,\beta)$ is a lattice, we say $L$ is **even** if $\beta(v,v) \in 2\ZZ$ for all $v\in L$, and is **odd** otherwise.
:::

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

:::{.lemma}
There is a bijection
\begin{align*}
\ts{\beta\in \Sym^2_\ZZ(L\dual) \st \beta \text{ is even}} &\mapstofrom \Quad_\ZZ(L) \\
\beta &\mapsto {1\over 2}q_\beta \\
\beta_q &\mapsfrom q
\end{align*}
In other words, the polar form of every integral symmetric form is even, and every *even* symmetric integral form $\beta$ is the polar form of an integral quadratic form, namely $q(v) \da {1\over 2}\beta(v,v)$.
Moreover, if $q$ is any quadratic form, then ${1\over 2}\beta_q$ recovers $q$.
:::

:::{.proof}
Note that for any integral $q$, the polar form is always even:
\[
\beta_q(v,v) \da q(v+v) - q(v) - q(v) = 4q(v)-2q(v) = 2q(v) \in 2\ZZ
.\]
Moreover, if $\beta$ is even, then ${1\over 2}q_\beta$ is integral, so both maps are well-defined.

We first consider the composite $\beta \mapsto {1\over 2}q_\beta \mapsto \beta_{{1\over 2} q_\beta}$:
\begin{align*}
\beta_{{1\over 2}q_\beta}(v, w)
&\da {1\over 2}q_{\beta}(v+w) - {1\over 2}q_{\beta}(v) - {1\over 2}q_{\beta}(w) \\
&= {1\over 2} \qty{\beta(v,v) + \beta(v,w) + \beta(w, v) + \beta(w,w) - \beta(v,v) - \beta(w,w)} \\
&= {1\over 2}\qty{\beta(v,w) + \beta(w, v) } \\
&= \beta(v, w)
\end{align*}
We then consider the composite $q\mapsto \beta_{q} \mapsto {1\over 2}q_{\beta_q}$;
\begin{align*}
{1\over 2}q_{\beta_q}(v)
&\da {1\over 2}\beta_q(v,v) \\
&\da {1\over 2}\qty{ q(v + v) - q(v) - q(v) } \\
&= {1\over 2}\qty{ q(2v) - 2q(v) } \\
&= {1\over 2}\qty{ 4q(v) - 2q(v) } \\
&= {1\over 2}\qty{ 2q(v)} \\
&= q(v)
\end{align*}
Thus these maps are mutually inverse.
:::

:::{.remark}
It is worth noting that some sources instead use the correspondence $\beta \mapsto q_\beta$ and $q\mapsto {1\over 2}\beta_q$.
Over $\QQ$, this is an equivalent formulation since $2$ is invertible, but over $\ZZ$ one loses the bijection with even lattices by using this convention. 
:::

:::{.definition title="Gram matrices"}
Let $(L, \beta)$ be a bilinear module.
Choosing a basis $B_L = (e_i)_{1\leq i\leq n}$, for any $v,w\in L$ one can write $v = \sum_j a_j e_j$ and $w= \sum_j b_j e_j$ for some coefficients $a_j, b_j \in \ZZ$.
Using bilinearity, one can then write
\[
\beta(v, w) 
= \beta\qty{ \sum_j a_j e_j, \sum_j b_j e_j} 
= \sum_{i, j} a_i b_j \cdot \beta(e_i, e_j) 
\da v^t G_\beta w
\]
for some (not necessarily unique) matrix $G_\beta \da (\beta(e_i, e_j))_{i,j} \in \Mat_{n\times n}(\QQ)$, which we refer to as the **Gram matrix of $\beta$**.

Similarly, if $(L, q)$ is a quadratic module, one can write 
\[
q(v) = q\qty{ \sum_j a_j e_j} = \sum_{i, j} a_i a_j \cdot (G_q)_{i, j} = v^t G_q v
\]
for some (not necessarily unique) matrix $G_q \in \Mat_{n\times n}(\QQ)$, which we similarly refer to as the **Gram matrix of $q$**.
:::

:::{.remark}
If $(L, \beta)$ is a bilinear module, then

- $\beta$ is symmetric if $G_\beta^t = G_\beta$,
- $\beta$ is skew-symmetric if $G_\beta^t = -G_\beta$, and
- $\beta$ is alternating if $\diag(G_\beta) = (0, 0,\cdots, 0)$ and $G_\beta^t = -G_\beta$.

Moreover, if $(L, \beta)$ is a lattice, it is even if and only if $G_\beta\in \Mat_{n\times n}(\ZZ)$ and $\diag(G_\beta)\in (2\ZZ)^n$.
:::


:::{.remark}
Note that if $(L, \beta)$ is a lattice with associated quadratic lattice $(L, \beta_q)$, the Gram matrix $G_{\beta_q}$ can be taken to be $G_{\beta}$. 
This is because if $\beta(v, w) = v^t G_\beta w$, then $q_\beta(v) = \beta(v,v) = v^t G_\beta v$.

One can show that one possible Gram matrix of a quadratic form $q$ is proportional to the Hessian of $q(x)$ regarded as a polynomial function $\QQ^n\to \QQ$, namely
\[
G_{H, q} = {1\over 2} H(q(x)), \qquad H(q(x))_{i,j} \da \qty{ {\partial^2 q \over \partial x_i \partial x_j} }
,\]
which is generally non-integral.
Alternatively, one can take a write a matrix $G_q$ in terms of $q$ and its polar form $\beta_q$ as
\[
G_{q} = \left(\begin{array}{cccc}
q(e_1) & \beta_q(e_1, e_2) & \cdots & \beta_q(e_1, e_n) \\ 
0 & q(e_2) & \cdots & \beta_q(e_2, e_n) \\ 
\vdots & \ddots & \ddots & \vdots \\ 
0 & \cdots & 0 & q(e_n) \end{array}\right), \qquad
a_{ij} \da \beta_q(e_i, e_j), \qquad i < j
,\]
which is integral whenever $q$ is integral.
One can then recover the Gram matrix for the polar form of $q$ as $G_{\beta_q} = G_q + G_q^t$.

These two choices of Gram matrices are related by $G_{q, H} = {1\over 2}(G_{q} + G_{q}^t)$, and so one can be recovered from the other over $\QQ$.
Over $\ZZ$, we will typically make a preferred choice of $G_q$ as the latter matrix to avoid denominators.
:::

:::{.example}
Consider the $\ZZ$-valued quadratic form on $\ZZ^3$ defined by
\[
q(x,y,z) = ax^2 + by^2 + cz^2 + dyz + exz + fxy, \qquad a,\cdots,f\in \ZZ
.\]
Using the Hessian, one obtains the symmetric (but non-integral) matrix
\[
G_{g, H} \da
{1\over 2}H(q(x,y,z)) =
\begin{pmatrix}
a               & {1 \over 2}f  & {1\over 2}e \\
{1\over 2} f    & b         & {1\over 2}d \\
{1\over 2}e     & {1\over 2}d & c
\end{pmatrix}
\in \Mat_{3\times 3}(\QQ)
\]
and verify that if $v = \tv{x,y,z}\in \ZZ^3$ then $v^t G_{q, H} v = q(x,y,z)$.
However, one can also take
\[
G_{q} = 
\begin{pmatrix}
a & f & e \\
0 & b & d \\
0 & 0 & c
\end{pmatrix}
\in \Mat_{3\times 3}(\ZZ)
,\]
which is now integral and similarly satisfies $v^t G_{q} v = q(x,y,z)$.
One can check directly that $G_{q, H} = {1\over 2}(G_q + G_q^t)$.
Letting $\beta_q$ be the polar form of $q$, either of the above matrices can be used to obtain the (integral) Gram matrix of $\beta_q$:
\[
G_{\beta_q} = 
\begin{pmatrix}
2a & f & e \\
f & 2b & d \\
e & d & 2c
\end{pmatrix}
 = G_{q, H} + G_{q, H}^t = G_{q} + G_{q}^t \in \Mat_{3\times 3}(\ZZ)
.\]
:::

:::{.definition title="Orthogonal direct sums"}
Let $(L, \beta_L)$ and $(M, \beta_M)$ be integral lattices.
We define their **orthogonal direct sum** as the lattice $(L \oplus M, \beta_{L\oplus M})$ where $L\oplus M$ is their direct sum as $\ZZ$-modules, and the bilinear form is given by

\begin{align*}
\beta_L \oplus \beta_M: (L\oplus M)\tensor_\ZZ (L\oplus M) &\to \ZZ \\
(\ell_1 + m_1, \ell_2 + m_2) &\mapsto \beta_L(\ell_1, \ell_2) + \beta_M(m_1, m_2)
.\end{align*}
We write $L^{\oplus n}$ for the $n$-fold direct sum $\bigoplus_{i=1}^n L$.

Similarly, if $(L, q_L)$ and $(M, q_M)$ are integral quadratic lattices, we define their direct sum as $(L\oplus M, q_L \oplus q_M)$ where
\begin{align*}
q_L \oplus q_M: L \oplus M &\to \ZZ \\
\ell + m &\mapsto q_L(\ell) + q_M(m)
\end{align*}
:::

:::{.remark}
In any fixed basis, the Gram matrix for a direct sum can be realized as the block sum of the respective Gram matrices, i.e. 
\[
G_{\beta_L \oplus \beta_M} = 
\left[\begin{array}{@{}c|c@{}}
  G_{\beta_L} & 0 \\
\hline
  0 & G_{\beta_M}
\end{array}\right]
,\qquad 
G_{q_L \oplus q_M} = 
\left[\begin{array}{@{}c|c@{}}
  G_{q_L} & 0 \\
\hline
  0 & G_{q_M}
\end{array}\right]
.\]
:::

> TODO: define primitive sublattices before indecomposable.

:::{.definition title="Indecomposable lattices"}
Let $(L, \beta)$ be a lattice.
If $L$ can not be written as a direct sum $L = S \oplus T$ for two primitive sublattices $S, T\leq L$, we say $L$ is **indecomposable**.
:::

:::{.remark}
Note that $L$ may be decomposable as a module but not as a lattice.
:::

> TODO: define rank and signature before these examples?

:::{.example title="Rank 1 and diagonal lattices "}
For $a\in \ZZ$ we define $\gens{a}$ to be the lattice corresponding to the bilinear form $\beta(x, y) = axy$ for $x,y \in \ZZ$, which has a $1\times 1$ Gram matrix $G_{\gens a} = [a]$.
The corresponding quadratic form is $q_\beta(x) = ax^2$ for $x\in \ZZ$, yielding a quadratic lattice that we write as $\sqgens{a}$ which has the Gram matrix $G_{\beta_q} = [a]$.

More generally, for $a_1, \cdots, a_n\in \ZZ$, we define the "diagonal" lattice $\gens{a_1, \cdots, a_n} \da \gens{a_1} \oplus \cdots \oplus \gens{a_n}$ which corresponds to the form
\[
\beta(x, y) = \sum_{i=1}^n a_i x_i y_i \quad (x,y\in \ZZ^n), \qquad
G_\beta = 
\begin{pmatrix}
a_1 &       &   & \\
    &  a_2  &   & \\
    &       & \ddots & \\
    &       &   & a_n
\end{pmatrix}
.\]
The corresponding quadratic form is
\[
q_\beta(x) = \sum_i a_i x_i^2
\quad (x\in \ZZ^n), \qquad
G_{q_\beta} = 
\begin{pmatrix}
a_1 &       &   & \\
    &  a_2  &   & \\
    &       & \ddots & \\
    &       &   & a_n
\end{pmatrix}
,\]
and we write this quadratic lattice as $\sqgens{a_1, \cdots, a_n} \da \sqgens{a_1} \oplus \cdots \oplus \sqgens{a_n}$.
We note that with our current conventions, the matrices $G_\beta$ and $G_{q_\beta}$ will always coincide.
:::

:::{.example title="Rank 2 bilinear and quadratic forms"}
For the following examples, let $L = \ZZ^2$ and fix a standard basis.

1. The map
\begin{align*}
\beta: \ZZ^2 \tensor_\ZZ \ZZ^2 &\to \ZZ \\
\qty{ \cvec{x_1}{y_1}, \cvec{x_2}{y_2}} &\mapsto a x_1 x_2 + b y_1 y_2
\end{align*}
is a symmetric bilinear form with Gram matrix $G_\beta = \matt a 0 0 b$. 
It coincides with the standard dot product when $a=b=1$.
The associated lattice $(L, \beta)$ is decomposable and equal to $\gens{a, b}$.
The associated quadratic form  is
\begin{align*}
q_\beta: \ZZ^2 &\to \ZZ \\
\cvec x y & \mapsto ax^2 + by^2
\end{align*}
with Gram matrix $G_{q_\beta} = G_\beta$, yielding the quadratic lattice $\gens{a, b}$.

3. The map
\begin{align*}
\beta: \ZZ^2 \tensor_\ZZ \ZZ^2 &\to \ZZ \\
\qty{ \cvec{x_1}{y_1}, \cvec{x_2}{y_2}} &\mapsto x_1 y_2 - x_2 y_1
\end{align*}
is an alternating, skew-symmetric form with Gram matrix $G_{\beta} = \matt{0}{1}{-1}{0}$.
The associated symmetric form is defined by $G_\beta^t + G_\beta$, which is the zero matrix, and thus the associated (symmetric) lattice and quadratic lattice are both zero.

4. The map
\begin{align*}
q: \ZZ^2 &\to \ZZ \\
\cvec x y &\mapsto ax^2 + bxy + cy^2
\end{align*}
is a binary quadratic form with possible Gram matrices
\[
G_{q, H} = \matt {a}{b\over 2}{b\over 2}{c} \in \Mat_{2\times 2}(\QQ),
\qquad
G_{q} = \matt{a}{b}{0}{c} \in \Mat_{2\times 2}(\ZZ)
.\]
Its polar form $\beta_q$ has Gram matrix 
\[
G_{\beta_q} = G_q + G_q^t = \matt{2a}{b}{b}{2c}
\]
and represents the symmetric form
\begin{align*}
\beta_q: \ZZ^2 \tensor_\ZZ \ZZ^2 &\to \ZZ \\
\qty{\cvec{x_1}{y_1}, \cvec{x_2}{y_2} } &\mapsto 2a x_1 x_2 + bx_2 y_1 + bx_1 y_2 + 2cy_1 y_2 
\end{align*}
The associated lattice $(L, \beta_q)$ is rank 2 and generally indecomposable.
:::


:::{.definition title="Definite forms"}
We say a lattice $(L, \beta)$ 

- **positive definite** if $\beta(v, v) > 0$,
- **positive semidefinite** if $\beta(v, v) \geq 0$,
- **negative definite** if $\beta(v, v) < 0$, or
- **positive semidefinite** if $\beta(v, v) \leq 0$

for all nonzero $v\in L$.
We say a lattice is **indefinite** if it is neither positive nor negative semidefinite.
:::

:::{.remark title="Criteria for definiteness"}
A symmetric matrix $A \in \Mat_{n\times n}(\QQ)$ is positive definite if and only if any of the following equivalent conditions hold:

- $A$ can be diagonalized over $\RR$ where each diagonal entry is positive,
- All eigenvalues of $A$ are real and positive,  or
- All of the leading principal minors of $A$ are positive.

Similar criteria can be used to check if $A$ is positive semidefinite and negative (semi)definite.
We most often apply these criteria to Gram matrices $A \da G_\beta$ for a lattice $(L, \beta)$ or $A \da G_{q, H}$ for a quadratic lattice $(L, q)$.
:::

:::{.definition title="Extensions of bilinear forms"}
Let $(L, \beta)$ be a lattice and let $S$ be any $\ZZ$-algebra.
Then there is naturally a pair $(L_S, \beta_S)$ where $L_S \da L\tensor_\ZZ S$ is an $S$-module whose bilinear form $\beta_S$ takes values in $\ZZ \tensor_\ZZ S \cong S$.
It is defined by
\begin{align*}
\beta_S: L_S \tensor_S L_S &\to \ZZ\tensor_\ZZ S = S \\
(v_1 \tensor s_1, v_2 \tensor s_2) &\mapsto \beta(v_1, v_2) \tensor s_1 s_2 = s_1s_2. \beta(v_1, v_2)
\end{align*}
where $s_1s_2$ is the multiplication in $S$.
When there is no danger of confusion, we write this as
\[
\beta_S( s_1v_1, s_2 v_2) \da s_1 s_2 .\beta(v_1, v_2) \qquad s_i\in S, v_i\in L
.\]
The action of $S$ on $L_S$ is defined by
\[
s_1.(v\tensor s_2) \da v\tensor(s_1s_2)
.\]
We will most frequently apply this to $S \da \QQ, \RR, \CC, \FF_p$, and $\ZZpadic$.
:::

:::{.remark title="On complex extensions"}
\label[remark]{rmk:complex_extensions_of_bilinear_forms}
Note that over $S=\CC$, the extended lattice $L_\CC$ carries both a **bilinear** extension $\beta_\CC$ and a **sesquilinear** extension $H_\CC^\beta$.
These are defined by 
\begin{align*}
\beta_\CC: L_\CC \tensor_\CC L_\CC &\to \CC \\
(z_1 \tensor v_1, z_2 \tensor v_2) &\mapsto z_1z_2.\beta(v_1, v_2) \\ \\
H^\beta: L_\CC \tensor_\CC L_\CC &\to \CC \\
(z_1 \tensor v_1, z_2 \tensor v_2) &\mapsto z_1\overline{z_2}.\beta(v_1, v_2) 
\end{align*}
where we've used the canonical complex conjugation on the complexification $L_\CC$ defined by $\overline{z\tensor v} \da \overline{z}\tensor v$.
These two extensions are related by $H^\beta(v, w) \da \beta_\CC(v, \overline{w})$ for $v,w\in L_\CC$.

To carry out explicit computations, one can use the decomposition $L_\CC \cong L_\RR + iL_\RR$ to write every element $v\in L_\CC$ as $v = x + iy$ where $x,y\in L_\RR$ and conjugation acts by $\bar{x+iy} \da x-iy$.
We then have
\begin{align*}
\beta_\CC(x_1 + iy_1, x_2 + iy_2) &= \beta_\RR(x_1, x_2) - \beta_\RR(y_1, y_2) + i\qty{\beta_\RR(y_1, x_2) + \beta_\RR(x_1, y_2)} \\
H_\CC^\beta(x_1 + iy_1, {x_2 + iy_2}) &= \beta_\RR(x_1, x_2) + \beta_\RR(y_1, y_2) + i\qty{\beta_\RR(y_1, x_2) - \beta_\RR(x_1, y_2)} \\
\end{align*}
:::

## Lattices

:::{.definition title="Scale and integrality"}
Let $(L, \beta)$ be an integral lattice.
The **scale** of $(L, \beta)$ is the fractional ideal of $\QQ$ defined by
$\mfa_L \da \beta(L, L) \subseteq \ZZ$.
When there is no danger of confusion, we identify $\mfa_L$ with its positive generator.
:::

:::{.remark}
Note that $\mfa_L = \ZZ$ if and only if $(L, \beta)$ is integral , while $\mfa_L = 2\ZZ$ is a stronger condition than $L$ being even.
The scale of $L$ can quickly be computed as the greatest common divisor of all entries in $G_\beta$ in any basis.
:::

:::{.definition title="Twists of lattices"}
Given a lattice $(L, \beta_L)$ and $n\in \QQ$, we define the **twist** of $L$ by $n$ as the pair $(L(n), \beta_{L(n)})$ where $L(n)$ has the same underlying module structure as $L$ and the rescaled bilinear form is defined as
\[
\beta_{L(n)}(v, w) \da n\cdot \beta_L(v,w) \qquad \forall v,w\in L, \qquad G_{\beta_{L(n)}} = n\cdot G_{\beta_L}
.\]
If $n\in \ZZ$ and $L$ is integral, then $L(n)$ is again integral, but for a general nonzero rational $n$ this yields a $\QQ$-valued lattice.

Similarly, if $(L, q_L)$ is a quadratic lattice, we define its twist $(L(n), q_{L(n)})$ as
\[
q_{L(n)}(v) \da n q_L(v) \qquad \forall v\in L, \qquad G_{q_{L(n)}} = n G_q
.\]
:::

:::{.remark}
\label[remark]{rmk:lattices_in_a_vector_space}
If $V$ is a finite rank module over a field $k$, we say $L$ is a **lattice in $V$** if $L$ is finitely generated as a $\ZZ$-submodule of $V$ and $L_k \cong V$ as $k$-modules.
This occurs if and only if every $\ZZ$-basis of $L$ extends to a $k$-basis of $V$, where we often take $k=\QQ$ or $\RR$.
All lattices in the previous sense can be regarded as lattices in $V \da L_\QQ$ or $L_\RR$ under the natural injections $L\injects L_\QQ$ and $L\injects L_\RR$.
:::


## Nondegeneracy of lattices

:::{.definition title="Orthogonal complements and discriminant groups"}
If $L$ is an integral lattice, there is a map
\begin{align*}
\iota: L &\to L\dual \\
v &\mapsto \beta(v, \wait)
\end{align*}
which for any $S\leq L$ defines an exact sequence of $\ZZ$-modules
\[
0\to S^{\perp L} \injects L \mapsvia{ \ro{\iota}{S} } L\dual
.\]

For $S=L$, we obtain a longer short exact sequence of the form
\[
0 \injects L^{\perp L} \da \ker(\iota) \injects L \mapsvia{\iota} L\dual \surjects A_L\da\coker(\iota) \to 0
.\]


We call

- $S^{\perp L}$ the **orthogonal complement of $S$ in $L$**, 
- $\radic(L) \da L^{\perp L} \da \ker(\iota)$ the **radical** of $L$, and
- $A_L \da \coker(\iota)$ the **discriminant group of $L$**.

We say $L$ is **nondegenerate** if $\radic(L) = 0$.

Note that we can explicitly write
\[
S^{\perp L} \da \ts{v\in L \st \beta(v, S) = 0}, \qquad A_L \da L\dual/\iota(L)
,\]
and if $\beta(v_1, v_2) = 0$, we write $v_1 \perp_L v_2$ or $v_1 \in \gens{v_2}^{\perp L}$.
Note that if $L$ is nondegenerate, then $\iota$ is an injection and we simply write $A_L = L\dual/L$.
:::

:::{.remark}
One can make similar definitions for a quadratic module $(L, q)$ in terms of its associated bilinear form $\beta_q$.
:::

:::{.remark}
Note that any $\beta$ induces a nondegenerate bilinear form on a quotient of $L$, namely
\begin{align*}
\tilde \beta: {L\over \radic(L)}\tensor_\ZZ {L\over \radic{L}} &\to \ZZ \\
(v + \radic{L}, w + \radic{L}) &\mapsto \beta(v, w)
\end{align*}

Moreover, since $\tilde L \da L/\radic(L)$ is finitely generated and free, there is a split short exact sequence
\[
0 \to \radic(L) \injects L \surjects \tilde L \to 0
,\]
and thus a (non-canonical) decomposition of $\ZZ$-modules $(L, \beta) = (\radic(L), 0) \oplus (\tilde L, \tilde \beta)$.
:::

:::{.remark}
In particular, if $\beta$ is nondegenerate then $\beta(v, L) = 0$ implies $v = 0$ in $L$.
If $S \leq L$ is sublattice which is a direct summand of $L$ as a $\ZZ$-module, then $T \da S^{\perp L}$ is also a direct summand of $L$ (again as a $\ZZ$-module) and
\[
\rank_\ZZ(S) + \rank_\ZZ(T) = \rank_\ZZ(L)
,\]
so $S \oplus T$ is generally a finite index sublattice of $L$.
:::

:::{.definition title="Discriminant"}
Given a lattice $(L, \beta)$ of rank $n$, the **discriminant** is the ideal generated by determinants of Gram matrices in all bases, i.e. 
\begin{align*}
\disc(L) \da \qty{ \ts{ \det(G_\beta) \st G_\beta \text{ is a Gram matrix of $\beta$ in some basis } } }   \subseteq \ZZ
\end{align*}
When there is no danger of confusion, we choose a representative $d$ of this ideal and simply write $\disc(L) = d$.
:::

:::{.remark}
A lattice is nondegenerate if and only if $\disc(L)$ is not a zero divisor in $\ZZ$ (i.e. $\disc(L) \neq 0$) and is unimodular if and only if $\disc(L)$ is a unit in $\ZZ$ (i.e. $\disc(L) = \pm 1$),
:::

:::{.proposition title="Computing indices of sublattices"}
\label[proposition]{prop:disc_of_full_rank_sublattice}
If $S\leq L$ is a finite index sublattice of a nondegenerate lattice, then
\[
[L: S]^2 = { \disc(S) \over \disc(L)}
.\]
:::

:::{.proof}
This follows from the existence of the Smith normal form for any basis matrix of $L$.
Picking such a basis matrix $B_L \da \sqgens{b_1^t,\cdots, b_n^t}$, writing the invariant factors of $B_L$ as $d_1,\cdots, d_n$, the matrix $B_S \da \sqgens{d_1 b_1^t,\cdots, d_n b_n^t}$ defines a basis for $S$.
Moreover, we have $[L:S] = \prod_{i=1}^n d_i$, and thus
\[
\disc(S) = \det(B_S) = \qty{\prod_{i=1}^n d_i}^2 \det(B_L) = [L:S]^2 \disc(L)
.\]
:::

:::{.definition title="Volume"}
For a lattice $L$, let $P_L$ be the parallelopiped defined by any $\ZZ$-basis of $L$, which is a fundamental domain for the action of $L$ on $L_\RR$ by translation.
We have $L_\RR/L \cong P_L$, and define the **volume of $L$** as the volume of $P_L$.

There are equalities
\[
\volume(L)^2 = \abs{\det(G_\beta)} \da \abs{\disc(L)}
.\]
Note that this is sometimes referred to as the **covolume** and denoted $\covol(L)$, since this quantity is $\volume(L_\RR/L)$.
:::


## Dual Lattices

:::{.definition title="Dual modules/lattices"}
\label[definition]{def:dual_module}
For an integral lattice $(L, \beta)$, we define its **dual** as
\[
L\dual \da \Hom_\ZZ(L, \ZZ)
.\]
If $S$ is an $R$-algebra, we define 
\[
L_S^{\vee S} \da \Hom_S(L_S, S)
,\]
and thus for example $L_\QQ{\vee \QQ} \da \Hom_\QQ(L_\QQ, \QQ)$.
:::

:::{.lemma}
Duality commutes with finite direct sums, so $(L \oplus M)\dual \cong L \dual \oplus M\dual$.
It commutes with homomorphisms in the sense that 
\[
\Hom_\ZZ(L, M)_S \da \Hom_\ZZ(L, M) \tensor_\ZZ S = \Hom_S(L\tensor_\ZZ , M\tensor_\ZZ S) \da \Hom_S(L_S, M_S)
,\]
and so in particular it commutes with base change and we have 
\[
(L\dual)_S \da L\dual \tensor_\ZZ S \da \Hom_\ZZ(L, \ZZ) \tensor_\ZZ S = \Hom_S(L_S, S) \da L_S^{\vee S}
.\]
In summary:
\[
(L \oplus M)\dual = L \dual \oplus M \dual, \qquad
\Hom_\ZZ(L, M)_S = \Hom_S(L_S, M_S), \qquad
(L\dual)_S = L_S^{\vee S}
.\]
:::


:::{.remark}
If $L$ is a nondegenerate integral lattice, then there is an injection $L\injects L\dual$ -- however, the extension $\beta_{\QQ}$ of $\beta$ to $L_\QQ$ is typically no longer $\ZZ$-valued, so $L_\QQ$ (and thus $L\dual$) are not necessarily integral lattices.
:::

:::{.lemma}
Let $(L, \beta)$ be a nondegenerate integral lattice.
By nondegeneracy, there is an injection $L \injects L\dual$ which extends to an isomorphism $L_\QQ \iso L_\QQ^{\vee \QQ}$ of $\QQ$-modules.
There is a bijection
\begin{align*}
\ts{v\in L_\QQ \st \beta_\QQ(v, L) \subseteq \ZZ} &\iso
L\dual \da \Hom_\ZZ(L, \ZZ) \\
v &\mapsto \ro{\beta_\QQ(v, \wait)}{L}
\end{align*}
Thus for nondegenerate integral lattices, we interchangeably identify these sets.
:::

:::{.proof}
Identifying $L_k$ with $L_k^{\vee k}$, every $k$-linear functional $f\in L_k^{\vee k}$ is of the form $f(\wait) = \beta_k(v, \wait)$ for some $v\in L_k$.
But then the restriction $\ro{f}{L}$ of $f$ to $L$ is in $L\dual$ if and only if $\ro{f}{L}(L) \da \beta_k(v, L) \subseteq \ZZ$ if and only if $\ro{f}{L} \in L^{\hash R}$.
:::

:::{.remark title="Equivalent conditions for a lattice to be nondegenerate/unimodular"}
Moreover, if $L$ is integral, then $L\injects L\dual$ with index $[L\dual: L] = \abs{\disc(L)}$, and thus the discriminant group satisfies $\size A_L = \abs{\disc(L)}$.

For an integral lattice over $R = \ZZ$, the following are equivalent:

- $L$ is nondegenerate,
- $\disc(L) \neq 0$,
- The morphism $\iota: L\to L\dual$ given by $v\mapsto \beta(v, \wait)$ is injective,
- $\radic(L) \da L^{\perp L} = 0$,
- $\volume(L) \neq 0$.

and similarly the following are equivalent:

- $L$ is unimodular,
- $\disc(L) = \pm 1$,
- $\iota$ is an isomorphism, so $L\iso L\dual$,
- $\radic(L) = 0$ and $A_L = 0$,
- $\vol(L) = 1$.

:::

:::{.remark}
If $(L, \beta)$ is a lattice with a $\ZZ$-basis $\ts{e_1,\cdots, e_n}$, then there exists a dual $\QQ$-basis for $L\dual$ given by $\ts{e_1\dual, \cdots, e_n\dual}$ satisfying $e_i\dual(e_j) = \delta_{ij}$.
:::

:::{.lemma}
Let $(L, \beta)$ be a definite lattice with Gram matrix $G_\beta$ in some basis $B_L$ and let $L\dual$ denote the dual of $L$ with dual basis $B_{L\dual}$.
Then
\begin{align*}
G_\beta = B_L^t B_L,\quad 
B_{L\dual} = B_L^{-t}, \quad
G_{\beta \dual} = G_\beta\inv = B_L\inv B_L^{-t}
.\end{align*}

Moreover, if $L$ is unimodular, then $G_{\beta\dual}$ expresses the dual basis $B_{L\dual}$ of $L$ in terms of the basis $B_L$.
:::

:::{.proof}
By definition, the Gram matrix for $\beta$ on $L$ in the basis $B_L$ is given by $G_\beta = B_L^t B_L$, since this precisely computes $\beta(e_i, e_j)$ for all $i, j$.
Similarly $G_{\beta\dual} = B_{L\dual}^t B_{L\dual}$ is in the dual basis $B_{L\dual}$ on $L\dual$.

Letting $B_{L\dual} = (e_i\dual)_{i\leq n}$ be the basis matrix for $L\dual$, we have $B_L^t B_{L\dual} = 1$ since $e_i\dual(e_j) = \delta_{ij}$, so if $B$ is full rank then $B_{L\dual} = B_L^{-t}$.

Combining these facts, we find
\begin{align*}
G_\beta G_{\beta\dual}
&= (B_L^t B_L)(B_{L\dual}^t B_{L\dual}) \\
&= B_L^t B_{L\dual}^{-t} B_{L\dual}^t B_{L\dual} \\
&= B_L^t B_{L\dual} \\
&= B_L^t B_L^{-t} \\
&= \id
,\end{align*}
and so we can express $G_{\beta\dual} = G_\beta\inv$.
:::

:::{.remark}
Since $L \mapsto L\dual$ is an functor of $R$-modules, there is an induced morphism
\begin{align*}
(\wait)\dual: \Hom_\ZZ(L_1, L_2) & \to \Hom_\ZZ(L_2\dual, L_1\dual) \\
f &\mapsto f\dual: g\mapsto g\circ f \qquad \forall g: L_2\to R
\end{align*}
In particular, for any $L$ there is a morphism of $\ZZ$-modules $\Aut_\ZZ(L) \to \Aut_\ZZ(L\dual)$.
:::

:::{.lemma}
If $f: L_1\to L_2$ is given by a matrix $M_f$ in fixed bases $B_{L_1}, B_{L_2}$ of $L_1$ and $L_2$, then $f\dual$ is given by $M_{f\dual} = M_f^t$ in the dual bases $B_{L_1\dual}, B_{L_2\dual}$.
Moreover, if $f$ is an isomorphism, then $M_{f\inv} = M_f\inv$ and $f\dual$ is an isomorphism with inverse $(f\dual)\inv = (f\inv)\dual$ represented by $M_{(f\dual)\inv} = M_f^{-t}$.
In summary, we have
\begin{align*}
M_{f\inv} = M_f\inv, \qquad 
M_{f\dual} = M_f^t, \qquad
M_{(f\dual)\inv} = M_f^{-t}    
\end{align*}

:::

:::{.lemma}
Let $(L, \beta)$ be a nondegenerate integral $\ZZ$-lattice with discriminant $d\da \disc(L)$.
Then $L\dual \subseteq {1\over d^2} L$, or equivalently $d^2 L\dual \subseteq L$.
In this case, one can write
\begin{align*}
\beta\dual: L\dual \tensor_\ZZ L\dual &\to d^{-2} \ZZ \subseteq \QQ \\
(v, w) &\mapsto {1\over d^2}\cdot \beta(dv, dw)
,\end{align*}
where notably $dv, dw\in L$ and so one can use the original bilinear form on $L$ without extending it to $\QQ$.
:::

:::{.lemma}
We have the following equalities of determinants and volumes:
\begin{align*}
\disc(L\dual) = {1\over \disc(L) }, \quad
\vol(L\dual) = {1\over \vol(L)}
\end{align*}
Thus if $L$ is unimodular then $\disc(L\dual) = \disc(L) = \pm 1$ and $\vol(L) = \vol(L\dual) = 1$.
:::

:::{.lemma title="Dual of a twist"}
For the twist $L(m)$ of an $R$-lattice, we have
\[
(L(m))\dual = L\dual\qty{1\over m}
.\]
If $L$ is unimodular, then
\[
(L(m))\dual = L\qty{1\over m} = {1\over m}L(m), \qquad A_L = {{1\over m}L(m) \over L(m)}
.\]
:::

:::{.definition title="Divisibility"}
Let $(L, \beta)$ be an integral $\ZZ$-lattice.
The **divisibility** of an element $v\in L$, denoted $\div_L(v)$, is the positive generator of the ideal $\beta(v, L) \subseteq \ZZ$.
:::

:::{.remark}
The element $v^* \da v/\div_L(v)$ is a primitive vector in $L\dual$, and thus $[v^*] \in A_L$ is an element of order $\div_L(v)$.
Moreover, $\div_L(v)$ always divides $\disc(L)$, and if $e\in L$ is isotropic, then $e$ extends to a copy of $U$ primitively embedded in $L$ if and only if $\div_L(e) = 1$, in which case $L = U \oplus U^{\perp L}$.
:::



## Morphisms and Isometry Classes

:::{.definition title="Morphisms and embeddings"}
The set of **morphisms** between lattices $(L_1, \beta_1)$ and $(L_2, \beta_2)$ is defined as 
\[
\Hom_{\Lat_\ZZ}(L_1, L_2)
\da \ts{f\in \Hom_\ZZ(L_1, L_2) \st \beta_1(v, w) = \beta_2(f(v), f(w)) \,\,\forall v, w\in L_1 }
.\]
An **embedding** $f$ of $L_1$ into $L_2$ is an injective morphism of lattices, and $f$ is a **primitive embedding** if $\coker(f)$ is torsionfree as a $\ZZ$-module.
We say a sublattice $S\leq L$ is a **primitive sublattice** if the inclusion $\iota:S\injects L$ is a primitive embedding.
:::

:::{.definition title="Equivalence of embeddings"}
\label[definition]{def:equivalent_embeddings}
Two primitive embeddings $\iota_1: S\injects L_1, \iota_2: S\injects L_2$ are **equivalent** if $\exists f\in \Isom(L_1, L_2)$ such that $\ro{f}{\iota_1(S)} = \id_{\iota_1(S)}$, and two such primitive sublattices are **equivalent** if $\exists f\in \Isom(L_1, L_2)$ such that $f(\iota_1(S)) = \iota_2(S)$.

In particular, given a sublattice $S\leq L$, two primitive embeddings $\iota_1, \iota_2: S\injects L$ are **equivalent** if there exists $g\in \Orth(L)$ such that $\iota_1 = g\circ \iota_2$.
Write $\Emb(S, L)$ for the equivalence classes of primitive embeddings of $S$ into $L$.
:::

:::{.definition title="Primitive elements"}
An element $v\in L$ is a **primitive element** if the inclusion $\gens{v}_\ZZ \injects L$ is a primitive embedding of lattices.
:::

:::{.definition title="Saturations"}
\label[definition]{def:saturation}
Let $\iota: S\injects L$ be an embedding of lattices.
Identifying $S$ with $\iota(S)$, we say $S$ is **saturated in $L$** if for all $v\in L$, if $nv\in S$ for some $n\in \ZZ$, then $v\in S$.
We define the **saturation of $S$ in $L$** as
\[
\Sat_L(S) \da \ts{v\in L \st nv\in S \text{ for some } n\in \ZZ\smz}
.\]
Thus $S$ is saturated in $L$ if and only if $S = \Sat_L(S)$.
:::

:::{.remark}
Over $\ZZ$, the following are equivalent:

- $\iota:S\injects L$ is a primitive embedding,
- $S$ is saturated in $L$,
- There exists a submodule $T\leq L$ such that $L\iso S \oplus T$ as $\ZZ$-modules,
- There exists a morphism $f: L\to M$ for some lattice $M$ with $\ker f = S$,
- $S = (S^{\perp L})^{\perp L}$,
- Any $\ZZ$-basis of $S$ can be extended to a $\ZZ$-basis of $L$,
- $S$ is a direct summand of $L$ as a $\ZZ$-module,
- $(S_\QQ) \intersect L = S$,
- $L\dual \surjects S\dual$, so every integral functional on $S$ lifts to an integral functional on $L$.
:::

:::{.remark}
If $S\injects L$ is a any embedding (not necessarily primitive), then $T\da S^{\perp L}$ is automatically primitive since 
\[
\Sat_L(T) = 
\Sat_L(S^{\perp L}) =
((S^{\perp L})^{\perp L})^{\perp L} =
\Sat_L(S)^{\perp L} = T
.\]
:::

:::{.definition title="Isometries and the orthogonal group"}
Their set of **isometries over $R$** is defined as 
\[
\Isom(L_1, L_2) \da \ts{f\in \Hom_{\Lat_\ZZ}(L_1, L_2) \st f \text{ is an isomorphism of $\ZZ$-modules}} 
.\]
If two lattices are isometric, we write $L_1\iso L_2$.
The **orthogonal group** of $L$ is defined as 
\[
\Orth(L) \da \Aut_{\Lat_\ZZ}(L) \da \Isom(L, L)
.\]
:::

:::{.example}
Over $\ZZ$, we have
\[
\Orth(U) = \ts{ I_1, I_{-1}, J_1, J_{-1} }
\da \ts{\id, -\id, \matt 0 1 1 0, \matt 0 {-1} {-1} 0} \cong C_2 \times C_2
.\]
:::

:::{.definition title="Isometry classes"}
Given an $R$-lattice $(L, \beta)$, we define its **isometry class** $\Cl(L)$ as the set of all lattices $(M,\beta_M)$ that are isometric to $L$ over $\ZZ$.

We let $\Lat_\ZZ$ be the category of nondegenerate $\ZZ$-lattices and $\Lat_\ZZ\modiso$ be the category of isometry classes of such lattices.
Then $L_1\iso L_2 \iff \Cl(L_1) = \Cl(L_2) \iff [L_1] = [L_2]$ in $\Lat_\ZZ\modiso$.
We similarly define $\Lat^n_\ZZ, \Lat^n_\ZZ\modiso$ for lattices of rank $n$.
:::

:::{.remark}
If $(L, q)$ is a quadratic lattice, we define $\Orth(L) \da \Orth(L, q) \da \Orth(L, \beta_q)$ using its polar form, and similarly define its isometry class $\Cl(L, q)$.
By a theorem of Minkowski, there are only finitely many isometry classes of integral $\ZZ$-lattices of a fixed rank $n$ and discriminant $d$.
:::

:::{.remark title="Isometry via group actions"}
Let $\Quad^n_\ZZ$ denote the set of all quadratic lattices $(L, q)$ of rank $n$, and define the following action:
\begin{align*}
\Mat_{n\times n}(\ZZ) &\to \Aut_\ZZ(\Quad^n_\ZZ) \\
M &\mapsto \qty{ (L, q) \mapsto (L, M.q) } \qquad (M.q)(x) \da q(M^t x)
\end{align*}
Note that this can be restricted to an action by any subgroup $G \leq \Mat_{n\times n}(\ZZ)$.

Similarly, let $\Lat^n_\ZZ$ denote the set of all symmetric bilinear forms $(L, \beta)$ of rank $n$, represented by their Gram matrices $G_\beta$, and define an action
\begin{align*}
\Mat_{n\times n}(\ZZ) &\to \Aut_\ZZ(\Lat^n_\ZZ) \\
M &\mapsto \qty{ (L, \beta) \mapsto (L, M.\beta)} \qquad M.\beta \da M.G_\beta = M G_\beta M^t
,\end{align*}
which again can be restricted to any subgroup.

We say two quadratic forms (resp. bilinear) forms are **$G$-equivalent** if they are in the same $G-$ orbit under the above action, and simply **equivalent** if they are in the same $G\da \GL_n(\ZZ)$ orbit.
We write their equivalence classes as
\[
\Cl(L, q) \in \Quad^n_\ZZ/\GL_n(\ZZ), \qquad \Cl(L) \in \Lat^n_\ZZ/\GL_n(\ZZ)
.\]
We can then identify the orthogonal group of a quadratic lattice as its stabilizer under the $\GL_n(\ZZ)$ action:
\begin{align*}
\Orth(L, q) \da \Stab_{\GL_n(\ZZ)}(L, q) 
&\da \ts{M\in \GL_n(\ZZ) \st M.q = q} \\
&= \ts{M\in \GL_n(\ZZ)\st M^t G_q M = G_q}
\end{align*}

Similarly, for lattices:
\begin{align*}
\Orth(L) \da \Stab_{\GL_n(\ZZ)}(L, \beta)
&\da \ts{M\in \GL_n(\ZZ) \st M.\beta = \beta} \\
&= \ts{M\in \GL_n(\ZZ) \st M G_\beta M^t = G_\beta}
\end{align*}

Note that a similar discussion applies to $\Mat_{n\times n}(\QQ)$ and subgroups thereof.

In particular, for a fixed lattice, this yields computationally quick ways to generate isometric lattices, namely by generating random matrices in $\SL_n(\ZZ)$ and conjugating $G_\beta$ to obtain a new Gram matrix.
Similarly, this yields a quick way to check if a given automorphism $f$ of $L$ is an isometry, namely by picking any basis, writing a matrix $M_f$ for $f$, and checking that it preserves $G_\beta$ under conjugation.
:::

:::{.example}
The bilinear forms $U(1/2)$ and $\I_{1, 1}$ over $\ZZ$ are $\GL_2(\QQ)$-equivalent: one can take $M \da \matt 1 1 1 {-1}$ and obtain 
\[
M G_{U(1/2)} M^t = \matt 1 1 1 {-1} \matt 0 {1\over 2} {1\over 2} {0} \matt 1 1 1 {-1} = \matt 1 0 0 {-1} = G_{\I_{1, 1}}
.\]

However, they are not $\GL_2(\ZZ)$-equivalent.
To see that no such $M$ works, one can note that these lattices correspond to the quadratic forms $q_1(x,y) = xy$ and $q_2(x,y) = x^2-y^2$ respectively on $\ZZ^2$, and representability of integers is an invariant of quadratic forms.
Over $\ZZ$, every integer is representable by $q_1$, namely by taking $x=1$ and letting $y$ freely vary, while 2 is not representable by $q_2$.
Writing $x^2-y^2 = (x+y)(x-y)$, if $x$ and $y$ have the same parity, then $x^2-y^2 \equiv 0 \pmod 4 \neq 2\pmod 4$, a contradiction.
If $x$ and $y$ have different parities, then $(x+y)(x-y)$ is odd, which is again a contradiction.
:::

:::{.remark}
An isometry $f\in \Orth(L)$ extends to an isometry $f_\QQ \da f\tensor \id_\QQ \in \Orth(L_\QQ)$ preserving $L\dual \subseteq L_\QQ$.
This induces an isomorphism $\ro{f}{A_L}$ which preserves the discriminant form, and thus there is a well-defined group homomorphism
\begin{align*}
\psi: \Orth(L) &\to \Orth(A_L) \\
f &\mapsto \ro{f}{A_L}([x]) \da [f\dual(x)]
\end{align*}
It is neither injective nor surjective in general, leading to the following:
:::

:::{.definition title="Stable orthogonal group"}
Let $\psi: \Orth(L\dual) \to \Orth(A_L)$ be the morphism described above, which we will write as $f\mapsto \ro{f}{A_L}$.
This induces an exact sequence
\[
0 \to \Orth^*(L)\da \ker(\psi) \to \Orth(L) \mapsvia{\psi} \Orth(A_L) \to \Orth^*(A_L)\da \coker(\psi) \to 0
.\]
We refer to $\Orth^*(L)$ as the **stable orthogonal group** of $L$, and $\Orth^*(A_L)$ similarly as the stable orthogonal group of $A_L$.
:::

:::{.remark}
When $L = \lkttd$, the stable orthogonal group $\Orth^*(L)$ corresponds to the group of isometries of $\lkt$ that preserve the polarization $h$ and act on a connected component of the 2-component period domain $\Omega_{L}$.
:::


:::{.remark}
Note that $\Orth(L(n)) \cong \Orth(L)$ for any $n\neq 0$.
:::

:::{.remark}
Note that $\Orth(L) \to \Orth(A_L)$ is surjective if and only if $\Orth^*(A_L) = 0$.
In this case, any isometry of $A_L$ can be lifted to an isometry of $L$.
:::


## Classification of lattices over fields

:::{.theorem title="Classification of lattices over fields, {\cite[Thm. 8.1.1]{petersSymmetricQuadraticForms2024}}"}
Let $(L, \beta)$ be a nondegenerate lattice of rank $n$ over a field $k$ where $\characteristic(k) \neq 2$.
Then $L$ is isometric to a diagonal form
\[
L \iso \bigoplus_{i=1}^n \gens{a_i}, \qquad a_i\in k\units
,\]
and in this basis $G_\beta$ is diagonal.
Thus
\[
\Lat^n_k\modiso \subseteq (k\units)^n, \qquad \characteristic(k) \neq 2
.\]
:::

:::{.remark}
Note that over general fields $k$, there is no guarantee of uniqueness of this decomposition.
Over $k=\RR$, up to isometry one can reduce to $a_i \in \ts{\pm 1}$ for all $i$.
By Sylvester's theorem, the numbers $p$ and $q$ of summands equal to $\gens{1}$ and $\gens{-1}$ respectively are well-defined and unique.
Moreover, if $k=\kbar$, one can take $a_i = 1$ for all $i$.
We can thus write
\[
\Lat^n_\RR\modiso \cong \ts{\Cl(\I_{p, q}) \st p+q=n,\,\, 0\leq p,q\leq n, n\geq 1}, \qquad \Lat^n_\CC\modiso = \ts{\Cl(\I_{n, 0}) \st n\geq 1 }
.\]
This motivates the following definition:
:::

:::{.definition title="Signature and index"}
Let $(L, \beta)$ be a nondegenerate $\ZZ$-lattice, and let $p$ (resp. $q$) be the number of summands $\gens{1}$ (resp. $\gens{-1}$) in the diagonalization of $(L_\RR, \beta_\RR)$.
The pair $(p, q)$ is called the **signature** of $L$, written $\signature(L) = (p, q)$, and the **index** of $L$ is the quantity $\tau(L) \da p-q$.
:::

:::{.remark}
As a matter of notation, given two lattices $L, M$ with $\signature(L) = (p, q)$ and $\signature(M) = (p', q')$, we write $\signature(M) \geq \signature(L)$ if both $p' \geq p$ and $q'\geq q$.
:::

:::{.remark title="Definite/indefinite/hyperbolic lattices"}
Let $(L)$ be a nondegenerate lattice of rank $n$ with $\signature(L) = (p, q)$.
If

- $p = 0$, $L$ is negative-definite,
- $q = 0$, $L$ is positive-definite,
- $p\neq 0$ and $q\neq 0$, $L$ is indefinite, and if
- $(p, q) = (1, n-1)$ or $(n-1, 1)$, we say $L$ is **hyperbolic**.

By convention, we typically adopt the convention that hyperbolic lattices have signature $(1, n-1)$.
:::

:::{.theorem title="Classification of $\mathbb{R}$-lattices"}
Let $(L_1, \beta_1)$ and $(L_2, \beta_2)$ be two nondegenerate $\RR$-lattices.
The following are equivalent:

- $\Cl_\RR(L_1) = \Cl_\RR(L_2)$, so $L_1$ is isometric to $L_2$ over $\RR$,
- $\signature(L_1) = \signature(L_2)$,
- $\rank_\RR(L_1) = \rank_\RR(L_2)$ and $\tau(L_1) = \tau(L_2)$.

Thus a lattice over $\RR$ is uniquely determined up to isometry by its signature, and is thus isometric to $\I_{p, q}$ for some $p, q$.
In this case, writing $\signature(L_1) = \signature(L_2) = (p, q)$, we have $\Cl(L) = \ts{\I_{p, q}}$, i.e. the class group is a single element represented by the isometry class of $\I_{p, q}$.
:::

## Torsion forms

:::{.definition title="Torsion bilinear/quadratic forms"}
A **torsion bilinear (resp. quadratic) form** is an $\QQ/\ZZ$-valued bilinear $\ZZ$-module $(G, \beta)$ (resp. an $\QQ/\ZZ$-valued quadratic $\ZZ$-module $(G, q)$) where $G$ is a finitely generated torsion $\ZZ$-module.


Thus a torsion form is a pair $(G, \beta)$ where $G$ is a finite abelian group and
$\beta: G \tensor_\ZZ G \to \QQ/\ZZ$ is a $\ZZ$-bilinear form
Similarly a torsion quadratic form is a pair $(G, q)$ where $q: G \to \QQ/\ZZ$ is a quadratic form.

We define $\Hom_{\Quad_\ZZ}(G_1, G_2), \Isom_{\Quad_\ZZ}(G_1, G_2)$, and $\Orth(G), \Orth(G, q)$ as in the case of $\ZZ$-valued bilinear forms, we write $\Cl(G)$ and $\Cl(G, q)$ for their isometry classes, and define $\Lat_{\QQ/\ZZ}(G)\modiso$ and $\Quad_{\QQ/\ZZ}(G)\modiso$ for the spaces of torsion bilinear (resp. quadratic) forms up to isometry on a fixed group $G$.
:::

:::{.theorem title="Classification of torsion $\mathbf{Q}/\mathbf{Z}$ forms on cyclic groups {\cite[Prop. 6.1.8]{petersSymmetricQuadraticForms2024}}"}
There is a classification of nondegenerate $\QQ/\ZZ$-valued symmetric torsion forms $\beta$ on $C_m$: each such form is isometric to $\gens{a\over m}$ for some $a\in \ZZ$ coprime to $m$, and they are classified by $D(C_m) \da C_m\units/(C_m\units)\sq$.
Explicitly, these are given by $\beta(x,y) = {a\over m}xy$.
Thus
\begin{align*}
\Lat_{\QQ/\ZZ}(C_m)\modiso &\cong \ts{\gens{u\over m} \st u\in D(C_m)}, \\
\Quad_{\QQ/\ZZ}(C_m)\modiso &\cong \ts{\sqgens{u\over 2m} \st u\in D(C_{2m})}
\end{align*}

For example, for symmetric bilinear forms,
\begin{align*}
\Lat_{\QQ/\ZZ}(C_2)\modiso &\cong \ts{ \gens{1\over 2} }, \\
\Lat_{\QQ/\ZZ}(C_4)\modiso &\cong \ts{ \gens{1\over 4}, \gens{3\over 4}}, \\
\Lat_{\QQ/\ZZ}(C_{2^k})\modiso &\cong \ts{ \gens{u\over 2^k},\quad u = \pm 1, \pm 3\pmod 8},\qquad (k\geq 3), 
\end{align*}
and for quadratic forms,
\begin{align*}
\Quad_{\QQ/\ZZ}(C_2)\modiso &\cong \ts{\sqgens{1\over 4}, \sqgens{3\over 4}} \\
\Quad_{\QQ/\ZZ}(C_4)\modiso &\cong \ts{\sqgens{1\over 8}, \sqgens{-3\over 8}, \sqgens{3\over 8}, \sqgens{-1\over 8}} \\
\Quad_{\QQ/\ZZ}(C_{2^k})\modiso &\cong \ts{\sqgens{u\over 2^{k+1} } \st u = \pm 1, \pm 3 \pmod 8}, \qquad (k\geq 3)
.\end{align*}
:::

## Discriminant Bilinear/Quadratic Forms

:::{.definition title="Discriminant bilinear/quadratic modules"}
If $(L, \beta)$ is a nondegenerate lattice, there is an injection $\iota: L\injects L\dual$ realizing $L$ as a finite-index sublattice of $L\dual$ and inducing an exact sequence
\[
0 \to L \injectsvia{\iota} L\dual \surjects A_L \da \coker(\iota_1) \to 0
.\]
We define the **discriminant bilinear module** as $A_L$, which is necessarily a torsion $\ZZ$-module.
It becomes a torsion bilinear $\ZZ$-module when equipped with the form
\begin{align*}
\beta_{A_L}: A_L \tensor_\ZZ A_L &\to \QQ/\ZZ \\
([v], [w]) &\mapsto \beta_\QQ(v, w) \pmod \ZZ
\end{align*}
where we identify $v,w\in L$ with their images in $L\dual$.
The pair $(A_L, \beta_{A_L})$ is referred to as the **discriminant bilinear form** associated to $L$.

Similarly, if $(L, q)$ is a nondegenerate quadratic form, $A_L$ admits a quadratic form
\begin{align*}
q_{A_L}: A_L &\to \QQ/\ZZ \\
[x] &\mapsto q_\QQ(x) \pmod \ZZ
\end{align*}
and we refer to $(A_L, q_{A_L})$ as the **discriminant quadratic form** of $L$.
:::

:::{.remark}
If $(L, \beta)$ is an *even* nondegenerate lattice, the discriminant quadratic form $q_{A_L}$ takes values in $\QQ/2\ZZ$ and is given by
\begin{align*}
q_{A_L}: A_L &\to \QQ/2\ZZ \\
[x] &\mapsto \beta_\QQ(x, x) \pmod{2\ZZ}
.\end{align*}
Moreover, $\beta_{A_L}$ is the bilinear form associated to $q_{A_L}$, i.e.
\[
\beta_{A_L}([v], [w]) = {1\over 2}\qty{ q_{A_L}([v] + [w]) - q_{A_L}([v]) - q_{A+L}([w])}
\]
where one applies the isomorphism ${1\over 2}: \QQ/2\ZZ \to \QQ/\ZZ$.
These forms are nondegenerate if and only if $L$ is nondegenerate, since if $\beta_\QQ(v, L\dual) = 0$ for some $v\in L$ then $v\in (L\dual)\dual = L$ and thus $[v] = [0] \in A_L$.
:::

:::{.remark}
There are equalities
\[
\size A_L = \abs{\disc(L)} = [L\dual : L]
,\]
and in particular $L$ is unimodular if and only if $A_L = 0$.
:::

:::{.definition title="Length of a lattice"}
For an $R$-lattice $(L, \beta)$, define its **length** $\ell(L)$ as the minimal number of generators of $A_L$.
:::

:::{.example}
We collect some examples of lengths of common lattices:

| $L$ | $A_L$ | $\ell(L)$ |
|-----|-------|-----------|
| $A_n$ | $C_{n+1}$ | $1$ |
| $D_{2n}$ | $C_2^2$ | $2$ |
| $D_{2n+1}$ | $C_4$ | $1$ |
| $E_6$ | $C_3$ | $1$ |
| $E_7$ | $C_2$ | $1$ |
| $E_8$ | $0$ | $0$ |
| $E_8(2)$ | $C_2^8$ | $8$ |
| $\gens{n}$ | $C_n$ | $1$ |
| $U$ | $0$ | $0$ |
| $U(2)$ | $C_2^2$ | $2$ |
| $E_{10}(2)$ | $C_2^{10}$ | $10$ |
| $\I_{p, q}(2)$ | $C_2^{p+q}$ | $p+q$ |
| $V$ | $C_3$ | $1$ |
| $V(2)$ | $C_2\times C_6$ | $2$ |
| $L_{2d}$ | $C_{2d}$ | $1$ |
| $\lkt$ | $0$ | $0$ |

:::

:::{.remark}
Since $L\dual \surjects A_L$, if $L\dual = \gens{v_1,\cdots, v_n}_\QQ$, then $A_L$ is generated by the class $\ts{[v_1], \cdots, [v_n]}$, although this may not be a *minimal* generating set.
In particular, there is an inequality $\ell(L) \leq \rank_\QQ(L\dual) = \rank(L)$, and by observing the table above we find that it is sharp.
:::

:::{.remark}
If $d\da\disc L$ is squarefree, then $\ell(L) = 0$ or 1 since $A_L \cong \ZZ/d\ZZ$.
This follows from writing $d = \size A_L = \prod m_i$ as a product of coprime integers and applying the Chinese remainder theorem.
:::

:::{.remark}
There is a short exact sequence
\[
0\to L/mL \injects A_{L(m)}\surjects A_L \to 0
,\]
so if $L$ is unimodular then $A_{L(m)} \cong L/mL \cong {1\over m}L(m)/L(m)$.

:::

## $p$-elementary Lattices

:::{.definition title="$p$-elementary Lattices"}
A lattice $(L, \beta)$ is **$p$-elementary** if $A_L$ is a $p$-elementary abelian group, i.e. $A_L \cong C_p^\ell$ for some $\ell$. 
:::

:::{.remark}
For nondegenerate integral lattices $(L, \beta)$ , one can compute $A_L \cong \bigoplus_{i=1}^n \ZZ/d_i \ZZ$ where $d_i$ are the invariant factors of $L$, found as diagonal entries in the Smith normal form of $G_\beta$.

For example, for $L = V(2)$, we have $G_\beta = \matt 4 2 2 4$ and $\SNF(G_\beta) = \matt 2 0 0 6$, and thus $A_L \cong \ZZ/2\ZZ \oplus \ZZ/6\ZZ$.
:::

:::{.definition title="Co-even/Co-odd"}
Let $L$ be a 2-elementary lattice.
We say

- $L$ is **Type I** if $q(A_L) \subseteq {1\over 2}\ZZ/\ZZ$, or
- $L$ is **Type II** if $q(A_L) \subseteq {1\over 4}\ZZ/\ZZ\sm {1\over 2}\ZZ/\ZZ$.
:::

:::{.example}
$\mfu(2) \da A_{U(2)}$ is Type I, and $\sqgens{1} = A_{\gens 2}$ is Type II.
:::

:::{.definition title="Coparity"}
If $L$ is a 2-elementary lattice, we define the **coparity** as
\[
\delta(L) \da 
\begin{cases}
0 & q_{A_L}(A_L) \subseteq {1\over 2}\ZZ/\ZZ \cong \ZZ/2\ZZ \\
1 & \text{otherwise}
\end{cases}
.\]
We say $L$ is **co-even** if $\delta = 0$, and **co-odd** if $\delta = 1$.
:::


## Reflections and transvections

:::{.definition title="Reflections"}
\label[definition]{def:reflections}
Let $(L, \beta)$ be a nondegenerate lattice and let $\alpha\in L$ be an anisotropic vector satisfying
\[
2\beta(\alpha, L) \subseteq \beta(\alpha, \alpha)\ZZ
.\]
Then the **reflection in $\alpha$** is the isometry
\[
s_\alpha(x) \da x - 2{\beta(\alpha, x) \over \beta(\alpha, \alpha) } \alpha \in \Orth^*(L)
,\]
so in particular $s_\alpha$ acts trivially on $A_L$.
Similarly, if $(L, q)$ is a quadratic lattice with $\alpha\in L$ satisfying $q(\alpha)\in R\units$, we set
\[
s_\alpha(x) \da x - {\beta_q(\alpha, x) \over q(\alpha)}\alpha \in \Orth(L, q)
.\]
We define the **Weyl group of $L$** by $W(L) \da \gens{s_\alpha \st \alpha \in L,\,\, 2\beta(\alpha,L) \subseteq \beta(\alpha,\alpha)\ZZ} \normal \Orth(L)$.

More generally, for $f\in \Orth(L)$ is a **generalized reflection** if there exists a subspace $S \leq L_k$ such that
\[
\ro{f}{S} = \id_S, \qquad \ro{f}{S^{\perp L} } = -\id_{S^{\perp L}}
.\]
:::

:::{.remark}
Equivalently, $v$ corresponds to a generalized reflection, i.e. $s_v(L) = L$, if and only if $v^2$ divides $2\div_L(v)$.
This is automatically satisfied if $v^2\in \ts{\pm 1,\pm 2}$, and the converse is only true if $L$ is unimodular.
Note that if $L$ is even, there are no vectors of norm $\pm 1$.
:::


:::{.lemma}
Reflections satisfy the following properties:

- $s_\alpha( \pm \alpha) = \mp \alpha$, so $s_\alpha(\gens{\alpha}) = \gens{\alpha}$,
- $s_\alpha = s_{-\alpha}$,
- $\ro{s_\alpha}{\gens{\alpha}^{\perp L}} = \id_{\gens{ \alpha}^{\perp L}}$,
- $s_\alpha^2 = \id_L$, and $\Fix_L(s_\alpha)$ is the hyperplane orthogonal to $\alpha$,
- $s_\alpha$ is uniquely determined by the hyperplanes $\ker(\id - s_\alpha)$ and $\ker(\id + s_\alpha)$,
- $s_{\alpha \beta} = s_\alpha\inv \circ s_\beta \circ s_\alpha$,
- If $\alpha$ is primitive, there is a basis $B = \ts{\alpha, e_2,\cdots, e_n}$ such that $s_{\alpha}$ takes the form
\[
s_\alpha = \left(\begin{array}{cccc}-1 & * & \cdots & * \\ 0 & 1 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & 1\end{array}\right)
.\]
- $\det s_\alpha = -1$.


:::

:::{.definition title="Eichler transvections"}
Let $e\in L_\QQ$ with $\beta_\QQ(e, e) = 0$ and let $a\in \gens{e}^{\perp L_\QQ}$.
Then the map
\[
E_{e, a}(v) \da v - \beta(a,v)e
\]
is in $\Orth(\gens{e}^{\perp L})$.
It extends to a unique element in $\Orth(L_\QQ)$ defined by
\[
E_{e, a}(v) \da v - \beta(a,v)e + \beta(e,v)a -{1\over 2}\beta(a,a) \beta(e,v)e
.\]
We define the **Eichler transvection group of $L$** as
\[
E(L) \da \ts{E_{e, a} \st \beta(e,e) = \beta(e, a) = 0, \div_L(e) = 1} \leq \SO^+(L)
\]
where $\SO^+(L) = \SO(L) \intersect \ker\norm{\wait}_{\spinor}$.
In particular, by a theorem of Eichler, if $L$ is an even lattice then $E(L) \leq \Orth^*(L)$.
:::

:::{.remark}
Note that \cite{Sca87} defines
\[
E_{f,x}(y) \da y + \beta(y,x)f - {1\over 2}\beta(x,x)\beta(y,f)f - \beta(y,f)x
.\]
:::


:::{.remark}
Note that if $v$ is nonisotropic and $v-w$ is not isotropic, then the (generally rational) reflection $s_{v-w}$ maps $w$ to $v$.
:::

:::{.lemma}
Eichler transvections satisfy the following properties:

- $E_{e, a+b} = E_{e, a}\circ E_{e, b}$,
- $\ro{E_{e, a}}{e^{\perp} \intersect a^{\perp}} = \id$,
- $E_{e, a}\inv = E_{e, -a}$,
- $E_{e, a}(e) = e$.

:::

:::{.lemma}
Let $L = U^2 = U_1 \oplus U_2$ be two copies of $U$ with a basis $L = \gens{e_1, f_1, e_2, f_2}$.
Then any $v\in L$ is in the $E(L)$ orbit of an element of the form $a(e_1 + bf_1)\in U_1$.
:::

:::{.proof}
A proof is given, for example, in \cite[Ex. 3.7.2]{Sca87}.
We form the isometry
\begin{align*}
L &\iso (\Mat_{2\times 2}(\ZZ), 2\det) \\
ae_1 + bf_1 + ce_2 + df_2 &\mapsto \matt a c {-d} b
\end{align*}
Then elements of $E(L)$ correspond to row and column additions, which correspond to left and right multiplication by the matrices 
\[
\matt 1 0 1 1, \qquad \matt 1 1 0 1
.\]
These can be used to put any such matrix in in Smith normal form, which in the $2\times 2$ case will be a matrix of the form $\matt a 0 0 {ab}$ where $a,b\in \ZZ$ are uniquely determined up to sign.

However, one can show that $v\sim_{E(L)} -v$, and so this ambiguity is not an issue modulo $E(L)$.
A computation then shows that
\[
E_{e_2, -f_1} \circ E_{f_2, -2v} \circ E_{e_2, -f_1}
\]
maps $v$ to $-v$.

TODO show computation.
:::

:::{.corollary}
If $L = U^2$, then $E(L)$ acts transitively on $L[k]$ for any $k$.
:::

:::{.proposition title="{\cite[Prop 3.7.3]{Sca87}}"}
Let $L$ be an even lattice that decomposes as $L \iso U^2 \oplus M$ where $M$ is any lattice, 
and suppose $v,w\in L[k]$ for some fixed $k$.
Then
\[
v\sim_{E(L)} w \iff [v^*] = [w^*]\in A_L
.\]
:::

:::{.proof}
Suppose that $\phi(v) = w$ for some $\phi\in E(L)$.
Then necessarily $\phi^*([v^*]) = [w^*]$ in $A_L$ by restriction.
However, $E(L) \subseteq \Orth^*(L)$, so $\phi$ must induce the identity on $A_L$ and thus $[v^*] = [w^*]$.

Suppose now that $[v^*] = [w^*]$ in $A_L$.
Write $L = U_1 \oplus U_2 \oplus M$; then by the above proposition we may assume that $v,w\in L' \da M \oplus U_1$ up to $E(U_1 \oplus U_2)$.
Since $[v^*] = [w^*]$, in particular these elements have the same order in $A_L$, and so $\div_L(v) = \div_L(w) = d$ is a fixed positive integer.
Thus there exist $x,y\in L'$ such that $\beta(x,v) = d$ and $\beta(y, w) = d$.
We now claim that $z \da {v\over d} - {w\over d} = {v-w\over d}$ is an element of $M \oplus U_1$.
This follows from the fact that $v^* \equiv w^* \pmod{L'}$, so ${v\over d} \equiv {w\over d} \pmod{L'}$.
Thus $z\da {v\over d} - {w\over d}\equiv 0\mod L$is an element of $L'$.

We now claim that 
\[
E_{e, y} \circ E_{f, -z} \circ E_{e, -x}
\]
maps $v$ to $w$.
This uses the fact that $dz^2 = 2vz$.

TODO computation.
:::





## Isotropic Submodules

:::{.definition title="Isotropic submodules"}
Let $(L, \beta)$ be a nondegenerate lattice. 
A submodule $W$ is **isotropic** if $\ro{\beta}{W} = 0$, or equivalently if $W \subseteq W^{\perp L}$.
:::

:::{.definition title="Witt index"}
Let $(L, \beta)$ be a nondegenerate lattice.
The **Witt index** $\WI(L)$ of $L$ is the maximal rank of an isotropic sublattice.
:::

:::{.remark}
One generally has $\WI(L_\QQ) \leq W(L_\RR)$, often with strict inequality.
If $L$ is nondegenerate of signature $(p, q)$, then $\WI(L_\RR) = \min\ts{p, q}$.
:::

:::{.definition title="Lagrangian submodules"}
A submodule $W\leq L$ with $\rank_ZZ(W) = \WI(L)$ is called a **maximally isotropic** or **Lagrangian** sublattice.
:::

:::{.proposition}
If $(L, \beta)$ is a nondegenerate lattice of rank $n$, then $\WI(L) \leq {1\over 2}n$.
:::

:::{.proof}
Using the previous proposition, since $W \subseteq W^{\perp}$ we have $\rank_ZZ(W) \leq \rank_ZZ(W^{\perp})$, so
\[
n = \rank_ZZ(L) = \rank_ZZ(W) + \rank_ZZ(W^{\perp}) \leq \rank_ZZ(W^\perp) + \rank_ZZ(W^{\perp}) = 2\rank_ZZ(W^{\perp}) \implies \rank_ZZ(W^{\perp}) \geq n/2
\]
and thus
\[
\rank_ZZ(W) = \rank_ZZ(L) - \rank_ZZ(W^\perp) \leq n - (n/2) = n/2
.\]
:::

## Examples of Lattices

:::{.example title="Particularly important lattices"}
The following are some of the most prominent examples of lattices:

1. (**Diagonal rank 1 lattices**) For any nonzero $n\in \ZZ$, let $L \da \gens{v}_\ZZ$ be generated by a single element $v$ with $\beta(v,v) \da n$.
    This lattice can also be written as $\gens{n}$, although it is sometimes useful to keep $v$ in the notation, e.g. when this corresponds to a sublattice of an ambient lattice $L$ with a fixed, named basis and $v\in L$.
    This lattice can be written as the twist $\gens{n} = \gens{1}(n)$.
    We have the following properties:

    | Property        | Explanation |
    |-----------------|-------------|
    | Rank            | $\rank(\gens n) = 1$. |
    | Decomposability | Indecomposable for any $n$. |
    | Degeneracy      | Nondegenerate for $n\geq 0$. |
    | Discriminant    | $\disc(\gens n) = n$. |
    | Signature       | $\signature(\gens n) = (1, 0)$ if $n > 0$ and $(0, 1)$ if $n<0$. |
    | Modularity      | Unimodular if and only if $n=\pm 1$. |
    | Definiteness    | Positive-definite if $n>0$ and negative-definite if $n<0$. |
    | Integrality     | Integral $\iff n\in \ZZ$. |
    | Parity          | Even $\iff n\in 2\ZZ$. |
    | Dual lattice    | $\gens{n}\dual = \gens{1\over n}$. |
    | Length          | $\ell(\gens n) = 1$. |
    | Discriminant group | $A_{\gens n} = C_n$. |
    | Quadratic form  | $\sqgens{n}$. |

    Note that if $\gens{n}$ is generated by an element $v$, we can write $\gens{n} \dual = \gens{{1\over n} v}_\ZZ$.


2. (**Type $\I$ lattices**) For any positive integer $n$ and non-negative integers $0\leq p, q \leq n$ with $p+q=n$, let $L = \gens{v_1,\cdots, v_p, w_1, \cdots, w_p} \cong \ZZ^n$ be generated by $p+q$ elements where 
    \[
    \beta(v_i, v_j) = \delta_{ij}, \quad
    \beta(w_i, w_j) = -\delta_{ij}, \quad
    \beta(v_i, w_j) = 0 \,\, \forall i,j
    .\]
    The Gram matrix is diagonal with $p$ copies of $+1$ and $q$ copies of $-1$, i.e.
    \[
    G_{\beta} = 
    \begin{pmatrix}
    1 & 0 & 0 & 0 & 0 \\
    0 & 1 & 0 & 0 & 0 \\
    0 & 0 & \ddots & 0 & 0 \\
    0 & 0 & 0 & -1 & 0 \\
    0 & 0 & 0 & 0 & -1
    \end{pmatrix}
    = 
    \left[\begin{array}{@{}c|c@{}}
    \id_{p\times p} & 0 \\
    \hline
    0 & -\id_{q\times q}
    \end{array}\right]
    \in \Mat_{p\times p}(\ZZ) \times \Mat_{q\times q}(\ZZ)
    .\]
    We write this lattice as
    \[
    \I_{p, q} \da \gens{1,1,\cdots, -1, -1} \da \gens{1}^{\oplus p} \oplus \gens{-1}^{\oplus q}
    .\]

    It is

    | Property        | Explanation |
    |-----------------|-------------|
    | Rank            | $\rank(\I_{p, q}) = p+q$. |
    | Decomposability | Decomposable into rank 1 sublattices. |
    | Degeneracy      | Nondegenerate unless $p=q=0$. |
    | Discriminant    | $\disc(\I_{p, q}) = (-1)^q$. |
    | Signature       | $\signature(\I_{p, q}) = (p, q)$. |
    | Modularity      | Unimodular for any $p,q\geq 0$. | 
    | Definiteness    | Positive-definite if $p>0, q=0$, negative-definite if $p=0,q>0$, indefinite if $p,q\geq 1$. |
    | Integrality     | Integral for any $p,q\geq 0$. |
    | Parity          | Odd for any $p,q\geq 0$. |
    | Dual lattice    | $\gens{n}\dual = \gens{1\over n}$. |
    | Length          | $\ell(I_{p, q}) = 0$. |
    | Discriminant group | $A_{\I_{p, q}} = 0$. |
    | Quadratic form  | $\sqgens{1}^{\oplus p} \oplus \sqgens{-1}^{\oplus q}$. |

    
    We occasionally use the notation
    \[
    \I_{p, 0} \da \gens{1}^{\oplus p}, \qquad \I_{0, q} \da \gens{-1}^{\oplus q}
    .\]

    Moreover, noting that $G_\beta\inv = G_\beta$ for the Gram matrix, we can identify $v_i\dual = v_i, w_i\dual = w_i$ for all $i$.

3. (**The hyperbolic lattice**) Let $L \da \gens{e, f}_\ZZ$ be generated by two elements $e,f$ satisfying $\beta(e, f) = \beta(f, e) = 1$ and $\beta(e, e) = \beta(f,f) = 0$.
    We write this lattice as $U$, the **hyperbolic lattice**, which has Gram matrix
    \[
    G_{U} = \matt 0 1 1 0 \in \Mat_{2\times 2}(\ZZ)
    .\]

    It is

    - Of rank 2,
    - Indecomposable,
    - Satisfies $\signature(U) = (1, 1)$,
    - Satisfies $\disc(U) = -1$,
    - Nondegenerate,
    - Integral,
    - Even,
    - Unimodular,
    - Can be written as $\II_{1, 1}$, defined below,
    - Has quadratic form $q_U(x,y) = 2xy$, 
    - Has associated quadratic lattice $\mfq \da \sqgens{2}$,
    - Has $A_L = 0$ and $\ell=0$.


4. (**The $E_8$ lattice**) Let $L = \gens{\alpha_1, \cdots, \alpha_8}_\ZZ$ be generated by 8 elements whose Gram matrix is the following:
    \[
    G_{E_8} \da 
    \left[\begin{array}{rrrrrrrr}
    -2 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
    0 & -2 & 0 & 1 & 0 & 0 & 0 & 0 \\
    1 & 0 & -2 & 1 & 0 & 0 & 0 & 0 \\
    0 & 1 & 1 & -2 & 1 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 & -2 & 1 & 0 & 0 \\
    0 & 0 & 0 & 0 & 1 & -2 & 1 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1 & -2 & 1 \\
    0 & 0 & 0 & 0 & 0 & 0 & 1 & -2
    \end{array}\right] \in \Mat_{8\times 8}(\ZZ)
    .\]
    We write this lattice as $E_8$, noting that it is precisely the lattice that arises from the Dynkin diagram of the $E_8$ root lattice:
    \[

    E_8: \qquad \dynkin[label, edge length=.75cm]E8 
    ,\]
    where we explain the precise procedure in \Cref{sec:coxeter_vinberg_diagrams}.
    Note that we take the *negative*-definite version of this lattice by convention.

    > TODO: reference.

    This lattice

    - Of rank 8,
    - Indecomposable,
    - Has $\signature(E_8) = (0, 8)$,
    - Is nondegenerate,
    - Is negative-definite,
    - Has $\disc(E_8) = 1$,
    - Is unimodular, so $E_8\dual \cong E_8$,
    - Is integral,
    - Is even,
    - Can be written as $\II_{0, 8}$, which is defined below.
    - Has $A_L = 0$ and $\ell = 0$.

    We occasionally use the dual basis $w_1, \cdots, w_8 \da \alpha_1\dual, \cdots, \alpha_8\dual$.
    Noting that the inverse Gram matrix is given by
    \[
    G_{E_8}\inv =
    \left[\begin{array}{rrrrrrrr}
    -4 & -5 & -7 & -10 & -8 & -6 & -4 & -2 \\
    -5 & -8 & -10 & -15 & -12 & -9 & -6 & -3 \\
    -7 & -10 & -14 & -20 & -16 & -12 & -8 & -4 \\
    -10 & -15 & -20 & -30 & -24 & -18 & -12 & -6 \\
    -8 & -12 & -16 & -24 & -20 & -15 & -10 & -5 \\
    -6 & -9 & -12 & -18 & -15 & -12 & -8 & -4 \\
    -4 & -6 & -8 & -12 & -10 & -8 & -6 & -3 \\
    -2 & -3 & -4 & -6 & -5 & -4 & -3 & -2
    \end{array}\right]
    ,\]
    we can write each $w_i$ in the $\alpha_i$ basis using its columns, i.e. 
    \begin{align*}
    w_1 &= -4 \alpha_1 -5 \alpha_2 -7 \alpha_3 -10 \alpha_4 -8 \alpha_5 -6 \alpha_6 -4 \alpha_7 -2 \alpha_8 \\
    w_2 &= -5 \alpha_1 -8 \alpha_2 -10 \alpha_3 -15 \alpha_4 -12 \alpha_5 -9 \alpha_6 -6 \alpha_7 -3 \alpha_8 \\
    \vdots
    \end{align*}
    and so on.


5. (**Type $\II$ lattices**) For $p, q\in \ZZ_{\geq 0}$, define 
    \begin{align*}
    \II_{p, q}
    \begin{cases}
    E_8(-1)^{\oplus {\tau \over 8}} \oplus U^{\oplus q}, & p-q > 0 \\
    E_8^{\oplus {-\tau \over 8}} \oplus U^{\oplus p}, & p-q < 0
    \end{cases}
    \end{align*}
    where $E_8$ is the **negative**-definite $E_8$ lattice defined above.

    This lattice

    - Is of rank $p + q$,
    - Is generally decomposable (by construction),
    - Has $\signature(\II_{p, q}) = (p, q)$ 
    - Is integral,
    - Is even,
    - Is nondegenerate,
    - Has $\disc(\II_{p, q}) = (-1)^p$,
    - Is unimodular, so $\II_{p, q} \cong \II_{p, q}\dual$, $A_L = 0$, and $\ell = 0$.

    We note that $G_\beta\inv$ is generally nontrivial due to the $E_8$ factors, making the dual basis somewhat nontrivial.

6. Let $L = \gens{v, w}_\ZZ$ be generated by two elements with 
    \[
    G_\beta = \matt 2 1 1 2 \in \GL_2(\ZZ)
    .\]
    We write this lattice as $V$.

    This lattice

    - Is rank 2,
    - Even,
    - Nondegenerate,
    - Not unimodular
    - Satisfies $\disc(V) = -3$,
    - Is of signature $\signature(V) = (2, 0)$,
    - Is positive-definite,
    - Has bilinear form $\beta(a, b) = 2a_1 b_1 + a_2 b_1 + a_1 b_2+ 2a_2 b_2$,
    - Has quadratic form $q(x, y) = 2x^2 + 2xy + 2y^2$
    - Has a quadratic lattice we denote by $\mfv$.
    - Has $A_L = C_3$ and $\ell = 1$,

7. For $k\geq 0$, define 
    \[
    V_k \da V_{\ZZ_2}(2^k) = \qty{ \ZZ_2^2, \matt{2^{k+1}}{2^k}{2^k}{2^{k+1}}}
    .\].

    This lattice $V_k$

    - Is the polar form of $q(x,y) = 2^k(x^2 + xy + y^2)$.
    - is indecomposable, 
    - Satisfies $\disc(V_k) = 3\cdot 2^{2k}$,
    - We write its discriminant form as $\mfv_k$.
    - Is $A_{V_k} = 2^{-k}V_k/V_k \cong C_{2^k}^2$ with quadratic form $q(x,y) = 2^{-k}(x^2 + xy + y^2) \in \QQ_2/\ZZ$ 
    - Has polar form $\matt {2^{-k+1}}{2^{-k}}{2^{-k}}{2^{-k+1}}$.

8. For $k\geq 0$, define 
    \[
    U_k \da U_{\ZZ_2}(2^k) = \qty{\ZZ_2^2, \matt 0 {2^k}{2^k} 0 }
    \]
    over the 2-adic integers.

    The lattice $U_k$

    - is the polar form of $q(x,y) = 2^k xy$,
    - Is indecomposable,
    - Satifies $\disc(U_0) = -1 \in \ZZ_2\units$ and $\disc(U_k) = -2^{2k}$,
    - Has quadratic lattice we denote by $\mfu_k$,
    - Has $2^{-k} U_k/U_k \cong C_{2^k}^2$ with quadratic form $q(x,y) = 2^{-k}xy \in \QQ_2/\ZZ$ 
    - Has polar form $\matt 0 {2^{-k}}{2^{-k}} 0$.


9. Let 
    \[
    L \da \ts{\matt a b c d \in \Mat_{2\times 2}(\ZZ) \st c\in 2\ZZ}
    \]
    and define $q(x) \da 2\det(x)$.
    The associated bilinear form $\beta(x,y) \da 2\qty{ \det(x+y) - \det(x) - \det(y)}$ is $\ZZ$-valued and thus $(L, \beta)$ is a lattice.

    This lattice

    - Is rank 4,
    - Has signature $\signature(L) = (2, 2)$,
    - Is indefinite,
    - Is even,
    - Has $\disc(L) = 4$,
    - Is not unimodular,
    - Is 2-elementary with invariants $(4,2,0)$,
    - Has $A_L = C_2^2$,
    - Is decomposable,
    - Admits an isometry
    \begin{align*}
    U \oplus U(2) &\iso L \\
    (a,b) \oplus (c, d) &\mapsto \matt a c {-2d} b
    \end{align*}


We summarize some relevant properties of the above lattices and some related variants:

| $L$              | $\rank(L)$ | $\signature(L)$ | Definiteness | Parity | Decomposable? | $\disc(L)$ | Unimodular? | $L\dual$ | $\ell(L)$ | $A_L$ |
|------------------|------------|-----------------|--------------|--------|-----------------|------------|-------------|----------|-----------|-------|
| $\gens{n}$       | $1$        | $(1, 0)$        | Positive     | Even $\iff n$ is even | No           | $n$   | $\iff n=\pm 1$ | ${1\over n }\gens{n}$ | $1$ | $C_n$ |
| $U$              | $2$        | $(1, 1)$        | Indefinite   | Even    | No           | $-1$  | Yes            | $U$                   | $0$ | $0$ |
| $U(2)$           | $2$        | $(1, 1)$        | Indefinite   | Even    | No           | $-4$  | No             | ${1\over 2}U(2)$      | $2$  | $C_2^2$ |
| $E_8$            | $8$        | $(0, 8)$        | Negative     | Even    | No           | $1$   | Yes | $E_8$ | $0$ | $0$ |
| $E_8(2)$         | $8$        | $(0, 8)$        | Negative     | Even    | No           | $256$ | No | ${1\over 2}E_8(2)$ | $8$ | $C_2^8$ |
| $\I_{p, q}$      | $p+q$      | $(p, q)$        | Indefinite $\iff p,q>0$ | Odd     | Yes          | $(-1)^q$ | Yes | $\I_{p, q}$ | $0$ | $0$ |
| $\I_{p, q}(2)$   | $p+q$      | $(p, q)$        | Indefinite $\iff p,q>0$ | Even    | Yes          | $(-2)^q$ | No | ${1\over 2}\I_{p, q}(2)$ | $p+q$ | $C_2^{p+q}$ |
| $\II_{p, q}$     | $p+q$        | $(p, q)$        | Indefinite $\iff p,q>0$ | Even    | $\iff p,q>0$          | $(-1)^q$ | Yes | $\II_{p, q}$ | $0$ | $0$ | 
| $\II_{p, q}(2)$  | $p+q$        | $(p, q)$        | Indefinite $\iff p,q>0$ | Even    | $\iff p,q>0$          | $2^p (-2)^q$ | No | ${1\over 2}\II_{p, q}(2)$ | $p+q$ | $C_2^{p+q}$ |
| $V$              | $2$        | $(2, 0)$        | Positive     | Even    | No           | $3$ | No | ${1\over 6}\gens{v_1, v1 + 3v_2}_\ZZ$ | $2$ | $C_2\times C_6$ |
| $V(2)$           | $2$        | $(2, 0)$        | Positive     | Even    | No           | $12$ | No | ${1\over 12}\gens{v_1, v_1 + 3v_2}_\ZZ$ | $2$ | $C_4 \times C_{12}$ |


Of particular importance are

| $(L, \beta)$ | $(A_L, q)$ | Co-even/Co-odd | $\signature(A_L)$ |
|--------------|------------|----------------|------------------|
| $\gens{2} \da \qty{\ZZ^2, \sqgens{2} }$ | $p \da \mfq_1(2) \da \qty{C_2, \sqgens{1\over 2}}$ | Co-odd | $1$ |
| $\gens{-2} \da \qty{\ZZ^2, \sqgens{-2}}$ | $q \da \mfq_1(-2) \da \qty{C_2, \sqgens{-{1\over 2}} }$ | Co-odd | $-1$ |
| $U(2) = \qty{\ZZ^2, \matt 0 2 2 0}$ | $u \da \mfu(2) \da \qty{C_2, \matt{0}{1\over 2}{1\over 2}{0}}$ | Co-even | $0$ |
| $V(2) \da \qty{\ZZ^2, \matt 4 2 2 4}$ | $v \da \mfv(2) \da \qty{C_2 \times C_6, \matt{1}{1\over 2}{1\over 2}{1\over 3}}$ | Co-even | $4$ |





By \cite[\S 2.6]{nonsymplectic_involutions} and \cite[Prop. 1.8.1]{nikulin1979integer-symmetric}, if $L$ is an even 2-elementary lattice, then $A_L$ can be written as a finite direct sum of the discriminant forms $p,q,u,v$ above, subject to relations
\begin{align*}
u^{\oplus 2} &= v^{\oplus 2} \\
p^{\oplus 4} &= q^{\oplus 4} \\
u \oplus p &= (p \oplus q) \oplus p \\
u \oplus q &= (p \oplus q) \oplus q \\
v \oplus p &= q^{\oplus 3} \\
v \oplus q &= p^{\oplus 3}
\end{align*}

Moreover, the even 2-elementary lattices that admit a primitive embedding into $\lkt$ are finite direct sums of the following lattices, whose discriminant forms are recorded as well:

| Lattice $L$ | Discriminant Form $A_L$ | Co-even/Co-odd |
|---------|-------------------|----------------|
| $A_1$   | $q \da \mfq_1(-2)$               | Co-odd              |
| $D_4$   | $v \da \mfv(2)$               | Co-even              |
| $D_6$   | $p^{\oplus 2} \da \mfq_1(2)^{\oplus 2}$               | Co-odd              |
| $D_8$   | $u \da \mfu(2)$               | Co-even              |
| $E_7$   | $p \da \mfq_1(2)$               | Co-odd              |
| $E_8$     | $0$               | Co-even              |
| $E_8(2)$  | $u^{\oplus 4}\da \mfu(2)^{\oplus 4}$               | Co-even              |
| $\gens{2}$ | $p \da \mfq_1(2)$               | Co-odd              |
| $U$   | $0$               | Co-even              |
| $U(2)$   | $u \da \mfu(2)$               | Co-even              |




:::

:::{.proposition title="\cite{gritsenkoHirzebruchMumfordVolumeOrthogonal2006}"}
Let $L = \gens{2d}$, then 

- $A_L = \sqgens{-{1\over 2d}} \cong C_{2d}$, and
- $\size \Orth(A_L) = 2^{\rho(d)}$,

where $\rho(d)$ is the number of prime divisors of $d$.
:::

:::{.proof}
Write $C_{2d} = \gens{v}$, where $q(v) = -{1\over 2d}\mod 2\ZZ$.
If $f\in \Orth(A_L)$, then $f(v) = [\lambda] v$ for some $1\leq \lambda \leq 2d$ coprime to $2d$.
For $f$ to be an isometry, we must have $v^2 = f(v)^2 = ([\lambda]v)^2$, and thus
\[
v^2 = {-1\over 2d}\mod 2\ZZ = [\lambda^2]\cdot v^2 \mod 2\ZZ = {-\lambda^2 \over 2d}\mod 2\ZZ \implies \lambda^2 = 1 \mod 4d\ZZ
,\]
which has $2^{\rho(d)+1}$ solutions over $C_{4d}$ and thus $2^{\rho(d)}$ solutions over $C_{2d}$.
:::

:::{.corollary}
Letting $L_{2d}^{(m)} \da \gens{-2d} \oplus U^2 \oplus E_8^{\oplus m}$, we have $\size \Orth(A_{L_{2d}^{(m)}}) = 2^{\rho(d)}$.
:::

:::{.proof}
This follows from the fact that the summand $U^2 \oplus E_8^{\oplus m}$ is unimodular.
:::


:::{.lemma title="{\cite[Lem. 4.6]{geemenRemarksBrauerGroups2004}}"}
Define the family of lattices[^lattice_family_why]
\[
\Lambda_{n, k} \da \gens{e, f \st e^2 = 2k,\, ef = fe = n,\, f^2 = 0} \cong \qty{\ZZ^2, \matt{2k}{n}{n}{0}}
.\]
There are exactly two primitive isotropic vectors (up to sign):
\[
\Lambda_{n, k}[0] = \ts{v_1 \da f, v_2 \da {ne - kf \over d} },
\qquad \gcd(n, k) = d
.\]
Then
\[
\Orth(\Lambda_{n, k}) =
\begin{cases}
C_2^2 = \ts{\pm \id, \pm J_{n, k}} & k=0 \text{ or } \qty{k\over d}^2 \equiv 1 \pmod{ \frac{n}{d} } \\
C_2 = \ts{\pm \id} & \text{otherwise}
\end{cases}
\]
where $J_{n, k}$ is the involution that swaps the isotropic vectors $v_1$ and $v_2$.
Explicitly, in the basis $\ts{e, f}$, it is given by the matrix 
\[
J_{n, k} = \matt {k\over d}{n\over d}{-\ell}{-{k\over d} }, \qquad\text{where }
\qty{k \over d}^2 - \qty{ n \over d}\ell = 1
.\]

[^lattice_family_why]: these lattices arise in the study of elliptic K3 surfaces; see \cite{geemenRemarksBrauerGroups2004,shinderLequivalenceDegreeFive2020,meinsmaDerivedEquivalenceElliptic2024}.
One can obtain a K3 surface with $\NS(X)\iso \Lambda_{n, k}$ for some $k$ by taking a general K3 surface containing a degree $n$ elliptic curve.

:::

:::{.lemma title="{\cite[Lem. 3.2, (ii)]{stellariRemarksFMpartnersK32005}, \cite[Prop. 3.7]{geemenRemarksBrauerGroups2004}}"}
The lattices $\Lambda_{n, k}$ and $\Lambda_{n', k'}$ are in the same genus if and only if $k=k'$ and $n'\equiv \ell^2 n\pmod{k}$ for some $\ell$ coprime to $k$.
Moreover, $\Lambda_{n, k}$ is isometric to $\Lambda_{n', k}$ if and only if $n\equiv n'\pmod k$ or $nn'\equiv 1\pmod k$.

In particular, if $k=0$, then $\cl(\Lambda_{n, 0}) = 1$ and $\Lambda_{n, 0}$ is unique in its genus.
:::

:::{.corollary}
For any positive integer $n$, we have $U(n) = \Lambda_{n, 0}$.
So $k=0, d=1, \ell = -{1\over n}$, and thus
\[
\Orth(U(n)) \cong \ts{\pm \id, \pm \matt 0 n {1\over n} 0 }\cong C_2^2, \qquad \cl(U(n)) = 1
.\]
:::

:::{.lemma title="\cite{meinsmaDerivedEquivalenceElliptic2024}"}
Let $\Lambda_{n, k} = \gens{e, f}$ as above.
Then $\disc(\Lambda_{n, k}) = \size A_L = n^2$, and
\[
\Lambda_{n, k}\dual = \gens{v_1^* \da -{2k\over n^2}f + {1\over n}e, v_2^* \da {1\over n} f}
\]
and 
\[
A_{\Lambda_{n, k}} \cong C_a \oplus C_b = \gens{[v_1^*], [v_2^*]}, \quad
G_{q_{A_L}} = \matt{-{2k\over n^2}}{1\over n}{1\over n}{0} 
\]
where $a \da \gcd(2k, n)$ and $b \da {n^2\over a}$.
In particular, we have
\[
\ell(\Lambda_{n, k}) = 
\begin{cases}
1 & \gcd(a, b) = 1 \\
2 & \text{otherwise}
\end{cases}
.\]
:::

:::{.corollary}
For $U(n) \da \Lambda_{n, 0}$, we have $k=0$ and thus $a=b=n$, and thus 
\[
A_{U(n)} = \gens{v_1^*, v_2^*} \da \gens{{1\over n} e, {1\over n} f} \cong C_n^2,\qquad
G_{A_{U(n)}} = \matt 0 {1\over n} {1\over n} 0, \qquad 
\ell(U(n)) = 2
.\]
:::

:::{.lemma}
There is an isometry
\begin{align*}
U_1 \oplus U_2 &\iso (\Mat_{2\times 2}(\ZZ), \det) \\
ae_1 + bf_1 + ce_2 + df_2 &\mapsto \matt c a b {-d}
\end{align*}
which induces
\begin{align*}
\Orth(U_1 \oplus U_2) &\iso {\SL_2(\ZZ)\times \SL_2(\ZZ) \over \ts{ \pm(\id, \id) }} \\
(B, A) &\mapsto (X\mapsto BXA\inv)
\end{align*}
Moreover,
\[
\SO^+(U_1 \oplus U_2) = \gens{E_{e_1, e_2}, E_{e_1, f_2}, E_{f_1, e_2}, E_{f_1, f_2} }
,\]
and any $v\in U_1 \oplus U_2$ satisfies $v\sim_{\SO^+(U_1 \oplus U_2)} w$ for some $w\in U_2$.
:::

## Genera, Isometry Classes, and Completions

### The Genus

:::{.remark}
We define the following notation when dealing with adelic rings:

- If $k$ is a global field with ring of integers $R$ and $v$ is a place of $k$, we write $\Pl(R) \da \Pl(k)$ for the set of places of $k$, $k_v$ and $R_v$ respectively for the completions of $k$ and $R$ at $v$, and define the adele ring as the restricted product
\[
\AA_R \da \AA_k \da \prod_{v\in \Pl(k)}' (R_v, k_v) \subseteq \prod_{v\in \Pl(k)} k_v
\]
consisting of sequences $(x_v)_{v\in \Pl(k)}$ such that $x_v\in R_v$ for all but finitely many $v$.


- $\Pl(\ZZ) \da \Pl(\QQ) = \Spec(\ZZ)\union\ts{\infty}$ is the set of places of $\ZZ$, where we write $v\in \Pl(\ZZ)$ for a place and $v=\infty$ for the Archimedean place $\RR$,

- $\ZZ_p \da \lim_{n\geq 1} \ZZ/p^n \ZZ$ for $p$ a prime is the ring of $p$-adic integers, and its fraction field $\QQ_p$ is the ring of $p$-adic rationals,

- $\hat{\ZZ}$ is the ring of profinite integers,
\[
\hat{\ZZ} = \prod_{v < \infty} \ZZ_v = \lim_{n\geq 1} \ZZ/n\ZZ
,\]

- $\AA_\ZZ$ is the ring of integral adeles,
\[
\AA_\ZZ = \prod_{v \leq \infty} \ZZ_v = \RR\times \hat{\ZZ}
.\]

- $\AA^f_\QQ$, is the ring of finite rational adeles,
\[
\AA^f_\QQ = \prod_{v < \infty}' \QQ_v = \hat{\ZZ}\tensor_\ZZ \QQ 
,\]
and in this notation we can write $\AA_\ZZ^f \da \prod_{v<\infty}\ZZ_v = \hat\ZZ$ for the ring of finite integral adeles,

- $\AA_\QQ$ is the full ring of rational adeles, 
\[
\AA_\QQ \da \AA_\ZZ\tensor_\ZZ \QQ = \RR \times \AA^f_\QQ = \RR \times \prod_{p < \infty}' \QQ_p = \prod_{v \leq \infty}' \QQ_v
.\]

:::

:::{.definition title="Genus"}
Let $(L, \beta)$ be a nondegenerate lattice.
We define the **genus** of $L$ as
\[
\gen(L) \da \gen_\ZZ(L) \da \ts{ (M, \beta_M) \st M_{\AA_\ZZ} \iso L_{\AA_\ZZ} }
,\]
i.e. all lattices $M$ such that $M_{\ZZpadic}$ is isometric to $L_{\ZZpadic}$ for all primes $p$, including $p=\infty$ corresponding to $M_\RR \iso L_\RR$.
:::

:::{.remark}
In general, given a class of objects defined over a ring $R$, we say they satisfy a **Hasse principle** (or a *local-global principle*) if whenever $L_v$ is isomorphic to $M_v$ for all places $v$ of $R$, then $L$ is isomorphic to $M$ over $R$ itself.
Note that $\QQ$-lattices satisfy a Hasse principle: two lattices $L, M$ over $\QQ$ are isometric (over $\QQ$) if and only iff $M_{\QQpadic}$ is isometric to $L_{\QQpadic}$ over $\QQpadic$ for all primes $p$, including $p=\infty$.
Thus $\gen_\QQ(L) = \Cl_\QQ(L)$ for lattices over $\QQ$.
We summarize this in the following:
:::

:::{.theorem title="Hasse-Minkowski Theorem/Weak Hasse Principle"}
Let $L, M$ be lattices defined over $\QQ$.
Then 
\[
\gen_\QQ(L) = \gen_\QQ(M) \iff \Cl_\QQ(L) = \Cl_\QQ(M)
.\]
i.e. $L$ is isometric to $M$ over $\QQ$ if and only if $L_{\QQpadic}$ is isometric to $M_{\QQpadic}$ over $\QQpadic$ for every prime $p$ and $L_\RR \iso M_\RR$.
Thus $\QQ$-lattices satisfy the Hasse principle. 
In particular, for a fixed lattice $L$, one has $\gen_\QQ(L) = \Cl_\QQ(L)$, and $L$ is unique in its $\QQ$-genus and thus unique up to isometry over $\QQ$.
:::

:::{.proof}
For a proof of this, see \cite[Thm. 1.3, \S 6.7]{casselsRationalQuadraticForms2008}.
:::

:::{.remark}
This remains true if $\QQ$ is replaced by any number field $K$, and $\QQpadic$ with $K_v$ for all places $v$ of $K$.
:::

:::{.remark}
If $L, M$ are $\ZZ$-lattices (not necessarily isometric over $\ZZ$) and $\gen(L) = \gen(M)$, then $\Cl_\QQ(L_\QQ) = \gen_\QQ(L_\QQ) = \gen_\QQ(M_\QQ) = \Cl_\QQ(M_\QQ)$, so $L_\QQ$ is necessarily isometric to $M_\QQ$ over $\QQ$.
So any invariant of $L_\QQ$ is an invariant of every lattice in $\gen(L)$, e.g. the discriminant.
A similar situation holds with $\QQ$ replaced by $\RR$, so any invariant of $L_\RR$ is an invariant of $\gen(L)$, e.g. the signature.
:::

:::{.remark}
Checking if two $\ZZ$-lattices are in the same genus is a computable problem: to see if $L_{\ZZpadic} \iso M_{\ZZpadic}$, one can block-diagonalize their corresponding Gram matrices over $\ZZpadic$ and check equivalence.
Moreover, one only has to check the finite number of primes $p$ dividing $2\disc(L)^2$.
:::

:::{.remark}
However, the Hasse principle does *not* hold for lattices over $\ZZ$ -- lattices may be in the same genus, i.e. locally isometric at every prime $p$, without being "globally" isometric over $\ZZ$.
Letting $L$ be a $\ZZ$-lattice, recall that $\Cl(L) = \ts{M \st M\iso L}$ is the set of lattices that are isometric to $L$ over $\ZZ$.
Since $M\iso L$ implies $M_{\AA_\ZZ}\iso L_{\AA_\ZZ}$, there is an inclusion $\Cl(L) \subseteq \gen(L)$ which is generally not an equality.
:::

:::{.theorem title="{\cite[Ch. 9, Thm 1.1]{casselsRationalQuadraticForms2008}}"}
Let $L$ be a nondegenerate $\ZZ$-lattice.
Then there are finitely many isometry classes of lattices in the genus of $L$.
:::

:::{.remark}
By \cite[Ch. 9, \S 4]{casselsRationalQuadraticForms2008}, $\gen(L)$ is a finite set, so $\Cl(L)$ is a finite set as well. 
Thus the genus of $L$ is partitioned into finitely many isometry classes, motivating the following definition:
:::

:::{.definition title="Class number"}
Let $(L, \beta)$ be a nondegenerate $\ZZ$-lattice.
We define the **class number** of $L$ to be the number of isometry classes in $\gen(L)$.
:::

:::{.remark}
By the above discussion, $\cl(L)$ is finite, and we can write
\[
\gen(L) = \coprod_{i=1}^{\cl(L)} \Cl(L_i), \qquad \size \gen(L) = \sum_{i=1}^{\cl(L)} \size \Cl(L_i)
\]
for some representatives $L_i$ of each isometry class.
Thus $\gen(L) = \Cl(L)$ if and only if $\cl(L) = 1$, and in particular, if $\cl(L) = 1$ then $L$ is unique in its genus and unique up to isometry.
:::

:::{.lemma}
Let $L$ be a nondegenerate lattice.
Then
\[
\Cl(L) = 1 \iff \Cl(L(n)) = 1 \qquad \forall n\in \ZZ\smz
.\]
This can be strengthened to
\[
\Cl(L) = 1 \iff \Cl(L(n)) = 1 \qquad \text{ for one } n\in \ZZ\smz
.\]
:::

### Stable Equivalence

:::{.definition title="Stably isometric"}
Let $L_1, L_2$ be lattices.
We say $L_1$ is **stably isometric** to $L_2$ if there exist unimodular lattices $P_1, P_2$ such that 
\[
L_1 \oplus P_1 \iso L_2 \oplus P_2
.\]
We define the **stable isometry class** of $L$ as 
\[
\Cl^{\stab}(L) \da \ts{(M, \beta_M) \st M \text{ is stably isometric to } L}
,\]
and write $\Cl^\stab(L_1) = \Cl^\stab(L_2)$ if $L_1$ is stably isometric to $L_2$.

If $L_1, L_2$ are even lattices, we additionally require $P_1, P_2$ to be even.
:::

:::{.remark}
Two even lattices are stably isometric if and only if they have isometric discriminant forms.
:::


:::{.theorem title="{\cite[Thm. 1.3.1]{nikulin1979integer-symmetric}, \cite[Thm. 4.1]{durfee1979fifteen}}"}
\label[theorem]{thm:stable_equiv_equals_disrim_equiv}
Let $L_1, L_2$ be two nondegenerate even lattices.
Then
\[
\Cl(A_{L_1}, q_{A_{L_1}}) = \Cl(A_{L_2}, q_{A_{L_2}}) \iff \Cl^{\stab}(L_1) = \Cl^{\stab}(L_2)
,\]
i.e. $L_1$ and $L_2$ have isomorphic discriminant quadratic forms if and only if $L_1$ is stably isometric to $L_2$.

Similarly, if $L_1, L_2$ are two nondegenerate odd lattices, then
\[
\Cl(A_{L_1}, \beta_{A_{L_1}}) = \Cl(A_{L_2}, \beta_{A_{L_2}}) \iff \Cl^{\stab}(L_1) = \Cl^{\stab}(L_2)
,\]
i.e. $L_1, L_2$ have isomorphic discriminant *bilinear* forms if and only if $L_1, L_2$ are stably equivalent (where $P_1, P_2$ are no longer required to be even.)
:::

:::{.corollary}
Let $L_1, L_2$ be nondegenerate lattices of the same signature. Then
\[
\Cl^\stab(L_1) = \Cl^\stab(L_2) \implies \gen(L_1) = \gen(L_2)
.\]
Thus $\Cl^\stab(L) \subseteq \gen(L)$ for even lattices, i.e. stably equivalent lattices are in the same genus.
:::

:::{.proof}
This follows from combining \Cref{thm:even_lattice_genus_signature_discriminant} with \Cref{thm:stable_equiv_equals_disrim_equiv}.
:::

:::{.corollary}
The set $\Cl^{\stable}(L)$ is finite.
:::

### Genera of nondegenerate lattices 

:::{.theorem title="{\cite[Cor. 1.9.4, Cor. 1.16.3]{nikulin1979integer-symmetric}}"}
\label[theorem]{thm:even_lattice_genus_signature_discriminant}
Let $L_1, L_2$ be two even, nondegenerate lattices.
Then $\gen(L_1) = \gen(L_2)$ if and only if

1. $\signature(L_1) = \signature(L_2)$, and
2. $\Cl(A_{L_1}, q_{A_{L_1}}) = \Cl(A_{L_2}, q_{A_{L_2}})$.

Thus the genus of a nondegenerate even lattice $L$ is determined by its signature and the isometry class of its discriminant *quadratic* form.

Similarly, let $L_1, L_2$ be two odd, nondegenerate lattices.
Then $\gen(L_1) = \gen(L_2)$ if and only if

1. $\signature(L_1) = \signature(L_2)$, and
2. $\Cl(A_{L_1}, \beta_{A_{L_1}}) = \Cl(A_{L_2}, \beta_{A_{L_2}})$.

Thus the genus of a nondegenerate even lattice $L$ is determined by its signature and the isometry class of its discriminant *bilinear* form.
:::

:::{.definition title="Genus invariant"}
Motivated by this result, for an even nondegenerate lattice $L$, we define its **genus invariant** as the triple $g(L) \da (p, q, \Cl(A_L, q_{A_L}))$ where $(p,q) \da \signature(L)$.
Similarly, if $L$ is odd, we instead define $g(L) \da (p, q, \Cl(A_L, \beta_{A_L}))$.

By the above theorems, the genus of a nondegenerate lattice $L$ is uniquely determined by its genus invariant $g(L)$.
:::

:::{.corollary}
Let $L_1, L_2$ be nondegenerate *indefinite, unimodular* lattices.
Then
\[
\gen(L_1) = \gen(L_2) \iff \signature(L_1) = \signature(L_2)
,\]
and the genus of $L$ is uniquely determined by its signature.
:::

:::{.corollary}
Let $L_1, L_2$ be nondegenerate, *definite, unimodular* lattices.
Then
\[
\gen(L_1) = \gen(L_2) \iff \rank(L_1) = \rank(L_2)
,\]
and the genus of $L$ is uniquely determined by its rank.
:::

### Isometry classes of even lattices

:::{.theorem title="{\cite[Cor. 1.13.3]{nikulin1979integer-symmetric}}"}
\label[theorem]{thm:sufficient_even_class_number_one}
Let $L$ be an even nondegenerate lattice.
If 
\[
\ell(L) \leq \rank(L) - 2
,\]
then $\gen(L) = \Cl(L)$ and thus $\cl(L) = 1$.
:::

:::{.corollary}
If $L$ is isometric to $P \oplus M$ where $P, M \leq L$ are sublattices and $P$ is unimodular, then $\cl(L) = 1$.
:::

:::{.proof}
Any unimodular sublattice of $L$ has rank at least 2,
so the assumptions of \Cref{thm:sufficient_even_class_number_one} are satisfied since $\ell(L) \leq \rank(L)$ always holds.
The result follows from the fact that $\ell(P) = 0$ for any unimodular lattice $P$ and the length $\ell(L)$ is additive in the sense that $\ell(P \oplus M) = \ell(P) + \ell(M)$.
:::

:::{.corollary title="Class number one for indefinite lattices {\cite[Cor. 14.4.3]{nikulin1979integer-symmetric}}"}
Let $L$ be a nondegenerate indefinite lattice with $\rank(L) \geq 3$.
Then if

- $\ell(L) \leq \rank(L) - 2$ if $L$ is even, or
- $\ell(L) \leq \rank(L) - 3$ if $L$ is odd,

then $\cl(L) = 1$.
:::

:::{.remark}
We note that for indefinite even lattices $L$, the class number of $L$ is "usually" one.
For *definite* lattices, the situation is reversed, and having class number one is somewhat rare.
By \cite[\S 3.4]{Sca87}, if $\rank(L) > 16 + \ell(L)$, then $\cl(L) \geq 2$.

TODO Scattone 8 \S 11.1
:::


:::{.theorem title="Nikulin's form of Witt cancellation {\cite[Cor. 1.13.4]{nikulin1979integer-symmetric}}"}
Let $L$ be an even lattice.
Then $L \oplus U$ is the unique lattice up to isometry with its signature and discriminant form.
:::

:::{.theorem title="Uniqueness of even indefinite lattices"}
If $L$ is an even indefinite lattice such that
\[
\ell(L) + 2\leq \rank_\ZZ(L)
,\]
then $\cl(L) = 1$.
:::

### Isometry classes of Hyperbolic Lattices

:::{.corollary title="Sufficient criteria for isometries of hyperbolic lattices"}
Let $L_1, L_2$ be two hyperbolic lattices.
Then $\Cl(L_1) = \Cl(L_2)$ if

- $\gen(L_1) = \gen(L_2)$, and
- $\rank(L_1) \geq \ell(L_1) + 2$.

:::

:::{.corollary title="Classification of even hyperbolic lattices"}
Let $L_1, L_2$ be two even hyperbolic lattices.
Then $\Cl(L_1) = \Cl(L_2)$ if

- $\signature(L_1) = \signature(L_2)$
- $A_{L_1} \iso A_{L_2}$
- $\rank(L_1) \geq \ell(L_1) + 2$.

:::

We conclude with the following:

:::{.theorem title="{\cite{kneserKlassenzahlenIndefiniterQuadratischer1956}}"}
Let $L$ be an indefinite lattice.
If $\rank L \geq 3$ and $\disc(L)$ is squarefree, then $\cl(L) = 1$.
:::

:::{.remark}
This follows from the fact that if $\cl(L) > 1$, then there exists a prime $p$ such that the quadratic form $q$ of $L$ can be diagonalized over $\ZZpadic$ where the diagonal entries are distinct powers of $p$.
:::



## Summary of classification results

### 2-elementary Lattices

:::{.remark}
Let $L$ be an even 2-elementary lattice.
If $L$ is indefinite and $p$-elementary, then $\cl(L) = 1$.
Otherwise, one may appeal to \cite[Thm. 1.14.2]{nikulin1979integer-symmetric}.
:::

:::{.theorem title="{\cite[Cor. 14.6.2, 14.6.3]{petersSymmetricQuadraticForms2024}} "}
Let $L$ be an even, indefinite, $p$-elementary lattice with $\rank(L) \geq 4$.
Then $\cl(L) = 1$, and $\Cl(L_1) = \Cl(L_2)$ if and only if

- $\signature(L_1) = \signature(L_2)$, and
- $\Cl(A_{L_1}, q_{A_{L_1}}) = \Cl(A_{L_2}, q_{A_{L_2}})$.

Moreover, this result can be refined: writing $\abs{ \disc(L)} = p^{\ell(L)}$, if $p > 2$ then $\Cl(L_1) = \Cl(L_2)$ if and only if 

1. $\signature(L_1) = \signature(L_2)$, and
2. $\ell(L_1) = \ell(L_2)$.

If $p = 2$, this holds if and only if

1. $L_1, L_2$ have the same parity (even/odd),
2. $\signature(L_1) = \signature(L_2)$, and
3. $\ell(L_1) = \ell(L_2)$.

Moreover, the $p=2$ case yields exactly two isometry types:
\[
(A_L, q) \iso 
\begin{cases}
\mfu_1^{\oplus {1\over 2}\ell(L)}, & L \text{ is even } (\tau_8(A_L) = 0) \\
\mfu_1^{\oplus {1\over 2}(\ell(L) - 2)} \oplus \mfv_1 & L \text{ is odd } (\tau_8(A_L) = 4)
\end{cases}
.\]
where $\tau_8(A_L)$ is the index $\tau(L) \pmod 8$ for any lattice $L$ with discriminant group $A_L$.
:::

:::{.remark}
By ???, any quadratic form on a finite group arises as the discriminant form of some even lattice.
See Scattone 36, Theorem 6.
TODO
:::


:::{.remark}
Let $L_1, L_2$ be even 2-elementary lattices.
Then $\gen(L_1) = \gen(L_2)$ if either 

- $L_1 \oplus U \iso L_2 \oplus U$, or
- $\signature(L_1) = \signature(L_2)$ and $A_{L_1} \iso A_{L_2}$.
:::

:::{.remark}
We recall the mirror move algorithm from \cite{nonsymplectic_involutions}.
We have Nikulin's 2-elementary diagram:

\begin{figure}[H]
\centering
\includegraphics{tikz/Vinberg-pyramid}
\caption{The 75 2-elementary lattices that can occur as primitive sublattices of $\lkt$, c.f. \cite[Fig. 1]{nonsymplectic_involutions} and \cite{Nik79}. White nodes are $\delta=0$, black are $\delta=1$, double circled are $\delta = 1,2$.}
\label[figure]{fig:nikulin-table}
\end{figure}
:::

:::{.remark title="2-elementary lattices"}
Let $L$ be a 2-elementary lattice. The **divisibility** of a vector
$v\in L$, denoted $\operatorname{div}_L(v)$, is defined by
$\beta_L(v, L) = \operatorname{div}_L(v)\ZZ$, i.e. the positive
integral generator of the image of the map $\beta_L(v, \cdot): L\to \ZZ$. For
2-elementary lattices, one always has
$\operatorname{div}_L(v) \in \ts{1, 2}$. We set
$v^* \da v/\operatorname{div}_L(v)\in A_L$. Letting
$q_L:A_L \to {1\over 2}\ZZ/\ZZ$ be the induced quadratic form on $A_L$,
we say $v^*$ is **characteristic** if $q_L(x) = \beta_L(v^*, x)\mod \ZZ$
for all $x\in A_L$, and is **ordinary** otherwise. We say that a
primitive isotropic vector $e\in L$ is

1.  **odd** if $\operatorname{div}_L(e) = 1$,

2.  **even ordinary** if $\operatorname{div}_L(e) = 2$ and $e^*$ is
    ordinary, or

3.  **even characteristic** if $\operatorname{div}_L(e) = 2$ and $e^*$
    is characteristic.

The 2-elementary hyperbolic lattices admitting a primitive embedding
into $\lkt$ were classified by Nikulin in \cite[\S 3.6.2]{nikulin1979integer-symmetric}. 
An indefinite 2-elementary lattice is determined up to isometry by a triple of invariants $(r,a,\delta)$. Here, $r\da \operatorname{rank}_\ZZ(L)$ is the rank, $a = \operatorname{rank}_{\FF_2}A_L$ is the exponent appearing in $A_L = (\ZZ/2\ZZ)^a$, and $\delta \in \ts{0, 1}$ is the **coparity**:
we set $\delta = 0$ if $q_L(A_L) \subseteq \ZZ$, so
$q_L(x) \equiv 0 \mod \ZZ$ for all $x\in A_L$, and $\delta=1$ otherwise.
We accordingly specify such lattices using the notation
$(r,a,\delta)_{n_+}$.
:::

:::{.remark}
By \cite[Prop. 1.8.1]{nikulin1979integer-symmetric}, the discriminant form $A_L$ of a 2-elementary lattice $L$ is is a isometric to a direct sum of quadratic forms, which are comprised of the discriminant forms of the lattices $A_1, A_1(-1), U(2)$, and $D_4$.
:::


### Indefinite unimodular lattices

:::{.theorem title="{\cite{milnor1958simply}}"}
Let $L$ be an indefinite even unimodular lattice with $\signature(L) = (p, q)$.
Then $\rank(L)$ is necessarily even, $\tau \equiv 0 \pmod{8}$, and 
\[
L \iso \II_{p, q} \da 
\begin{cases}
E_8(-1)^{\oplus {\tau \over 8}} \oplus U^{\oplus q}, & p-q > 0 \\
E_8^{\oplus {-\tau \over 8}} \oplus U^{\oplus p}, & p-q < 0
\end{cases}
,\]
where $E_8$ is the negative-definite $E_8$ lattice.
:::

:::{.proof}
See \cite[Ch. 5]{serreCourseArithmetic1973}.
:::

:::{.theorem}
Let $L$ be an indefinite odd unimodular lattice with $\signature(L) = (p, q)$.
Then $L \iso \I_{p, q}$.
:::

:::{.theorem}
Any indefinite unimodular lattice is determined up to isometry by its rank, index, and parity.
The same is true for definite unimodular lattices $L$ with $\rank L \leq 8$.
:::

:::{.theorem}
Let $L$ be a unimodular integral lattice with $\rank_\ZZ L \leq 4$.
Then either

- $L$ is odd and $L\iso \I_{p, q}$ for some $p,q$, or
- $L$ is even and either $L\iso U$ or $U^2$.

:::

:::{.corollary}
Let $L$ be an indefinite unimodular lattice.
Then $L[0] \neq \emptyset$, and either

- $L\cong U \oplus M$, or
- $L\cong {\rm I}_{1,1} \oplus M$

where $M$ is again unimodular.
:::

### Unimodular lattices

:::{.remark title="Number of unimodular lattices by dimension"}
The following is a table from \cite[Table 2.2]{conway1999sphere-packings} detailing the number of $n$-dimensional unimodular lattices, where 

- $a_n$ is the number of such lattices $L$ with $N_L(1) = 0$,
- If $n\equiv 0 \pmod 8$, $a_n = d_n + e_n$ is the number of odd and even lattices respectively,
- $b_n$ is the *total* number of unimodular lattices of dimension $n$.

\begin{table}[h!]
\centering
\begin{tabular}{|l|crrrrrrrc|}
\hline$n$ & 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 \\
$a_{n}$ & $0+1$ & 0 & 0 & 0 & 0 & 0 & 0 & 0 & $0+1$ \\
$b_{n}$ & $0+1$ & 1 & 1 & 1 & 1 & 1 & 1 & 1 & $1+1$ \\
\hline$n$ & 9 & 10 & 11 & 12 & 13 & 14 & 15 & 16 & 17 \\
$a_{n}$ & 0 & 0 & 0 & 1 & 0 & 1 & 1 & $1+2$ & 1 \\
$b_{n}$ & 2 & 2 & 2 & 3 & 3 & 4 & 5 & $6+2$ & 9 \\
\hline$n$ & 18 & 19 & 20 & 21 & 22 & 23 & 24 & 25 & 26 \\
$a_{n}$ & 4 & 3 & 12 & 12 & 28 & 49 & $156+24$ & 368 & $?$ \\
$b_{n}$ & 13 & 16 & 28 & 40 & 68 & 117 & $273+24$ & 665 & $?$ \\
\hline
\end{tabular}
\caption{Numbers of isometry classes of unimodular lattices in various ranks.}
\end{table}

For $1\leq n\leq 8$, there is a unique definite odd unimodular lattice $\rm{I}_{n, 0} \cong \gens{1}^{\oplus n}$.
For $n\geq 9,10,11$, there is also $E_8 \oplus \I_{n-8, 0}$, and for $n=12$ there is additionally a lattice called $D_{12}^+$.
:::

:::{.remark}
Let $X_n$ denote the set of unimodular lattices of rank $n$, modulo isometry, and define the generating function $F_{X_n}(x) \da \sum_{i=0}^\infty \size X_n \cdot x^n$.
The following data is due to \cite{chenevierUnimodularHunting2024}:
\begin{align*}
F_{X_n}(x) &= 1 + 1 x + 1 x^{2} + 1 x^{3} + 1 x^{4} + 1 x^{5} + 1 x^{6} + 2 x^{7} + 2 x^{8} \\
&\quad + 2 x^{9} + 2 x^{10} + 2 x^{11} + 2 x^{12} + 4 x^{13} + 5 x^{14} + 8 x^{15} + 9 x^{16} \\
&\quad + 13 x^{17} + 16 x^{18} + 28 x^{19} + 40 x^{20} + 68 x^{21} + 117 x^{22} + 297 x^{23} + 665 x^{24} \\
&\quad + 2566 x^{25} + 17059 x^{26} + \cdots
\end{align*}



:::


### Summary

:::{.theorem title="Summary of classification results"}
Let $(L, q)$ be a nondegenerate quadratic form.
We summarize below the classification up to isometry of such forms over various rings $R$.
The following criteria for $(L_1, q_1)$ and $(L_2, q_2)$ are necessary and sufficient for $\Cl_R(L_1, q_1) = \Cl_R(L_2, q_2)$:

- $R = \FF_p$, $p\geq 3$ an odd prime:
    - $\rank_{\FF_p}(L_1) = \rank_{\FF_p}(L_2) \pmod{2\ZZ}$,
    - If both $\disc(L_1), \disc(L_2)$ are zero or nonzero in $D(\FF_q)$.
- $R = \QQ_p$:
    - $\rank_{\QQpadic}(L_1) = \rank_{\QQpadic}(L_2)$,
    - $\disc(L_1) = \disc(L_2) \in D(\QQpadic)$,
    - $\eps_p(L_1) = \eps_p(L_2)$, where $\eps_p$ is the **Hasse invariant** at $p$.
- $R = \QQ$:
    - $\rank_\QQ(L_1) = \rank_\QQ(L_2)$,
    - $\tau(L_1) = \tau(L_2)$,
    - $\disc(L_1) = \disc(L_2) \in D(\QQ)$,
    - $\eps_p(L_1) = \eps_p(L_2)$ for all primes $p\leq \infty$, or equivalently,
    - $L_{1, \QQpadic} \iso L_{2, \QQpadic}$ for all primes $p\leq \infty$.
- Over $\RR$:
    - $\signature(L_1) = \signature(L_2)$.
- Over $\CC$:
    - $\rank_\CC(L_1) = \rank_\CC(L_2)$.
- Over $\ZZ$: indefinite, unimodular
    - The parity of $L_1, L_2$ agree (even/odd),
    - $\signature(L_1) = \signature(L_2)$.


There is similarly a classification of torsion quadratic forms for various groups $G$:

- $G$ a 2-primary group:
    - $\tau_8(L_1) = \tau_8(L_2)$

:::

## Theta functions

:::{.definition title="Theta function and zeta functions"}
The **theta function ** of a positive definite lattice $(L, \beta)$ is
\[
\Theta_L(z) \da \sum_{v\in L} q^{{1\over 2}\beta(v, v)} = \sum_{m=0}^\infty N_L(m) q^m,\quad 
N_L(m) \da \size L[m],\,\, q \da e^{2 i\pi z}
.\]
This is a holomorphic function for $z\in \HH$.
The **zeta function** of $L$ is 
\[
\zeta_L(s) \da \sum_{v\in L\smz} \beta(v,v)^{-s}
.\]
:::

:::{.remark}
If $L \iso M$ then $N_{L}(k) = N_{M}(k)$ for all $k$ and thus $\Theta_{L}(z) = \Theta_{M}(z)$.
So the theta function of $L$ is an invariant of its isometry class.
:::

:::{.definition}
The **Jacobi theta functions** are defined as
\begin{align*}
\theta_2(z) &\da \sum_{n\in \ZZ} q^{\qty{n + {1\over 2}}^2 } \\
\theta_3(z) &\da \sum_{n\in \ZZ} q^{{1\over 2}n^2} \\
\theta_4(z) &\da \sum_{n\in \ZZ} (-1)^n q^{{1\over 2}n^2} 
\end{align*}
where $q \da e^{2\pi i z}$.
These have expansions
\begin{align*}
\theta_2(z) &= 2q^{1\over 4}\qty{1 + q^2  + q^{6} + q^{12} + \bigo(q^{20}) } \\
\theta_3(z) &= 1 + 2q   + 2q^4      + 2q^9      + \bigo(q^{16}) \\
\theta_4(z) &= 1 - 2q   + 2q^4      - 2q^9      + \bigo(q^{16})
\end{align*}
:::

:::{.remark}
The theta function is an additive invariant, i.e.
\[
\Theta_{L_1 \oplus L_2}(z) = \Theta_{L_1}(z) \cdot \Theta_{L_2}(z), \qquad \Theta_{L^{\oplus n}}(z) = (\Theta_L(z))^n
\]
and for the dual lattice,
\[
\Theta_{L\dual}(e^{-2\pi t}) = \disc(L)^{1\over 2} \cdot t^{-{n\over 2}}\cdot \Theta_{L}(e^{-2\pi t})
.\]
Moreover, the Poisson summation formula states
\[
\sum_{v\in L} f(v) = \disc(L)^{-{1\over 2}} \cdot \sum_{w\in L\dual}\hat{f}(w)
,\]
which for theta functions yields
\[
\Theta_{L\dual}(z) = \disc(L)^{1\over 2}\cdot \qty{i\over z}^{n\over 2}\cdot \Theta_L(-1/z)
.\]
There is also a relation for twists:
\[
\Theta_{L(n)}(z) =\Theta_L(n^2 z)
.\]
:::

:::{.example}
By directly counting vectors of various norms, one can compute
\[
\Theta_{\I_{1, 0}}(z) = \sum_{m\in \ZZ} q^{m^2} = 1 + 2q + 2q^4 + 2q^9 + \bigo(q^{16}) = \theta_3(z)
,\]
where $\theta_3(z)$ is the third *Jacobi theta function* defined above.
By additivity, we have
\[
\Theta_{\I_{n, 0}}(z) = \Theta_{\I_{1, 0}}(z)^n = \theta_3(z)^n
.\]
This is often applied in classical number-theoretic contexts, such as counting the number of representations of a number $m$ as a sum of squares.
For example,
\[
\size\ts{x \in \ZZ^n \st \sum_{i=1}^n x_i^2 = k} = \size \I_{n, 0}[k] = [q^k]\,\theta_3(z)^n
,\]
where $[q^k]\, f(z)$ denotes the coefficient of $q^k$ in the series expansion of $f(z)$.
For example, one can compute
\begin{align*}
\Theta_{\I_{1, 0}}(z) &= 1 + 2q + 2q^4 + 2q^9 + \bigo(q^{10}) \\
\Theta_{\I_{2, 0}}(z) &= 1 + 4q + 4q^2 + 4q^4 + \bigo(q^{5}) \\
\Theta_{\I_{3, 0}}(z) &= 1 + 6q + 12q^2 + 8q^3 + \bigo(q^{4}) \\
\Theta_{\I_{4, 0}}(z) &= 1 + 8q + 24q^2 + 32q^3 + \bigo(q^{4})
\end{align*}

:::

:::{.example title="The theta function of $D_n$"}
One can show that
\[
\Theta_{D_n}(z) = {1\over 2}(\theta_3(z)^n + \theta_4(z)^n)
.\]
This yields
\begin{align*}
\Theta_{D_4}(z) &= 1 + 24q^2 + 24q^4 + \bigo(q^6) \\
\Theta_{D_5}(z) &= 1 + 40q^2 + 90q^4 + \bigo(q^6) \\
\Theta_{D_6}(z) &= 1 + 60q^2 + 252q^4 + \bigo(q^6) \\
\Theta_{D_7}(z) &= 1 + 84q^2 + 574q^4 + \bigo(q^6) 
,\end{align*}
which by an inductive argument shows that the number of roots in $D_n$ is $4 \cdot {n\choose 2} = 2n(n-1)$.

:::

:::{.example title="The theta function of $E_8$"}
Let $\sigma_k(m) \da \sum_{d \mid m} d^k$ be the $k$th sum of divisors function, one has
\[
\Theta_{E_8}(z) = 1 + 240 \sum_{m\geq 1} \sigma_3(m) q^{2m} 
= 1 + 240 q^2 + 2160 q^4 + \bigo(q^6)
.\]
In particular, this shows that $E_8$ has exactly 240 roots.

If $L$ is any unimodular lattice, $\Theta_L$ can be written as a polynomial in $\Theta_{E_8}(z)$ and 
\[
\Delta_{24}(z) \da q^2 \prod_{m\geq 1} (1-q^{2m})^{24}
= \sum_{m\geq 0}\tau(m) q^{2m}
= q^2 - 24q^4 + 252q^6 + \bigo(q^8)
\]
where $\tau$ is Ramanujan's $\tau$ function.
:::


:::{.theorem title="Even definite unimodular lattices exist only in ranks 0 mod 8"}
Let $L$ be an even positive definite unimodular lattice.
Then $n\da \rank_\ZZ L \equiv 0 \pmod 8$.
:::

:::{.proof}
We first write its theta function
\[
\Theta_L(z) \da \sum_{v\in L} q^{\beta(v,v)\over 2}, \qquad q = e^{2\pi i z}
,\]
which we claim is a modular form of weight $n/2$, and thus satisfies the transformation property
\[
\Theta_L(-1/z) = (z/i)^{n\over 2} \Theta_L(z)
.\]
We first write $\Theta_L(z) = \sum_{v\in L} g(v, z)$ where 
\[
g(v,z) \da (e^{2\pi i z})^{\beta(v,v)\over 2} = e^{\pi i z \beta(v,v)}
,\]
and thus restricting to $z \da it$ with $t > 0$, we have
\[
g(v, -1/it) = e^{- \pi \beta(v,v)\over t}
.\]
Recall the general Poisson summation formula,
\[
\Theta_L(z) \da \sum_{v\in L} f(v, z) = {1\over \vol(L)} \sum_{w\in L\dual}\hat{f}(w, z)
,\]
where we take the Fourier transform in the $v$ and $w$ variables.
Setting $f(v, t) \da g(v, -1/it)$ we have the Fourier transform 
\[
\hat{f}(w, t) = t^{n\over 2} e^{-\pi t \beta(w, w)}
,\]
and noting that $\vol(L) = 1$ we have
\begin{align*}
\Theta_L(-1/z) 
&\da \Theta_L(-1/it) \\
&= \sum_{v\in L} f(v, t) \\
&= \sum_{w\in L\dual} \hat{f}(w, t) \\
&= \sum_{w\in L\dual} t^{n\over 2} e^{-\pi t \beta(w, w)} \\
&= t^{n\over 2}\sum_{v\in L} e^{-\pi t \beta(v, v)} \\
&= t^{n\over 2}\sum_{v\in L} g(v, it) \\
&= t^{n\over 2} \Theta_L(it) \\
&= \qty{it\over i}^{n\over 2} \Theta_L(it) \\
&= \qty{z\over i}^{n\over 2}\Theta_L(z)
,\end{align*}
which is the desired transformation property.

We now use the fact that $\SL_2(\ZZ)\actson \HH$ by 
\[
S \da \matt 0 {-1} 1 0 . z = { 0z - 1 \over 1z + 0} = -{1\over z}, \qquad T \da \matt 1 1 0 1 . z = {1z + 1 \over 0z + 1} = z+1
\]
where $(ST)^3 = \id$.
Note that since $e^{2\pi i (z+1)} = e^{2\pi i z}$, we have $\Theta_L(Tz) = \Theta_L(z+1) = \Theta_L(z)$ and thus
\[
\Theta_L(TS.z) = \Theta_L\qty{T.(-1/z)} = \Theta_L(-1/z) = \qty{z\over i}^{n\over 2}\Theta_L(z)
= (-i)^{n\over 2}z^{n\over 2}\Theta_L(z)
.\]
By replacing $L$ with $L^2$ or $L^4$, we can assume $n\equiv 4 \mod 8$, and thus
\[
\Theta_L(TS.z) = -z^{n\over 2}\cdot \Theta_L(z)
,\]
and we arrive at the contradiction
\begin{align*}
\Theta_L(z) 
&= \Theta_L((TS)^3.z) \\
&= \Theta_L(TS . (TS)^2.z) \\
&= -((TS)^2.z)^{n\over 2} \cdot \Theta_L((TS)^2.z) \\
&= -((TS)^2.z)^{n\over 2} \cdot \Theta_L(TS.TS.z) \\
&= ((TS)^2.z)^{n\over 2} \cdot (TS.z)^{n\over 2}\cdot \Theta_L(TS.z) \\
&= -((TS)^2.z)^{n\over 2} \cdot (TS.z)^{n\over 2} \cdot z^{n\over 2}\cdot \Theta_L(z) \\
&= - \qty{-1\over z-1}^{n\over 2} \cdot \qty{z-1\over 1}^{n\over 2} \cdot z^{n\over 2}\cdot \Theta_L(z) \\
&= -\qty{ \qty{-1\over z-1}\cdot {z-1\over z} \cdot z }^{n\over 2} \Theta_L(z) \\
&= - \Theta_L(z)
,\end{align*}
implying $\Theta_L(z) = 0$.
:::

### The mass formula

:::{.definition title="Mass of a genus/lattice"}
Let $L$ be a definite integral lattice, and define the **mass** of $L$ (equivalently, the mass of $\gen(L)$) by
\[
m(L) \da \sum_{\Cl(L_i) \in \gen(L)} {1\over \size{\Orth(L_i)}} = \sum_{i=1}^{\cl(L)} {1\over \size{\Orth(L_i)}}
\]
where $L_i$ are representatives of each isometry class in the genus of $L$.
:::

:::{.remark}
By \cite[\S 3.4]{Sca87}, the Smith-Minkowski-Siegel mass formula expresses $m(L)$ as an infinite product
\[
{1\over m(L)} = \prod_{p\leq \infty}a_p(L)
\]
where $p$ ranges over all primes, including $p=\infty$, and $a_p$ depends only on the isometry class of $L_{\ZZpadic}$.
There are explicit formulas: for $p<\infty$, one has

\[
a_p(L) = \lim_{t\to\infty} {1\over 2} E_{p^t}(G_\beta) p^{-tn(n-1)\over 2}, \qquad n\da \rank_\ZZ(L)
\]
where for any matrix $M$, 
\[
E_q(M) \da \size\ts{A \in \Mat_{n\times n}(\ZZ/q\ZZ) \st A^tMA \equiv M \pmod q}
.\]
For $p=\infty$, the factor is given by
\[
a_\infty(L) = \pi^{n(n+1)\over 4}\qty{2 \Gamma\qty{1\over 2}\Gamma\qty{2\over 2}\cdots \Gamma\qty{n\over 2} \abs{\disc(L)}^{n(n+1)\over 2} }\inv
.\]
Moreover, in practical computations, this infinite formula reduces to a finite computation and the infinite product has nontrivial terms at only finitely many primes.
One can show that for odd $n$ and all primes $p$ that do not divide $2\abs{\disc(L)}$,
\[
a_p(L) = \gamma_p(n) \da \qty{1 - {1\over p^2}}\qty{1 - {1\over p^4}}\cdots\qty{1 - {1\over p^{2m}}}, \qquad n = 2m+1
,\]
and then apply the identity
\[
\prod_{p<\infty} {1\over \gamma_p(n)} = \zeta(2)\zeta(4)\cdots\zeta(2m)
.\]

Explicitly, one has
\[
m(L) = {a_\infty(L) \over \zeta(2)\zeta(4)\cdots\zeta(m)} \cdot \prod_{p\mid 2\abs{\disc(L)}} {a_p(L) \over \gamma_p(n)}
.\]

\cite{Sca87} uses this to determine
\[
m(\gens{-2k} \oplus E_8^2) = 
\frac{691 \cdot 3617}{
2^{31} \cdot 3^{10} \cdot 5^{4} \cdot 7^{2} \cdot 11 \cdot 13 \cdot 17} \cdot k^{8} 
\prod_{p \divides k} \frac{1}{2}\qty{1+{1\over p^8}} 
\]
and thus 
\[
2^{-p(k)} M_1 k^8 <
\cl(\gens{-2k} \oplus E_8^2) <
Mk^8,\qquad 
M = 2 \cdot 691 \cdot 3617,
M_1 = {M \over 2^{32} \cdot 3^{10} \cdot 5^{4} \cdot 7^{2} \cdot 11 \cdot 13 \cdot 17}
\]
where $p(k)$ is the number of primes dividing $k$.
Thus this class number is asymptotically of order $k^8$.
:::


:::{.theorem title="The Smith-Minkowski-Seigel mass formula {\cite[\S 4, \S 7]{conwayLowDimensionalLatticesIV1988}}"}
Then if $L$ is even, unimodular, and positive definite of rank $n$, there is an equality
\begin{align*}
m(L) &= 2^{1-n} \pi^{-{n(n+1)\over 4}} \cdot \qty{\prod_{1\leq j\leq n}\Gamma\qty{j\over 2} } \cdot \qty{\prod_{0 \leq 2k \leq n-2}\zeta(2k) }\cdot \zeta\qty{n\over 2} \\
&= 2\zeta(n/2) {\zeta(2) \cdot \zeta(4) \cdots \zeta(n-2) \over \vol(S^0)\cdot \vol(S^1)\cdots \vol(S^{n-1})} \\
& = {B_{n\over 2}\over n}\cdot \prod_{1 \leq 2j \leq n-2} {B_{2j} \over 4j}
,\end{align*}
where $\zeta$ is the Riemann zeta function, $B_k$ are the Bernoulli numbers generated by
\[
{z\over e^z-1} = \sum_j B_j {z^j\over j!}
,\]
and
\[
\vol(S^{j-1}) = {2\pi^{j\over 2} \over \Gamma(j/2)} \\
\]
is the volume of the $(j-1)$-dimensional sphere.
:::

:::{.remark}
There are effective methods for computing the mass of a genus $\genus(L)$ with knowledge of only one lattice in the genus, and this can be used to estimate $\cl(L)$.
:::


:::{.corollary}
There is a unique even, unimodular, positive definite lattice of rank $8$: the $E_8$ lattice.
:::

:::{.proof}
One can show that $\Orth(E_8) = W_{E_8}$, and 
\[
\size W_{E_8} = 2^{14}\cdot 3^5 \cdot 5^2 \cdot 7
.\]
Setting $n=8$, we have
\begin{align*}
m(E_8) 
&= {1\over 8}B_4 \cdot \qty{ {1\over 4}B_2 + {1\over 8}B_4 + {1\over 12}B_6 } \\
&= {1\over 8}{-1\over 30} \cdot\qty{ {1\over 4}{1\over 6} \cdot {1\over 8}{-1\over 30} \cdot {1\over 12}{1\over 42} } \\
&= (1/696729600)\inv \\
&= (2^{14} \cdot 3^5 \cdot 5^2 \cdot 7)\inv \\
&= 1/\size W_{E_8}
,\end{align*}
which forces $\gen(E_8) = \Cl(E_8)$ and $\cl(E_8) = 1$, using the fact that all even unimodular lattices of a given rank $n$ are in the same genus.
:::

:::{.remark}
This formula is used in moduli problems, e.g in \cite{Sca87} where it is used to estimate the number of boundary curves in the Baily Borel compactification of $F_{2d}$ -- it is determined that this number grows asymptotically like $(2k)^8$.
:::


:::{.remark}
For even unimodular lattices $L$ of rank $n=8k$, one generally has
\[
m(L) = {B_{4k} \over 8k } \prod_{j=1}^{4k-1}{B_{2j} \over j}
.\]
For odd unimodular lattices of rank $n$, one instead has $m(L) = M(n)$, where $M_n$ is a constant depending only on $n$.
The first few values are given by the following from \cite[Table 16.2]{conway1999sphere-packings}.
One can also generate by direct computations, e.g. in \cite{sagemath}, the following computations of the sizes of orthogonal groups of the lattice $\I_{n, 0}$:

| $n$ | $M(n)$ | $\size \Orth(\I_{n,0})$ |
|-----|--------|-------------------------|
| $0$ | $1$    | $1$ |
| $1$ | ${1\over 2}$    | $2$ |
| $2$ | ${1\over 8}$    | $8$ |
| $3$ | ${1\over 48}$    | $48$ |
| $4$ | ${1\over 384}$    | $384$ |
| $5$ | ${1\over 3,840}$    | $3,840$ |
| $6$ | ${1\over 46,080}$    | $46,080$ |
| $7$ | ${1\over 645,120}$    | $645,120$ |
| $8$ | ${1\over 10,321,920}$    | $10,321,920$ |
| $9$ | ${17 \over 2,786,918,400}$    | $185,794,560$ |


One can also verify the general formula $\size \Orth(\I_{n, 0}) = 2^n \cdot n!$.
This verifies that $\I_{n, 0}$ is the unique odd unimodular lattice in ranks $n = \leq 8$, and that there is at least one other inequivalent rank $9$ lattice.
By \cite[\S 2.4]{conway1999sphere-packings}, the missing lattice is $E_8 \oplus \I_{1, 0}$, and one can compute $\size\Orth(E_8 \oplus \I_{1, 0}) = 1,393,459,200$ and verify that
\[
{1\over \size \Orth(\I_{9, 0})} + {1\over \size \Orth(E_8 \oplus \I_{1, 0})} = {1\over 185,794, 560} + {1\over 1,393,459, 200} = {17 \over 2786918400} = M(9)
.\]
Thus there are exactly two isometry classes of odd definite unimodular rank 9 lattices.
:::

## Embeddings

:::{.proposition title="Finiteness of embeddings for even, unimodular lattices"}
Recalling the definitions in \Cref{def:equivalent_embeddings}, if $S$ and $L$ are even lattices and $L$ is unimodular, then $\Emb(S, L)$ is a finite set.
:::

:::{.proof}
By \cite[Prop. 1.6.1]{nikulin1979integer-symmetric}, such a primitive embedding $\iota: S\injects L$ is determined by an isometry $\gamma: A_{S} \iso A_T(-1)$, two such primitive embeddings are equivalent if and only if $\gamma_1$ is conjugate to $\gamma_2$ under $\Orth(A_T)$, and $\iota_1(S_1) \iso \iota_2(S_2)$ are equivalent primitive sublattices if $\exists (\phi, \psi)\in \Orth(S) \oplus \Orth(T)$ such that $\gamma_1 \circ \ro{\phi}{A_S} = \ro{\psi}{A_T}\circ \gamma_2$.

Since $A_S, A_T$ are finite abelian groups, $\Isom(A_S, A_T)$ is a finite set, as is $\Orth(A_T)$.
Moreover, noting that if $S_1\iso S_2$ then $A_{S_1}\iso A_{S_2}$ and thus $\Emb(S_1, L) \cong \Emb(S_2, L)$, so $\Emb(S, L)$ only depends on the isometry class of $S$.
Since $\gen(S)$ is a finite set, there are only finitely many isometry classes of $S$, so $\cl(S)$ is finite and thus $\Emb(S, L)$ a finite set.
:::

### Gluing and Overlattices

:::{.definition title="Overlattices"}
Let $S\injects L$ be an embedding of lattices.
We say $L$ is an **overlattice** of $S$ if $\iota(S)$ is a finite index sublattice.
:::


:::{.remark}
Moreover, 
\[
H_{L}^\perp = L\dual/S, \qquad H_{L}^\perp/H_{L} = A_{L}
.\]
:::
:::{.remark}
A primitive embedding $S\injects L$ with $T \da S^{\perp L}$ is uniquely determined by the choice of

1. A subgroup $H \leq A_L$, the *embedding subgroup*, and
2. An isometry $\gamma: H \iso H' \subseteq A_S$, the *embedding isometry*.

Letting $\Gamma$ be the graph of $\gamma$ in $A_L \oplus A_S(-1)$, one has $A_T = \Gamma^{\perp}/\Gamma$ and 
\[
\abs{\disc T} = { \abs{\disc L} \cdot \abs{\disc S} \over (\size H)^2 }
.\]

Equivalently, if $\cl(L) = 1$, such an embedding is determined by

1. A subgroup $H \leq A_S$, the *gluing subgroup*, and
2. An isometry $\gamma: H\iso H' \subseteq A_T$, the *gluing isometry*.

In this situation, we similarly let $\Gamma$ be the graph of $\gamma$ in $A_S \oplus A_T(-1)$, obtain $A_L = \Gamma^{\perp}/\Gamma$, and
\[
\abs{\disc L} = { \abs{\disc S} \cdot \abs{\disc T} \over (\size H)^2 }
.\]

:::

:::{.remark}
Let $S\injects L$ be an embedding of even lattices.
We define $H_L \da L/S$.
There is a chain of embeddings
\[
S \injects L \injects L\dual \injects S\dual
,\]
and thus 
\[
H_L \injects L\dual/S \injects S\dual/S = A_S, \qquad 
{L\dual/S \over H_L} = {L\dual/S \over L/S} \cong L\dual/L = A_L
.\]
By \cite[Prop. 1.4.1]{nikulin1979integer-symmetric}, there is a bijection
\begin{align*}
\ts{\text{Even overlattices of } S}&\mapstofrom \ts{\text{Isotropic subgroups of } A_S} \\
L &\mapsto H_L
\end{align*}
By \cite[Prop. 1.4.2]{nikulin1979integer-symmetric}, this restricts to an isomorphism
\begin{align*}
\ts{\text{Even overlattices of } S}\modiso &\mapstofrom \ts{\text{Isotropic subgroups of } A_S}/\Orth(S) \\
L &\mapsto H_L
\end{align*}
where $\Orth(S)$ acts on the set of subgroups of $A_S$ by conjugation, and two overlattices $L_1, L_2$ of $S$ are isomorphic if there is an isometry $\tilde \phi: L_1\to L_2$ lifting some isometry $\phi\in \Orth(S)$.
We summarize this in the following theorem:
:::


:::{.theorem}
Let $\iota: S\injects L$ be an embedding of lattices, and define $H_L \da L/\iota(S)$.
Use the chain of embeddings $S \injects L \injects L\dual \injects S\dual$ to produce embeddings $H_{L} \injects L\dual/S \injects A_S$, noting that $\qty{ L\dual/S }/H_{L}\cong A_{L}$ and that the discriminant form is identically zero on the subgroup $H_{L}$.
We can thus regard $H_L$ as a subgroup of $A_S$.

Conversely, for a subgroup $H\leq A_S$, write $\eta: S\dual \to A_S$ and define a lattice $S_H \da \eta\inv(H) \subseteq S\dual$.
We note that $S_H \contains S$, so $S_H$ is an overlattice of $S$.

These constructions are mutually inverse and define a bijection
\begin{align*}
\ts{\text{Overlattices $L$ of } S} &\mapstofrom \ts{\text{Isotropic subgroups } H \leq A_S} \\
L &\mapsto H_{L} \da L/S \\
L\da S_H &\mapsfrom H
\end{align*}
:::

:::{.remark}
Let $S, T \da S^{\perp L} \injects L$ be primitive embeddings.
Then $S \oplus T\injects L$ embeds primitively, and by the previous remark,
\[
H_L \da {L\over S \oplus T} \injects A_{S \oplus T} = A_S \oplus A_T
.\]

The primitivity of $S\injects L$ and $T\injects L$ is equivalent to the projections of $H_L \subseteq A_S \oplus A_T$ inducing injections
\[
p_S: H_L \injects A_S, \qquad p_T: H_L \injects A_T
.\]
Defining $H_{L, S} \da p_S(H_L)$ and $H_{L, T}\da p_T(H_L)$, these embeddings become isomorphisms onto their images,
\[
p_S: H_L \iso H_{L, S} \subseteq A_S, \qquad p_T: H_L \iso H_{L, T} \subseteq A_T
.\]
This induces an isomorphism of subgroups
\[
\gamma^L_{S, T} \da p_T \circ p_S\inv: H_{L, S} \iso H_{L, T}
.\]
:::

:::{.remark}
If $S \injects L$ is a primitive embedding into an even unimodular lattice, then
\[
H_L \da {L\over S \oplus T} \subseteq A_S \oplus A_T(-1)
\]
is the graph of the **glue map** $\phi_L: A_S\iso A_T(-1)$, so
\[
H_L = \Gamma_{\phi_L} \da \ts{(v, \phi_L(v)) \st v\in A_S}
.\]
Conversely, given any $f\in \Isom(A_S, A_T(-1))$, its graph $\Gamma_f \subseteq A_S \oplus A_T(-1)$ induces a primitive extension $S \oplus T \leq L$ for some even unimodular lattice $L$.

There is a surjection
\begin{align*}
\Orth(L) \surjects 
&\ts{(f,g)\in \Orth(S \oplus T) \st \ro{(f+g)}{A_S \oplus A_T}(H_L) = H_L  } \\
&= \ts{(f,g)\in \Orth(S \oplus T) \st \phi_L \circ \ro{f}{A_T} = \ro{f}{A_S}\circ  \phi_M }
\end{align*}
i.e. a pair of isometries of $S$ and $T$ lifts to an isometry of $L$ if and only if they preserve $H_L$, or equivalently commute with the glue map.
:::

:::{.remark}
Another way to see this: let $S \injects L$ be a primitive sublattice of a unimodular lattice.
The composition
\begin{align*}
L \iso L\dual \surjects S\dual &\surjects A_S \\
v \qquad\qquad\qquad\qquad\qquad\qquad & \mapsto \overline{ \ro{\beta_L(v, \wait)}{S} }
\end{align*}
is surjective with kernel $S \oplus T$, and thus induces an exact sequence and an isomorphism
\[
0 \to S \oplus T \injects L \surjects A_S, \qquad
\iota_S: {L\over S \oplus T}\iso A_S
.\]
Interchanging the roles of $S$ and $T$ yields another isomorphism
\[
\iota_T: {L\over S \oplus T} \iso A_T
,\]
and thus we obtain
\[
j_S = \iota_T \circ \iota_S\inv: A_S \iso A_T
.\]

Then $f \oplus g\in \Orth(S) \oplus \Orth(T)$ lifts to an element of $\Orth(L)$ if and only if $j_S \circ f = g\circ j_S$.
:::

:::{.theorem title="{\cite[Prop. 1.4.2]{nikulin1979integer-symmetric}}"}
Let $L_1, L_2$ be two overlattices of $L$ and let $f\in \Orth(L)$.
Then $f$ extends to $\tilde f\in \Isom(L_1, L_2)$ if and only if $\ro{f}{A_L}$ induces an isomorphism $H_{L_1}\iso H_{L_2}$ on isotropy groups.
Moreover, two embeddings $\iota_i: L \injects L_i$ are isomorphic if and only if $H_{L_1} = H_{L_2}$.
:::


:::{.theorem title="{\cite[Cor. 1.6.2]{Nik79}}"}
Let $S, T$ be lattices.
A primitive embedding $S\injects L$ into a unimodular lattice for which $S^{\perp L} \cong T$ is determined by an isomorphism $\gamma: A_S \iso A_L(-1)$, i.e. such that $\beta_L = -\beta_S$.
Moreover, two such embeddings are isomorphic if and only if they are conjugate by some $\ro{f}{T} \in \Orth(A_T)$ where $f\in \Orth(T)$.
:::

### Even, Unimodular, and $p$-elementary Embeddings

:::{.theorem title="{\cite[Thm. 1.14.1]{nikulin1979integer-symmetric}}"}
Let $\iota: S\injects L$ be an embedding of an even lattice into a unimodular lattice, and let $T\da S^{\perp L}$.
Then $\iota$ is unique up to $\Orth(L)$ if

1. $\cl(T) = 1$, and
2. $\Orth_*(A_{T}) = 0$.

Moreover, if $L$ is either indefinite or of rank $8$, then these conditions are necessary and sufficient.
:::

:::{.remark}
Condition 1 is automatically satisfied if $A_L = C_2^3 \oplus M$ for some form $M$. 
:::

:::{.theorem title="{\cite[Thm 1.14.2]{nikulin1979integer-symmetric}}"}
Let $T$ be an even indefinite lattice such that 

1. $\rank(T) \geq A_{T_p} + 2$ for all $p\neq 2$, and
2. if $\rank(T) = A_{T_2}$, then $q_{T_2}$ splits of a summand of the form $\mfu_+^{(2)}(2)$ or $\mfv_+^{(2)}(2)$.

Then $\cl(T) = 1$ and $\Orth_*(A_L) = 0$.

:::

:::{.theorem title="{\cite[Cor. 1.12.3, Thm 1.14.4]{Nik79}}"}
\label[theorem]{thm:nikulin_primitive_embedding_unimodular_unique}
Let $\iota: S\injects L$ be an embedding of an even lattice into a unimodular lattice and let $T\da S^{\perp L}$.
Then $\iota$ is primitive if 

1. $\tau(L) \equiv 0 \pmod 8$,
2. $\signature(L) \geq \signature(S)$, and
3. $\rank(T) \geq \ell(A_S) + 1$.

If additionally

1. $\signature(L) > \signature(S)$,
2. $\rank(T) > \ell(A_{S_p}) + 1$ for all $p\neq 2$, and
3. If $\rank(T) = \ell(A_{S_2})$, then $A_S$ splits off a factor of the form $\mfu_+^{(2)}(2)$ or $\mfv_+^{(2)}(2)$,

then $\iota$ is unique up to $\Orth(L)$.
:::

:::{.corollary}
Let $\iota: S\injects L$ be a primitive embedding of an even lattice into an even unimodular lattice where $T \da S^{\perp L} \contains U$.
Then $\iota$ is unique up to $\Orth(L)$.
:::

:::{.proof}
There is a decomposition $T = U \oplus U^{\perp T}$ where $U^{\perp T} \subseteq T^{\perp L} = (S^{\perp L})^{\perp L} = S$, and there are isometries
\[
A_S(-1) \iso A_T \iso A_{U^{\perp T}}
\]
since $U$ is unimodular.
We then have
\[
\ell(S) = \ell(T) = \ell(U^{\perp T}) \leq \rank_\ZZ(U^{\perp T}) = \rank_\ZZ(T) - 2 
,\]
and thus $\ell(S) + 2 \leq \rank(T)$.
:::

:::{.theorem title="{\cite[Thm. 1.1.2]{nikulin1979integer-symmetric}, \cite{james1966on-witts-theorem}}"}
Let $S$ be a lattice of rank $n$ and let $L$ be an even unimodular lattice of signature $(p, q)$.
If $n \leq \min(p, q)$, then there exists a primitive embedding $\iota: S\injects L$.
If the inequality is strict, it is unique up to $\Orth(L)$.
:::

:::{.theorem title="{\cite[1.15.1]{nikulin1979integer-symmetric}}"}
Let $S$ be an even lattice with $\signature(S) = (p, q)$ and let $(\tilde p, \tilde q, A_L)$ be the invariants of some genus $\gen(L)$ of even lattices.

A primitive embedding in $\Emb(S, L)$ into some $L\in \gen(L)$ is determined by a tuple $(H_S, H_Q, \gamma, T, \gamma_K)$ where

1. $H_S, H_Q \leq A_S$ are subgroups,
2. $\gamma: H_S \iso H \leq A_L$ is an isometry of subgroups,
3. $T$ is an even lattice with $\signature(T) = (\tilde p, \tilde q) - (p, q)$ and $A_T = -\delta$ where $\delta = (A_S \oplus \Gamma_\gamma^\perp)/\Gamma_\gamma$ where $\Gamma_\gamma$ is the pushout of $\gamma$ in $A_S \oplus A_L$, and
4. $\gamma_T: A_T \iso (-\delta)$ is an isometry.
:::

:::{.remark}
This can be used to compute primitive embeddings $S\injects L$ along with $T = S^{\perp L}$.
:::

:::{.theorem title="{\cite[Thm. 2.9]{BHPV04}}"}
Let $S$ be an even lattice and let $L$ be an even unimodular lattice containing $U^{\oplus m}$ as a sublattice.
If $\rank S \leq m$ then there exists a primitive embedding $\iota: S\injects L$,
If the inequality is strict, then $\iota$ is unique up to $\Orth(L)$.
:::

:::{.theorem}
See \cite[2.2.4]{Sca87}, originally due to James.

Let $S$ be an even lattice and $L$ an even unimodular lattice.
If $\rank(S) \leq \Index(L)$, then there is a primitive embedding $S\injects L$ which is unique up to $\Orth(L)$.
:::


### K3 Embeddings

:::{.proposition title="Embeddings of hyperbolic lattices into the K3 lattice"}
Let $S$ be an even hyperbolic lattice.
If

1. $\rank_\ZZ(S) \leq 20$, and
2. $\ell(A_S) \leq 20-\rank_\ZZ(S)$,

Then there exists an embedding $\iota: S\injects \lkt$ which is unique up to $\Orth(\lkt)$.
:::

:::{.proof}
This follows from \cite[Cor. 1.13.3]{nikulin1979integer-symmetric}.
:::

:::{.corollary}
If $S$ is any even hyperbolic lattice with $\rank S \leq 9$, 
then $S$ embeds uniquely into $\lkt$, up to $\Orth(\lkt)$.
:::

### Embedding direct sums

:::{.proposition}
Let $L$ be a unimodular lattice.
If $\iota: S\injects L$ is a primitive embedding and $L = \gens{e_1,\cdots, e_n}_\ZZ$ is a basis for $L$ such that $S = \gens{e_1,\cdots, e_k}_\ZZ$, then there is a basis for $S^{\perp L}$ given by $T \da \gens{e_{k+1}\dual, \cdots, e_n\dual}_\ZZ$.
Moreover, if $v\in L$ is primitive, then there exists a $w\in L$ such that $\beta(v, w) = 1$.
:::

:::{.proof}
We have $T \da \gens{e_{k+1}\dual, \cdots, e_n\dual}_\ZZ \subseteq S^{\perp}$ since $\beta(e_i, e_j\dual) = \delta_{ij}$. To see that $S^{\perp L} \subseteq T$, let $v\in S^{\perp L} \subseteq L$.
Then $\beta(v, s) = 0$ for any $s\in S = \gens{e_1,\cdots, e_k}_\ZZ$, and thus $v\in \gens{e_1,\cdots, e_k}_\ZZ^{\perp L} = \gens{e_{k+1}\dual, \cdots, e_n\dual} = T$.

For the latter statement, let $\gens{v}_\ZZ \injects L$ be a primitive embedding and extend $v$ to an $R$-basis of $L$, say $\ts{v, e_2, \cdots, e_n}$.
Then take $w\da v\dual$.
:::

:::{.remark}
Let $S\injects L$ be a primitive embedding of a lattice into a unimodular lattice, and let $T\da S^{\perp L}$.
Then $L$ is an overlattice of $S \oplus T$ with associated isotropic subgroup $H_L \da L/(S \oplus T) \subset A_S \oplus A_T$.
Since $S \injects L$ is primitive and $L$ is unimodular, there is an isomorphism $(A_S, q_S) \iso (A_T, -q_S)$.
The converse similarly holds, and thus we have:
:::

:::{.theorem}
If $L$ is a unimodular lattice and $S$ is a nondegenerate primitive sublattice with orthogonal complement $T = S^{\perp L}$, there is an isometry $A_S \iso A_T(-1)$.
:::

:::{.proof}
See \cite[Lem. 2.5]{BHPV04}.
:::

:::{.proposition}
Let $L$ be a unimodular lattice and $\iota: S \injects L$ be a primitively embedded sublattice.
Then $\abs{\disc(S)} = \abs{\disc(T)}$, and if $S$ is unimodular, then $L \cong S \oplus T$.
:::

:::{.proof}
We have
\[
\abs{\disc(S)} = \size A_S = \size A_T = \abs{\disc(T)}
.\]
The isometry follows from \Cref{prop:disc_of_full_rank_sublattice}: since $S \oplus T \leq L$ is a full-rank sublattice, $T$ is also unimodular and thus
\[
[L: S \oplus T]^2 = {\disc(S \oplus T) \over \disc(L)} = {\disc(S) \cdot \disc(T) \over \disc(L)} = 1
.\]

:::

:::{.lemma}
If $L$ is even and unimodular and $v^2\neq 0$, then
\[
\ts{f\in \Orth(v^\perp) \st \ro{f}{A_{v^\perp}} = \id} 
= \ts{\ro{f}{v^\perp} \st f\in \Orth(L), f(v) = v} \subseteq \Orth(v^\perp)
.\]

:::

## Splitting Theorems

:::{.lemma}
Let $U$ be the hyperbolic lattice.
Then $\disc(U) = 1, \signature(U) = (1,1)$, and for any primitive embedding $U \injects L$ there is a decomposition $L \cong U \oplus U^{\perp}$ given by the isometry
\begin{align*}
U &\injects U \oplus U^{\perp} \cong L \\
x &\mapsto \beta(e, x)f + \beta(f, x)e + x', \qquad x' \da x-\beta(e,x)f -\beta(f,x)e,
\end{align*}
and one can verify that $x'\in U^{\perp L}$.
Moreover, this also holds with $U$ replaced by $U^{\oplus n}$ for any $n\geq 1$.
:::

:::{.remark}
In fact, the above statement holds with $U$ replaced by any unimodular lattice. (TODO: record proof)
A useful trick: if $v$ is isotropic and $vw = 1$, then $\tilde w \da w - {1\over 2}q(w)x$ is isotropic and $v,\tilde w$ span a copy of $U$.
One can also then represent any $n\in \ZZ$, since $q({1\over 2}n v + \tilde w) = n$.
:::


<!--:::{.corollary}-->
<!--Let $L$ be an even unimodular lattice and let $v\in L[0]$ be a nonzero isotropic vector.-->
<!--Then $L\iso U \oplus U^{\perp L}$ where $v\mapsto e$.-->
<!--:::-->

<!--:::{.proof}-->
<!--Let $\signature L = (p, q)$ and suppose $p, q \geq 2$.-->
<!--By the theorem, there is a primitive embedding $U \injects L$, and thus $L \iso U \oplus U^{\perp}$.-->
<!--By the previous lemma, $\Orth(L) \actson I_1(L)$ transitively, so there is an isometry $\psi \in \Orth(L)$ with $\psi(v) = e$.-->

<!--If $p,q\geq 1$, since $L$ is unimodular, pick $w\in L$ such that $\beta(v, w) = 1$.-->
<!--Set $\tilde w \da w - {\beta(w,w)\over 2}v$, then $\beta(v, \tilde w) = 1$ and $\beta(\tilde w, \tilde w) = 0$.-->
<!--Then define the isometry-->
<!--\begin{align*}-->
<!--\gens{v, \tilde w} &\iso U \\-->
<!--v &\mapsto e \\-->
<!--\tilde w &\mapsto f-->
<!--\end{align*}-->
<!--producing a primitively embedded copy of $U \injects L$.-->
<!--One thus similarly has $L \iso U \oplus U^{\perp L}$, and $v\mapsto e$ by the above assignment.-->
<!--:::-->

:::{.lemma}
If $L$ contains an isotropic element $v$, then $v$ can be completed to a copy of $U$ with $L = U \oplus M$ for some $M$ if and only if $\div_L(v) = 1$.
:::

## Lifting Problems

### Lifting from embedded sublattices

:::{.theorem title="{\cite[Cor. 1.5.2]{nikulin1979integer-symmetric}}"}
Let $S_1, S_2 \injects L$ be primitive embeddings with orthogonal complements $T_1, T_2$ and let $\phi: S_1\iso S_2$ be an isometry.
Then $\phi$ extends to an isometry $\hat \phi\in \Orth(L)$ if and only if there exists an isometry $\psi: T_1\iso T_2$ such that the following diagram commutes:

\[\begin{tikzcd}
	{A_{S_1}} && {A_{S_2}} \\
	\\
	{A_{T_1}} && {A_{T_2}}
	\arrow["{\bar \phi}", from=1-1, to=1-3]
	\arrow["{\gamma^L_{S_1, T_1}}"', from=1-1, to=3-1]
	\arrow["{\gamma^L_{S_2, T_2}}", from=1-3, to=3-3]
	\arrow["{\bar \psi}", from=3-1, to=3-3]
\end{tikzcd}\]
:::

:::{.corollary}
\label[corollary]{cor:nikulin_extend_isometries_perp}
Let $S_1 = S_2 = S \injects L$ a single primitive sublattice in the previous corollary and $\phi \in \Orth(S)$, and let $T_1 = T_2 = T \da S^{\perp L}$.
Then $\phi$ extends to an isometry $\hat \phi\in \Orth(L)$ if and only if there exists some $\psi\in \Orth(T)$ such that
\[
\ro{\psi}{A_T} \circ \gamma^L_{S, T} = \gamma^L_{S, T} \circ \ro{\phi}{A_S}
,\]
so the following diagram commutes:

\[\begin{tikzcd}
	{A_S} && {A_S} \\
	\\
	{A_T} && {A_T}
	\arrow["{\ro{\phi}{A_S}}", from=1-1, to=1-3]
	\arrow["{\gamma^L_{S, T}}"', from=1-1, to=3-1]
	\arrow["{\gamma^L_{S, T}}", from=1-3, to=3-3]
	\arrow["{\ro{\psi}{A_T}}", from=3-1, to=3-3]
\end{tikzcd}\]


In particular, if $\gamma^L_{S, T}: A_S \iso A_T$ is an isomorphism, this says that the restrictions of $\phi$ and $\psi$ to $A_S$ and $A_T$ coincide under the identification $A_S \cong A_T$.

In other words, there is a surjection
\[
\Orth(L) \surjects \ts{f\in \Orth(S) \oplus \Orth(T) \st \ro{f}{A_S} = \ro{f}{A_T}}
.\]
:::

:::{.theorem}
Let $S \injects L$ be a primitive embedding of even lattices where $L$ is unimodular and write $T\da S^{\perp L}$.
Then there is a morphism
\begin{align*}
\Orth(L, T) \da \ts{f\in \Orth(L) \st \ro{f}{T} = \id } &\to \Orth(S) \\
f &\mapsto \ro{f}{S}
\end{align*}
which induces an isomorphism
\[
\Orth(L, T) \iso \Orth*(S)
.\]
In other words, any isometry of $L$ which induces the identity on $T$ necessarily acts on $A_S$ and $A_T$ trivially.
:::

:::{.proof}
To see that $\Orth(L, T) \subseteq \Orth^*(S)$, let $f\in \Orth(L)$ with $\ro{f}{T} = \id_T$.
Since $T = S^{\perp}$, we have $A_S = A_T(-1)$, and thus
\[
\ro{f}{A_S} = \ro{f}{A_S(-1)} = \ro{f}{A_T} = \ro{( \ro{f}{T})}{A_T} = \ro{\id_T}{A_T} = \id_{A_T} = \id_{A_S}
,\]
so $\ro{f}{S}$ acts trivially on $A_S$ and thus $\ro{f}{S} \in \Orth^*(S)$.

Conversely, if $f\in \Orth(S)$ satisfies $\ro{f}{A_S} = \id_{A_S}$, define the isometry $F = f \oplus \id_T \in \Orth(S \oplus T)$.
Since $\ro{F}{A_T} = \id_{A_T}$, by \Cref{cor:nikulin_extend_isometries_perp} there is a lift $\tilde F\in \Orth(L)$, and since $\ro{F}{T} = \id_T$, we in fact have $F\in \Orth(L, T)$.

In this notation, the bijection is thus given by
\begin{align*}
\Orth(L, T) &\iso \Orth^*(S) \\
f &\mapsto \ro{f}{S} \\
F &\mapsfrom f
\end{align*}
:::

:::{.proposition title="Lifting isometries stabilizing an embedding"}
Let $S \injects L$ be a primitive sublattice of an even unimodular lattice, and define
\[
\Orth(L, S) \da \Stab_{\Orth(L)}(S) = \ts{f\in \Orth(L) \st f(S) = S}
.\]
Then
\[
\Orth(T) \surjects \Orth(A_T) \implies \Orth(L, S)\surjects \Orth(S)
,\]
so if $\Orth_*(A_T) = 0$, any isometry of $S$ can be extended to an isometry of $L$ stabilizing $S$.
:::

:::{.proof}
Let $f\in \Orth(S)$, and let $\phi_L: A_S \iso A_T(-1)$ be the glue map associated to the primitive embedding $S\injects L$.
Since $\Orth(T) \surjects \Orth(A_T)$, let 
\[
\tilde g \da \phi_L \circ \ro{f}{A_S} \circ \phi_L\inv \in \Orth(A_T)
.\]
Then $\tilde g = \ro{g}{A_T}$ for some $g\in \Orth(T)$, and
\[
\tilde g \circ \phi_L = 
(\phi_L \circ \ro{f}{A_S} \circ \phi_L\inv) \circ \phi_L
= \phi_L \circ \ro{f}{A_S}
.\]
Thus the isometry $F \da f \oplus t\in \Orth(S) \oplus \Orth(T)$ extends to some $\tilde F\in \Orth(L)$.
:::

:::{.corollary}
Let $S\injects L$ be a primitive embedding into a unimodular lattice and let $f\in \Orth(S)$.
If $f$ lifts to an element of $\ts{F\in \Orth(L) \st \ro{F}{T} = \pm \id}$, then this extension is unique.
Such an extension exists if and only if $f$ induces $\pm \id$ on $A_S$. 
:::

### Lifting from discriminant groups

:::{.theorem title="{\cite[Thm. 1.14.2]{nikulin1979integer-symmetric}}"}
Let $S$ be an even indefinite lattice with $\ell(S) + 2\leq \rank_\ZZ(S)$.
Then $\Orth_*(A_S) = 0$, so $\Orth(S) \surjects \Orth(A_S)$.
:::

:::{.theorem title="{\cite[Prop. 9.2]{hassettInvolutionsK3Surfaces2024}}"}
Let $L$ be an even hyperbolic lattice admitting a primitive embedding $E_8(2) \injects L$.
If $\ell(L) \leq 11$, then $\cl(L) = 1$ and $\Orth_*(L) = 0$.
:::

## Group actions

:::{.lemma title="{\cite[Lem. 3.2]{grossiSymplecticBirationalTransformations2023}}"}
If $G \leq \Orth(L)$ is of order 2 which induces an order 2 isometry on $A_L$, then $\abs{\disc(L_G)} = \abs{\disc(L^G)}$.
:::

### Orbits

:::{.definition title="Set of primitive vectors of a fixed square"}
For a nondegenerate lattice $L$, define
\[
L[k] \da \ts{v\in L \st v^2 = k,\,\, v\text{ is primitive}}
.\]
:::

:::{.theorem title="Finiteness of orbits of vectors, {\cite[Thm. 3.6]{kamenovaFamiliesLagrangianFibrations2012}}"}
Let $L$ be a lattice with $\rank(L) \geq 7$.
Then $L[0]/\Orth(L)$ is finite.
:::

:::{.proof}
We sketch the proof given in \cite[Thm. 3.6]{kamenovaFamiliesLagrangianFibrations2012}.

Let $d \da \abs{\disc(L)}$.
Let $v\in L$ be primitive with $v^2 = 0$.
Choose $w\in L$ such that $\alpha \da vw$ is minimal.
Then $\alpha$ divides $d$.
Let $K \da \gens{v, w}_\ZZ \leq L$, then $\disc(K) = v^2 w^2 - (vw)^2 = -\alpha^2$, which is bounded since $-d^2 \leq -\alpha^2 \leq 0$.
We have $\size K[0] \leq 2\rank(K) = 4$.
There are only finitely many ways of expressing $L$ as an overlattice of $K \oplus K^{\perp L}$, since these correspond to isotropic subgroups in $A_L$, which has size at most $d$.

Toward a contradiction, if $L[0]/\Orth(L)$ is infinite, then there are infinitely many non-isomorphic pairs $(K, K^{\perp L})$.
However, for infinitely many such pairs, we would have $\Cl^{\stab}(K) = \Cl^\stab(K_1^{\perp L})$ for some $K_1$, since there are only finitely many choices for $K$.
This contradicts the finiteness of $\Cl^\stab(K)$.
:::

:::{.theorem title="{\cite[Satz 30.2]{kneserQuadratischeFormen2002a}}"}
\label[theorem]{thm:finiteness_of_embeddings}
Let $S$ be a nondegenerate lattice.
Then given any $n,d\neq 0$, there are only finitely many isometry classes of primitive embeddings $u: S\injects L$ where $L$ is of rank $n$ and discriminant $d$.
:::

:::{.corollary}
If $L$ is any nondegenerate lattice, then $L[k]/\Orth(L)$ is finite for any $k \in \ZZ$.
:::

:::{.proof}
Given $v_i \in L[k]$, let $S_i \da \gens{v_i}_\ZZ$.
This yields an embedding $u_i: S_i \injects L$, of which there are finitely many up to $\Orth(L)$ by \Cref{thm:finiteness_of_embeddings}.
:::

:::{.lemma}
Let $L$ be an even unimodular lattice.
If $\signature(L) \geq (1, 1)$, then for any $d$, $L[d]\neq 0$, i.e. there exists a primitive element of square $2d$.
If$\signature(L) \geq (2,2)$, then $\Orth(L)$ acts transitively on $L[d]$ for each $d$, and thus $L[d]/\Orth(L)$ is a single orbit.
:::

:::{.proof}
This is equivalent to the existence of a primitive embedding $\gens{2d}\injects L$, which exists by \Cref{thm:nikulin_primitive_embedding_unimodular_unique}.
:::

:::{.theorem title="{\cite[Prop. 3.3]{gritsenkoAbelianisationOrthogonalGroups2008}}"}
Let $L = U \oplus U_1 \oplus M \da U \oplus L_1$.
Define
\[
E(L) \da \ts{ E_{e, a} \st e,a\in L, e^2 = ea = 0, \div_L(e) = 0}, \quad E_U(L_1) \da \gens{E_{e, a}, E_{f, a} \st a\in L_1}
.\]

If $u,v\in L$ are primitive with

- $u^2 = v^2 = p$,
- $[u^*] = [v^*] \in A_L$,

then there exists a transvection $\tau\in E_U(L_1)$ with $\tau(u) = v$.

Moreover, $E(L) = E_U(L_1)$.
:::

:::{.remark}
This may be Eichler's criterion, see \cite{eichlerQuadratischeFormenUnd1974}.
:::

:::{.proof}
We just prove the first assertion.
Let $u,v\in L$ with $u^2=v^2=p$, and choose $u', v'\in L_1$ such that $uu' = vv' = d$.
We can find $\tau\in E_{U_1}(U_2)$ such that $\tau(u)\in L_1$, so we can assume $u,v\in L_1$.
We then take the composition of Eichler transformations
\[
u \mapsvia{E_{e, u'}} u-de \mapsvia{E_{f, w}} vide \mapsvia{E_{e, -v'}} v
,\]
which is a translation by $w\da (u-v)/d$ in $U_1^{\perp L_1}$.

:::

## Characteristic Elements

:::{.definition title="Characteristic elements"}
Let $L$ be an integral lattice.
An element $c\in L$ is **characteristic** if $\beta(c,x) = \beta(x,x) \pmod{2\ZZ}$ for every $x\in L$.
A **characteristic covector** is an element $\xi\in L\dual$ such that $\beta(\xi, x) = \beta(x,x) \pmod{2\ZZ}$ for all $x\in L$.
We define the set
\[
\chi\dual(L) \da \ts{f\in L\dual \st f(v) = \beta(v,v) \, \forall v\in L}
.\]
Every lattice with odd discriminant contains a characteristic element, and the **$\sigma$-invariant** of $L$ is defined as 
\[
\sigma(L) = \beta(c, c) \pmod{8\ZZ}
.\]
It is an additive invariant.
:::

:::{.example}
Let $X$ be a smooth compact real 4-manifold with intersection form $(L, \beta)$ on $H^2(X; \ZZ)$.
Then the second Stiefel-Whitney class $w_2(X) \in H^2(X; \FF_2)$ is characteristic for $L_{\FF_2}$, so
\[
\beta(v,v) = \beta(w_2(X), v) \qquad \forall v\in L_{\FF_2}
.\]

If $X$ is a smooth complex surface, the first Chern class $c_1(X)$ is characteristic for $L$ itself.
:::

:::{.lemma title="{\cite[Lem. 2.1]{petersNotePrimitiveCohomology2023}}"}
If $L$ is a lattice with odd discriminant and $h\in L$ is nonisotropic, then $h^{\perp L}$ is an even lattice if and only if $h$ is a characteristic element.
:::



### ?


:::{.remark}
Over $R = \ZZ$, let $X_n$ denote the space of rank $n$ unimodular lattices.
There is a moduli space of such lattices given by
\[
X_n \iso \dcosetl{\SL_n(\ZZ)}{\SL_n(\RR)}
.\]
:::
