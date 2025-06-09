






















# Lattice Theory

::: remark
Throughout this section, \( R \) is an integral domain which we often take to be \( {\mathbf{Z}} \). We write \( k \) for its field of fractions, often taken to be \( {\mathbf{Q}} \). We write the group of units as \( R^{\times} \), and \( L, M \) are generally finitely generated projective \( R \)-modules. Over \( R={\mathbf{Z}} \), these will be regarded as free modules of finite \( {\mathbf{Z}} \)-rank. We write \( { {\mathbf{Z}}_{\widehat{p}} } \) for the ring of \( p \)-adic integers, and \( { {\mathbf{Q}}_{\widehat{p}} } \) for its field of fractions We write \( \beta \) for a general symmetric bilinear form. If \( S \) is an \( {\mathbf{Z}} \)-module, we write \( L_S \coloneqq L \otimes_{\mathbf{Z}}S \) for the base change of \( L \) to an \( S \)-module. In particular, if \( L \) is a \( {\mathbf{Z}} \)-module, there are naturally defined extensions \( L_{\mathbf{Q}}, L_{\mathbf{R}}, L_{\mathbf{C}} \), as well as \( L_{{ {\mathbf{Z}}_{\widehat{p}} }} \) for any prime \( p \). We write \( { \mathbf{F} }_p \) for the finite field with \( p \) elements, and \( C_n \) for the cyclic group of order \( n \).
:::

## Bilinear/Quadratic Modules and Lattices

From here onward, \( L \) will be a free \( {\mathbf{Z}} \)-module of finite rank \( n \).

::: {.definition title="Bilinear modules/forms"}
Let \( L \) be a \( {\mathbf{Z}} \)-module. A **bilinear form** \( \beta \) on \( L \) is a morphism `\begin{align*}
\beta \in { \operatorname{Hom} }_{\mathbf{Z}}( L \otimes_{\mathbf{Z}}L, &{\mathbf{Z}}) \\
v\otimes w &\mapsto \beta(v, w)
,\end{align*}`{=tex} which can be regard as an element of \( \operatorname{Sym}^2_{\mathbf{Z}}(L {}^{ \vee }) \). We often omit \( \beta \) from the notation and simply write \( vw \) or \( v\cdot w \) for \( \beta(v, w) \). We refer to a general pair \( (L, \beta) \) as a **bilinear \( {\mathbf{Z}} \)-module**. We write \( T^2_{\mathbf{Z}}(L {}^{ \vee }) \) or simply \( \operatorname{Bil}_{\mathbf{Z}}(L) \) for the set of bilinear forms on a fixed module \( L \).

More generally, we may allow bilinear forms to be \( {\mathbf{Q}} \)-valued, in which case we say \( \beta \) is **integral** if its image \( \beta(L, L) \) is contained in \( {\mathbf{Z}} \).
:::

::: {.definition title="Symmetric/skew-symmetric bilinear forms"}
A bilinear form \( \beta: L\otimes_{\mathbf{Z}}L\to {\mathbf{Q}} \) is **\( {\varepsilon} \)-symmetric** for \( {\varepsilon}\in {\mathbf{Q}} \) if
\[
\beta(a, b) = {\varepsilon}. \beta(b, a)
.\]

-   If \( {\varepsilon}= 1 \), we say \( \beta \) is **symmetric**.
-   If \( {\varepsilon}= -1 \) we say \( \beta \) is **skew-symmetric**.
-   \( \beta \) is **alternating** if \( \beta(a,a) = 0 \) for all \( a\in L \).
:::

::: remark
Note that any bilinear form \( \omega \) gives rise to a symmetric form defined by \( \beta \coloneqq{1\over 2}(\omega^t + \omega) \), where \( \omega^t(a,b) \coloneqq\omega(b,a) \). If \( \omega \) is skew-symmetric, then the associated symmetric form is zero.
:::

::: {.definition title="Quadratic modules/forms"}
A **quadratic form** on \( L \) is a morphism of sets \( q: L\to S \) such that

-   \( q(\lambda . v) = \lambda^2 .q(v)\in {\mathbf{Q}} \) for all \( v\in L \) and all \( \lambda \in {\mathbf{Q}} \), and
-   Its **polar form** `\begin{align*}
    \beta_q: L \otimes_{\mathbf{Z}}L &\to {\mathbf{Q}}\\
    (v, w) &\mapsto \beta_q(v,w)\coloneqq q(v + w) - q(v) - q(w)
    \end{align*}`{=tex} is a symmetric bilinear form on \( L \).

We similarly say \( q \) is **integral** if \( q(L) \subseteq {\mathbf{Z}} \), and refer to the pair \( (L, q) \) as a **quadratic \( {\mathbf{Z}} \)-module**. We write \(  \mathrm{Quad}_{\mathbf{Z}}(L) \) or simply \(  \mathrm{Quad}_{\mathbf{Z}}(L) \) for the set of all quadratic forms on a fixed module \( L \).
:::

::: {.definition title="Lattices"}
A **lattice** is a pair \( (L, \beta) \) where \( L \) is a free \( {\mathbf{Z}} \)-module of finite rank and \( \beta \) is a (possibly \( {\mathbf{Q}} \)-valued) nondegenerate symmetric bilinear form. We often require \( \beta \) to be integral, but occasionally also refer to modules with \( {\mathbf{Q}} \)-valued forms as lattices by abuse of language.

Similarly, we refer to a pair \( (L, q) \) as a **quadratic lattice** if \( q \) is a nondegenerate quadratic form, again possibly \( {\mathbf{Q}} \)-valued, which is often required to be integral.
:::

::: {.definition title="Even/odd lattices"}
If \( (L,\beta) \) is a lattice, we say \( L \) is **even** if \( \beta(v,v) \in 2{\mathbf{Z}} \) for all \( v\in L \), and is **odd** otherwise.
:::

::: {.lemma title="Correspondence between bilinear and quadratic forms"}
Every \( {\mathbf{Q}} \)-valued bilinear module \( (L, \beta) \) (not necessarily symmetric) determines a \( {\mathbf{Q}} \)-valued quadratic module \( (L, q_\beta) \) `\begin{align*}
q_\beta: L &\to {\mathbf{Q}}\\
v &\mapsto q_\beta(v) \coloneqq\beta(v,v)
,\end{align*}`{=tex} which only depends on the symmetric part of \( \beta \), given by \( {1\over 2}(\beta^t + \beta) \). Conversely, every \( {\mathbf{Q}} \)-valued quadratic module \( (L, q) \) determines a *symmetric* module \( (L, \beta_q) \) where `\begin{align*}
\beta_q: L\otimes_{\mathbf{Z}}L &\to {\mathbf{Q}}\\
v \otimes w &\mapsto \beta_q(v) \coloneqq q(v + w) - q(v) - q(w)
\end{align*}`{=tex} is the polar form of \( q \). Thus there are maps `\begin{align*}
T^2_{\mathbf{Z}}(L {}^{ \vee }) &\to  \mathrm{Quad}_{\mathbf{Z}}(L)   \to \operatorname{Sym}^2_{\mathbf{Z}}(L) \\
\beta   &\mapsto q_\beta             \\
        &\qquad\qquad\qquad\qquad      q        \mapsto \beta_q
.\end{align*}`{=tex} Moreover, by ???, the map \( \beta\mapsto q_\beta \) is surjective, i.e. every \( {\mathbf{Z}} \)-valued quadratic form \( q \) can be written as the quadratic form \( \beta(v,v) \) associated to a bilinear form \( \beta \). However, note that the lift of \( q \) to \( \beta \) need not be unique.
:::

::: lemma
There is a bijection `\begin{align*}
\left\{{\beta\in \operatorname{Sym}^2_{\mathbf{Z}}(L {}^{ \vee }) {~\mathrel{\Big\vert}~}\beta \text{ is even}}\right\} &\rightleftharpoons \mathrm{Quad}_{\mathbf{Z}}(L) \\
\beta &\mapsto {1\over 2}q_\beta \\
\beta_q &\mapsfrom q
\end{align*}`{=tex} In other words, the polar form of every integral symmetric form is even, and every *even* symmetric integral form \( \beta \) is the polar form of an integral quadratic form, namely \( q(v) \coloneqq{1\over 2}\beta(v,v) \). Moreover, if \( q \) is any quadratic form, then \( {1\over 2}\beta_q \) recovers \( q \).
:::

::: proof
Note that for any integral \( q \), the polar form is always even:
\[
\beta_q(v,v) \coloneqq q(v+v) - q(v) - q(v) = 4q(v)-2q(v) = 2q(v) \in 2{\mathbf{Z}}
.\]
Moreover, if \( \beta \) is even, then \( {1\over 2}q_\beta \) is integral, so both maps are well-defined.

We first consider the composite \( \beta \mapsto {1\over 2}q_\beta \mapsto \beta_{{1\over 2} q_\beta} \): `\begin{align*}
\beta_{{1\over 2}q_\beta}(v, w)
&\coloneqq{1\over 2}q_{\beta}(v+w) - {1\over 2}q_{\beta}(v) - {1\over 2}q_{\beta}(w) \\
&= {1\over 2} \qty{\beta(v,v) + \beta(v,w) + \beta(w, v) + \beta(w,w) - \beta(v,v) - \beta(w,w)} \\
&= {1\over 2}\qty{\beta(v,w) + \beta(w, v) } \\
&= \beta(v, w)
\end{align*}`{=tex} We then consider the composite \( q\mapsto \beta_{q} \mapsto {1\over 2}q_{\beta_q} \); `\begin{align*}
{1\over 2}q_{\beta_q}(v)
&\coloneqq{1\over 2}\beta_q(v,v) \\
&\coloneqq{1\over 2}\qty{ q(v + v) - q(v) - q(v) } \\
&= {1\over 2}\qty{ q(2v) - 2q(v) } \\
&= {1\over 2}\qty{ 4q(v) - 2q(v) } \\
&= {1\over 2}\qty{ 2q(v)} \\
&= q(v)
\end{align*}`{=tex} Thus these maps are mutually inverse.
:::

::: remark
It is worth noting that some sources instead use the correspondence \( \beta \mapsto q_\beta \) and \( q\mapsto {1\over 2}\beta_q \). Over \( {\mathbf{Q}} \), this is an equivalent formulation since \( 2 \) is invertible, but over \( {\mathbf{Z}} \) one loses the bijection with even lattices by using this convention.
:::

::: {.definition title="Gram matrices"}
Let \( (L, \beta) \) be a bilinear module. Choosing a basis \( B_L = (e_i)_{1\leq i\leq n} \), for any \( v,w\in L \) one can write \( v = \sum_j a_j e_j \) and \( w= \sum_j b_j e_j \) for some coefficients \( a_j, b_j \in {\mathbf{Z}} \). Using bilinearity, one can then write
\[
\beta(v, w) 
= \beta\qty{ \sum_j a_j e_j, \sum_j b_j e_j} 
= \sum_{i, j} a_i b_j \cdot \beta(e_i, e_j) 
\coloneqq v^t G_\beta w
\]
for some (not necessarily unique) matrix \( G_\beta \coloneqq(\beta(e_i, e_j))_{i,j} \in \operatorname{Mat}_{n\times n}({\mathbf{Q}}) \), which we refer to as the **Gram matrix of \( \beta \)**.

Similarly, if \( (L, q) \) is a quadratic module, one can write
\[
q(v) = q\qty{ \sum_j a_j e_j} = \sum_{i, j} a_i a_j \cdot (G_q)_{i, j} = v^t G_q v
\]
for some (not necessarily unique) matrix \( G_q \in \operatorname{Mat}_{n\times n}({\mathbf{Q}}) \), which we similarly refer to as the **Gram matrix of \( q \)**.
:::

::: remark
If \( (L, \beta) \) is a bilinear module, then

-   \( \beta \) is symmetric if \( G_\beta^t = G_\beta \),
-   \( \beta \) is skew-symmetric if \( G_\beta^t = -G_\beta \), and
-   \( \beta \) is alternating if \( \operatorname{diag}(G_\beta) = (0, 0,\cdots, 0) \) and \( G_\beta^t = -G_\beta \).

Moreover, if \( (L, \beta) \) is a lattice, it is even if and only if \( G_\beta\in \operatorname{Mat}_{n\times n}({\mathbf{Z}}) \) and \( \operatorname{diag}(G_\beta)\in (2{\mathbf{Z}})^n \).
:::

::: remark
Note that if \( (L, \beta) \) is a lattice with associated quadratic lattice \( (L, \beta_q) \), the Gram matrix \( G_{\beta_q} \) can be taken to be \( G_{\beta} \). This is because if \( \beta(v, w) = v^t G_\beta w \), then \( q_\beta(v) = \beta(v,v) = v^t G_\beta v \).

One can show that one possible Gram matrix of a quadratic form \( q \) is proportional to the Hessian of \( q(x) \) regarded as a polynomial function \( {\mathbf{Q}}^n\to {\mathbf{Q}} \), namely
\[
G_{H, q} = {1\over 2} H(q(x)), \qquad H(q(x))_{i,j} \coloneqq\qty{ {\partial^2 q \over \partial x_i \partial x_j} }
,\]
which is generally non-integral. Alternatively, one can take a write a matrix \( G_q \) in terms of \( q \) and its polar form \( \beta_q \) as
\[
G_{q} = \left(\begin{array}{cccc}
q(e_1) & \beta_q(e_1, e_2) & \cdots & \beta_q(e_1, e_n) \\ 
0 & q(e_2) & \cdots & \beta_q(e_2, e_n) \\ 
\vdots & \ddots & \ddots & \vdots \\ 
0 & \cdots & 0 & q(e_n) \end{array}\right), \qquad
a_{ij} \coloneqq\beta_q(e_i, e_j), \qquad i < j
,\]
which is integral whenever \( q \) is integral. One can then recover the Gram matrix for the polar form of \( q \) as \( G_{\beta_q} = G_q + G_q^t \).

These two choices of Gram matrices are related by \( G_{q, H} = {1\over 2}(G_{q} + G_{q}^t) \), and so one can be recovered from the other over \( {\mathbf{Q}} \). Over \( {\mathbf{Z}} \), we will typically make a preferred choice of \( G_q \) as the latter matrix to avoid denominators.
:::

::: example
Consider the \( {\mathbf{Z}} \)-valued quadratic form on \( {\mathbf{Z}}^3 \) defined by
\[
q(x,y,z) = ax^2 + by^2 + cz^2 + dyz + exz + fxy, \qquad a,\cdots,f\in {\mathbf{Z}}
.\]
Using the Hessian, one obtains the symmetric (but non-integral) matrix
\[
G_{g, H} \coloneqq
{1\over 2}H(q(x,y,z)) =
\begin{pmatrix}
a               & {1 \over 2}f  & {1\over 2}e \\
{1\over 2} f    & b         & {1\over 2}d \\
{1\over 2}e     & {1\over 2}d & c
\end{pmatrix}
\in \operatorname{Mat}_{3\times 3}({\mathbf{Q}})
\]
and verify that if \( v = {\left[ {x,y,z} \right]}\in {\mathbf{Z}}^3 \) then \( v^t G_{q, H} v = q(x,y,z) \). However, one can also take
\[
G_{q} = 
\begin{pmatrix}
a & f & e \\
0 & b & d \\
0 & 0 & c
\end{pmatrix}
\in \operatorname{Mat}_{3\times 3}({\mathbf{Z}})
,\]
which is now integral and similarly satisfies \( v^t G_{q} v = q(x,y,z) \). One can check directly that \( G_{q, H} = {1\over 2}(G_q + G_q^t) \). Letting \( \beta_q \) be the polar form of \( q \), either of the above matrices can be used to obtain the (integral) Gram matrix of \( \beta_q \):
\[
G_{\beta_q} = 
\begin{pmatrix}
2a & f & e \\
f & 2b & d \\
e & d & 2c
\end{pmatrix}
 = G_{q, H} + G_{q, H}^t = G_{q} + G_{q}^t \in \operatorname{Mat}_{3\times 3}({\mathbf{Z}})
.\]
:::

::: {.definition title="Orthogonal direct sums"}
Let \( (L, \beta_L) \) and \( (M, \beta_M) \) be integral lattices. We define their **orthogonal direct sum** as the lattice \( (L \oplus M, \beta_{L\oplus M}) \) where \( L\oplus M \) is their direct sum as \( {\mathbf{Z}} \)-modules, and the bilinear form is given by

`\begin{align*}
\beta_L \oplus \beta_M: (L\oplus M)\otimes_{\mathbf{Z}}(L\oplus M) &\to {\mathbf{Z}}\\
(\ell_1 + m_1, \ell_2 + m_2) &\mapsto \beta_L(\ell_1, \ell_2) + \beta_M(m_1, m_2)
.\end{align*}`{=tex} We write \( L^{\oplus n} \) for the \( n \)-fold direct sum \( \bigoplus_{i=1}^n L \).

Similarly, if \( (L, q_L) \) and \( (M, q_M) \) are integral quadratic lattices, we define their direct sum as \( (L\oplus M, q_L \oplus q_M) \) where `\begin{align*}
q_L \oplus q_M: L \oplus M &\to {\mathbf{Z}}\\
\ell + m &\mapsto q_L(\ell) + q_M(m)
\end{align*}`{=tex}
:::

::: remark
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

::: {.definition title="Indecomposable lattices"}
Let \( (L, \beta) \) be a lattice. If \( L \) can not be written as a direct sum \( L = S \oplus T \) for two primitive sublattices \( S, T\leq L \), we say \( L \) is **indecomposable**.
:::

::: remark
Note that \( L \) may be decomposable as a module but not as a lattice.
:::

> TODO: define rank and signature before these examples?

::: {.example title="Rank 1 and diagonal lattices "}
For \( a\in {\mathbf{Z}} \) we define \( \left\langle{a}\right\rangle \) to be the lattice corresponding to the bilinear form \( \beta(x, y) = axy \) for \( x,y \in {\mathbf{Z}} \), which has a \( 1\times 1 \) Gram matrix \( G_{\left\langle{a}\right\rangle} = [a] \). The corresponding quadratic form is \( q_\beta(x) = ax^2 \) for \( x\in {\mathbf{Z}} \), yielding a quadratic lattice that we write as \( \left[ {a} \right] \) which has the Gram matrix \( G_{\beta_q} = [a] \).

More generally, for \( a_1, \cdots, a_n\in {\mathbf{Z}} \), we define the "diagonal" lattice \( \left\langle{a_1, \cdots, a_n}\right\rangle \coloneqq\left\langle{a_1}\right\rangle \oplus \cdots \oplus \left\langle{a_n}\right\rangle \) which corresponds to the form
\[
\beta(x, y) = \sum_{i=1}^n a_i x_i y_i \quad (x,y\in {\mathbf{Z}}^n), \qquad
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
\quad (x\in {\mathbf{Z}}^n), \qquad
G_{q_\beta} = 
\begin{pmatrix}
a_1 &       &   & \\
    &  a_2  &   & \\
    &       & \ddots & \\
    &       &   & a_n
\end{pmatrix}
,\]
and we write this quadratic lattice as \( \left[ {a_1, \cdots, a_n} \right] \coloneqq\left[ {a_1} \right] \oplus \cdots \oplus \left[ {a_n} \right] \). We note that with our current conventions, the matrices \( G_\beta \) and \( G_{q_\beta} \) will always coincide.
:::

::: {.example title="Rank 2 bilinear and quadratic forms"}
For the following examples, let \( L = {\mathbf{Z}}^2 \) and fix a standard basis.

1.  The map `\begin{align*}
    \beta: {\mathbf{Z}}^2 \otimes_{\mathbf{Z}}{\mathbf{Z}}^2 &\to {\mathbf{Z}}\\
    \qty{ { \begin{bmatrix} {x_1} \\ {y_1} \end{bmatrix} }, { \begin{bmatrix} {x_2} \\ {y_2} \end{bmatrix} }} &\mapsto a x_1 x_2 + b y_1 y_2
    \end{align*}`{=tex} is a symmetric bilinear form with Gram matrix \( G_\beta = { \begin{bmatrix} {a} & {0}  \\ {0} & {b} \end{bmatrix} } \). It coincides with the standard dot product when \( a=b=1 \). The associated lattice \( (L, \beta) \) is decomposable and equal to \( \left\langle{a, b}\right\rangle \). The associated quadratic form is `\begin{align*}
    q_\beta: {\mathbf{Z}}^2 &\to {\mathbf{Z}}\\
    { \begin{bmatrix} {x} \\ {y} \end{bmatrix} } & \mapsto ax^2 + by^2
    \end{align*}`{=tex} with Gram matrix \( G_{q_\beta} = G_\beta \), yielding the quadratic lattice \( \left\langle{a, b}\right\rangle \).

2.  The map `\begin{align*}
    \beta: {\mathbf{Z}}^2 \otimes_{\mathbf{Z}}{\mathbf{Z}}^2 &\to {\mathbf{Z}}\\
    \qty{ { \begin{bmatrix} {x_1} \\ {y_1} \end{bmatrix} }, { \begin{bmatrix} {x_2} \\ {y_2} \end{bmatrix} }} &\mapsto x_1 y_2 - x_2 y_1
    \end{align*}`{=tex} is an alternating, skew-symmetric form with Gram matrix \( G_{\beta} = { \begin{bmatrix} {0} & {1}  \\ {-1} & {0} \end{bmatrix} } \). The associated symmetric form is defined by \( G_\beta^t + G_\beta \), which is the zero matrix, and thus the associated (symmetric) lattice and quadratic lattice are both zero.

3.  The map `\begin{align*}
    q: {\mathbf{Z}}^2 &\to {\mathbf{Z}}\\
    { \begin{bmatrix} {x} \\ {y} \end{bmatrix} } &\mapsto ax^2 + bxy + cy^2
    \end{align*}`{=tex} is a binary quadratic form with possible Gram matrices
    \[
    G_{q, H} = { \begin{bmatrix} {a} & {b\over 2}  \\ {b\over 2} & {c} \end{bmatrix} } \in \operatorname{Mat}_{2\times 2}({\mathbf{Q}}),
    \qquad
    G_{q} = { \begin{bmatrix} {a} & {b}  \\ {0} & {c} \end{bmatrix} } \in \operatorname{Mat}_{2\times 2}({\mathbf{Z}})
    .\]
    Its polar form \( \beta_q \) has Gram matrix
    \[
    G_{\beta_q} = G_q + G_q^t = { \begin{bmatrix} {2a} & {b}  \\ {b} & {2c} \end{bmatrix} }
    \]
    and represents the symmetric form `\begin{align*}
    \beta_q: {\mathbf{Z}}^2 \otimes_{\mathbf{Z}}{\mathbf{Z}}^2 &\to {\mathbf{Z}}\\
    \qty{{ \begin{bmatrix} {x_1} \\ {y_1} \end{bmatrix} }, { \begin{bmatrix} {x_2} \\ {y_2} \end{bmatrix} } } &\mapsto 2a x_1 x_2 + bx_2 y_1 + bx_1 y_2 + 2cy_1 y_2 
    \end{align*}`{=tex} The associated lattice \( (L, \beta_q) \) is rank 2 and generally indecomposable.
:::

::: {.definition title="Definite forms"}
We say a lattice \( (L, \beta) \)

-   **positive definite** if \( \beta(v, v) > 0 \),
-   **positive semidefinite** if \( \beta(v, v) \geq 0 \),
-   **negative definite** if \( \beta(v, v) < 0 \), or
-   **positive semidefinite** if \( \beta(v, v) \leq 0 \)

for all nonzero \( v\in L \). We say a lattice is **indefinite** if it is neither positive nor negative semidefinite.
:::

::: {.remark title="Criteria for definiteness"}
A symmetric matrix \( A \in \operatorname{Mat}_{n\times n}({\mathbf{Q}}) \) is positive definite if and only if any of the following equivalent conditions hold:

-   \( A \) can be diagonalized over \( {\mathbf{R}} \) where each diagonal entry is positive,
-   All eigenvalues of \( A \) are real and positive, or
-   All of the leading principal minors of \( A \) are positive.

Similar criteria can be used to check if \( A \) is positive semidefinite and negative (semi)definite. We most often apply these criteria to Gram matrices \( A \coloneqq G_\beta \) for a lattice \( (L, \beta) \) or \( A \coloneqq G_{q, H} \) for a quadratic lattice \( (L, q) \).
:::

::: {.definition title="Extensions of bilinear forms"}
Let \( (L, \beta) \) be a lattice and let \( S \) be any \( {\mathbf{Z}} \)-algebra. Then there is naturally a pair \( (L_S, \beta_S) \) where \( L_S \coloneqq L\otimes_{\mathbf{Z}}S \) is an \( S \)-module whose bilinear form \( \beta_S \) takes values in \( {\mathbf{Z}}\otimes_{\mathbf{Z}}S \cong S \). It is defined by `\begin{align*}
\beta_S: L_S \otimes_S L_S &\to {\mathbf{Z}}\otimes_{\mathbf{Z}}S = S \\
(v_1 \otimes s_1, v_2 \otimes s_2) &\mapsto \beta(v_1, v_2) \otimes s_1 s_2 = s_1s_2. \beta(v_1, v_2)
\end{align*}`{=tex} where \( s_1s_2 \) is the multiplication in \( S \). When there is no danger of confusion, we write this as
\[
\beta_S( s_1v_1, s_2 v_2) \coloneqq s_1 s_2 .\beta(v_1, v_2) \qquad s_i\in S, v_i\in L
.\]
The action of \( S \) on \( L_S \) is defined by
\[
s_1.(v\otimes s_2) \coloneqq v\otimes(s_1s_2)
.\]
We will most frequently apply this to \( S \coloneqq{\mathbf{Q}}, {\mathbf{R}}, {\mathbf{C}}, { \mathbf{F} }_p \), and \( { {\mathbf{Z}}_{\widehat{p}} } \).
:::

::: {.remark title="On complex extensions"}
`\label[remark]{rmk:complex_extensions_of_bilinear_forms}`{=tex} Note that over \( S={\mathbf{C}} \), the extended lattice \( L_{\mathbf{C}} \) carries both a **bilinear** extension \( \beta_{\mathbf{C}} \) and a **sesquilinear** extension \( H_{\mathbf{C}}^\beta \). These are defined by `\begin{align*}
\beta_{\mathbf{C}}: L_{\mathbf{C}}\otimes_{\mathbf{C}}L_{\mathbf{C}}&\to {\mathbf{C}}\\
(z_1 \otimes v_1, z_2 \otimes v_2) &\mapsto z_1z_2.\beta(v_1, v_2) \\ \\
H^\beta: L_{\mathbf{C}}\otimes_{\mathbf{C}}L_{\mathbf{C}}&\to {\mathbf{C}}\\
(z_1 \otimes v_1, z_2 \otimes v_2) &\mapsto z_1\overline{z_2}.\beta(v_1, v_2) 
\end{align*}`{=tex} where we've used the canonical complex conjugation on the complexification \( L_{\mathbf{C}} \) defined by \( \overline{z\otimes v} \coloneqq\overline{z}\otimes v \). These two extensions are related by \( H^\beta(v, w) \coloneqq\beta_{\mathbf{C}}(v, \overline{w}) \) for \( v,w\in L_{\mathbf{C}} \).

To carry out explicit computations, one can use the decomposition \( L_{\mathbf{C}}\cong L_{\mathbf{R}}+ iL_{\mathbf{R}} \) to write every element \( v\in L_{\mathbf{C}} \) as \( v = x + iy \) where \( x,y\in L_{\mathbf{R}} \) and conjugation acts by \( \overline{x+iy} \coloneqq x-iy \). We then have `\begin{align*}
\beta_{\mathbf{C}}(x_1 + iy_1, x_2 + iy_2) &= \beta_{\mathbf{R}}(x_1, x_2) - \beta_{\mathbf{R}}(y_1, y_2) + i\qty{\beta_{\mathbf{R}}(y_1, x_2) + \beta_{\mathbf{R}}(x_1, y_2)} \\
H_{\mathbf{C}}^\beta(x_1 + iy_1, {x_2 + iy_2}) &= \beta_{\mathbf{R}}(x_1, x_2) + \beta_{\mathbf{R}}(y_1, y_2) + i\qty{\beta_{\mathbf{R}}(y_1, x_2) - \beta_{\mathbf{R}}(x_1, y_2)} \\
\end{align*}`{=tex}
:::

## Lattices

::: {.definition title="Scale and integrality"}
Let \( (L, \beta) \) be an integral lattice. The **scale** of \( (L, \beta) \) is the fractional ideal of \( {\mathbf{Q}} \) defined by \( {\mathfrak{a}}_L \coloneqq\beta(L, L) \subseteq {\mathbf{Z}} \). When there is no danger of confusion, we identify \( {\mathfrak{a}}_L \) with its positive generator.
:::

::: remark
Note that \( {\mathfrak{a}}_L = {\mathbf{Z}} \) if and only if \( (L, \beta) \) is integral , while \( {\mathfrak{a}}_L = 2{\mathbf{Z}} \) is a stronger condition than \( L \) being even. The scale of \( L \) can quickly be computed as the greatest common divisor of all entries in \( G_\beta \) in any basis.
:::

::: {.definition title="Twists of lattices"}
Given a lattice \( (L, \beta_L) \) and \( n\in {\mathbf{Q}} \), we define the **twist** of \( L \) by \( n \) as the pair \( (L(n), \beta_{L(n)}) \) where \( L(n) \) has the same underlying module structure as \( L \) and the rescaled bilinear form is defined as
\[
\beta_{L(n)}(v, w) \coloneqq n\cdot \beta_L(v,w) \qquad \forall v,w\in L, \qquad G_{\beta_{L(n)}} = n\cdot G_{\beta_L}
.\]
If \( n\in {\mathbf{Z}} \) and \( L \) is integral, then \( L(n) \) is again integral, but for a general nonzero rational \( n \) this yields a \( {\mathbf{Q}} \)-valued lattice.

Similarly, if \( (L, q_L) \) is a quadratic lattice, we define its twist \( (L(n), q_{L(n)}) \) as
\[
q_{L(n)}(v) \coloneqq n q_L(v) \qquad \forall v\in L, \qquad G_{q_{L(n)}} = n G_q
.\]
:::

::: remark
`\label[remark]{rmk:lattices_in_a_vector_space}`{=tex} If \( V \) is a finite rank module over a field \( k \), we say \( L \) is a **lattice in \( V \)** if \( L \) is finitely generated as a \( {\mathbf{Z}} \)-submodule of \( V \) and \( L_k \cong V \) as \( k \)-modules. This occurs if and only if every \( {\mathbf{Z}} \)-basis of \( L \) extends to a \( k \)-basis of \( V \), where we often take \( k={\mathbf{Q}} \) or \( {\mathbf{R}} \). All lattices in the previous sense can be regarded as lattices in \( V \coloneqq L_{\mathbf{Q}} \) or \( L_{\mathbf{R}} \) under the natural injections \( L\hookrightarrow L_{\mathbf{Q}} \) and \( L\hookrightarrow L_{\mathbf{R}} \).
:::

## Nondegeneracy of lattices

::: {.definition title="Orthogonal complements and discriminant groups"}
If \( L \) is an integral lattice, there is a map `\begin{align*}
\iota: L &\to L {}^{ \vee }\\
v &\mapsto \beta(v, {-})
\end{align*}`{=tex} which for any \( S\leq L \) defines an exact sequence of \( {\mathbf{Z}} \)-modules
\[
0\to S^{\perp L} \hookrightarrow L \xrightarrow{ { \left.{{\iota}} \right|_{{S}} } } L {}^{ \vee }
.\]

For \( S=L \), we obtain a longer short exact sequence of the form
\[
0 \hookrightarrow L^{\perp L} \coloneqq\ker(\iota) \hookrightarrow L \xrightarrow{\iota} L {}^{ \vee }\twoheadrightarrow A_L\coloneqq\operatorname{coker}(\iota) \to 0
.\]

We call

-   \( S^{\perp L} \) the **orthogonal complement of \( S \) in \( L \)**,
-   \( \operatorname{rad}(L) \coloneqq L^{\perp L} \coloneqq\ker(\iota) \) the **radical** of \( L \), and
-   \( A_L \coloneqq\operatorname{coker}(\iota) \) the **discriminant group of \( L \)**.

We say \( L \) is **nondegenerate** if \( \operatorname{rad}(L) = 0 \).

Note that we can explicitly write
\[
S^{\perp L} \coloneqq\left\{{v\in L {~\mathrel{\Big\vert}~}\beta(v, S) = 0}\right\}, \qquad A_L \coloneqq L {}^{ \vee }/\iota(L)
,\]
and if \( \beta(v_1, v_2) = 0 \), we write \( v_1 \perp_L v_2 \) or \( v_1 \in \left\langle{v_2}\right\rangle^{\perp L} \). Note that if \( L \) is nondegenerate, then \( \iota \) is an injection and we simply write \( A_L = L {}^{ \vee }/L \).
:::

::: remark
One can make similar definitions for a quadratic module \( (L, q) \) in terms of its associated bilinear form \( \beta_q \).
:::

::: remark
Note that any \( \beta \) induces a nondegenerate bilinear form on a quotient of \( L \), namely `\begin{align*}
\tilde \beta: {L\over \operatorname{rad}(L)}\otimes_{\mathbf{Z}}{L\over \operatorname{rad}{L}} &\to {\mathbf{Z}}\\
(v + \operatorname{rad}{L}, w + \operatorname{rad}{L}) &\mapsto \beta(v, w)
\end{align*}`{=tex}

Moreover, since \( \tilde L \coloneqq L/\operatorname{rad}(L) \) is finitely generated and free, there is a split short exact sequence
\[
0 \to \operatorname{rad}(L) \hookrightarrow L \twoheadrightarrow\tilde L \to 0
,\]
and thus a (non-canonical) decomposition of \( {\mathbf{Z}} \)-modules \( (L, \beta) = (\operatorname{rad}(L), 0) \oplus (\tilde L, \tilde \beta) \).
:::

::: remark
In particular, if \( \beta \) is nondegenerate then \( \beta(v, L) = 0 \) implies \( v = 0 \) in \( L \). If \( S \leq L \) is sublattice which is a direct summand of \( L \) as a \( {\mathbf{Z}} \)-module, then \( T \coloneqq S^{\perp L} \) is also a direct summand of \( L \) (again as a \( {\mathbf{Z}} \)-module) and
\[
\operatorname{rank}_{\mathbf{Z}}(S) + \operatorname{rank}_{\mathbf{Z}}(T) = \operatorname{rank}_{\mathbf{Z}}(L)
,\]
so \( S \oplus T \) is generally a finite index sublattice of \( L \).
:::

::: {.definition title="Discriminant"}
Given a lattice \( (L, \beta) \) of rank \( n \), the **discriminant** is the ideal generated by determinants of Gram matrices in all bases, i.e.  `\begin{align*}
{\operatorname{disc}}(L) \coloneqq\qty{ \left\{{ \operatorname{det}(G_\beta) {~\mathrel{\Big\vert}~}G_\beta \text{ is a Gram matrix of $\beta$ in some basis } }\right\} }   \subseteq {\mathbf{Z}}
\end{align*}`{=tex} When there is no danger of confusion, we choose a representative \( d \) of this ideal and simply write \( {\operatorname{disc}}(L) = d \).
:::

::: remark
A lattice is nondegenerate if and only if \( {\operatorname{disc}}(L) \) is not a zero divisor in \( {\mathbf{Z}} \) (i.e. \( {\operatorname{disc}}(L) \neq 0 \)) and is unimodular if and only if \( {\operatorname{disc}}(L) \) is a unit in \( {\mathbf{Z}} \) (i.e. \( {\operatorname{disc}}(L) = \pm 1 \)),
:::

::: {.proposition title="Computing indices of sublattices"}
`\label[proposition]{prop:disc_of_full_rank_sublattice}`{=tex} If \( S\leq L \) is a finite index sublattice of a nondegenerate lattice, then
\[
[L: S]^2 = { {\operatorname{disc}}(S) \over {\operatorname{disc}}(L)}
.\]
:::

::: proof
This follows from the existence of the Smith normal form for any basis matrix of \( L \). Picking such a basis matrix \( B_L \coloneqq\left[ {b_1^t,\cdots, b_n^t} \right] \), writing the invariant factors of \( B_L \) as \( d_1,\cdots, d_n \), the matrix \( B_S \coloneqq\left[ {d_1 b_1^t,\cdots, d_n b_n^t} \right] \) defines a basis for \( S \). Moreover, we have \( [L:S] = \prod_{i=1}^n d_i \), and thus
\[
{\operatorname{disc}}(S) = \operatorname{det}(B_S) = \qty{\prod_{i=1}^n d_i}^2 \operatorname{det}(B_L) = [L:S]^2 {\operatorname{disc}}(L)
.\]
:::

::: {.definition title="Volume"}
For a lattice \( L \), let \( P_L \) be the parallelopiped defined by any \( {\mathbf{Z}} \)-basis of \( L \), which is a fundamental domain for the action of \( L \) on \( L_{\mathbf{R}} \) by translation. We have \( L_{\mathbf{R}}/L \cong P_L \), and define the **volume of \( L \)** as the volume of \( P_L \).

There are equalities
\[
\operatorname{Vol}(L)^2 = {\left\lvert {\operatorname{det}(G_\beta)} \right\rvert} \coloneqq{\left\lvert {{\operatorname{disc}}(L)} \right\rvert}
.\]
Note that this is sometimes referred to as the **covolume** and denoted \( \operatorname{coVol}(L) \), since this quantity is \( \operatorname{Vol}(L_{\mathbf{R}}/L) \).
:::

## Dual Lattices

::: {.definition title="Dual modules/lattices"}
`\label[definition]{def:dual_module}`{=tex} For an integral lattice \( (L, \beta) \), we define its **dual** as
\[
L {}^{ \vee }\coloneqq{ \operatorname{Hom} }_{\mathbf{Z}}(L, {\mathbf{Z}})
.\]
If \( S \) is an \( R \)-algebra, we define
\[
L_S^{\vee S} \coloneqq{ \operatorname{Hom} }_S(L_S, S)
,\]
and thus for example \( L_{\mathbf{Q}}{\vee {\mathbf{Q}}} \coloneqq{ \operatorname{Hom} }_{\mathbf{Q}}(L_{\mathbf{Q}}, {\mathbf{Q}}) \).
:::

::: lemma
Duality commutes with finite direct sums, so \( (L \oplus M) {}^{ \vee }\cong L  {}^{ \vee }\oplus M {}^{ \vee } \). It commutes with homomorphisms in the sense that
\[
{ \operatorname{Hom} }_{\mathbf{Z}}(L, M)_S \coloneqq{ \operatorname{Hom} }_{\mathbf{Z}}(L, M) \otimes_{\mathbf{Z}}S = { \operatorname{Hom} }_S(L\otimes_{\mathbf{Z}}, M\otimes_{\mathbf{Z}}S) \coloneqq{ \operatorname{Hom} }_S(L_S, M_S)
,\]
and so in particular it commutes with base change and we have
\[
(L {}^{ \vee })_S \coloneqq L {}^{ \vee }\otimes_{\mathbf{Z}}S \coloneqq{ \operatorname{Hom} }_{\mathbf{Z}}(L, {\mathbf{Z}}) \otimes_{\mathbf{Z}}S = { \operatorname{Hom} }_S(L_S, S) \coloneqq L_S^{\vee S}
.\]
In summary:
\[
(L \oplus M) {}^{ \vee }= L  {}^{ \vee }\oplus M  {}^{ \vee }, \qquad
{ \operatorname{Hom} }_{\mathbf{Z}}(L, M)_S = { \operatorname{Hom} }_S(L_S, M_S), \qquad
(L {}^{ \vee })_S = L_S^{\vee S}
.\]
:::

::: remark
If \( L \) is a nondegenerate integral lattice, then there is an injection \( L\hookrightarrow L {}^{ \vee } \) -- however, the extension \( \beta_{{\mathbf{Q}}} \) of \( \beta \) to \( L_{\mathbf{Q}} \) is typically no longer \( {\mathbf{Z}} \)-valued, so \( L_{\mathbf{Q}} \) (and thus \( L {}^{ \vee } \)) are not necessarily integral lattices.
:::

::: lemma
Let \( (L, \beta) \) be a nondegenerate integral lattice. By nondegeneracy, there is an injection \( L \hookrightarrow L {}^{ \vee } \) which extends to an isomorphism \( L_{\mathbf{Q}} { \, \xrightarrow{\sim}\, }L_{\mathbf{Q}}^{\vee {\mathbf{Q}}} \) of \( {\mathbf{Q}} \)-modules. There is a bijection `\begin{align*}
\left\{{v\in L_{\mathbf{Q}}{~\mathrel{\Big\vert}~}\beta_{\mathbf{Q}}(v, L) \subseteq {\mathbf{Z}}}\right\} & { \, \xrightarrow{\sim}\, }
L {}^{ \vee }\coloneqq{ \operatorname{Hom} }_{\mathbf{Z}}(L, {\mathbf{Z}}) \\
v &\mapsto { \left.{{\beta_{\mathbf{Q}}(v, {-})}} \right|_{{L}} }
\end{align*}`{=tex} Thus for nondegenerate integral lattices, we interchangeably identify these sets.
:::

::: proof
Identifying \( L_k \) with \( L_k^{\vee k} \), every \( k \)-linear functional \( f\in L_k^{\vee k} \) is of the form \( f({-}) = \beta_k(v, {-}) \) for some \( v\in L_k \). But then the restriction \( { \left.{{f}} \right|_{{L}} } \) of \( f \) to \( L \) is in \( L {}^{ \vee } \) if and only if \( { \left.{{f}} \right|_{{L}} }(L) \coloneqq\beta_k(v, L) \subseteq {\mathbf{Z}} \) if and only if \( { \left.{{f}} \right|_{{L}} } \in L^{{\sharp}R} \).
:::

::: {.remark title="Equivalent conditions for a lattice to be nondegenerate/unimodular"}
Moreover, if \( L \) is integral, then \( L\hookrightarrow L {}^{ \vee } \) with index \( [L {}^{ \vee }: L] = {\left\lvert {{\operatorname{disc}}(L)} \right\rvert} \), and thus the discriminant group satisfies \( {\sharp}A_L = {\left\lvert {{\operatorname{disc}}(L)} \right\rvert} \).

For an integral lattice over \( R = {\mathbf{Z}} \), the following are equivalent:

-   \( L \) is nondegenerate,
-   \( {\operatorname{disc}}(L) \neq 0 \),
-   The morphism \( \iota: L\to L {}^{ \vee } \) given by \( v\mapsto \beta(v, {-}) \) is injective,
-   \( \operatorname{rad}(L) \coloneqq L^{\perp L} = 0 \),
-   \( \operatorname{Vol}(L) \neq 0 \).

and similarly the following are equivalent:

-   \( L \) is unimodular,
-   \( {\operatorname{disc}}(L) = \pm 1 \),
-   \( \iota \) is an isomorphism, so \( L { \, \xrightarrow{\sim}\, }L {}^{ \vee } \),
-   \( \operatorname{rad}(L) = 0 \) and \( A_L = 0 \),
-   \( \operatorname{vol}(L) = 1 \).
:::

::: remark
If \( (L, \beta) \) is a lattice with a \( {\mathbf{Z}} \)-basis \( \left\{{e_1,\cdots, e_n}\right\} \), then there exists a dual \( {\mathbf{Q}} \)-basis for \( L {}^{ \vee } \) given by \( \left\{{e_1 {}^{ \vee }, \cdots, e_n {}^{ \vee }}\right\} \) satisfying \( e_i {}^{ \vee }(e_j) = \delta_{ij} \).
:::

::: lemma
Let \( (L, \beta) \) be a definite lattice with Gram matrix \( G_\beta \) in some basis \( B_L \) and let \( L {}^{ \vee } \) denote the dual of \( L \) with dual basis \( B_{L {}^{ \vee }} \). Then `\begin{align*}
G_\beta = B_L^t B_L,\quad 
B_{L {}^{ \vee }} = B_L^{-t}, \quad
G_{\beta  {}^{ \vee }} = G_\beta^{-1}= B_L^{-1}B_L^{-t}
.\end{align*}`{=tex}

Moreover, if \( L \) is unimodular, then \( G_{\beta {}^{ \vee }} \) expresses the dual basis \( B_{L {}^{ \vee }} \) of \( L \) in terms of the basis \( B_L \).
:::

::: proof
By definition, the Gram matrix for \( \beta \) on \( L \) in the basis \( B_L \) is given by \( G_\beta = B_L^t B_L \), since this precisely computes \( \beta(e_i, e_j) \) for all \( i, j \). Similarly \( G_{\beta {}^{ \vee }} = B_{L {}^{ \vee }}^t B_{L {}^{ \vee }} \) is in the dual basis \( B_{L {}^{ \vee }} \) on \( L {}^{ \vee } \).

Letting \( B_{L {}^{ \vee }} = (e_i {}^{ \vee })_{i\leq n} \) be the basis matrix for \( L {}^{ \vee } \), we have \( B_L^t B_{L {}^{ \vee }} = 1 \) since \( e_i {}^{ \vee }(e_j) = \delta_{ij} \), so if \( B \) is full rank then \( B_{L {}^{ \vee }} = B_L^{-t} \).

Combining these facts, we find `\begin{align*}
G_\beta G_{\beta {}^{ \vee }}
&= (B_L^t B_L)(B_{L {}^{ \vee }}^t B_{L {}^{ \vee }}) \\
&= B_L^t B_{L {}^{ \vee }}^{-t} B_{L {}^{ \vee }}^t B_{L {}^{ \vee }} \\
&= B_L^t B_{L {}^{ \vee }} \\
&= B_L^t B_L^{-t} \\
&= \operatorname{id}
,\end{align*}`{=tex} and so we can express \( G_{\beta {}^{ \vee }} = G_\beta^{-1} \).
:::

::: remark
Since \( L \mapsto L {}^{ \vee } \) is an functor of \( R \)-modules, there is an induced morphism `\begin{align*}
({-}) {}^{ \vee }: { \operatorname{Hom} }_{\mathbf{Z}}(L_1, L_2) & \to { \operatorname{Hom} }_{\mathbf{Z}}(L_2 {}^{ \vee }, L_1 {}^{ \vee }) \\
f &\mapsto f {}^{ \vee }: g\mapsto g\circ f \qquad \forall g: L_2\to R
\end{align*}`{=tex} In particular, for any \( L \) there is a morphism of \( {\mathbf{Z}} \)-modules \( \mathop{\mathrm{Aut}}_{\mathbf{Z}}(L) \to \mathop{\mathrm{Aut}}_{\mathbf{Z}}(L {}^{ \vee }) \).
:::

::: lemma
If \( f: L_1\to L_2 \) is given by a matrix \( M_f \) in fixed bases \( B_{L_1}, B_{L_2} \) of \( L_1 \) and \( L_2 \), then \( f {}^{ \vee } \) is given by \( M_{f {}^{ \vee }} = M_f^t \) in the dual bases \( B_{L_1 {}^{ \vee }}, B_{L_2 {}^{ \vee }} \). Moreover, if \( f \) is an isomorphism, then \( M_{f^{-1}} = M_f^{-1} \) and \( f {}^{ \vee } \) is an isomorphism with inverse \( (f {}^{ \vee })^{-1}= (f^{-1}) {}^{ \vee } \) represented by \( M_{(f {}^{ \vee })^{-1}} = M_f^{-t} \). In summary, we have `\begin{align*}
M_{f^{-1}} = M_f^{-1}, \qquad 
M_{f {}^{ \vee }} = M_f^t, \qquad
M_{(f {}^{ \vee })^{-1}} = M_f^{-t}    
\end{align*}`{=tex}
:::

::: lemma
Let \( (L, \beta) \) be a nondegenerate integral \( {\mathbf{Z}} \)-lattice with discriminant \( d\coloneqq{\operatorname{disc}}(L) \). Then \( L {}^{ \vee }\subseteq {1\over d^2} L \), or equivalently \( d^2 L {}^{ \vee }\subseteq L \). In this case, one can write `\begin{align*}
\beta {}^{ \vee }: L {}^{ \vee }\otimes_{\mathbf{Z}}L {}^{ \vee }&\to d^{-2} {\mathbf{Z}}\subseteq {\mathbf{Q}}\\
(v, w) &\mapsto {1\over d^2}\cdot \beta(dv, dw)
,\end{align*}`{=tex} where notably \( dv, dw\in L \) and so one can use the original bilinear form on \( L \) without extending it to \( {\mathbf{Q}} \).
:::

::: lemma
We have the following equalities of determinants and volumes: `\begin{align*}
{\operatorname{disc}}(L {}^{ \vee }) = {1\over {\operatorname{disc}}(L) }, \quad
\operatorname{vol}(L {}^{ \vee }) = {1\over \operatorname{vol}(L)}
\end{align*}`{=tex} Thus if \( L \) is unimodular then \( {\operatorname{disc}}(L {}^{ \vee }) = {\operatorname{disc}}(L) = \pm 1 \) and \( \operatorname{vol}(L) = \operatorname{vol}(L {}^{ \vee }) = 1 \).
:::

::: {.lemma title="Dual of a twist"}
For the twist \( L(m) \) of an \( R \)-lattice, we have
\[
(L(m)) {}^{ \vee }= L {}^{ \vee }\qty{1\over m}
.\]
If \( L \) is unimodular, then
\[
(L(m)) {}^{ \vee }= L\qty{1\over m} = {1\over m}L(m), \qquad A_L = {{1\over m}L(m) \over L(m)}
.\]
:::

::: {.definition title="Divisibility"}
Let \( (L, \beta) \) be an integral \( {\mathbf{Z}} \)-lattice. The **divisibility** of an element \( v\in L \), denoted \( \operatorname{div}_L(v) \), is the positive generator of the ideal \( \beta(v, L) \subseteq {\mathbf{Z}} \).
:::

::: remark
The element \( v^* \coloneqq v/\operatorname{div}_L(v) \) is a primitive vector in \( L {}^{ \vee } \), and thus \( [v^*] \in A_L \) is an element of order \( \operatorname{div}_L(v) \). Moreover, \( \operatorname{div}_L(v) \) always divides \( {\operatorname{disc}}(L) \), and if \( e\in L \) is isotropic, then \( e \) extends to a copy of \( U \) primitively embedded in \( L \) if and only if \( \operatorname{div}_L(e) = 1 \), in which case \( L = U \oplus U^{\perp L} \).
:::

## Morphisms and Isometry Classes

::: {.definition title="Morphisms and embeddings"}
The set of **morphisms** between lattices \( (L_1, \beta_1) \) and \( (L_2, \beta_2) \) is defined as
\[
{ \operatorname{Hom} }_{ \mathrm{Lat}_{\mathbf{Z}}}(L_1, L_2)
\coloneqq\left\{{f\in { \operatorname{Hom} }_{\mathbf{Z}}(L_1, L_2) {~\mathrel{\Big\vert}~}\beta_1(v, w) = \beta_2(f(v), f(w)) \,\,\forall v, w\in L_1 }\right\}
.\]
An **embedding** \( f \) of \( L_1 \) into \( L_2 \) is an injective morphism of lattices, and \( f \) is a **primitive embedding** if \( \operatorname{coker}(f) \) is torsionfree as a \( {\mathbf{Z}} \)-module. We say a sublattice \( S\leq L \) is a **primitive sublattice** if the inclusion \( \iota:S\hookrightarrow L \) is a primitive embedding.
:::

::: {.definition title="Equivalence of embeddings"}
`\label[definition]{def:equivalent_embeddings}`{=tex} Two primitive embeddings \( \iota_1: S\hookrightarrow L_1, \iota_2: S\hookrightarrow L_2 \) are **equivalent** if \( \exists f\in {\mathrm{Isom}}(L_1, L_2) \) such that \( { \left.{{f}} \right|_{{\iota_1(S)}} } = \operatorname{id}_{\iota_1(S)} \), and two such primitive sublattices are **equivalent** if \( \exists f\in {\mathrm{Isom}}(L_1, L_2) \) such that \( f(\iota_1(S)) = \iota_2(S) \).

In particular, given a sublattice \( S\leq L \), two primitive embeddings \( \iota_1, \iota_2: S\hookrightarrow L \) are **equivalent** if there exists \( g\in {\operatorname{O}}(L) \) such that \( \iota_1 = g\circ \iota_2 \). Write \( {\operatorname{Emb}}(S, L) \) for the equivalence classes of primitive embeddings of \( S \) into \( L \).
:::

::: {.definition title="Primitive elements"}
An element \( v\in L \) is a **primitive element** if the inclusion \( \left\langle{v}\right\rangle_{\mathbf{Z}}\hookrightarrow L \) is a primitive embedding of lattices.
:::

::: {.definition title="Saturations"}
`\label[definition]{def:saturation}`{=tex} Let \( \iota: S\hookrightarrow L \) be an embedding of lattices. Identifying \( S \) with \( \iota(S) \), we say \( S \) is **saturated in \( L \)** if for all \( v\in L \), if \( nv\in S \) for some \( n\in {\mathbf{Z}} \), then \( v\in S \). We define the **saturation of \( S \) in \( L \)** as
\[
\operatorname{Sat}_L(S) \coloneqq\left\{{v\in L {~\mathrel{\Big\vert}~}nv\in S \text{ for some } n\in {\mathbf{Z}}\setminus\left\{{0}\right\}}\right\}
.\]
Thus \( S \) is saturated in \( L \) if and only if \( S = \operatorname{Sat}_L(S) \).
:::

::: remark
Over \( {\mathbf{Z}} \), the following are equivalent:

-   \( \iota:S\hookrightarrow L \) is a primitive embedding,
-   \( S \) is saturated in \( L \),
-   There exists a submodule \( T\leq L \) such that \( L { \, \xrightarrow{\sim}\, }S \oplus T \) as \( {\mathbf{Z}} \)-modules,
-   There exists a morphism \( f: L\to M \) for some lattice \( M \) with \( \ker f = S \),
-   \( S = (S^{\perp L})^{\perp L} \),
-   Any \( {\mathbf{Z}} \)-basis of \( S \) can be extended to a \( {\mathbf{Z}} \)-basis of \( L \),
-   \( S \) is a direct summand of \( L \) as a \( {\mathbf{Z}} \)-module,
-   \( (S_{\mathbf{Q}}) \cap L = S \),
-   \( L {}^{ \vee }\twoheadrightarrow S {}^{ \vee } \), so every integral functional on \( S \) lifts to an integral functional on \( L \).
:::

::: remark
If \( S\hookrightarrow L \) is a any embedding (not necessarily primitive), then \( T\coloneqq S^{\perp L} \) is automatically primitive since
\[
\operatorname{Sat}_L(T) = 
\operatorname{Sat}_L(S^{\perp L}) =
((S^{\perp L})^{\perp L})^{\perp L} =
\operatorname{Sat}_L(S)^{\perp L} = T
.\]
:::

::: {.definition title="Isometries and the orthogonal group"}
Their set of **isometries over \( R \)** is defined as
\[
{\mathrm{Isom}}(L_1, L_2) \coloneqq\left\{{f\in { \operatorname{Hom} }_{ \mathrm{Lat}_{\mathbf{Z}}}(L_1, L_2) {~\mathrel{\Big\vert}~}f \text{ is an isomorphism of ${\mathbf{Z}}$-modules}}\right\} 
.\]
If two lattices are isometric, we write \( L_1 { \, \xrightarrow{\sim}\, }L_2 \). The **orthogonal group** of \( L \) is defined as
\[
{\operatorname{O}}(L) \coloneqq\mathop{\mathrm{Aut}}_{ \mathrm{Lat}_{\mathbf{Z}}}(L) \coloneqq{\mathrm{Isom}}(L, L)
.\]
:::

::: example
Over \( {\mathbf{Z}} \), we have
\[
{\operatorname{O}}(U) = \left\{{ I_1, I_{-1}, J_1, J_{-1} }\right\}
\coloneqq\left\{{\operatorname{id}, -\operatorname{id}, { \begin{bmatrix} {0} & {1}  \\ {1} & {0} \end{bmatrix} }, { \begin{bmatrix} {0} & {-1}  \\ {-1} & {0} \end{bmatrix} }}\right\} \cong C_2 \times C_2
.\]
:::

::: {.definition title="Isometry classes"}
Given an \( R \)-lattice \( (L, \beta) \), we define its **isometry class** \(  \operatorname{Cl}(L) \) as the set of all lattices \( (M,\beta_M) \) that are isometric to \( L \) over \( {\mathbf{Z}} \).

We let \(  \mathrm{Lat}_{\mathbf{Z}} \) be the category of nondegenerate \( {\mathbf{Z}} \)-lattices and \(  \mathrm{Lat}_{\mathbf{Z}}{_{\scriptstyle / \sim} } \) be the category of isometry classes of such lattices. Then \( L_1 { \, \xrightarrow{\sim}\, }L_2 \iff  \operatorname{Cl}(L_1) =  \operatorname{Cl}(L_2) \iff [L_1] = [L_2] \) in \(  \mathrm{Lat}_{\mathbf{Z}}{_{\scriptstyle / \sim} } \). We similarly define \(  \mathrm{Lat}^n_{\mathbf{Z}},  \mathrm{Lat}^n_{\mathbf{Z}}{_{\scriptstyle / \sim} } \) for lattices of rank \( n \).
:::

::: remark
If \( (L, q) \) is a quadratic lattice, we define \( {\operatorname{O}}(L) \coloneqq{\operatorname{O}}(L, q) \coloneqq{\operatorname{O}}(L, \beta_q) \) using its polar form, and similarly define its isometry class \(  \operatorname{Cl}(L, q) \). By a theorem of Minkowski, there are only finitely many isometry classes of integral \( {\mathbf{Z}} \)-lattices of a fixed rank \( n \) and discriminant \( d \).
:::

::: {.remark title="Isometry via group actions"}
Let \(  \mathrm{Quad}^n_{\mathbf{Z}} \) denote the set of all quadratic lattices \( (L, q) \) of rank \( n \), and define the following action: `\begin{align*}
\operatorname{Mat}_{n\times n}({\mathbf{Z}}) &\to \mathop{\mathrm{Aut}}_{\mathbf{Z}}( \mathrm{Quad}^n_{\mathbf{Z}}) \\
M &\mapsto \qty{ (L, q) \mapsto (L, M.q) } \qquad (M.q)(x) \coloneqq q(M^t x)
\end{align*}`{=tex} Note that this can be restricted to an action by any subgroup \( G \leq \operatorname{Mat}_{n\times n}({\mathbf{Z}}) \).

Similarly, let \(  \mathrm{Lat}^n_{\mathbf{Z}} \) denote the set of all symmetric bilinear forms \( (L, \beta) \) of rank \( n \), represented by their Gram matrices \( G_\beta \), and define an action `\begin{align*}
\operatorname{Mat}_{n\times n}({\mathbf{Z}}) &\to \mathop{\mathrm{Aut}}_{\mathbf{Z}}( \mathrm{Lat}^n_{\mathbf{Z}}) \\
M &\mapsto \qty{ (L, \beta) \mapsto (L, M.\beta)} \qquad M.\beta \coloneqq M.G_\beta = M G_\beta M^t
,\end{align*}`{=tex} which again can be restricted to any subgroup.

We say two quadratic forms (resp. bilinear) forms are **\( G \)-equivalent** if they are in the same \( G- \) orbit under the above action, and simply **equivalent** if they are in the same \( G\coloneqq\operatorname{GL}_n({\mathbf{Z}}) \) orbit. We write their equivalence classes as
\[
 \operatorname{Cl}(L, q) \in  \mathrm{Quad}^n_{\mathbf{Z}}/\operatorname{GL}_n({\mathbf{Z}}), \qquad  \operatorname{Cl}(L) \in  \mathrm{Lat}^n_{\mathbf{Z}}/\operatorname{GL}_n({\mathbf{Z}})
.\]
We can then identify the orthogonal group of a quadratic lattice as its stabilizer under the \( \operatorname{GL}_n({\mathbf{Z}}) \) action: `\begin{align*}
{\operatorname{O}}(L, q) \coloneqq{\operatorname{Stab}}_{\operatorname{GL}_n({\mathbf{Z}})}(L, q) 
&\coloneqq\left\{{M\in \operatorname{GL}_n({\mathbf{Z}}) {~\mathrel{\Big\vert}~}M.q = q}\right\} \\
&= \left\{{M\in \operatorname{GL}_n({\mathbf{Z}}){~\mathrel{\Big\vert}~}M^t G_q M = G_q}\right\}
\end{align*}`{=tex}

Similarly, for lattices: `\begin{align*}
{\operatorname{O}}(L) \coloneqq{\operatorname{Stab}}_{\operatorname{GL}_n({\mathbf{Z}})}(L, \beta)
&\coloneqq\left\{{M\in \operatorname{GL}_n({\mathbf{Z}}) {~\mathrel{\Big\vert}~}M.\beta = \beta}\right\} \\
&= \left\{{M\in \operatorname{GL}_n({\mathbf{Z}}) {~\mathrel{\Big\vert}~}M G_\beta M^t = G_\beta}\right\}
\end{align*}`{=tex}

Note that a similar discussion applies to \( \operatorname{Mat}_{n\times n}({\mathbf{Q}}) \) and subgroups thereof.

In particular, for a fixed lattice, this yields computationally quick ways to generate isometric lattices, namely by generating random matrices in \( {\operatorname{SL}}_n({\mathbf{Z}}) \) and conjugating \( G_\beta \) to obtain a new Gram matrix. Similarly, this yields a quick way to check if a given automorphism \( f \) of \( L \) is an isometry, namely by picking any basis, writing a matrix \( M_f \) for \( f \), and checking that it preserves \( G_\beta \) under conjugation.
:::

::: example
The bilinear forms \( U(1/2) \) and \(  {\textrm{I}} _{1, 1} \) over \( {\mathbf{Z}} \) are \( \operatorname{GL}_2({\mathbf{Q}}) \)-equivalent: one can take \( M \coloneqq{ \begin{bmatrix} {1} & {1}  \\ {1} & {-1} \end{bmatrix} } \) and obtain
\[
M G_{U(1/2)} M^t = { \begin{bmatrix} {1} & {1}  \\ {1} & {-1} \end{bmatrix} } { \begin{bmatrix} {0} & {1\over 2}  \\ {1\over 2} & {0} \end{bmatrix} } { \begin{bmatrix} {1} & {1}  \\ {1} & {-1} \end{bmatrix} } = { \begin{bmatrix} {1} & {0}  \\ {0} & {-1} \end{bmatrix} } = G_{ {\textrm{I}} _{1, 1}}
.\]

However, they are not \( \operatorname{GL}_2({\mathbf{Z}}) \)-equivalent. To see that no such \( M \) works, one can note that these lattices correspond to the quadratic forms \( q_1(x,y) = xy \) and \( q_2(x,y) = x^2-y^2 \) respectively on \( {\mathbf{Z}}^2 \), and representability of integers is an invariant of quadratic forms. Over \( {\mathbf{Z}} \), every integer is representable by \( q_1 \), namely by taking \( x=1 \) and letting \( y \) freely vary, while 2 is not representable by \( q_2 \). Writing \( x^2-y^2 = (x+y)(x-y) \), if \( x \) and \( y \) have the same parity, then \( x^2-y^2 \equiv 0 \pmod 4 \neq 2\pmod 4 \), a contradiction. If \( x \) and \( y \) have different parities, then \( (x+y)(x-y) \) is odd, which is again a contradiction.
:::

::: remark
An isometry \( f\in {\operatorname{O}}(L) \) extends to an isometry \( f_{\mathbf{Q}}\coloneqq f\otimes\operatorname{id}_{\mathbf{Q}}\in {\operatorname{O}}(L_{\mathbf{Q}}) \) preserving \( L {}^{ \vee }\subseteq L_{\mathbf{Q}} \). This induces an isomorphism \( { \left.{{f}} \right|_{{A_L}} } \) which preserves the discriminant form, and thus there is a well-defined group homomorphism `\begin{align*}
\psi: {\operatorname{O}}(L) &\to {\operatorname{O}}(A_L) \\
f &\mapsto { \left.{{f}} \right|_{{A_L}} }([x]) \coloneqq[f {}^{ \vee }(x)]
\end{align*}`{=tex} It is neither injective nor surjective in general, leading to the following:
:::

::: {.definition title="Stable orthogonal group"}
Let \( \psi: {\operatorname{O}}(L {}^{ \vee }) \to {\operatorname{O}}(A_L) \) be the morphism described above, which we will write as \( f\mapsto { \left.{{f}} \right|_{{A_L}} } \). This induces an exact sequence
\[
0 \to {\operatorname{O}}^*(L)\coloneqq\ker(\psi) \to {\operatorname{O}}(L) \xrightarrow{\psi} {\operatorname{O}}(A_L) \to {\operatorname{O}}^*(A_L)\coloneqq\operatorname{coker}(\psi) \to 0
.\]
We refer to \( {\operatorname{O}}^*(L) \) as the **stable orthogonal group** of \( L \), and \( {\operatorname{O}}^*(A_L) \) similarly as the stable orthogonal group of \( A_L \).
:::

::: remark
When \( L =  {L_{\mathrm{K3}, 2d}}  \), the stable orthogonal group \( {\operatorname{O}}^*(L) \) corresponds to the group of isometries of \(  {L_{\mathrm{K3}}}  \) that preserve the polarization \( h \) and act on a connected component of the 2-component period domain \( \Omega_{L} \).
:::

::: remark
Note that \( {\operatorname{O}}(L(n)) \cong {\operatorname{O}}(L) \) for any \( n\neq 0 \).
:::

::: remark
Note that \( {\operatorname{O}}(L) \to {\operatorname{O}}(A_L) \) is surjective if and only if \( {\operatorname{O}}^*(A_L) = 0 \). In this case, any isometry of \( A_L \) can be lifted to an isometry of \( L \).
:::

## Classification of lattices over fields

::: {.theorem title="Classification of lattices over fields, {\\cite[Thm. 8.1.1]{petersSymmetricQuadraticForms2024}}"}
Let \( (L, \beta) \) be a nondegenerate lattice of rank \( n \) over a field \( k \) where \( \operatorname{ch}(k) \neq 2 \). Then \( L \) is isometric to a diagonal form
\[
L  { \, \xrightarrow{\sim}\, }\bigoplus_{i=1}^n \left\langle{a_i}\right\rangle, \qquad a_i\in k^{\times}
,\]
and in this basis \( G_\beta \) is diagonal. Thus
\[
 \mathrm{Lat}^n_k{_{\scriptstyle / \sim} }\subseteq (k^{\times})^n, \qquad \operatorname{ch}(k) \neq 2
.\]
:::

::: remark
Note that over general fields \( k \), there is no guarantee of uniqueness of this decomposition. Over \( k={\mathbf{R}} \), up to isometry one can reduce to \( a_i \in \left\{{\pm 1}\right\} \) for all \( i \). By Sylvester's theorem, the numbers \( p \) and \( q \) of summands equal to \( \left\langle{1}\right\rangle \) and \( \left\langle{-1}\right\rangle \) respectively are well-defined and unique. Moreover, if \( k={ \overline{k} } \), one can take \( a_i = 1 \) for all \( i \). We can thus write
\[
 \mathrm{Lat}^n_{\mathbf{R}}{_{\scriptstyle / \sim} }\cong \left\{{ \operatorname{Cl}( {\textrm{I}} _{p, q}) {~\mathrel{\Big\vert}~}p+q=n,\,\, 0\leq p,q\leq n, n\geq 1}\right\}, \qquad  \mathrm{Lat}^n_{\mathbf{C}}{_{\scriptstyle / \sim} }= \left\{{ \operatorname{Cl}( {\textrm{I}} _{n, 0}) {~\mathrel{\Big\vert}~}n\geq 1 }\right\}
.\]
This motivates the following definition:
:::

::: {.definition title="Signature and index"}
Let \( (L, \beta) \) be a nondegenerate \( {\mathbf{Z}} \)-lattice, and let \( p \) (resp. \( q \)) be the number of summands \( \left\langle{1}\right\rangle \) (resp. \( \left\langle{-1}\right\rangle \)) in the diagonalization of \( (L_{\mathbf{R}}, \beta_{\mathbf{R}}) \). The pair \( (p, q) \) is called the **signature** of \( L \), written \( \operatorname{sig}(L) = (p, q) \), and the **index** of \( L \) is the quantity \( \tau(L) \coloneqq p-q \).
:::

::: remark
As a matter of notation, given two lattices \( L, M \) with \( \operatorname{sig}(L) = (p, q) \) and \( \operatorname{sig}(M) = (p', q') \), we write \( \operatorname{sig}(M) \geq \operatorname{sig}(L) \) if both \( p' \geq p \) and \( q'\geq q \).
:::

::: {.remark title="Definite/indefinite/hyperbolic lattices"}
Let \( (L) \) be a nondegenerate lattice of rank \( n \) with \( \operatorname{sig}(L) = (p, q) \). If

-   \( p = 0 \), \( L \) is negative-definite,
-   \( q = 0 \), \( L \) is positive-definite,
-   \( p\neq 0 \) and \( q\neq 0 \), \( L \) is indefinite, and if
-   \( (p, q) = (1, n-1) \) or \( (n-1, 1) \), we say \( L \) is **hyperbolic**.

By convention, we typically adopt the convention that hyperbolic lattices have signature \( (1, n-1) \).
:::

::: {.theorem title="Classification of $\\mathbb{R}$-lattices"}
Let \( (L_1, \beta_1) \) and \( (L_2, \beta_2) \) be two nondegenerate \( {\mathbf{R}} \)-lattices. The following are equivalent:

-   \(  \operatorname{Cl}_{\mathbf{R}}(L_1) =  \operatorname{Cl}_{\mathbf{R}}(L_2) \), so \( L_1 \) is isometric to \( L_2 \) over \( {\mathbf{R}} \),
-   \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \),
-   \( \operatorname{rank}_{\mathbf{R}}(L_1) = \operatorname{rank}_{\mathbf{R}}(L_2) \) and \( \tau(L_1) = \tau(L_2) \).

Thus a lattice over \( {\mathbf{R}} \) is uniquely determined up to isometry by its signature, and is thus isometric to \(  {\textrm{I}} _{p, q} \) for some \( p, q \). In this case, writing \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) = (p, q) \), we have \(  \operatorname{Cl}(L) = \left\{{ {\textrm{I}} _{p, q}}\right\} \), i.e. the class group is a single element represented by the isometry class of \(  {\textrm{I}} _{p, q} \).
:::

## Torsion forms

::: {.definition title="Torsion bilinear/quadratic forms"}
A **torsion bilinear (resp. quadratic) form** is an \( {\mathbf{Q}}/{\mathbf{Z}} \)-valued bilinear \( {\mathbf{Z}} \)-module \( (G, \beta) \) (resp. an \( {\mathbf{Q}}/{\mathbf{Z}} \)-valued quadratic \( {\mathbf{Z}} \)-module \( (G, q) \)) where \( G \) is a finitely generated torsion \( {\mathbf{Z}} \)-module.

Thus a torsion form is a pair \( (G, \beta) \) where \( G \) is a finite abelian group and \( \beta: G \otimes_{\mathbf{Z}}G \to {\mathbf{Q}}/{\mathbf{Z}} \) is a \( {\mathbf{Z}} \)-bilinear form Similarly a torsion quadratic form is a pair \( (G, q) \) where \( q: G \to {\mathbf{Q}}/{\mathbf{Z}} \) is a quadratic form.

We define \( { \operatorname{Hom} }_{ \mathrm{Quad}_{\mathbf{Z}}}(G_1, G_2), {\mathrm{Isom}}_{ \mathrm{Quad}_{\mathbf{Z}}}(G_1, G_2) \), and \( {\operatorname{O}}(G), {\operatorname{O}}(G, q) \) as in the case of \( {\mathbf{Z}} \)-valued bilinear forms, we write \(  \operatorname{Cl}(G) \) and \(  \operatorname{Cl}(G, q) \) for their isometry classes, and define \(  \mathrm{Lat}_{{\mathbf{Q}}/{\mathbf{Z}}}(G){_{\scriptstyle / \sim} } \) and \(  \mathrm{Quad}_{{\mathbf{Q}}/{\mathbf{Z}}}(G){_{\scriptstyle / \sim} } \) for the spaces of torsion bilinear (resp. quadratic) forms up to isometry on a fixed group \( G \).
:::

::: {.theorem title="Classification of torsion $\\mathbf{Q}/\\mathbf{Z}$ forms on cyclic groups {\\cite[Prop. 6.1.8]{petersSymmetricQuadraticForms2024}}"}
There is a classification of nondegenerate \( {\mathbf{Q}}/{\mathbf{Z}} \)-valued symmetric torsion forms \( \beta \) on \( C_m \): each such form is isometric to \( \left\langle{a\over m}\right\rangle \) for some \( a\in {\mathbf{Z}} \) coprime to \( m \), and they are classified by \( D(C_m) \coloneqq C_m^{\times}/(C_m^{\times})\square \). Explicitly, these are given by \( \beta(x,y) = {a\over m}xy \). Thus `\begin{align*}
 \mathrm{Lat}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_m){_{\scriptstyle / \sim} }&\cong \left\{{\left\langle{u\over m}\right\rangle {~\mathrel{\Big\vert}~}u\in D(C_m)}\right\}, \\
 \mathrm{Quad}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_m){_{\scriptstyle / \sim} }&\cong \left\{{\left[ {u\over 2m} \right] {~\mathrel{\Big\vert}~}u\in D(C_{2m})}\right\}
\end{align*}`{=tex}

For example, for symmetric bilinear forms, `\begin{align*}
 \mathrm{Lat}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_2){_{\scriptstyle / \sim} }&\cong \left\{{ \left\langle{1\over 2}\right\rangle }\right\}, \\
 \mathrm{Lat}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_4){_{\scriptstyle / \sim} }&\cong \left\{{ \left\langle{1\over 4}\right\rangle, \left\langle{3\over 4}\right\rangle}\right\}, \\
 \mathrm{Lat}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_{2^k}){_{\scriptstyle / \sim} }&\cong \left\{{ \left\langle{u\over 2^k}\right\rangle,\quad u = \pm 1, \pm 3\pmod 8}\right\},\qquad (k\geq 3), 
\end{align*}`{=tex} and for quadratic forms, `\begin{align*}
 \mathrm{Quad}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_2){_{\scriptstyle / \sim} }&\cong \left\{{\left[ {1\over 4} \right], \left[ {3\over 4} \right]}\right\} \\
 \mathrm{Quad}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_4){_{\scriptstyle / \sim} }&\cong \left\{{\left[ {1\over 8} \right], \left[ {-3\over 8} \right], \left[ {3\over 8} \right], \left[ {-1\over 8} \right]}\right\} \\
 \mathrm{Quad}_{{\mathbf{Q}}/{\mathbf{Z}}}(C_{2^k}){_{\scriptstyle / \sim} }&\cong \left\{{\left[ {u\over 2^{k+1} } \right] {~\mathrel{\Big\vert}~}u = \pm 1, \pm 3 \pmod 8}\right\}, \qquad (k\geq 3)
.\end{align*}`{=tex}
:::

## Discriminant Bilinear/Quadratic Forms

::: {.definition title="Discriminant bilinear/quadratic modules"}
If \( (L, \beta) \) is a nondegenerate lattice, there is an injection \( \iota: L\hookrightarrow L {}^{ \vee } \) realizing \( L \) as a finite-index sublattice of \( L {}^{ \vee } \) and inducing an exact sequence
\[
0 \to L \xhookrightarrow{\iota} L {}^{ \vee }\twoheadrightarrow A_L \coloneqq\operatorname{coker}(\iota_1) \to 0
.\]
We define the **discriminant bilinear module** as \( A_L \), which is necessarily a torsion \( {\mathbf{Z}} \)-module. It becomes a torsion bilinear \( {\mathbf{Z}} \)-module when equipped with the form `\begin{align*}
\beta_{A_L}: A_L \otimes_{\mathbf{Z}}A_L &\to {\mathbf{Q}}/{\mathbf{Z}}\\
([v], [w]) &\mapsto \beta_{\mathbf{Q}}(v, w) \pmod {\mathbf{Z}}
\end{align*}`{=tex} where we identify \( v,w\in L \) with their images in \( L {}^{ \vee } \). The pair \( (A_L, \beta_{A_L}) \) is referred to as the **discriminant bilinear form** associated to \( L \).

Similarly, if \( (L, q) \) is a nondegenerate quadratic form, \( A_L \) admits a quadratic form `\begin{align*}
q_{A_L}: A_L &\to {\mathbf{Q}}/{\mathbf{Z}}\\
[x] &\mapsto q_{\mathbf{Q}}(x) \pmod {\mathbf{Z}}
\end{align*}`{=tex} and we refer to \( (A_L, q_{A_L}) \) as the **discriminant quadratic form** of \( L \).
:::

::: remark
If \( (L, \beta) \) is an *even* nondegenerate lattice, the discriminant quadratic form \( q_{A_L} \) takes values in \( {\mathbf{Q}}/2{\mathbf{Z}} \) and is given by `\begin{align*}
q_{A_L}: A_L &\to {\mathbf{Q}}/2{\mathbf{Z}}\\
[x] &\mapsto \beta_{\mathbf{Q}}(x, x) \pmod{2{\mathbf{Z}}}
.\end{align*}`{=tex} Moreover, \( \beta_{A_L} \) is the bilinear form associated to \( q_{A_L} \), i.e.
\[
\beta_{A_L}([v], [w]) = {1\over 2}\qty{ q_{A_L}([v] + [w]) - q_{A_L}([v]) - q_{A+L}([w])}
\]
where one applies the isomorphism \( {1\over 2}: {\mathbf{Q}}/2{\mathbf{Z}}\to {\mathbf{Q}}/{\mathbf{Z}} \). These forms are nondegenerate if and only if \( L \) is nondegenerate, since if \( \beta_{\mathbf{Q}}(v, L {}^{ \vee }) = 0 \) for some \( v\in L \) then \( v\in (L {}^{ \vee }) {}^{ \vee }= L \) and thus \( [v] = [0] \in A_L \).
:::

::: remark
There are equalities
\[
{\sharp}A_L = {\left\lvert {{\operatorname{disc}}(L)} \right\rvert} = [L {}^{ \vee }: L]
,\]
and in particular \( L \) is unimodular if and only if \( A_L = 0 \).
:::

::: {.definition title="Length of a lattice"}
For an \( R \)-lattice \( (L, \beta) \), define its **length** \( \ell(L) \) as the minimal number of generators of \( A_L \).
:::

::: example
We collect some examples of lengths of common lattices:

  \( L \)                              \( A_L \)             \( \ell(L) \)
  ------------------------------------ --------------------- ---------------
  \( A_n \)                            \( C_{n+1} \)         \( 1 \)
  \( D_{2n} \)                         \( C_2^2 \)           \( 2 \)
  \( D_{2n+1} \)                       \( C_4 \)             \( 1 \)
  \( E_6 \)                            \( C_3 \)             \( 1 \)
  \( E_7 \)                            \( C_2 \)             \( 1 \)
  \( E_8 \)                            \( 0 \)               \( 0 \)
  \( E_8(2) \)                         \( C_2^8 \)           \( 8 \)
  \( \left\langle{n}\right\rangle \)   \( C_n \)             \( 1 \)
  \( U \)                              \( 0 \)               \( 0 \)
  \( U(2) \)                           \( C_2^2 \)           \( 2 \)
  \( E_{10}(2) \)                      \( C_2^{10} \)        \( 10 \)
  \(  {\textrm{I}} _{p, q}(2) \)       \( C_2^{p+q} \)       \( p+q \)
  \( V \)                              \( C_3 \)             \( 1 \)
  \( V(2) \)                           \( C_2\times C_6 \)   \( 2 \)
  \( L_{2d} \)                         \( C_{2d} \)          \( 1 \)
  \(  {L_{\mathrm{K3}}}  \)            \( 0 \)               \( 0 \)
:::

::: remark
Since \( L {}^{ \vee }\twoheadrightarrow A_L \), if \( L {}^{ \vee }= \left\langle{v_1,\cdots, v_n}\right\rangle_{\mathbf{Q}} \), then \( A_L \) is generated by the class \( \left\{{[v_1], \cdots, [v_n]}\right\} \), although this may not be a *minimal* generating set. In particular, there is an inequality \( \ell(L) \leq \operatorname{rank}_{\mathbf{Q}}(L {}^{ \vee }) = \operatorname{rank}(L) \), and by observing the table above we find that it is sharp.
:::

::: remark
If \( d\coloneqq{\operatorname{disc}}L \) is squarefree, then \( \ell(L) = 0 \) or 1 since \( A_L \cong {\mathbf{Z}}/d{\mathbf{Z}} \). This follows from writing \( d = {\sharp}A_L = \prod m_i \) as a product of coprime integers and applying the Chinese remainder theorem.
:::

::: remark
There is a short exact sequence
\[
0\to L/mL \hookrightarrow A_{L(m)}\twoheadrightarrow A_L \to 0
,\]
so if \( L \) is unimodular then \( A_{L(m)} \cong L/mL \cong {1\over m}L(m)/L(m) \).
:::

## \( p \)-elementary Lattices {#p-elementary-lattices}

::: {.definition title="$p$-elementary Lattices"}
A lattice \( (L, \beta) \) is **\( p \)-elementary** if \( A_L \) is a \( p \)-elementary abelian group, i.e. \( A_L \cong C_p^\ell \) for some \( \ell \).
:::

::: remark
For nondegenerate integral lattices \( (L, \beta) \) , one can compute \( A_L \cong \bigoplus_{i=1}^n {\mathbf{Z}}/d_i {\mathbf{Z}} \) where \( d_i \) are the invariant factors of \( L \), found as diagonal entries in the Smith normal form of \( G_\beta \).

For example, for \( L = V(2) \), we have \( G_\beta = { \begin{bmatrix} {4} & {2}  \\ {2} & {4} \end{bmatrix} } \) and \( \mathrm{SNF}(G_\beta) = { \begin{bmatrix} {2} & {0}  \\ {0} & {6} \end{bmatrix} } \), and thus \( A_L \cong {\mathbf{Z}}/2{\mathbf{Z}}\oplus {\mathbf{Z}}/6{\mathbf{Z}} \).
:::

::: {.definition title="Co-even/Co-odd"}
Let \( L \) be a 2-elementary lattice. We say

-   \( L \) is **Type I** if \( q(A_L) \subseteq {1\over 2}{\mathbf{Z}}/{\mathbf{Z}} \), or
-   \( L \) is **Type II** if \( q(A_L) \subseteq {1\over 4}{\mathbf{Z}}/{\mathbf{Z}}\setminus{1\over 2}{\mathbf{Z}}/{\mathbf{Z}} \).
:::

::: example
\( {\mathfrak{u}}(2) \coloneqq A_{U(2)} \) is Type I, and \( \left[ {1} \right] = A_{\left\langle{2}\right\rangle} \) is Type II.
:::

::: {.definition title="Coparity"}
If \( L \) is a 2-elementary lattice, we define the **coparity** as
\[
\delta(L) \coloneqq
\begin{cases}
0 & q_{A_L}(A_L) \subseteq {1\over 2}{\mathbf{Z}}/{\mathbf{Z}}\cong {\mathbf{Z}}/2{\mathbf{Z}}\\
1 & \text{otherwise}
\end{cases}
.\]
We say \( L \) is **co-even** if \( \delta = 0 \), and **co-odd** if \( \delta = 1 \).
:::

## Reflections and transvections

::: {.definition title="Reflections"}
`\label[definition]{def:reflections}`{=tex} Let \( (L, \beta) \) be a nondegenerate lattice and let \( \alpha\in L \) be an anisotropic vector satisfying
\[
2\beta(\alpha, L) \subseteq \beta(\alpha, \alpha){\mathbf{Z}}
.\]
Then the **reflection in \( \alpha \)** is the isometry
\[
s_\alpha(x) \coloneqq x - 2{\beta(\alpha, x) \over \beta(\alpha, \alpha) } \alpha \in {\operatorname{O}}^*(L)
,\]
so in particular \( s_\alpha \) acts trivially on \( A_L \). Similarly, if \( (L, q) \) is a quadratic lattice with \( \alpha\in L \) satisfying \( q(\alpha)\in R^{\times} \), we set
\[
s_\alpha(x) \coloneqq x - {\beta_q(\alpha, x) \over q(\alpha)}\alpha \in {\operatorname{O}}(L, q)
.\]
We define the **Weyl group of \( L \)** by \( W(L) \coloneqq\left\langle{s_\alpha {~\mathrel{\Big\vert}~}\alpha \in L,\,\, 2\beta(\alpha,L) \subseteq \beta(\alpha,\alpha){\mathbf{Z}}}\right\rangle {~\trianglelefteq~}{\operatorname{O}}(L) \).

More generally, for \( f\in {\operatorname{O}}(L) \) is a **generalized reflection** if there exists a subspace \( S \leq L_k \) such that
\[
{ \left.{{f}} \right|_{{S}} } = \operatorname{id}_S, \qquad { \left.{{f}} \right|_{{S^{\perp L} }} } = -\operatorname{id}_{S^{\perp L}}
.\]
:::

::: remark
Equivalently, \( v \) corresponds to a generalized reflection, i.e. \( s_v(L) = L \), if and only if \( v^2 \) divides \( 2\operatorname{div}_L(v) \). This is automatically satisfied if \( v^2\in \left\{{\pm 1,\pm 2}\right\} \), and the converse is only true if \( L \) is unimodular. Note that if \( L \) is even, there are no vectors of norm \( \pm 1 \).
:::

::: lemma
Reflections satisfy the following properties:

-   \( s_\alpha( \pm \alpha) = \mp \alpha \), so \( s_\alpha(\left\langle{\alpha}\right\rangle) = \left\langle{\alpha}\right\rangle \),
-   \( s_\alpha = s_{-\alpha} \),
-   \( { \left.{{s_\alpha}} \right|_{{\left\langle{\alpha}\right\rangle^{\perp L}}} } = \operatorname{id}_{\left\langle{ \alpha}\right\rangle^{\perp L}} \),
-   \( s_\alpha^2 = \operatorname{id}_L \), and \(  \mathrm{Fix}_L(s_\alpha) \) is the hyperplane orthogonal to \( \alpha \),
-   \( s_\alpha \) is uniquely determined by the hyperplanes \( \ker(\operatorname{id}- s_\alpha) \) and \( \ker(\operatorname{id}+ s_\alpha) \),
-   \( s_{\alpha \beta} = s_\alpha^{-1}\circ s_\beta \circ s_\alpha \),
-   If \( \alpha \) is primitive, there is a basis \( B = \left\{{\alpha, e_2,\cdots, e_n}\right\} \) such that \( s_{\alpha} \) takes the form
    \[
    s_\alpha = \left(\begin{array}{cccc}-1 & * & \cdots & * \\ 0 & 1 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & 1\end{array}\right)
    .\]
-   \( \operatorname{det}s_\alpha = -1 \).
:::

::: {.definition title="Eichler transvections"}
Let \( e\in L_{\mathbf{Q}} \) with \( \beta_{\mathbf{Q}}(e, e) = 0 \) and let \( a\in \left\langle{e}\right\rangle^{\perp L_{\mathbf{Q}}} \). Then the map
\[
E_{e, a}(v) \coloneqq v - \beta(a,v)e
\]
is in \( {\operatorname{O}}(\left\langle{e}\right\rangle^{\perp L}) \). It extends to a unique element in \( {\operatorname{O}}(L_{\mathbf{Q}}) \) defined by
\[
E_{e, a}(v) \coloneqq v - \beta(a,v)e + \beta(e,v)a -{1\over 2}\beta(a,a) \beta(e,v)e
.\]
We define the **Eichler transvection group of \( L \)** as
\[
E(L) \coloneqq\left\{{E_{e, a} {~\mathrel{\Big\vert}~}\beta(e,e) = \beta(e, a) = 0, \operatorname{div}_L(e) = 1}\right\} \leq {\operatorname{SO}}^+(L)
\]
where \( {\operatorname{SO}}^+(L) = {\operatorname{SO}}(L) \cap\ker{\left\lVert {{-}} \right\rVert}_{ \mathrm{sp}} \). In particular, by a theorem of Eichler, if \( L \) is an even lattice then \( E(L) \leq {\operatorname{O}}^*(L) \).
:::

::: remark
Note that `\cite{Sca87}`{=tex} defines
\[
E_{f,x}(y) \coloneqq y + \beta(y,x)f - {1\over 2}\beta(x,x)\beta(y,f)f - \beta(y,f)x
.\]
:::

::: remark
Note that if \( v \) is nonisotropic and \( v-w \) is not isotropic, then the (generally rational) reflection \( s_{v-w} \) maps \( w \) to \( v \).
:::

::: lemma
Eichler transvections satisfy the following properties:

-   \( E_{e, a+b} = E_{e, a}\circ E_{e, b} \),
-   \( { \left.{{E_{e, a}}} \right|_{{e^{\perp} \cap a^{\perp}}} } = \operatorname{id} \),
-   \( E_{e, a}^{-1}= E_{e, -a} \),
-   \( E_{e, a}(e) = e \).
:::

::: lemma
Let \( L = U^2 = U_1 \oplus U_2 \) be two copies of \( U \) with a basis \( L = \left\langle{e_1, f_1, e_2, f_2}\right\rangle \). Then any \( v\in L \) is in the \( E(L) \) orbit of an element of the form \( a(e_1 + bf_1)\in U_1 \).
:::

::: proof
A proof is given, for example, in `\cite[Ex. 3.7.2]{Sca87}`{=tex}. We form the isometry `\begin{align*}
L & { \, \xrightarrow{\sim}\, }(\operatorname{Mat}_{2\times 2}({\mathbf{Z}}), 2\operatorname{det}) \\
ae_1 + bf_1 + ce_2 + df_2 &\mapsto { \begin{bmatrix} {a} & {c}  \\ {-d} & {b} \end{bmatrix} }
\end{align*}`{=tex} Then elements of \( E(L) \) correspond to row and column additions, which correspond to left and right multiplication by the matrices
\[
{ \begin{bmatrix} {1} & {0}  \\ {1} & {1} \end{bmatrix} }, \qquad { \begin{bmatrix} {1} & {1}  \\ {0} & {1} \end{bmatrix} }
.\]
These can be used to put any such matrix in in Smith normal form, which in the \( 2\times 2 \) case will be a matrix of the form \( { \begin{bmatrix} {a} & {0}  \\ {0} & {ab} \end{bmatrix} } \) where \( a,b\in {\mathbf{Z}} \) are uniquely determined up to sign.

However, one can show that \( v\sim_{E(L)} -v \), and so this ambiguity is not an issue modulo \( E(L) \). A computation then shows that
\[
E_{e_2, -f_1} \circ E_{f_2, -2v} \circ E_{e_2, -f_1}
\]
maps \( v \) to \( -v \).

TODO show computation.
:::

::: corollary
If \( L = U^2 \), then \( E(L) \) acts transitively on \( L[k] \) for any \( k \).
:::

::: {.proposition title="{\\cite[Prop 3.7.3]{Sca87}}"}
Let \( L \) be an even lattice that decomposes as \( L  { \, \xrightarrow{\sim}\, }U^2 \oplus M \) where \( M \) is any lattice, and suppose \( v,w\in L[k] \) for some fixed \( k \). Then
\[
v\sim_{E(L)} w \iff [v^*] = [w^*]\in A_L
.\]
:::

::: proof
Suppose that \( \phi(v) = w \) for some \( \phi\in E(L) \). Then necessarily \( \phi^*([v^*]) = [w^*] \) in \( A_L \) by restriction. However, \( E(L) \subseteq {\operatorname{O}}^*(L) \), so \( \phi \) must induce the identity on \( A_L \) and thus \( [v^*] = [w^*] \).

Suppose now that \( [v^*] = [w^*] \) in \( A_L \). Write \( L = U_1 \oplus U_2 \oplus M \); then by the above proposition we may assume that \( v,w\in L' \coloneqq M \oplus U_1 \) up to \( E(U_1 \oplus U_2) \). Since \( [v^*] = [w^*] \), in particular these elements have the same order in \( A_L \), and so \( \operatorname{div}_L(v) = \operatorname{div}_L(w) = d \) is a fixed positive integer. Thus there exist \( x,y\in L' \) such that \( \beta(x,v) = d \) and \( \beta(y, w) = d \). We now claim that \( z \coloneqq{v\over d} - {w\over d} = {v-w\over d} \) is an element of \( M \oplus U_1 \). This follows from the fact that \( v^* \equiv w^* \pmod{L'} \), so \( {v\over d} \equiv {w\over d} \pmod{L'} \). Thus \( z\coloneqq{v\over d} - {w\over d}\equiv 0\operatorname{mod}L \)is an element of \( L' \).

We now claim that
\[
E_{e, y} \circ E_{f, -z} \circ E_{e, -x}
\]
maps \( v \) to \( w \). This uses the fact that \( dz^2 = 2vz \).

TODO computation.
:::

## Isotropic Submodules

::: {.definition title="Isotropic submodules"}
Let \( (L, \beta) \) be a nondegenerate lattice. A submodule \( W \) is **isotropic** if \( { \left.{{\beta}} \right|_{{W}} } = 0 \), or equivalently if \( W \subseteq W^{\perp L} \).
:::

::: {.definition title="Witt index"}
Let \( (L, \beta) \) be a nondegenerate lattice. The **Witt index** \( \mathrm{WI}(L) \) of \( L \) is the maximal rank of an isotropic sublattice.
:::

::: remark
One generally has \( \mathrm{WI}(L_{\mathbf{Q}}) \leq W(L_{\mathbf{R}}) \), often with strict inequality. If \( L \) is nondegenerate of signature \( (p, q) \), then \( \mathrm{WI}(L_{\mathbf{R}}) = \min\left\{{p, q}\right\} \).
:::

::: {.definition title="Lagrangian submodules"}
A submodule \( W\leq L \) with \( \operatorname{rank}_ZZ(W) = \mathrm{WI}(L) \) is called a **maximally isotropic** or **Lagrangian** sublattice.
:::

::: proposition
If \( (L, \beta) \) is a nondegenerate lattice of rank \( n \), then \( \mathrm{WI}(L) \leq {1\over 2}n \).
:::

::: proof
Using the previous proposition, since \( W \subseteq W^{\perp} \) we have \( \operatorname{rank}_ZZ(W) \leq \operatorname{rank}_ZZ(W^{\perp}) \), so
\[
n = \operatorname{rank}_ZZ(L) = \operatorname{rank}_ZZ(W) + \operatorname{rank}_ZZ(W^{\perp}) \leq \operatorname{rank}_ZZ(W^\perp) + \operatorname{rank}_ZZ(W^{\perp}) = 2\operatorname{rank}_ZZ(W^{\perp}) \implies \operatorname{rank}_ZZ(W^{\perp}) \geq n/2
\]
and thus
\[
\operatorname{rank}_ZZ(W) = \operatorname{rank}_ZZ(L) - \operatorname{rank}_ZZ(W^\perp) \leq n - (n/2) = n/2
.\]
:::

## Examples of Lattices

::: {.example title="Particularly important lattices"}
The following are some of the most prominent examples of lattices:

1.  (**Diagonal rank 1 lattices**) For any nonzero \( n\in {\mathbf{Z}} \), let \( L \coloneqq\left\langle{v}\right\rangle_{\mathbf{Z}} \) be generated by a single element \( v \) with \( \beta(v,v) \coloneqq n \). This lattice can also be written as \( \left\langle{n}\right\rangle \), although it is sometimes useful to keep \( v \) in the notation, e.g. when this corresponds to a sublattice of an ambient lattice \( L \) with a fixed, named basis and \( v\in L \). This lattice can be written as the twist \( \left\langle{n}\right\rangle = \left\langle{1}\right\rangle(n) \). We have the following properties:

      --------------------------------------------------------------------------------------------------------------------------------------------------------
      Property                                 Explanation
      ---------------------------------------- ---------------------------------------------------------------------------------------------------------------
      Rank                                     \( \operatorname{rank}(\left\langle{n}\right\rangle) = 1 \).

      Decomposability                          Indecomposable for any \( n \).

      Degeneracy                               Nondegenerate for \( n\geq 0 \).

      Discriminant                             \( {\operatorname{disc}}(\left\langle{n}\right\rangle) = n \).

      Signature                                \( \operatorname{sig}(\left\langle{n}\right\rangle) = (1, 0) \) if \( n > 0 \) and \( (0, 1) \) if \( n<0 \).

      Modularity                               Unimodular if and only if \( n=\pm 1 \).

      Definiteness                             Positive-definite if \( n>0 \) and negative-definite if \( n<0 \).

      Integrality                              Integral \( \iff n\in {\mathbf{Z}} \).

      Parity                                   Even \( \iff n\in 2{\mathbf{Z}} \).

      Dual lattice                             \( \left\langle{n}\right\rangle {}^{ \vee }= \left\langle{1\over n}\right\rangle \).

      Length                                   \( \ell(\left\langle{n}\right\rangle) = 1 \).

      Discriminant group                       \( A_{\left\langle{n}\right\rangle} = C_n \).

      Quadratic form                           \( \left[ {n} \right] \).
      --------------------------------------------------------------------------------------------------------------------------------------------------------

    Note that if \( \left\langle{n}\right\rangle \) is generated by an element \( v \), we can write \( \left\langle{n}\right\rangle  {}^{ \vee }= \left\langle{{1\over n} v}\right\rangle_{\mathbf{Z}} \).

2.  (**Type \(  {\textrm{I}}  \) lattices**) For any positive integer \( n \) and non-negative integers \( 0\leq p, q \leq n \) with \( p+q=n \), let \( L = \left\langle{v_1,\cdots, v_p, w_1, \cdots, w_p}\right\rangle \cong {\mathbf{Z}}^n \) be generated by \( p+q \) elements where
    \[
     \beta(v_i, v_j) = \delta_{ij}, \quad
     \beta(w_i, w_j) = -\delta_{ij}, \quad
     \beta(v_i, w_j) = 0 \,\, \forall i,j
     .\]
    The Gram matrix is diagonal with \( p \) copies of \( +1 \) and \( q \) copies of \( -1 \), i.e.
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
     \operatorname{id}_{p\times p} & 0 \\
     \hline
     0 & -\operatorname{id}_{q\times q}
     \end{array}\right]
     \in \operatorname{Mat}_{p\times p}({\mathbf{Z}}) \times \operatorname{Mat}_{q\times q}({\mathbf{Z}})
     .\]
    We write this lattice as
    \[
      {\textrm{I}} _{p, q} \coloneqq\left\langle{1,1,\cdots, -1, -1}\right\rangle \coloneqq\left\langle{1}\right\rangle^{\oplus p} \oplus \left\langle{-1}\right\rangle^{\oplus q}
     .\]

    It is

      --------------------------------------------------------------------------------------------------------------------------------------------------
      Property                                 Explanation
      ---------------------------------------- ---------------------------------------------------------------------------------------------------------
      Rank                                     \( \operatorname{rank}( {\textrm{I}} _{p, q}) = p+q \).

      Decomposability                          Decomposable into rank 1 sublattices.

      Degeneracy                               Nondegenerate unless \( p=q=0 \).

      Discriminant                             \( {\operatorname{disc}}( {\textrm{I}} _{p, q}) = (-1)^q \).

      Signature                                \( \operatorname{sig}( {\textrm{I}} _{p, q}) = (p, q) \).

      Modularity                               Unimodular for any \( p,q\geq 0 \).

      Definiteness                             Positive-definite if \( p>0, q=0 \), negative-definite if \( p=0,q>0 \), indefinite if \( p,q\geq 1 \).

      Integrality                              Integral for any \( p,q\geq 0 \).

      Parity                                   Odd for any \( p,q\geq 0 \).

      Dual lattice                             \( \left\langle{n}\right\rangle {}^{ \vee }= \left\langle{1\over n}\right\rangle \).

      Length                                   \( \ell(I_{p, q}) = 0 \).

      Discriminant group                       \( A_{ {\textrm{I}} _{p, q}} = 0 \).

      Quadratic form                           \( \left[ {1} \right]^{\oplus p} \oplus \left[ {-1} \right]^{\oplus q} \).
      --------------------------------------------------------------------------------------------------------------------------------------------------

    We occasionally use the notation
    \[
      {\textrm{I}} _{p, 0} \coloneqq\left\langle{1}\right\rangle^{\oplus p}, \qquad  {\textrm{I}} _{0, q} \coloneqq\left\langle{-1}\right\rangle^{\oplus q}
     .\]

    Moreover, noting that \( G_\beta^{-1}= G_\beta \) for the Gram matrix, we can identify \( v_i {}^{ \vee }= v_i, w_i {}^{ \vee }= w_i \) for all \( i \).

3.  (**The hyperbolic lattice**) Let \( L \coloneqq\left\langle{e, f}\right\rangle_{\mathbf{Z}} \) be generated by two elements \( e,f \) satisfying \( \beta(e, f) = \beta(f, e) = 1 \) and \( \beta(e, e) = \beta(f,f) = 0 \). We write this lattice as \( U \), the **hyperbolic lattice**, which has Gram matrix
    \[
     G_{U} = { \begin{bmatrix} {0} & {1}  \\ {1} & {0} \end{bmatrix} } \in \operatorname{Mat}_{2\times 2}({\mathbf{Z}})
     .\]

    It is

    -   Of rank 2,
    -   Indecomposable,
    -   Satisfies \( \operatorname{sig}(U) = (1, 1) \),
    -   Satisfies \( {\operatorname{disc}}(U) = -1 \),
    -   Nondegenerate,
    -   Integral,
    -   Even,
    -   Unimodular,
    -   Can be written as \(  {\textrm{II}} _{1, 1} \), defined below,
    -   Has quadratic form \( q_U(x,y) = 2xy \),
    -   Has associated quadratic lattice \( {\mathfrak{q}}\coloneqq\left[ {2} \right] \),
    -   Has \( A_L = 0 \) and \( \ell=0 \).

4.  (**The \( E_8 \) lattice**) Let \( L = \left\langle{\alpha_1, \cdots, \alpha_8}\right\rangle_{\mathbf{Z}} \) be generated by 8 elements whose Gram matrix is the following:
    \[
     G_{E_8} \coloneqq
     \left[\begin{array}{rrrrrrrr}
     -2 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
     0 & -2 & 0 & 1 & 0 & 0 & 0 & 0 \\
     1 & 0 & -2 & 1 & 0 & 0 & 0 & 0 \\
     0 & 1 & 1 & -2 & 1 & 0 & 0 & 0 \\
     0 & 0 & 0 & 1 & -2 & 1 & 0 & 0 \\
     0 & 0 & 0 & 0 & 1 & -2 & 1 & 0 \\
     0 & 0 & 0 & 0 & 0 & 1 & -2 & 1 \\
     0 & 0 & 0 & 0 & 0 & 0 & 1 & -2
     \end{array}\right] \in \operatorname{Mat}_{8\times 8}({\mathbf{Z}})
     .\]
    We write this lattice as \( E_8 \), noting that it is precisely the lattice that arises from the Dynkin diagram of the \( E_8 \) root lattice: \[

    E_8: `\qquad `{=tex}`\dynkin[label, edge length=.75cm]`{=tex}E8 ,\] where we explain the precise procedure in `\Cref{sec:coxeter_vinberg_diagrams}`{=tex}. Note that we take the *negative*-definite version of this lattice by convention.

    > TODO: reference.

    This lattice

    -   Of rank 8,
    -   Indecomposable,
    -   Has \( \operatorname{sig}(E_8) = (0, 8) \),
    -   Is nondegenerate,
    -   Is negative-definite,
    -   Has \( {\operatorname{disc}}(E_8) = 1 \),
    -   Is unimodular, so \( E_8 {}^{ \vee }\cong E_8 \),
    -   Is integral,
    -   Is even,
    -   Can be written as \(  {\textrm{II}} _{0, 8} \), which is defined below.
    -   Has \( A_L = 0 \) and \( \ell = 0 \).

    We occasionally use the dual basis \( w_1, \cdots, w_8 \coloneqq\alpha_1 {}^{ \vee }, \cdots, \alpha_8 {}^{ \vee } \). Noting that the inverse Gram matrix is given by
    \[
     G_{E_8}^{-1}=
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
    we can write each \( w_i \) in the \( \alpha_i \) basis using its columns, i.e.  `\begin{align*}
     w_1 &= -4 \alpha_1 -5 \alpha_2 -7 \alpha_3 -10 \alpha_4 -8 \alpha_5 -6 \alpha_6 -4 \alpha_7 -2 \alpha_8 \\
     w_2 &= -5 \alpha_1 -8 \alpha_2 -10 \alpha_3 -15 \alpha_4 -12 \alpha_5 -9 \alpha_6 -6 \alpha_7 -3 \alpha_8 \\
     \vdots
     \end{align*}`{=tex} and so on.

5.  (**Type \(  {\textrm{II}}  \) lattices**) For \( p, q\in {\mathbf{Z}}_{\geq 0} \), define `\begin{align*}
      {\textrm{II}} _{p, q}
     \begin{cases}
     E_8(-1)^{\oplus {\tau \over 8}} \oplus U^{\oplus q}, & p-q > 0 \\
     E_8^{\oplus {-\tau \over 8}} \oplus U^{\oplus p}, & p-q < 0
     \end{cases}
     \end{align*}`{=tex} where \( E_8 \) is the **negative**-definite \( E_8 \) lattice defined above.

    This lattice

    -   Is of rank \( p + q \),
    -   Is generally decomposable (by construction),
    -   Has \( \operatorname{sig}( {\textrm{II}} _{p, q}) = (p, q) \)
    -   Is integral,
    -   Is even,
    -   Is nondegenerate,
    -   Has \( {\operatorname{disc}}( {\textrm{II}} _{p, q}) = (-1)^p \),
    -   Is unimodular, so \(  {\textrm{II}} _{p, q} \cong  {\textrm{II}} _{p, q} {}^{ \vee } \), \( A_L = 0 \), and \( \ell = 0 \).

    We note that \( G_\beta^{-1} \) is generally nontrivial due to the \( E_8 \) factors, making the dual basis somewhat nontrivial.

6.  Let \( L = \left\langle{v, w}\right\rangle_{\mathbf{Z}} \) be generated by two elements with
    \[
     G_\beta = { \begin{bmatrix} {2} & {1}  \\ {1} & {2} \end{bmatrix} } \in \operatorname{GL}_2({\mathbf{Z}})
     .\]
    We write this lattice as \( V \).

    This lattice

    -   Is rank 2,
    -   Even,
    -   Nondegenerate,
    -   Not unimodular
    -   Satisfies \( {\operatorname{disc}}(V) = -3 \),
    -   Is of signature \( \operatorname{sig}(V) = (2, 0) \),
    -   Is positive-definite,
    -   Has bilinear form \( \beta(a, b) = 2a_1 b_1 + a_2 b_1 + a_1 b_2+ 2a_2 b_2 \),
    -   Has quadratic form \( q(x, y) = 2x^2 + 2xy + 2y^2 \)
    -   Has a quadratic lattice we denote by \( {\mathfrak{v}} \).
    -   Has \( A_L = C_3 \) and \( \ell = 1 \),

7.  For \( k\geq 0 \), define
    \[
     V_k \coloneqq V_{{\mathbf{Z}}_2}(2^k) = \qty{ {\mathbf{Z}}_2^2, { \begin{bmatrix} {2^{k+1}} & {2^k}  \\ {2^k} & {2^{k+1}} \end{bmatrix} }}
     .\]
    .

    This lattice \( V_k \)

    -   Is the polar form of \( q(x,y) = 2^k(x^2 + xy + y^2) \).
    -   is indecomposable,
    -   Satisfies \( {\operatorname{disc}}(V_k) = 3\cdot 2^{2k} \),
    -   We write its discriminant form as \( {\mathfrak{v}}_k \).
    -   Is \( A_{V_k} = 2^{-k}V_k/V_k \cong C_{2^k}^2 \) with quadratic form \( q(x,y) = 2^{-k}(x^2 + xy + y^2) \in {\mathbf{Q}}_2/{\mathbf{Z}} \)
    -   Has polar form \( { \begin{bmatrix} {2^{-k+1}} & {2^{-k}}  \\ {2^{-k}} & {2^{-k+1}} \end{bmatrix} } \).

8.  For \( k\geq 0 \), define
    \[
     U_k \coloneqq U_{{\mathbf{Z}}_2}(2^k) = \qty{{\mathbf{Z}}_2^2, { \begin{bmatrix} {0} & {2^k}  \\ {2^k} & {0} \end{bmatrix} } }
     \]
    over the 2-adic integers.

    The lattice \( U_k \)

    -   is the polar form of \( q(x,y) = 2^k xy \),
    -   Is indecomposable,
    -   Satifies \( {\operatorname{disc}}(U_0) = -1 \in {\mathbf{Z}}_2^{\times} \) and \( {\operatorname{disc}}(U_k) = -2^{2k} \),
    -   Has quadratic lattice we denote by \( {\mathfrak{u}}_k \),
    -   Has \( 2^{-k} U_k/U_k \cong C_{2^k}^2 \) with quadratic form \( q(x,y) = 2^{-k}xy \in {\mathbf{Q}}_2/{\mathbf{Z}} \)
    -   Has polar form \( { \begin{bmatrix} {0} & {2^{-k}}  \\ {2^{-k}} & {0} \end{bmatrix} } \).

9.  Let
    \[
     L \coloneqq\left\{{{ \begin{bmatrix} {a} & {b}  \\ {c} & {d} \end{bmatrix} } \in \operatorname{Mat}_{2\times 2}({\mathbf{Z}}) {~\mathrel{\Big\vert}~}c\in 2{\mathbf{Z}}}\right\}
     \]
    and define \( q(x) \coloneqq 2\operatorname{det}(x) \). The associated bilinear form \( \beta(x,y) \coloneqq 2\qty{ \operatorname{det}(x+y) - \operatorname{det}(x) - \operatorname{det}(y)} \) is \( {\mathbf{Z}} \)-valued and thus \( (L, \beta) \) is a lattice.

    This lattice

    -   Is rank 4,
    -   Has signature \( \operatorname{sig}(L) = (2, 2) \),
    -   Is indefinite,
    -   Is even,
    -   Has \( {\operatorname{disc}}(L) = 4 \),
    -   Is not unimodular,
    -   Is 2-elementary with invariants \( (4,2,0) \),
    -   Has \( A_L = C_2^2 \),
    -   Is decomposable,
    -   Admits an isometry `\begin{align*}
         U \oplus U(2) & { \, \xrightarrow{\sim}\, }L \\
         (a,b) \oplus (c, d) &\mapsto { \begin{bmatrix} {a} & {c}  \\ {-2d} & {b} \end{bmatrix} }
         \end{align*}`{=tex}

We summarize some relevant properties of the above lattices and some related variants:

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  \( L \)                              \( \operatorname{rank}(L) \)   \( \operatorname{sig}(L) \)   Definiteness                  Parity                      Decomposable?      \( {\operatorname{disc}}(L) \)   Unimodular?          \( L {}^{ \vee } \)                                                        \( \ell(L) \)   \( A_L \)
  ------------------------------------ ------------------------------ ----------------------------- ----------------------------- --------------------------- ------------------ -------------------------------- -------------------- -------------------------------------------------------------------------- --------------- -------------------------
  \( \left\langle{n}\right\rangle \)   \( 1 \)                        \( (1, 0) \)                  Positive                      Even \( \iff n \) is even   No                 \( n \)                          \( \iff n=\pm 1 \)   \( {1\over n }\left\langle{n}\right\rangle \)                              \( 1 \)         \( C_n \)

  \( U \)                              \( 2 \)                        \( (1, 1) \)                  Indefinite                    Even                        No                 \( -1 \)                         Yes                  \( U \)                                                                    \( 0 \)         \( 0 \)

  \( U(2) \)                           \( 2 \)                        \( (1, 1) \)                  Indefinite                    Even                        No                 \( -4 \)                         No                   \( {1\over 2}U(2) \)                                                       \( 2 \)         \( C_2^2 \)

  \( E_8 \)                            \( 8 \)                        \( (0, 8) \)                  Negative                      Even                        No                 \( 1 \)                          Yes                  \( E_8 \)                                                                  \( 0 \)         \( 0 \)

  \( E_8(2) \)                         \( 8 \)                        \( (0, 8) \)                  Negative                      Even                        No                 \( 256 \)                        No                   \( {1\over 2}E_8(2) \)                                                     \( 8 \)         \( C_2^8 \)

  \(  {\textrm{I}} _{p, q} \)          \( p+q \)                      \( (p, q) \)                  Indefinite \( \iff p,q>0 \)   Odd                         Yes                \( (-1)^q \)                     Yes                  \(  {\textrm{I}} _{p, q} \)                                                \( 0 \)         \( 0 \)

  \(  {\textrm{I}} _{p, q}(2) \)       \( p+q \)                      \( (p, q) \)                  Indefinite \( \iff p,q>0 \)   Even                        Yes                \( (-2)^q \)                     No                   \( {1\over 2} {\textrm{I}} _{p, q}(2) \)                                   \( p+q \)       \( C_2^{p+q} \)

  \(  {\textrm{II}} _{p, q} \)         \( p+q \)                      \( (p, q) \)                  Indefinite \( \iff p,q>0 \)   Even                        \( \iff p,q>0 \)   \( (-1)^q \)                     Yes                  \(  {\textrm{II}} _{p, q} \)                                               \( 0 \)         \( 0 \)

  \(  {\textrm{II}} _{p, q}(2) \)      \( p+q \)                      \( (p, q) \)                  Indefinite \( \iff p,q>0 \)   Even                        \( \iff p,q>0 \)   \( 2^p (-2)^q \)                 No                   \( {1\over 2} {\textrm{II}} _{p, q}(2) \)                                  \( p+q \)       \( C_2^{p+q} \)

  \( V \)                              \( 2 \)                        \( (2, 0) \)                  Positive                      Even                        No                 \( 3 \)                          No                   \( {1\over 6}\left\langle{v_1, v1 + 3v_2}\right\rangle_{\mathbf{Z}} \)     \( 2 \)         \( C_2\times C_6 \)

  \( V(2) \)                           \( 2 \)                        \( (2, 0) \)                  Positive                      Even                        No                 \( 12 \)                         No                   \( {1\over 12}\left\langle{v_1, v_1 + 3v_2}\right\rangle_{\mathbf{Z}} \)   \( 2 \)         \( C_4 \times C_{12} \)
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Of particular importance are

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  \( (L, \beta) \)                                                                                      \( (A_L, q) \)                                                                                                                                     Co-even/Co-odd     \( \operatorname{sig}(A_L) \)
  ----------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------- ------------------ -------------------------------
  \( \left\langle{2}\right\rangle \coloneqq\qty{{\mathbf{Z}}^2, \left[ {2} \right] } \)                 \( p \coloneqq{\mathfrak{q}}_1(2) \coloneqq\qty{C_2, \left[ {1\over 2} \right]} \)                                                                 Co-odd             \( 1 \)

  \( \left\langle{-2}\right\rangle \coloneqq\qty{{\mathbf{Z}}^2, \left[ {-2} \right]} \)                \( q \coloneqq{\mathfrak{q}}_1(-2) \coloneqq\qty{C_2, \left[ {-{1\over 2}} \right] } \)                                                            Co-odd             \( -1 \)

  \( U(2) = \qty{{\mathbf{Z}}^2, { \begin{bmatrix} {0} & {2}  \\ {2} & {0} \end{bmatrix} }} \)          \( u \coloneqq{\mathfrak{u}}(2) \coloneqq\qty{C_2, { \begin{bmatrix} {0} & {1\over 2}  \\ {1\over 2} & {0} \end{bmatrix} }} \)                     Co-even            \( 0 \)

  \( V(2) \coloneqq\qty{{\mathbf{Z}}^2, { \begin{bmatrix} {4} & {2}  \\ {2} & {4} \end{bmatrix} }} \)   \( v \coloneqq{\mathfrak{v}}(2) \coloneqq\qty{C_2 \times C_6, { \begin{bmatrix} {1} & {1\over 2}  \\ {1\over 2} & {1\over 3} \end{bmatrix} }} \)   Co-even            \( 4 \)
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

By `\cite[\S 2.6]{nonsymplectic_involutions}`{=tex} and `\cite[Prop. 1.8.1]{nikulin1979integer-symmetric}`{=tex}, if \( L \) is an even 2-elementary lattice, then \( A_L \) can be written as a finite direct sum of the discriminant forms \( p,q,u,v \) above, subject to relations `\begin{align*}
u^{\oplus 2} &= v^{\oplus 2} \\
p^{\oplus 4} &= q^{\oplus 4} \\
u \oplus p &= (p \oplus q) \oplus p \\
u \oplus q &= (p \oplus q) \oplus q \\
v \oplus p &= q^{\oplus 3} \\
v \oplus q &= p^{\oplus 3}
\end{align*}`{=tex}

Moreover, the even 2-elementary lattices that admit a primitive embedding into \(  {L_{\mathrm{K3}}}  \) are finite direct sums of the following lattices, whose discriminant forms are recorded as well:

  ---------------------------------------------------------------------------------------------------------------------------
  Lattice \( L \)                      Discriminant Form \( A_L \)                                  Co-even/Co-odd
  ------------------------------------ ------------------------------------------------------------ -------------------------
  \( A_1 \)                            \( q \coloneqq{\mathfrak{q}}_1(-2) \)                        Co-odd

  \( D_4 \)                            \( v \coloneqq{\mathfrak{v}}(2) \)                           Co-even

  \( D_6 \)                            \( p^{\oplus 2} \coloneqq{\mathfrak{q}}_1(2)^{\oplus 2} \)   Co-odd

  \( D_8 \)                            \( u \coloneqq{\mathfrak{u}}(2) \)                           Co-even

  \( E_7 \)                            \( p \coloneqq{\mathfrak{q}}_1(2) \)                         Co-odd

  \( E_8 \)                            \( 0 \)                                                      Co-even

  \( E_8(2) \)                         \( u^{\oplus 4}\coloneqq{\mathfrak{u}}(2)^{\oplus 4} \)      Co-even

  \( \left\langle{2}\right\rangle \)   \( p \coloneqq{\mathfrak{q}}_1(2) \)                         Co-odd

  \( U \)                              \( 0 \)                                                      Co-even

  \( U(2) \)                           \( u \coloneqq{\mathfrak{u}}(2) \)                           Co-even
  ---------------------------------------------------------------------------------------------------------------------------
:::

::: {.proposition title="\\cite{gritsenkoHirzebruchMumfordVolumeOrthogonal2006}"}
Let \( L = \left\langle{2d}\right\rangle \), then

-   \( A_L = \left[ {-{1\over 2d}} \right] \cong C_{2d} \), and
-   \( {\sharp}{\operatorname{O}}(A_L) = 2^{\rho(d)} \),

where \( \rho(d) \) is the number of prime divisors of \( d \).
:::

::: proof
Write \( C_{2d} = \left\langle{v}\right\rangle \), where \( q(v) = -{1\over 2d}\operatorname{mod}2{\mathbf{Z}} \). If \( f\in {\operatorname{O}}(A_L) \), then \( f(v) = [\lambda] v \) for some \( 1\leq \lambda \leq 2d \) coprime to \( 2d \). For \( f \) to be an isometry, we must have \( v^2 = f(v)^2 = ([\lambda]v)^2 \), and thus
\[
v^2 = {-1\over 2d}\operatorname{mod}2{\mathbf{Z}}= [\lambda^2]\cdot v^2 \operatorname{mod}2{\mathbf{Z}}= {-\lambda^2 \over 2d}\operatorname{mod}2{\mathbf{Z}}\implies \lambda^2 = 1 \operatorname{mod}4d{\mathbf{Z}}
,\]
which has \( 2^{\rho(d)+1} \) solutions over \( C_{4d} \) and thus \( 2^{\rho(d)} \) solutions over \( C_{2d} \).
:::

::: corollary
Letting \( L_{2d}^{(m)} \coloneqq\left\langle{-2d}\right\rangle \oplus U^2 \oplus E_8^{\oplus m} \), we have \( {\sharp}{\operatorname{O}}(A_{L_{2d}^{(m)}}) = 2^{\rho(d)} \).
:::

::: proof
This follows from the fact that the summand \( U^2 \oplus E_8^{\oplus m} \) is unimodular.
:::

::: {.lemma title="{\\cite[Lem. 4.6]{geemenRemarksBrauerGroups2004}}"}
Define the family of lattices[^1]
\[
\Lambda_{n, k} \coloneqq\left\langle{e, f {~\mathrel{\Big\vert}~}e^2 = 2k,\, ef = fe = n,\, f^2 = 0}\right\rangle \cong \qty{{\mathbf{Z}}^2, { \begin{bmatrix} {2k} & {n}  \\ {n} & {0} \end{bmatrix} }}
.\]
There are exactly two primitive isotropic vectors (up to sign):
\[
\Lambda_{n, k}[0] = \left\{{v_1 \coloneqq f, v_2 \coloneqq{ne - kf \over d} }\right\},
\qquad \gcd(n, k) = d
.\]
Then
\[
{\operatorname{O}}(\Lambda_{n, k}) =
\begin{cases}
C_2^2 = \left\{{\pm \operatorname{id}, \pm J_{n, k}}\right\} & k=0 \text{ or } \qty{k\over d}^2 \equiv 1 \pmod{ \frac{n}{d} } \\
C_2 = \left\{{\pm \operatorname{id}}\right\} & \text{otherwise}
\end{cases}
\]
where \( J_{n, k} \) is the involution that swaps the isotropic vectors \( v_1 \) and \( v_2 \). Explicitly, in the basis \( \left\{{e, f}\right\} \), it is given by the matrix
\[
J_{n, k} = { \begin{bmatrix} {k\over d} & {n\over d}  \\ {-\ell} & {-{k\over d} } \end{bmatrix} }, \qquad\text{where }
\qty{k \over d}^2 - \qty{ n \over d}\ell = 1
.\]
:::

::: {.lemma title="{\\cite[Lem. 3.2, (ii)]{stellariRemarksFMpartnersK32005}, \\cite[Prop. 3.7]{geemenRemarksBrauerGroups2004}}"}
The lattices \( \Lambda_{n, k} \) and \( \Lambda_{n', k'} \) are in the same genus if and only if \( k=k' \) and \( n'\equiv \ell^2 n\pmod{k} \) for some \( \ell \) coprime to \( k \). Moreover, \( \Lambda_{n, k} \) is isometric to \( \Lambda_{n', k} \) if and only if \( n\equiv n'\pmod k \) or \( nn'\equiv 1\pmod k \).

In particular, if \( k=0 \), then \( { \operatorname{cl}}(\Lambda_{n, 0}) = 1 \) and \( \Lambda_{n, 0} \) is unique in its genus.
:::

::: corollary
For any positive integer \( n \), we have \( U(n) = \Lambda_{n, 0} \). So \( k=0, d=1, \ell = -{1\over n} \), and thus
\[
{\operatorname{O}}(U(n)) \cong \left\{{\pm \operatorname{id}, \pm { \begin{bmatrix} {0} & {n}  \\ {1\over n} & {0} \end{bmatrix} } }\right\}\cong C_2^2, \qquad { \operatorname{cl}}(U(n)) = 1
.\]
:::

::: {.lemma title="\\cite{meinsmaDerivedEquivalenceElliptic2024}"}
Let \( \Lambda_{n, k} = \left\langle{e, f}\right\rangle \) as above. Then \( {\operatorname{disc}}(\Lambda_{n, k}) = {\sharp}A_L = n^2 \), and
\[
\Lambda_{n, k} {}^{ \vee }= \left\langle{v_1^* \coloneqq-{2k\over n^2}f + {1\over n}e, v_2^* \coloneqq{1\over n} f}\right\rangle
\]
and
\[
A_{\Lambda_{n, k}} \cong C_a \oplus C_b = \left\langle{[v_1^*], [v_2^*]}\right\rangle, \quad
G_{q_{A_L}} = { \begin{bmatrix} {-{2k\over n^2}} & {1\over n}  \\ {1\over n} & {0} \end{bmatrix} } 
\]
where \( a \coloneqq\gcd(2k, n) \) and \( b \coloneqq{n^2\over a} \). In particular, we have
\[
\ell(\Lambda_{n, k}) = 
\begin{cases}
1 & \gcd(a, b) = 1 \\
2 & \text{otherwise}
\end{cases}
.\]
:::

::: corollary
For \( U(n) \coloneqq\Lambda_{n, 0} \), we have \( k=0 \) and thus \( a=b=n \), and thus
\[
A_{U(n)} = \left\langle{v_1^*, v_2^*}\right\rangle \coloneqq\left\langle{{1\over n} e, {1\over n} f}\right\rangle \cong C_n^2,\qquad
G_{A_{U(n)}} = { \begin{bmatrix} {0} & {1\over n}  \\ {1\over n} & {0} \end{bmatrix} }, \qquad 
\ell(U(n)) = 2
.\]
:::

::: lemma
There is an isometry `\begin{align*}
U_1 \oplus U_2 & { \, \xrightarrow{\sim}\, }(\operatorname{Mat}_{2\times 2}({\mathbf{Z}}), \operatorname{det}) \\
ae_1 + bf_1 + ce_2 + df_2 &\mapsto { \begin{bmatrix} {c} & {a}  \\ {b} & {-d} \end{bmatrix} }
\end{align*}`{=tex} which induces `\begin{align*}
{\operatorname{O}}(U_1 \oplus U_2) & { \, \xrightarrow{\sim}\, }{{\operatorname{SL}}_2({\mathbf{Z}})\times {\operatorname{SL}}_2({\mathbf{Z}}) \over \left\{{ \pm(\operatorname{id}, \operatorname{id}) }\right\}} \\
(B, A) &\mapsto (X\mapsto BXA^{-1})
\end{align*}`{=tex} Moreover,
\[
{\operatorname{SO}}^+(U_1 \oplus U_2) = \left\langle{E_{e_1, e_2}, E_{e_1, f_2}, E_{f_1, e_2}, E_{f_1, f_2} }\right\rangle
,\]
and any \( v\in U_1 \oplus U_2 \) satisfies \( v\sim_{{\operatorname{SO}}^+(U_1 \oplus U_2)} w \) for some \( w\in U_2 \).
:::

## Genera, Isometry Classes, and Completions

### The Genus

::: remark
We define the following notation when dealing with adelic rings:

-   If \( k \) is a global field with ring of integers \( R \) and \( v \) is a place of \( k \), we write \( \operatorname{Pl}(R) \coloneqq\operatorname{Pl}(k) \) for the set of places of \( k \), \( k_v \) and \( R_v \) respectively for the completions of \( k \) and \( R \) at \( v \), and define the adele ring as the restricted product
    \[
    {\mathbf{A}}_R \coloneqq{\mathbf{A}}_k \coloneqq\prod_{v\in \operatorname{Pl}(k)}' (R_v, k_v) \subseteq \prod_{v\in \operatorname{Pl}(k)} k_v
    \]
    consisting of sequences \( (x_v)_{v\in \operatorname{Pl}(k)} \) such that \( x_v\in R_v \) for all but finitely many \( v \).

-   \( \operatorname{Pl}({\mathbf{Z}}) \coloneqq\operatorname{Pl}({\mathbf{Q}}) = \operatorname{Spec}({\mathbf{Z}})\cup\left\{{\infty}\right\} \) is the set of places of \( {\mathbf{Z}} \), where we write \( v\in \operatorname{Pl}({\mathbf{Z}}) \) for a place and \( v=\infty \) for the Archimedean place \( {\mathbf{R}} \),

-   \( {\mathbf{Z}}_p \coloneqq\lim_{n\geq 1} {\mathbf{Z}}/p^n {\mathbf{Z}} \) for \( p \) a prime is the ring of \( p \)-adic integers, and its fraction field \( {\mathbf{Q}}_p \) is the ring of \( p \)-adic rationals,

-   \( \widehat{{\mathbf{Z}}} \) is the ring of profinite integers,
    \[
    \widehat{{\mathbf{Z}}} = \prod_{v < \infty} {\mathbf{Z}}_v = \lim_{n\geq 1} {\mathbf{Z}}/n{\mathbf{Z}}
    ,\]

-   \( {\mathbf{A}}_{\mathbf{Z}} \) is the ring of integral adeles,
    \[
    {\mathbf{A}}_{\mathbf{Z}}= \prod_{v \leq \infty} {\mathbf{Z}}_v = {\mathbf{R}}\times \widehat{{\mathbf{Z}}}
    .\]

-   \( {\mathbf{A}}^f_{\mathbf{Q}} \), is the ring of finite rational adeles,
    \[
    {\mathbf{A}}^f_{\mathbf{Q}}= \prod_{v < \infty}' {\mathbf{Q}}_v = \widehat{{\mathbf{Z}}}\otimes_{\mathbf{Z}}{\mathbf{Q}}
    ,\]
    and in this notation we can write \( {\mathbf{A}}_{\mathbf{Z}}^f \coloneqq\prod_{v<\infty}{\mathbf{Z}}_v = \widehat{{\mathbf{Z}}} \) for the ring of finite integral adeles,

-   \( {\mathbf{A}}_{\mathbf{Q}} \) is the full ring of rational adeles,
    \[
    {\mathbf{A}}_{\mathbf{Q}}\coloneqq{\mathbf{A}}_{\mathbf{Z}}\otimes_{\mathbf{Z}}{\mathbf{Q}}= {\mathbf{R}}\times {\mathbf{A}}^f_{\mathbf{Q}}= {\mathbf{R}}\times \prod_{p < \infty}' {\mathbf{Q}}_p = \prod_{v \leq \infty}' {\mathbf{Q}}_v
    .\]
:::

::: {.definition title="Genus"}
Let \( (L, \beta) \) be a nondegenerate lattice. We define the **genus** of \( L \) as
\[
{\operatorname{gen}}(L) \coloneqq{\operatorname{gen}}_{\mathbf{Z}}(L) \coloneqq\left\{{ (M, \beta_M) {~\mathrel{\Big\vert}~}M_{{\mathbf{A}}_{\mathbf{Z}}}  { \, \xrightarrow{\sim}\, }L_{{\mathbf{A}}_{\mathbf{Z}}} }\right\}
,\]
i.e. all lattices \( M \) such that \( M_{{ {\mathbf{Z}}_{\widehat{p}} }} \) is isometric to \( L_{{ {\mathbf{Z}}_{\widehat{p}} }} \) for all primes \( p \), including \( p=\infty \) corresponding to \( M_{\mathbf{R}} { \, \xrightarrow{\sim}\, }L_{\mathbf{R}} \).
:::

::: remark
In general, given a class of objects defined over a ring \( R \), we say they satisfy a **Hasse principle** (or a *local-global principle*) if whenever \( L_v \) is isomorphic to \( M_v \) for all places \( v \) of \( R \), then \( L \) is isomorphic to \( M \) over \( R \) itself. Note that \( {\mathbf{Q}} \)-lattices satisfy a Hasse principle: two lattices \( L, M \) over \( {\mathbf{Q}} \) are isometric (over \( {\mathbf{Q}} \)) if and only iff \( M_{{ {\mathbf{Q}}_{\widehat{p}} }} \) is isometric to \( L_{{ {\mathbf{Q}}_{\widehat{p}} }} \) over \( { {\mathbf{Q}}_{\widehat{p}} } \) for all primes \( p \), including \( p=\infty \). Thus \( {\operatorname{gen}}_{\mathbf{Q}}(L) =  \operatorname{Cl}_{\mathbf{Q}}(L) \) for lattices over \( {\mathbf{Q}} \). We summarize this in the following:
:::

::: {.theorem title="Hasse-Minkowski Theorem/Weak Hasse Principle"}
Let \( L, M \) be lattices defined over \( {\mathbf{Q}} \). Then
\[
{\operatorname{gen}}_{\mathbf{Q}}(L) = {\operatorname{gen}}_{\mathbf{Q}}(M) \iff  \operatorname{Cl}_{\mathbf{Q}}(L) =  \operatorname{Cl}_{\mathbf{Q}}(M)
.\]
i.e. \( L \) is isometric to \( M \) over \( {\mathbf{Q}} \) if and only if \( L_{{ {\mathbf{Q}}_{\widehat{p}} }} \) is isometric to \( M_{{ {\mathbf{Q}}_{\widehat{p}} }} \) over \( { {\mathbf{Q}}_{\widehat{p}} } \) for every prime \( p \) and \( L_{\mathbf{R}} { \, \xrightarrow{\sim}\, }M_{\mathbf{R}} \). Thus \( {\mathbf{Q}} \)-lattices satisfy the Hasse principle. In particular, for a fixed lattice \( L \), one has \( {\operatorname{gen}}_{\mathbf{Q}}(L) =  \operatorname{Cl}_{\mathbf{Q}}(L) \), and \( L \) is unique in its \( {\mathbf{Q}} \)-genus and thus unique up to isometry over \( {\mathbf{Q}} \).
:::

::: proof
For a proof of this, see `\cite[Thm. 1.3, \S 6.7]{casselsRationalQuadraticForms2008}`{=tex}.
:::

::: remark
This remains true if \( {\mathbf{Q}} \) is replaced by any number field \( K \), and \( { {\mathbf{Q}}_{\widehat{p}} } \) with \( K_v \) for all places \( v \) of \( K \).
:::

::: remark
If \( L, M \) are \( {\mathbf{Z}} \)-lattices (not necessarily isometric over \( {\mathbf{Z}} \)) and \( {\operatorname{gen}}(L) = {\operatorname{gen}}(M) \), then \(  \operatorname{Cl}_{\mathbf{Q}}(L_{\mathbf{Q}}) = {\operatorname{gen}}_{\mathbf{Q}}(L_{\mathbf{Q}}) = {\operatorname{gen}}_{\mathbf{Q}}(M_{\mathbf{Q}}) =  \operatorname{Cl}_{\mathbf{Q}}(M_{\mathbf{Q}}) \), so \( L_{\mathbf{Q}} \) is necessarily isometric to \( M_{\mathbf{Q}} \) over \( {\mathbf{Q}} \). So any invariant of \( L_{\mathbf{Q}} \) is an invariant of every lattice in \( {\operatorname{gen}}(L) \), e.g. the discriminant. A similar situation holds with \( {\mathbf{Q}} \) replaced by \( {\mathbf{R}} \), so any invariant of \( L_{\mathbf{R}} \) is an invariant of \( {\operatorname{gen}}(L) \), e.g. the signature.
:::

::: remark
Checking if two \( {\mathbf{Z}} \)-lattices are in the same genus is a computable problem: to see if \( L_{{ {\mathbf{Z}}_{\widehat{p}} }}  { \, \xrightarrow{\sim}\, }M_{{ {\mathbf{Z}}_{\widehat{p}} }} \), one can block-diagonalize their corresponding Gram matrices over \( { {\mathbf{Z}}_{\widehat{p}} } \) and check equivalence. Moreover, one only has to check the finite number of primes \( p \) dividing \( 2{\operatorname{disc}}(L)^2 \).
:::

::: remark
However, the Hasse principle does *not* hold for lattices over \( {\mathbf{Z}} \) -- lattices may be in the same genus, i.e. locally isometric at every prime \( p \), without being "globally" isometric over \( {\mathbf{Z}} \). Letting \( L \) be a \( {\mathbf{Z}} \)-lattice, recall that \(  \operatorname{Cl}(L) = \left\{{M {~\mathrel{\Big\vert}~}M { \, \xrightarrow{\sim}\, }L}\right\} \) is the set of lattices that are isometric to \( L \) over \( {\mathbf{Z}} \). Since \( M { \, \xrightarrow{\sim}\, }L \) implies \( M_{{\mathbf{A}}_{\mathbf{Z}}} { \, \xrightarrow{\sim}\, }L_{{\mathbf{A}}_{\mathbf{Z}}} \), there is an inclusion \(  \operatorname{Cl}(L) \subseteq {\operatorname{gen}}(L) \) which is generally not an equality.
:::

::: {.theorem title="{\\cite[Ch. 9, Thm 1.1]{casselsRationalQuadraticForms2008}}"}
Let \( L \) be a nondegenerate \( {\mathbf{Z}} \)-lattice. Then there are finitely many isometry classes of lattices in the genus of \( L \).
:::

::: remark
By `\cite[Ch. 9, \S 4]{casselsRationalQuadraticForms2008}`{=tex}, \( {\operatorname{gen}}(L) \) is a finite set, so \(  \operatorname{Cl}(L) \) is a finite set as well. Thus the genus of \( L \) is partitioned into finitely many isometry classes, motivating the following definition:
:::

::: {.definition title="Class number"}
Let \( (L, \beta) \) be a nondegenerate \( {\mathbf{Z}} \)-lattice. We define the **class number** of \( L \) to be the number of isometry classes in \( {\operatorname{gen}}(L) \).
:::

::: remark
By the above discussion, \( { \operatorname{cl}}(L) \) is finite, and we can write
\[
{\operatorname{gen}}(L) = \coprod_{i=1}^{{ \operatorname{cl}}(L)}  \operatorname{Cl}(L_i), \qquad {\sharp}{\operatorname{gen}}(L) = \sum_{i=1}^{{ \operatorname{cl}}(L)} {\sharp} \operatorname{Cl}(L_i)
\]
for some representatives \( L_i \) of each isometry class. Thus \( {\operatorname{gen}}(L) =  \operatorname{Cl}(L) \) if and only if \( { \operatorname{cl}}(L) = 1 \), and in particular, if \( { \operatorname{cl}}(L) = 1 \) then \( L \) is unique in its genus and unique up to isometry.
:::

::: lemma
Let \( L \) be a nondegenerate lattice. Then
\[
 \operatorname{Cl}(L) = 1 \iff  \operatorname{Cl}(L(n)) = 1 \qquad \forall n\in {\mathbf{Z}}\setminus\left\{{0}\right\}
.\]
This can be strengthened to
\[
 \operatorname{Cl}(L) = 1 \iff  \operatorname{Cl}(L(n)) = 1 \qquad \text{ for one } n\in {\mathbf{Z}}\setminus\left\{{0}\right\}
.\]
:::

### Stable Equivalence

::: {.definition title="Stably isometric"}
Let \( L_1, L_2 \) be lattices. We say \( L_1 \) is **stably isometric** to \( L_2 \) if there exist unimodular lattices \( P_1, P_2 \) such that
\[
L_1 \oplus P_1  { \, \xrightarrow{\sim}\, }L_2 \oplus P_2
.\]
We define the **stable isometry class** of \( L \) as
\[
 \operatorname{Cl}^{{\operatorname{Stab}}}(L) \coloneqq\left\{{(M, \beta_M) {~\mathrel{\Big\vert}~}M \text{ is stably isometric to } L}\right\}
,\]
and write \(  \operatorname{Cl}^{\operatorname{Stab}}(L_1) =  \operatorname{Cl}^{\operatorname{Stab}}(L_2) \) if \( L_1 \) is stably isometric to \( L_2 \).

If \( L_1, L_2 \) are even lattices, we additionally require \( P_1, P_2 \) to be even.
:::

::: remark
Two even lattices are stably isometric if and only if they have isometric discriminant forms.
:::

::: {.theorem title="{\\cite[Thm. 1.3.1]{nikulin1979integer-symmetric}, \\cite[Thm. 4.1]{durfee1979fifteen}}"}
`\label[theorem]{thm:stable_equiv_equals_disrim_equiv}`{=tex} Let \( L_1, L_2 \) be two nondegenerate even lattices. Then
\[
 \operatorname{Cl}(A_{L_1}, q_{A_{L_1}}) =  \operatorname{Cl}(A_{L_2}, q_{A_{L_2}}) \iff  \operatorname{Cl}^{{\operatorname{Stab}}}(L_1) =  \operatorname{Cl}^{{\operatorname{Stab}}}(L_2)
,\]
i.e. \( L_1 \) and \( L_2 \) have isomorphic discriminant quadratic forms if and only if \( L_1 \) is stably isometric to \( L_2 \).

Similarly, if \( L_1, L_2 \) are two nondegenerate odd lattices, then
\[
 \operatorname{Cl}(A_{L_1}, \beta_{A_{L_1}}) =  \operatorname{Cl}(A_{L_2}, \beta_{A_{L_2}}) \iff  \operatorname{Cl}^{{\operatorname{Stab}}}(L_1) =  \operatorname{Cl}^{{\operatorname{Stab}}}(L_2)
,\]
i.e. \( L_1, L_2 \) have isomorphic discriminant *bilinear* forms if and only if \( L_1, L_2 \) are stably equivalent (where \( P_1, P_2 \) are no longer required to be even.)
:::

::: corollary
Let \( L_1, L_2 \) be nondegenerate lattices of the same signature. Then
\[
 \operatorname{Cl}^{\operatorname{Stab}}(L_1) =  \operatorname{Cl}^{\operatorname{Stab}}(L_2) \implies {\operatorname{gen}}(L_1) = {\operatorname{gen}}(L_2)
.\]
Thus \(  \operatorname{Cl}^{\operatorname{Stab}}(L) \subseteq {\operatorname{gen}}(L) \) for even lattices, i.e. stably equivalent lattices are in the same genus.
:::

::: proof
This follows from combining `\Cref{thm:even_lattice_genus_signature_discriminant}`{=tex} with `\Cref{thm:stable_equiv_equals_disrim_equiv}`{=tex}.
:::

::: corollary
The set \(  \operatorname{Cl}^{\mathrm{st}}(L) \) is finite.
:::

### Genera of nondegenerate lattices

::: {.theorem title="{\\cite[Cor. 1.9.4, Cor. 1.16.3]{nikulin1979integer-symmetric}}"}
`\label[theorem]{thm:even_lattice_genus_signature_discriminant}`{=tex} Let \( L_1, L_2 \) be two even, nondegenerate lattices. Then \( {\operatorname{gen}}(L_1) = {\operatorname{gen}}(L_2) \) if and only if

1.  \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \), and
2.  \(  \operatorname{Cl}(A_{L_1}, q_{A_{L_1}}) =  \operatorname{Cl}(A_{L_2}, q_{A_{L_2}}) \).

Thus the genus of a nondegenerate even lattice \( L \) is determined by its signature and the isometry class of its discriminant *quadratic* form.

Similarly, let \( L_1, L_2 \) be two odd, nondegenerate lattices. Then \( {\operatorname{gen}}(L_1) = {\operatorname{gen}}(L_2) \) if and only if

1.  \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \), and
2.  \(  \operatorname{Cl}(A_{L_1}, \beta_{A_{L_1}}) =  \operatorname{Cl}(A_{L_2}, \beta_{A_{L_2}}) \).

Thus the genus of a nondegenerate even lattice \( L \) is determined by its signature and the isometry class of its discriminant *bilinear* form.
:::

::: {.definition title="Genus invariant"}
Motivated by this result, for an even nondegenerate lattice \( L \), we define its **genus invariant** as the triple \( g(L) \coloneqq(p, q,  \operatorname{Cl}(A_L, q_{A_L})) \) where \( (p,q) \coloneqq\operatorname{sig}(L) \). Similarly, if \( L \) is odd, we instead define \( g(L) \coloneqq(p, q,  \operatorname{Cl}(A_L, \beta_{A_L})) \).

By the above theorems, the genus of a nondegenerate lattice \( L \) is uniquely determined by its genus invariant \( g(L) \).
:::

::: corollary
Let \( L_1, L_2 \) be nondegenerate *indefinite, unimodular* lattices. Then
\[
{\operatorname{gen}}(L_1) = {\operatorname{gen}}(L_2) \iff \operatorname{sig}(L_1) = \operatorname{sig}(L_2)
,\]
and the genus of \( L \) is uniquely determined by its signature.
:::

::: corollary
Let \( L_1, L_2 \) be nondegenerate, *definite, unimodular* lattices. Then
\[
{\operatorname{gen}}(L_1) = {\operatorname{gen}}(L_2) \iff \operatorname{rank}(L_1) = \operatorname{rank}(L_2)
,\]
and the genus of \( L \) is uniquely determined by its rank.
:::

### Isometry classes of even lattices

::: {.theorem title="{\\cite[Cor. 1.13.3]{nikulin1979integer-symmetric}}"}
`\label[theorem]{thm:sufficient_even_class_number_one}`{=tex} Let \( L \) be an even nondegenerate lattice. If
\[
\ell(L) \leq \operatorname{rank}(L) - 2
,\]
then \( {\operatorname{gen}}(L) =  \operatorname{Cl}(L) \) and thus \( { \operatorname{cl}}(L) = 1 \).
:::

::: corollary
If \( L \) is isometric to \( P \oplus M \) where \( P, M \leq L \) are sublattices and \( P \) is unimodular, then \( { \operatorname{cl}}(L) = 1 \).
:::

::: proof
Any unimodular sublattice of \( L \) has rank at least 2, so the assumptions of `\Cref{thm:sufficient_even_class_number_one}`{=tex} are satisfied since \( \ell(L) \leq \operatorname{rank}(L) \) always holds. The result follows from the fact that \( \ell(P) = 0 \) for any unimodular lattice \( P \) and the length \( \ell(L) \) is additive in the sense that \( \ell(P \oplus M) = \ell(P) + \ell(M) \).
:::

::: {.corollary title="Class number one for indefinite lattices {\\cite[Cor. 14.4.3]{nikulin1979integer-symmetric}}"}
Let \( L \) be a nondegenerate indefinite lattice with \( \operatorname{rank}(L) \geq 3 \). Then if

-   \( \ell(L) \leq \operatorname{rank}(L) - 2 \) if \( L \) is even, or
-   \( \ell(L) \leq \operatorname{rank}(L) - 3 \) if \( L \) is odd,

then \( { \operatorname{cl}}(L) = 1 \).
:::

::: remark
We note that for indefinite even lattices \( L \), the class number of \( L \) is "usually" one. For *definite* lattices, the situation is reversed, and having class number one is somewhat rare. By `\cite[\S 3.4]{Sca87}`{=tex}, if \( \operatorname{rank}(L) > 16 + \ell(L) \), then \( { \operatorname{cl}}(L) \geq 2 \).

TODO Scattone 8 `\S `{=tex}11.1
:::

::: {.theorem title="Nikulin's form of Witt cancellation {\\cite[Cor. 1.13.4]{nikulin1979integer-symmetric}}"}
Let \( L \) be an even lattice. Then \( L \oplus U \) is the unique lattice up to isometry with its signature and discriminant form.
:::

::: {.theorem title="Uniqueness of even indefinite lattices"}
If \( L \) is an even indefinite lattice such that
\[
\ell(L) + 2\leq \operatorname{rank}_{\mathbf{Z}}(L)
,\]
then \( { \operatorname{cl}}(L) = 1 \).
:::

### Isometry classes of Hyperbolic Lattices

::: {.corollary title="Sufficient criteria for isometries of hyperbolic lattices"}
Let \( L_1, L_2 \) be two hyperbolic lattices. Then \(  \operatorname{Cl}(L_1) =  \operatorname{Cl}(L_2) \) if

-   \( {\operatorname{gen}}(L_1) = {\operatorname{gen}}(L_2) \), and
-   \( \operatorname{rank}(L_1) \geq \ell(L_1) + 2 \).
:::

::: {.corollary title="Classification of even hyperbolic lattices"}
Let \( L_1, L_2 \) be two even hyperbolic lattices. Then \(  \operatorname{Cl}(L_1) =  \operatorname{Cl}(L_2) \) if

-   \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \)
-   \( A_{L_1}  { \, \xrightarrow{\sim}\, }A_{L_2} \)
-   \( \operatorname{rank}(L_1) \geq \ell(L_1) + 2 \).
:::

We conclude with the following:

::: {.theorem title="{\\cite{kneserKlassenzahlenIndefiniterQuadratischer1956}}"}
Let \( L \) be an indefinite lattice. If \( \operatorname{rank}L \geq 3 \) and \( {\operatorname{disc}}(L) \) is squarefree, then \( { \operatorname{cl}}(L) = 1 \).
:::

::: remark
This follows from the fact that if \( { \operatorname{cl}}(L) > 1 \), then there exists a prime \( p \) such that the quadratic form \( q \) of \( L \) can be diagonalized over \( { {\mathbf{Z}}_{\widehat{p}} } \) where the diagonal entries are distinct powers of \( p \).
:::

## Summary of classification results

### 2-elementary Lattices {#elementary-lattices}

::: remark
Let \( L \) be an even 2-elementary lattice. If \( L \) is indefinite and \( p \)-elementary, then \( { \operatorname{cl}}(L) = 1 \). Otherwise, one may appeal to `\cite[Thm. 1.14.2]{nikulin1979integer-symmetric}`{=tex}.
:::

::: {.theorem title="{\\cite[Cor. 14.6.2, 14.6.3]{petersSymmetricQuadraticForms2024}} "}
Let \( L \) be an even, indefinite, \( p \)-elementary lattice with \( \operatorname{rank}(L) \geq 4 \). Then \( { \operatorname{cl}}(L) = 1 \), and \(  \operatorname{Cl}(L_1) =  \operatorname{Cl}(L_2) \) if and only if

-   \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \), and
-   \(  \operatorname{Cl}(A_{L_1}, q_{A_{L_1}}) =  \operatorname{Cl}(A_{L_2}, q_{A_{L_2}}) \).

Moreover, this result can be refined: writing \( {\left\lvert { {\operatorname{disc}}(L)} \right\rvert} = p^{\ell(L)} \), if \( p > 2 \) then \(  \operatorname{Cl}(L_1) =  \operatorname{Cl}(L_2) \) if and only if

1.  \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \), and
2.  \( \ell(L_1) = \ell(L_2) \).

If \( p = 2 \), this holds if and only if

1.  \( L_1, L_2 \) have the same parity (even/odd),
2.  \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \), and
3.  \( \ell(L_1) = \ell(L_2) \).

Moreover, the \( p=2 \) case yields exactly two isometry types:
\[
(A_L, q)  { \, \xrightarrow{\sim}\, }
\begin{cases}
{\mathfrak{u}}_1^{\oplus {1\over 2}\ell(L)}, & L \text{ is even } (\tau_8(A_L) = 0) \\
{\mathfrak{u}}_1^{\oplus {1\over 2}(\ell(L) - 2)} \oplus {\mathfrak{v}}_1 & L \text{ is odd } (\tau_8(A_L) = 4)
\end{cases}
.\]
where \( \tau_8(A_L) \) is the index \( \tau(L) \pmod 8 \) for any lattice \( L \) with discriminant group \( A_L \).
:::

::: remark
By ???, any quadratic form on a finite group arises as the discriminant form of some even lattice. See Scattone 36, Theorem 6. TODO
:::

::: remark
Let \( L_1, L_2 \) be even 2-elementary lattices. Then \( {\operatorname{gen}}(L_1) = {\operatorname{gen}}(L_2) \) if either

-   \( L_1 \oplus U  { \, \xrightarrow{\sim}\, }L_2 \oplus U \), or
-   \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \) and \( A_{L_1}  { \, \xrightarrow{\sim}\, }A_{L_2} \).
:::

::: remark
We recall the mirror move algorithm from `\cite{nonsymplectic_involutions}`{=tex}. We have Nikulin's 2-elementary diagram:

```{=tex}
\begin{figure}[H]
\centering
\includegraphics{tikz/Vinberg-pyramid}
\caption{The 75 2-elementary lattices that can occur as primitive sublattices of $ {L_{\mathrm{K3}}} $, c.f. \cite[Fig. 1]{nonsymplectic_involutions} and \cite{Nik79}. White nodes are $\delta=0$, black are $\delta=1$, double circled are $\delta = 1,2$.}
\label[figure]{fig:nikulin-table}
\end{figure}
```
:::

::: {.remark title="2-elementary lattices"}
Let \( L \) be a 2-elementary lattice. The **divisibility** of a vector \( v\in L \), denoted \( \operatorname{div}_L(v) \), is defined by \( \beta_L(v, L) = \operatorname{div}_L(v){\mathbf{Z}} \), i.e. the positive integral generator of the image of the map \( \beta_L(v, \cdot): L\to {\mathbf{Z}} \). For 2-elementary lattices, one always has \( \operatorname{div}_L(v) \in \left\{{1, 2}\right\} \). We set \( v^* \coloneqq v/\operatorname{div}_L(v)\in A_L \). Letting \( q_L:A_L \to {1\over 2}{\mathbf{Z}}/{\mathbf{Z}} \) be the induced quadratic form on \( A_L \), we say \( v^* \) is **characteristic** if \( q_L(x) = \beta_L(v^*, x)\operatorname{mod}{\mathbf{Z}} \) for all \( x\in A_L \), and is **ordinary** otherwise. We say that a primitive isotropic vector \( e\in L \) is

1.  **odd** if \( \operatorname{div}_L(e) = 1 \),

2.  **even ordinary** if \( \operatorname{div}_L(e) = 2 \) and \( e^* \) is ordinary, or

3.  **even characteristic** if \( \operatorname{div}_L(e) = 2 \) and \( e^* \) is characteristic.

The 2-elementary hyperbolic lattices admitting a primitive embedding into \(  {L_{\mathrm{K3}}}  \) were classified by Nikulin in `\cite[\S 3.6.2]{nikulin1979integer-symmetric}`{=tex}. An indefinite 2-elementary lattice is determined up to isometry by a triple of invariants \( (r,a,\delta) \). Here, \( r\coloneqq\operatorname{rank}_{\mathbf{Z}}(L) \) is the rank, \( a = \operatorname{rank}_{{ \mathbf{F} }_2}A_L \) is the exponent appearing in \( A_L = ({\mathbf{Z}}/2{\mathbf{Z}})^a \), and \( \delta \in \left\{{0, 1}\right\} \) is the **coparity**: we set \( \delta = 0 \) if \( q_L(A_L) \subseteq {\mathbf{Z}} \), so \( q_L(x) \equiv 0 \operatorname{mod}{\mathbf{Z}} \) for all \( x\in A_L \), and \( \delta=1 \) otherwise. We accordingly specify such lattices using the notation \( (r,a,\delta)_{n_+} \).
:::

::: remark
By `\cite[Prop. 1.8.1]{nikulin1979integer-symmetric}`{=tex}, the discriminant form \( A_L \) of a 2-elementary lattice \( L \) is is a isometric to a direct sum of quadratic forms, which are comprised of the discriminant forms of the lattices \( A_1, A_1(-1), U(2) \), and \( D_4 \).
:::

### Indefinite unimodular lattices

::: {.theorem title="{\\cite{milnor1958simply}}"}
Let \( L \) be an indefinite even unimodular lattice with \( \operatorname{sig}(L) = (p, q) \). Then \( \operatorname{rank}(L) \) is necessarily even, \( \tau \equiv 0 \pmod{8} \), and
\[
L  { \, \xrightarrow{\sim}\, } {\textrm{II}} _{p, q} \coloneqq
\begin{cases}
E_8(-1)^{\oplus {\tau \over 8}} \oplus U^{\oplus q}, & p-q > 0 \\
E_8^{\oplus {-\tau \over 8}} \oplus U^{\oplus p}, & p-q < 0
\end{cases}
,\]
where \( E_8 \) is the negative-definite \( E_8 \) lattice.
:::

::: proof
See `\cite[Ch. 5]{serreCourseArithmetic1973}`{=tex}.
:::

::: theorem
Let \( L \) be an indefinite odd unimodular lattice with \( \operatorname{sig}(L) = (p, q) \). Then \( L  { \, \xrightarrow{\sim}\, } {\textrm{I}} _{p, q} \).
:::

::: theorem
Any indefinite unimodular lattice is determined up to isometry by its rank, index, and parity. The same is true for definite unimodular lattices \( L \) with \( \operatorname{rank}L \leq 8 \).
:::

::: theorem
Let \( L \) be a unimodular integral lattice with \( \operatorname{rank}_{\mathbf{Z}}L \leq 4 \). Then either

-   \( L \) is odd and \( L { \, \xrightarrow{\sim}\, } {\textrm{I}} _{p, q} \) for some \( p,q \), or
-   \( L \) is even and either \( L { \, \xrightarrow{\sim}\, }U \) or \( U^2 \).
:::

::: corollary
Let \( L \) be an indefinite unimodular lattice. Then \( L[0] \neq \emptyset \), and either

-   \( L\cong U \oplus M \), or
-   \( L\cong {\rm I}_{1,1} \oplus M \)

where \( M \) is again unimodular.
:::

### Unimodular lattices

::: {.remark title="Number of unimodular lattices by dimension"}
The following is a table from `\cite[Table 2.2]{conway1999sphere-packings}`{=tex} detailing the number of \( n \)-dimensional unimodular lattices, where

-   \( a_n \) is the number of such lattices \( L \) with \( N_L(1) = 0 \),
-   If \( n\equiv 0 \pmod 8 \), \( a_n = d_n + e_n \) is the number of odd and even lattices respectively,
-   \( b_n \) is the *total* number of unimodular lattices of dimension \( n \).

```{=tex}
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
```
For \( 1\leq n\leq 8 \), there is a unique definite odd unimodular lattice \( \rm{I}_{n, 0} \cong \left\langle{1}\right\rangle^{\oplus n} \). For \( n\geq 9,10,11 \), there is also \( E_8 \oplus  {\textrm{I}} _{n-8, 0} \), and for \( n=12 \) there is additionally a lattice called \( D_{12}^+ \).
:::

::: remark
Let \( X_n \) denote the set of unimodular lattices of rank \( n \), modulo isometry, and define the generating function \( F_{X_n}(x) \coloneqq\sum_{i=0}^\infty {\sharp}X_n \cdot x^n \). The following data is due to `\cite{chenevierUnimodularHunting2024}`{=tex}: `\begin{align*}
F_{X_n}(x) &= 1 + 1 x + 1 x^{2} + 1 x^{3} + 1 x^{4} + 1 x^{5} + 1 x^{6} + 2 x^{7} + 2 x^{8} \\
&\quad + 2 x^{9} + 2 x^{10} + 2 x^{11} + 2 x^{12} + 4 x^{13} + 5 x^{14} + 8 x^{15} + 9 x^{16} \\
&\quad + 13 x^{17} + 16 x^{18} + 28 x^{19} + 40 x^{20} + 68 x^{21} + 117 x^{22} + 297 x^{23} + 665 x^{24} \\
&\quad + 2566 x^{25} + 17059 x^{26} + \cdots
\end{align*}`{=tex}
:::

### Summary

::: {.theorem title="Summary of classification results"}
Let \( (L, q) \) be a nondegenerate quadratic form. We summarize below the classification up to isometry of such forms over various rings \( R \). The following criteria for \( (L_1, q_1) \) and \( (L_2, q_2) \) are necessary and sufficient for \(  \operatorname{Cl}_R(L_1, q_1) =  \operatorname{Cl}_R(L_2, q_2) \):

-   \( R = { \mathbf{F} }_p \), \( p\geq 3 \) an odd prime:
    -   \( \operatorname{rank}_{{ \mathbf{F} }_p}(L_1) = \operatorname{rank}_{{ \mathbf{F} }_p}(L_2) \pmod{2{\mathbf{Z}}} \),
    -   If both \( {\operatorname{disc}}(L_1), {\operatorname{disc}}(L_2) \) are zero or nonzero in \( D({ \mathbf{F} }_q) \).
-   \( R = {\mathbf{Q}}_p \):
    -   \( \operatorname{rank}_{{ {\mathbf{Q}}_{\widehat{p}} }}(L_1) = \operatorname{rank}_{{ {\mathbf{Q}}_{\widehat{p}} }}(L_2) \),
    -   \( {\operatorname{disc}}(L_1) = {\operatorname{disc}}(L_2) \in D({ {\mathbf{Q}}_{\widehat{p}} }) \),
    -   \( {\varepsilon}_p(L_1) = {\varepsilon}_p(L_2) \), where \( {\varepsilon}_p \) is the **Hasse invariant** at \( p \).
-   \( R = {\mathbf{Q}} \):
    -   \( \operatorname{rank}_{\mathbf{Q}}(L_1) = \operatorname{rank}_{\mathbf{Q}}(L_2) \),
    -   \( \tau(L_1) = \tau(L_2) \),
    -   \( {\operatorname{disc}}(L_1) = {\operatorname{disc}}(L_2) \in D({\mathbf{Q}}) \),
    -   \( {\varepsilon}_p(L_1) = {\varepsilon}_p(L_2) \) for all primes \( p\leq \infty \), or equivalently,
    -   \( L_{1, { {\mathbf{Q}}_{\widehat{p}} }}  { \, \xrightarrow{\sim}\, }L_{2, { {\mathbf{Q}}_{\widehat{p}} }} \) for all primes \( p\leq \infty \).
-   Over \( {\mathbf{R}} \):
    -   \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \).
-   Over \( {\mathbf{C}} \):
    -   \( \operatorname{rank}_{\mathbf{C}}(L_1) = \operatorname{rank}_{\mathbf{C}}(L_2) \).
-   Over \( {\mathbf{Z}} \): indefinite, unimodular
    -   The parity of \( L_1, L_2 \) agree (even/odd),
    -   \( \operatorname{sig}(L_1) = \operatorname{sig}(L_2) \).

There is similarly a classification of torsion quadratic forms for various groups \( G \):

-   \( G \) a 2-primary group:
    -   \( \tau_8(L_1) = \tau_8(L_2) \)
:::

## Theta functions

::: {.definition title="Theta function and zeta functions"}
The **theta function ** of a positive definite lattice \( (L, \beta) \) is
\[
\Theta_L(z) \coloneqq\sum_{v\in L} q^{{1\over 2}\beta(v, v)} = \sum_{m=0}^\infty N_L(m) q^m,\quad 
N_L(m) \coloneqq{\sharp}L[m],\,\, q \coloneqq e^{2 i\pi z}
.\]
This is a holomorphic function for \( z\in {\mathbb{H}} \). The **zeta function** of \( L \) is
\[
\zeta_L(s) \coloneqq\sum_{v\in L\setminus\left\{{0}\right\}} \beta(v,v)^{-s}
.\]
:::

::: remark
If \( L  { \, \xrightarrow{\sim}\, }M \) then \( N_{L}(k) = N_{M}(k) \) for all \( k \) and thus \( \Theta_{L}(z) = \Theta_{M}(z) \). So the theta function of \( L \) is an invariant of its isometry class.
:::

::: definition
The **Jacobi theta functions** are defined as `\begin{align*}
\theta_2(z) &\coloneqq\sum_{n\in {\mathbf{Z}}} q^{\qty{n + {1\over 2}}^2 } \\
\theta_3(z) &\coloneqq\sum_{n\in {\mathbf{Z}}} q^{{1\over 2}n^2} \\
\theta_4(z) &\coloneqq\sum_{n\in {\mathbf{Z}}} (-1)^n q^{{1\over 2}n^2} 
\end{align*}`{=tex} where \( q \coloneqq e^{2\pi i z} \). These have expansions `\begin{align*}
\theta_2(z) &= 2q^{1\over 4}\qty{1 + q^2  + q^{6} + q^{12} + { \mathsf{O}}(q^{20}) } \\
\theta_3(z) &= 1 + 2q   + 2q^4      + 2q^9      + { \mathsf{O}}(q^{16}) \\
\theta_4(z) &= 1 - 2q   + 2q^4      - 2q^9      + { \mathsf{O}}(q^{16})
\end{align*}`{=tex}
:::

::: remark
The theta function is an additive invariant, i.e.
\[
\Theta_{L_1 \oplus L_2}(z) = \Theta_{L_1}(z) \cdot \Theta_{L_2}(z), \qquad \Theta_{L^{\oplus n}}(z) = (\Theta_L(z))^n
\]
and for the dual lattice,
\[
\Theta_{L {}^{ \vee }}(e^{-2\pi t}) = {\operatorname{disc}}(L)^{1\over 2} \cdot t^{-{n\over 2}}\cdot \Theta_{L}(e^{-2\pi t})
.\]
Moreover, the Poisson summation formula states
\[
\sum_{v\in L} f(v) = {\operatorname{disc}}(L)^{-{1\over 2}} \cdot \sum_{w\in L {}^{ \vee }}\widehat{f}(w)
,\]
which for theta functions yields
\[
\Theta_{L {}^{ \vee }}(z) = {\operatorname{disc}}(L)^{1\over 2}\cdot \qty{i\over z}^{n\over 2}\cdot \Theta_L(-1/z)
.\]
There is also a relation for twists:
\[
\Theta_{L(n)}(z) =\Theta_L(n^2 z)
.\]
:::

::: example
By directly counting vectors of various norms, one can compute
\[
\Theta_{ {\textrm{I}} _{1, 0}}(z) = \sum_{m\in {\mathbf{Z}}} q^{m^2} = 1 + 2q + 2q^4 + 2q^9 + { \mathsf{O}}(q^{16}) = \theta_3(z)
,\]
where \( \theta_3(z) \) is the third *Jacobi theta function* defined above. By additivity, we have
\[
\Theta_{ {\textrm{I}} _{n, 0}}(z) = \Theta_{ {\textrm{I}} _{1, 0}}(z)^n = \theta_3(z)^n
.\]
This is often applied in classical number-theoretic contexts, such as counting the number of representations of a number \( m \) as a sum of squares. For example,
\[
{\sharp}\left\{{x \in {\mathbf{Z}}^n {~\mathrel{\Big\vert}~}\sum_{i=1}^n x_i^2 = k}\right\} = {\sharp} {\textrm{I}} _{n, 0}[k] = [q^k]\,\theta_3(z)^n
,\]
where \( [q^k]\, f(z) \) denotes the coefficient of \( q^k \) in the series expansion of \( f(z) \). For example, one can compute `\begin{align*}
\Theta_{ {\textrm{I}} _{1, 0}}(z) &= 1 + 2q + 2q^4 + 2q^9 + { \mathsf{O}}(q^{10}) \\
\Theta_{ {\textrm{I}} _{2, 0}}(z) &= 1 + 4q + 4q^2 + 4q^4 + { \mathsf{O}}(q^{5}) \\
\Theta_{ {\textrm{I}} _{3, 0}}(z) &= 1 + 6q + 12q^2 + 8q^3 + { \mathsf{O}}(q^{4}) \\
\Theta_{ {\textrm{I}} _{4, 0}}(z) &= 1 + 8q + 24q^2 + 32q^3 + { \mathsf{O}}(q^{4})
\end{align*}`{=tex}
:::

::: {.example title="The theta function of $D_n$"}
One can show that
\[
\Theta_{D_n}(z) = {1\over 2}(\theta_3(z)^n + \theta_4(z)^n)
.\]
This yields `\begin{align*}
\Theta_{D_4}(z) &= 1 + 24q^2 + 24q^4 + { \mathsf{O}}(q^6) \\
\Theta_{D_5}(z) &= 1 + 40q^2 + 90q^4 + { \mathsf{O}}(q^6) \\
\Theta_{D_6}(z) &= 1 + 60q^2 + 252q^4 + { \mathsf{O}}(q^6) \\
\Theta_{D_7}(z) &= 1 + 84q^2 + 574q^4 + { \mathsf{O}}(q^6) 
,\end{align*}`{=tex} which by an inductive argument shows that the number of roots in \( D_n \) is \( 4 \cdot {n\choose 2} = 2n(n-1) \).
:::

::: {.example title="The theta function of $E_8$"}
Let \( \sigma_k(m) \coloneqq\sum_{d \mathrel{\Big|}m} d^k \) be the \( k \)th sum of divisors function, one has
\[
\Theta_{E_8}(z) = 1 + 240 \sum_{m\geq 1} \sigma_3(m) q^{2m} 
= 1 + 240 q^2 + 2160 q^4 + { \mathsf{O}}(q^6)
.\]
In particular, this shows that \( E_8 \) has exactly 240 roots.

If \( L \) is any unimodular lattice, \( \Theta_L \) can be written as a polynomial in \( \Theta_{E_8}(z) \) and
\[
\Delta_{24}(z) \coloneqq q^2 \prod_{m\geq 1} (1-q^{2m})^{24}
= \sum_{m\geq 0}\tau(m) q^{2m}
= q^2 - 24q^4 + 252q^6 + { \mathsf{O}}(q^8)
\]
where \( \tau \) is Ramanujan's \( \tau \) function.
:::

::: {.theorem title="Even definite unimodular lattices exist only in ranks 0 mod 8"}
Let \( L \) be an even positive definite unimodular lattice. Then \( n\coloneqq\operatorname{rank}_{\mathbf{Z}}L \equiv 0 \pmod 8 \).
:::

::: proof
We first write its theta function
\[
\Theta_L(z) \coloneqq\sum_{v\in L} q^{\beta(v,v)\over 2}, \qquad q = e^{2\pi i z}
,\]
which we claim is a modular form of weight \( n/2 \), and thus satisfies the transformation property
\[
\Theta_L(-1/z) = (z/i)^{n\over 2} \Theta_L(z)
.\]
We first write \( \Theta_L(z) = \sum_{v\in L} g(v, z) \) where
\[
g(v,z) \coloneqq(e^{2\pi i z})^{\beta(v,v)\over 2} = e^{\pi i z \beta(v,v)}
,\]
and thus restricting to \( z \coloneqq it \) with \( t > 0 \), we have
\[
g(v, -1/it) = e^{- \pi \beta(v,v)\over t}
.\]
Recall the general Poisson summation formula,
\[
\Theta_L(z) \coloneqq\sum_{v\in L} f(v, z) = {1\over \operatorname{vol}(L)} \sum_{w\in L {}^{ \vee }}\widehat{f}(w, z)
,\]
where we take the Fourier transform in the \( v \) and \( w \) variables. Setting \( f(v, t) \coloneqq g(v, -1/it) \) we have the Fourier transform
\[
\widehat{f}(w, t) = t^{n\over 2} e^{-\pi t \beta(w, w)}
,\]
and noting that \( \operatorname{vol}(L) = 1 \) we have `\begin{align*}
\Theta_L(-1/z) 
&\coloneqq\Theta_L(-1/it) \\
&= \sum_{v\in L} f(v, t) \\
&= \sum_{w\in L {}^{ \vee }} \widehat{f}(w, t) \\
&= \sum_{w\in L {}^{ \vee }} t^{n\over 2} e^{-\pi t \beta(w, w)} \\
&= t^{n\over 2}\sum_{v\in L} e^{-\pi t \beta(v, v)} \\
&= t^{n\over 2}\sum_{v\in L} g(v, it) \\
&= t^{n\over 2} \Theta_L(it) \\
&= \qty{it\over i}^{n\over 2} \Theta_L(it) \\
&= \qty{z\over i}^{n\over 2}\Theta_L(z)
,\end{align*}`{=tex} which is the desired transformation property.

We now use the fact that \( {\operatorname{SL}}_2({\mathbf{Z}})\curvearrowright{\mathbb{H}} \) by
\[
S \coloneqq{ \begin{bmatrix} {0} & {-1}  \\ {1} & {0} \end{bmatrix} } . z = { 0z - 1 \over 1z + 0} = -{1\over z}, \qquad T \coloneqq{ \begin{bmatrix} {1} & {1}  \\ {0} & {1} \end{bmatrix} } . z = {1z + 1 \over 0z + 1} = z+1
\]
where \( (ST)^3 = \operatorname{id} \). Note that since \( e^{2\pi i (z+1)} = e^{2\pi i z} \), we have \( \Theta_L(Tz) = \Theta_L(z+1) = \Theta_L(z) \) and thus
\[
\Theta_L(TS.z) = \Theta_L\qty{T.(-1/z)} = \Theta_L(-1/z) = \qty{z\over i}^{n\over 2}\Theta_L(z)
= (-i)^{n\over 2}z^{n\over 2}\Theta_L(z)
.\]
By replacing \( L \) with \( L^2 \) or \( L^4 \), we can assume \( n\equiv 4 \operatorname{mod}8 \), and thus
\[
\Theta_L(TS.z) = -z^{n\over 2}\cdot \Theta_L(z)
,\]
and we arrive at the contradiction `\begin{align*}
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
,\end{align*}`{=tex} implying \( \Theta_L(z) = 0 \).
:::

### The mass formula

::: {.definition title="Mass of a genus/lattice"}
Let \( L \) be a definite integral lattice, and define the **mass** of \( L \) (equivalently, the mass of \( {\operatorname{gen}}(L) \)) by
\[
m(L) \coloneqq\sum_{ \operatorname{Cl}(L_i) \in {\operatorname{gen}}(L)} {1\over {\sharp}{{\operatorname{O}}(L_i)}} = \sum_{i=1}^{{ \operatorname{cl}}(L)} {1\over {\sharp}{{\operatorname{O}}(L_i)}}
\]
where \( L_i \) are representatives of each isometry class in the genus of \( L \).
:::

::: remark
By `\cite[\S 3.4]{Sca87}`{=tex}, the Smith-Minkowski-Siegel mass formula expresses \( m(L) \) as an infinite product
\[
{1\over m(L)} = \prod_{p\leq \infty}a_p(L)
\]
where \( p \) ranges over all primes, including \( p=\infty \), and \( a_p \) depends only on the isometry class of \( L_{{ {\mathbf{Z}}_{\widehat{p}} }} \). There are explicit formulas: for \( p<\infty \), one has

\[
a_p(L) = \lim_{t\to\infty} {1\over 2} E_{p^t}(G_\beta) p^{-tn(n-1)\over 2}, \qquad n\coloneqq\operatorname{rank}_{\mathbf{Z}}(L)
\]
where for any matrix \( M \),
\[
E_q(M) \coloneqq{\sharp}\left\{{A \in \operatorname{Mat}_{n\times n}({\mathbf{Z}}/q{\mathbf{Z}}) {~\mathrel{\Big\vert}~}A^tMA \equiv M \pmod q}\right\}
.\]
For \( p=\infty \), the factor is given by
\[
a_\infty(L) = \pi^{n(n+1)\over 4}\qty{2 \Gamma\qty{1\over 2}\Gamma\qty{2\over 2}\cdots \Gamma\qty{n\over 2} {\left\lvert {{\operatorname{disc}}(L)} \right\rvert}^{n(n+1)\over 2} }^{-1}
.\]
Moreover, in practical computations, this infinite formula reduces to a finite computation and the infinite product has nontrivial terms at only finitely many primes. One can show that for odd \( n \) and all primes \( p \) that do not divide \( 2{\left\lvert {{\operatorname{disc}}(L)} \right\rvert} \),
\[
a_p(L) = \gamma_p(n) \coloneqq\qty{1 - {1\over p^2}}\qty{1 - {1\over p^4}}\cdots\qty{1 - {1\over p^{2m}}}, \qquad n = 2m+1
,\]
and then apply the identity
\[
\prod_{p<\infty} {1\over \gamma_p(n)} = \zeta(2)\zeta(4)\cdots\zeta(2m)
.\]

Explicitly, one has
\[
m(L) = {a_\infty(L) \over \zeta(2)\zeta(4)\cdots\zeta(m)} \cdot \prod_{p\mathrel{\Big|}2{\left\lvert {{\operatorname{disc}}(L)} \right\rvert}} {a_p(L) \over \gamma_p(n)}
.\]

`\cite{Sca87}`{=tex} uses this to determine
\[
m(\left\langle{-2k}\right\rangle \oplus E_8^2) = 
\frac{691 \cdot 3617}{
2^{31} \cdot 3^{10} \cdot 5^{4} \cdot 7^{2} \cdot 11 \cdot 13 \cdot 17} \cdot k^{8} 
\prod_{p  \mathrel{|} k} \frac{1}{2}\qty{1+{1\over p^8}} 
\]
and thus
\[
2^{-p(k)} M_1 k^8 <
{ \operatorname{cl}}(\left\langle{-2k}\right\rangle \oplus E_8^2) <
Mk^8,\qquad 
M = 2 \cdot 691 \cdot 3617,
M_1 = {M \over 2^{32} \cdot 3^{10} \cdot 5^{4} \cdot 7^{2} \cdot 11 \cdot 13 \cdot 17}
\]
where \( p(k) \) is the number of primes dividing \( k \). Thus this class number is asymptotically of order \( k^8 \).
:::

::: {.theorem title="The Smith-Minkowski-Seigel mass formula {\\cite[\\S 4, \\S 7]{conwayLowDimensionalLatticesIV1988}}"}
Then if \( L \) is even, unimodular, and positive definite of rank \( n \), there is an equality `\begin{align*}
m(L) &= 2^{1-n} \pi^{-{n(n+1)\over 4}} \cdot \qty{\prod_{1\leq j\leq n}\Gamma\qty{j\over 2} } \cdot \qty{\prod_{0 \leq 2k \leq n-2}\zeta(2k) }\cdot \zeta\qty{n\over 2} \\
&= 2\zeta(n/2) {\zeta(2) \cdot \zeta(4) \cdots \zeta(n-2) \over \operatorname{vol}(S^0)\cdot \operatorname{vol}(S^1)\cdots \operatorname{vol}(S^{n-1})} \\
& = {B_{n\over 2}\over n}\cdot \prod_{1 \leq 2j \leq n-2} {B_{2j} \over 4j}
,\end{align*}`{=tex} where \( \zeta \) is the Riemann zeta function, \( B_k \) are the Bernoulli numbers generated by
\[
{z\over e^z-1} = \sum_j B_j {z^j\over j!}
,\]
and
\[
\operatorname{vol}(S^{j-1}) = {2\pi^{j\over 2} \over \Gamma(j/2)} \\
\]
is the volume of the \( (j-1) \)-dimensional sphere.
:::

::: remark
There are effective methods for computing the mass of a genus \( {\operatorname{gen}}(L) \) with knowledge of only one lattice in the genus, and this can be used to estimate \( { \operatorname{cl}}(L) \).
:::

::: corollary
There is a unique even, unimodular, positive definite lattice of rank \( 8 \): the \( E_8 \) lattice.
:::

::: proof
One can show that \( {\operatorname{O}}(E_8) = W_{E_8} \), and
\[
{\sharp}W_{E_8} = 2^{14}\cdot 3^5 \cdot 5^2 \cdot 7
.\]
Setting \( n=8 \), we have `\begin{align*}
m(E_8) 
&= {1\over 8}B_4 \cdot \qty{ {1\over 4}B_2 + {1\over 8}B_4 + {1\over 12}B_6 } \\
&= {1\over 8}{-1\over 30} \cdot\qty{ {1\over 4}{1\over 6} \cdot {1\over 8}{-1\over 30} \cdot {1\over 12}{1\over 42} } \\
&= (1/696729600)^{-1}\\
&= (2^{14} \cdot 3^5 \cdot 5^2 \cdot 7)^{-1}\\
&= 1/{\sharp}W_{E_8}
,\end{align*}`{=tex} which forces \( {\operatorname{gen}}(E_8) =  \operatorname{Cl}(E_8) \) and \( { \operatorname{cl}}(E_8) = 1 \), using the fact that all even unimodular lattices of a given rank \( n \) are in the same genus.
:::

::: remark
This formula is used in moduli problems, e.g in `\cite{Sca87}`{=tex} where it is used to estimate the number of boundary curves in the Baily Borel compactification of \( F_{2d} \) -- it is determined that this number grows asymptotically like \( (2k)^8 \).
:::

::: remark
For even unimodular lattices \( L \) of rank \( n=8k \), one generally has
\[
m(L) = {B_{4k} \over 8k } \prod_{j=1}^{4k-1}{B_{2j} \over j}
.\]
For odd unimodular lattices of rank \( n \), one instead has \( m(L) = M(n) \), where \( M_n \) is a constant depending only on \( n \). The first few values are given by the following from `\cite[Table 16.2]{conway1999sphere-packings}`{=tex}. One can also generate by direct computations, e.g. in `\cite{sagemath}`{=tex}, the following computations of the sizes of orthogonal groups of the lattice \(  {\textrm{I}} _{n, 0} \):

  \( n \)   \( M(n) \)                       \( {\sharp}{\operatorname{O}}( {\textrm{I}} _{n,0}) \)
  --------- -------------------------------- --------------------------------------------------------
  \( 0 \)   \( 1 \)                          \( 1 \)
  \( 1 \)   \( {1\over 2} \)                 \( 2 \)
  \( 2 \)   \( {1\over 8} \)                 \( 8 \)
  \( 3 \)   \( {1\over 48} \)                \( 48 \)
  \( 4 \)   \( {1\over 384} \)               \( 384 \)
  \( 5 \)   \( {1\over 3,840} \)             \( 3,840 \)
  \( 6 \)   \( {1\over 46,080} \)            \( 46,080 \)
  \( 7 \)   \( {1\over 645,120} \)           \( 645,120 \)
  \( 8 \)   \( {1\over 10,321,920} \)        \( 10,321,920 \)
  \( 9 \)   \( {17 \over 2,786,918,400} \)   \( 185,794,560 \)

One can also verify the general formula \( {\sharp}{\operatorname{O}}( {\textrm{I}} _{n, 0}) = 2^n \cdot n! \). This verifies that \(  {\textrm{I}} _{n, 0} \) is the unique odd unimodular lattice in ranks \( n = \leq 8 \), and that there is at least one other inequivalent rank \( 9 \) lattice. By `\cite[\S 2.4]{conway1999sphere-packings}`{=tex}, the missing lattice is \( E_8 \oplus  {\textrm{I}} _{1, 0} \), and one can compute \( {\sharp}{\operatorname{O}}(E_8 \oplus  {\textrm{I}} _{1, 0}) = 1,393,459,200 \) and verify that
\[
{1\over {\sharp}{\operatorname{O}}( {\textrm{I}} _{9, 0})} + {1\over {\sharp}{\operatorname{O}}(E_8 \oplus  {\textrm{I}} _{1, 0})} = {1\over 185,794, 560} + {1\over 1,393,459, 200} = {17 \over 2786918400} = M(9)
.\]
Thus there are exactly two isometry classes of odd definite unimodular rank 9 lattices.
:::

## Embeddings

::: {.proposition title="Finiteness of embeddings for even, unimodular lattices"}
Recalling the definitions in `\Cref{def:equivalent_embeddings}`{=tex}, if \( S \) and \( L \) are even lattices and \( L \) is unimodular, then \( {\operatorname{Emb}}(S, L) \) is a finite set.
:::

::: proof
By `\cite[Prop. 1.6.1]{nikulin1979integer-symmetric}`{=tex}, such a primitive embedding \( \iota: S\hookrightarrow L \) is determined by an isometry \( \gamma: A_{S}  { \, \xrightarrow{\sim}\, }A_T(-1) \), two such primitive embeddings are equivalent if and only if \( \gamma_1 \) is conjugate to \( \gamma_2 \) under \( {\operatorname{O}}(A_T) \), and \( \iota_1(S_1)  { \, \xrightarrow{\sim}\, }\iota_2(S_2) \) are equivalent primitive sublattices if \( \exists (\phi, \psi)\in {\operatorname{O}}(S) \oplus {\operatorname{O}}(T) \) such that \( \gamma_1 \circ { \left.{{\phi}} \right|_{{A_S}} } = { \left.{{\psi}} \right|_{{A_T}} }\circ \gamma_2 \).

Since \( A_S, A_T \) are finite abelian groups, \( {\mathrm{Isom}}(A_S, A_T) \) is a finite set, as is \( {\operatorname{O}}(A_T) \). Moreover, noting that if \( S_1 { \, \xrightarrow{\sim}\, }S_2 \) then \( A_{S_1} { \, \xrightarrow{\sim}\, }A_{S_2} \) and thus \( {\operatorname{Emb}}(S_1, L) \cong {\operatorname{Emb}}(S_2, L) \), so \( {\operatorname{Emb}}(S, L) \) only depends on the isometry class of \( S \). Since \( {\operatorname{gen}}(S) \) is a finite set, there are only finitely many isometry classes of \( S \), so \( { \operatorname{cl}}(S) \) is finite and thus \( {\operatorname{Emb}}(S, L) \) a finite set.
:::

### Gluing and Overlattices

::: {.definition title="Overlattices"}
Let \( S\hookrightarrow L \) be an embedding of lattices. We say \( L \) is an **overlattice** of \( S \) if \( \iota(S) \) is a finite index sublattice.
:::

::: remark
Moreover,
\[
H_{L}^\perp = L {}^{ \vee }/S, \qquad H_{L}^\perp/H_{L} = A_{L}
.\]
:::

::: remark
A primitive embedding \( S\hookrightarrow L \) with \( T \coloneqq S^{\perp L} \) is uniquely determined by the choice of

1.  A subgroup \( H \leq A_L \), the *embedding subgroup*, and
2.  An isometry \( \gamma: H  { \, \xrightarrow{\sim}\, }H' \subseteq A_S \), the *embedding isometry*.

Letting \( \Gamma \) be the graph of \( \gamma \) in \( A_L \oplus A_S(-1) \), one has \( A_T = \Gamma^{\perp}/\Gamma \) and
\[
{\left\lvert {{\operatorname{disc}}T} \right\rvert} = { {\left\lvert {{\operatorname{disc}}L} \right\rvert} \cdot {\left\lvert {{\operatorname{disc}}S} \right\rvert} \over ({\sharp}H)^2 }
.\]

Equivalently, if \( { \operatorname{cl}}(L) = 1 \), such an embedding is determined by

1.  A subgroup \( H \leq A_S \), the *gluing subgroup*, and
2.  An isometry \( \gamma: H { \, \xrightarrow{\sim}\, }H' \subseteq A_T \), the *gluing isometry*.

In this situation, we similarly let \( \Gamma \) be the graph of \( \gamma \) in \( A_S \oplus A_T(-1) \), obtain \( A_L = \Gamma^{\perp}/\Gamma \), and
\[
{\left\lvert {{\operatorname{disc}}L} \right\rvert} = { {\left\lvert {{\operatorname{disc}}S} \right\rvert} \cdot {\left\lvert {{\operatorname{disc}}T} \right\rvert} \over ({\sharp}H)^2 }
.\]
:::

::: remark
Let \( S\hookrightarrow L \) be an embedding of even lattices. We define \( H_L \coloneqq L/S \). There is a chain of embeddings
\[
S \hookrightarrow L \hookrightarrow L {}^{ \vee }\hookrightarrow S {}^{ \vee }
,\]
and thus
\[
H_L \hookrightarrow L {}^{ \vee }/S \hookrightarrow S {}^{ \vee }/S = A_S, \qquad 
{L {}^{ \vee }/S \over H_L} = {L {}^{ \vee }/S \over L/S} \cong L {}^{ \vee }/L = A_L
.\]
By `\cite[Prop. 1.4.1]{nikulin1979integer-symmetric}`{=tex}, there is a bijection `\begin{align*}
\left\{{\text{Even overlattices of } S}\right\}&\rightleftharpoons\left\{{\text{Isotropic subgroups of } A_S}\right\} \\
L &\mapsto H_L
\end{align*}`{=tex} By `\cite[Prop. 1.4.2]{nikulin1979integer-symmetric}`{=tex}, this restricts to an isomorphism `\begin{align*}
\left\{{\text{Even overlattices of } S}\right\}{_{\scriptstyle / \sim} }&\rightleftharpoons\left\{{\text{Isotropic subgroups of } A_S}\right\}/{\operatorname{O}}(S) \\
L &\mapsto H_L
\end{align*}`{=tex} where \( {\operatorname{O}}(S) \) acts on the set of subgroups of \( A_S \) by conjugation, and two overlattices \( L_1, L_2 \) of \( S \) are isomorphic if there is an isometry \( \tilde \phi: L_1\to L_2 \) lifting some isometry \( \phi\in {\operatorname{O}}(S) \). We summarize this in the following theorem:
:::

::: theorem
Let \( \iota: S\hookrightarrow L \) be an embedding of lattices, and define \( H_L \coloneqq L/\iota(S) \). Use the chain of embeddings \( S \hookrightarrow L \hookrightarrow L {}^{ \vee }\hookrightarrow S {}^{ \vee } \) to produce embeddings \( H_{L} \hookrightarrow L {}^{ \vee }/S \hookrightarrow A_S \), noting that \( \qty{ L {}^{ \vee }/S }/H_{L}\cong A_{L} \) and that the discriminant form is identically zero on the subgroup \( H_{L} \). We can thus regard \( H_L \) as a subgroup of \( A_S \).

Conversely, for a subgroup \( H\leq A_S \), write \( \eta: S {}^{ \vee }\to A_S \) and define a lattice \( S_H \coloneqq\eta^{-1}(H) \subseteq S {}^{ \vee } \). We note that \( S_H \supseteq S \), so \( S_H \) is an overlattice of \( S \).

These constructions are mutually inverse and define a bijection `\begin{align*}
\left\{{\text{Overlattices $L$ of } S}\right\} &\rightleftharpoons\left\{{\text{Isotropic subgroups } H \leq A_S}\right\} \\
L &\mapsto H_{L} \coloneqq L/S \\
L\coloneqq S_H &\mapsfrom H
\end{align*}`{=tex}
:::

::: remark
Let \( S, T \coloneqq S^{\perp L} \hookrightarrow L \) be primitive embeddings. Then \( S \oplus T\hookrightarrow L \) embeds primitively, and by the previous remark,
\[
H_L \coloneqq{L\over S \oplus T} \hookrightarrow A_{S \oplus T} = A_S \oplus A_T
.\]

The primitivity of \( S\hookrightarrow L \) and \( T\hookrightarrow L \) is equivalent to the projections of \( H_L \subseteq A_S \oplus A_T \) inducing injections
\[
p_S: H_L \hookrightarrow A_S, \qquad p_T: H_L \hookrightarrow A_T
.\]
Defining \( H_{L, S} \coloneqq p_S(H_L) \) and \( H_{L, T}\coloneqq p_T(H_L) \), these embeddings become isomorphisms onto their images,
\[
p_S: H_L  { \, \xrightarrow{\sim}\, }H_{L, S} \subseteq A_S, \qquad p_T: H_L  { \, \xrightarrow{\sim}\, }H_{L, T} \subseteq A_T
.\]
This induces an isomorphism of subgroups
\[
\gamma^L_{S, T} \coloneqq p_T \circ p_S^{-1}: H_{L, S}  { \, \xrightarrow{\sim}\, }H_{L, T}
.\]
:::

::: remark
If \( S \hookrightarrow L \) is a primitive embedding into an even unimodular lattice, then
\[
H_L \coloneqq{L\over S \oplus T} \subseteq A_S \oplus A_T(-1)
\]
is the graph of the **glue map** \( \phi_L: A_S { \, \xrightarrow{\sim}\, }A_T(-1) \), so
\[
H_L = \Gamma_{\phi_L} \coloneqq\left\{{(v, \phi_L(v)) {~\mathrel{\Big\vert}~}v\in A_S}\right\}
.\]
Conversely, given any \( f\in {\mathrm{Isom}}(A_S, A_T(-1)) \), its graph \( \Gamma_f \subseteq A_S \oplus A_T(-1) \) induces a primitive extension \( S \oplus T \leq L \) for some even unimodular lattice \( L \).

There is a surjection `\begin{align*}
{\operatorname{O}}(L) \twoheadrightarrow
&\left\{{(f,g)\in {\operatorname{O}}(S \oplus T) {~\mathrel{\Big\vert}~}{ \left.{{(f+g)}} \right|_{{A_S \oplus A_T}} }(H_L) = H_L  }\right\} \\
&= \left\{{(f,g)\in {\operatorname{O}}(S \oplus T) {~\mathrel{\Big\vert}~}\phi_L \circ { \left.{{f}} \right|_{{A_T}} } = { \left.{{f}} \right|_{{A_S}} }\circ  \phi_M }\right\}
\end{align*}`{=tex} i.e. a pair of isometries of \( S \) and \( T \) lifts to an isometry of \( L \) if and only if they preserve \( H_L \), or equivalently commute with the glue map.
:::

::: remark
Another way to see this: let \( S \hookrightarrow L \) be a primitive sublattice of a unimodular lattice. The composition `\begin{align*}
L  { \, \xrightarrow{\sim}\, }L {}^{ \vee }\twoheadrightarrow S {}^{ \vee }&\twoheadrightarrow A_S \\
v \qquad\qquad\qquad\qquad\qquad\qquad & \mapsto \overline{ { \left.{{\beta_L(v, {-})}} \right|_{{S}} } }
\end{align*}`{=tex} is surjective with kernel \( S \oplus T \), and thus induces an exact sequence and an isomorphism
\[
0 \to S \oplus T \hookrightarrow L \twoheadrightarrow A_S, \qquad
\iota_S: {L\over S \oplus T} { \, \xrightarrow{\sim}\, }A_S
.\]
Interchanging the roles of \( S \) and \( T \) yields another isomorphism
\[
\iota_T: {L\over S \oplus T}  { \, \xrightarrow{\sim}\, }A_T
,\]
and thus we obtain
\[
j_S = \iota_T \circ \iota_S^{-1}: A_S  { \, \xrightarrow{\sim}\, }A_T
.\]

Then \( f \oplus g\in {\operatorname{O}}(S) \oplus {\operatorname{O}}(T) \) lifts to an element of \( {\operatorname{O}}(L) \) if and only if \( j_S \circ f = g\circ j_S \).
:::

::: {.theorem title="{\\cite[Prop. 1.4.2]{nikulin1979integer-symmetric}}"}
Let \( L_1, L_2 \) be two overlattices of \( L \) and let \( f\in {\operatorname{O}}(L) \). Then \( f \) extends to \( \tilde f\in {\mathrm{Isom}}(L_1, L_2) \) if and only if \( { \left.{{f}} \right|_{{A_L}} } \) induces an isomorphism \( H_{L_1} { \, \xrightarrow{\sim}\, }H_{L_2} \) on isotropy groups. Moreover, two embeddings \( \iota_i: L \hookrightarrow L_i \) are isomorphic if and only if \( H_{L_1} = H_{L_2} \).
:::

::: {.theorem title="{\\cite[Cor. 1.6.2]{Nik79}}"}
Let \( S, T \) be lattices. A primitive embedding \( S\hookrightarrow L \) into a unimodular lattice for which \( S^{\perp L} \cong T \) is determined by an isomorphism \( \gamma: A_S  { \, \xrightarrow{\sim}\, }A_L(-1) \), i.e. such that \( \beta_L = -\beta_S \). Moreover, two such embeddings are isomorphic if and only if they are conjugate by some \( { \left.{{f}} \right|_{{T}} } \in {\operatorname{O}}(A_T) \) where \( f\in {\operatorname{O}}(T) \).
:::

### Even, Unimodular, and \( p \)-elementary Embeddings {#even-unimodular-and-p-elementary-embeddings}

::: {.theorem title="{\\cite[Thm. 1.14.1]{nikulin1979integer-symmetric}}"}
Let \( \iota: S\hookrightarrow L \) be an embedding of an even lattice into a unimodular lattice, and let \( T\coloneqq S^{\perp L} \). Then \( \iota \) is unique up to \( {\operatorname{O}}(L) \) if

1.  \( { \operatorname{cl}}(T) = 1 \), and
2.  \( {\operatorname{O}}_*(A_{T}) = 0 \).

Moreover, if \( L \) is either indefinite or of rank \( 8 \), then these conditions are necessary and sufficient.
:::

::: remark
Condition 1 is automatically satisfied if \( A_L = C_2^3 \oplus M \) for some form \( M \).
:::

::: {.theorem title="{\\cite[Thm 1.14.2]{nikulin1979integer-symmetric}}"}
Let \( T \) be an even indefinite lattice such that

1.  \( \operatorname{rank}(T) \geq A_{T_p} + 2 \) for all \( p\neq 2 \), and
2.  if \( \operatorname{rank}(T) = A_{T_2} \), then \( q_{T_2} \) splits of a summand of the form \( {\mathfrak{u}}_+^{(2)}(2) \) or \( {\mathfrak{v}}_+^{(2)}(2) \).

Then \( { \operatorname{cl}}(T) = 1 \) and \( {\operatorname{O}}_*(A_L) = 0 \).
:::

::: {.theorem title="{\\cite[Cor. 1.12.3, Thm 1.14.4]{Nik79}}"}
`\label[theorem]{thm:nikulin_primitive_embedding_unimodular_unique}`{=tex} Let \( \iota: S\hookrightarrow L \) be an embedding of an even lattice into a unimodular lattice and let \( T\coloneqq S^{\perp L} \). Then \( \iota \) is primitive if

1.  \( \tau(L) \equiv 0 \pmod 8 \),
2.  \( \operatorname{sig}(L) \geq \operatorname{sig}(S) \), and
3.  \( \operatorname{rank}(T) \geq \ell(A_S) + 1 \).

If additionally

1.  \( \operatorname{sig}(L) > \operatorname{sig}(S) \),
2.  \( \operatorname{rank}(T) > \ell(A_{S_p}) + 1 \) for all \( p\neq 2 \), and
3.  If \( \operatorname{rank}(T) = \ell(A_{S_2}) \), then \( A_S \) splits off a factor of the form \( {\mathfrak{u}}_+^{(2)}(2) \) or \( {\mathfrak{v}}_+^{(2)}(2) \),

then \( \iota \) is unique up to \( {\operatorname{O}}(L) \).
:::

::: corollary
Let \( \iota: S\hookrightarrow L \) be a primitive embedding of an even lattice into an even unimodular lattice where \( T \coloneqq S^{\perp L} \supseteq U \). Then \( \iota \) is unique up to \( {\operatorname{O}}(L) \).
:::

::: proof
There is a decomposition \( T = U \oplus U^{\perp T} \) where \( U^{\perp T} \subseteq T^{\perp L} = (S^{\perp L})^{\perp L} = S \), and there are isometries
\[
A_S(-1)  { \, \xrightarrow{\sim}\, }A_T  { \, \xrightarrow{\sim}\, }A_{U^{\perp T}}
\]
since \( U \) is unimodular. We then have
\[
\ell(S) = \ell(T) = \ell(U^{\perp T}) \leq \operatorname{rank}_{\mathbf{Z}}(U^{\perp T}) = \operatorname{rank}_{\mathbf{Z}}(T) - 2 
,\]
and thus \( \ell(S) + 2 \leq \operatorname{rank}(T) \).
:::

::: {.theorem title="{\\cite[Thm. 1.1.2]{nikulin1979integer-symmetric}, \\cite{james1966on-witts-theorem}}"}
Let \( S \) be a lattice of rank \( n \) and let \( L \) be an even unimodular lattice of signature \( (p, q) \). If \( n \leq \min(p, q) \), then there exists a primitive embedding \( \iota: S\hookrightarrow L \). If the inequality is strict, it is unique up to \( {\operatorname{O}}(L) \).
:::

::: {.theorem title="{\\cite[1.15.1]{nikulin1979integer-symmetric}}"}
Let \( S \) be an even lattice with \( \operatorname{sig}(S) = (p, q) \) and let \( (\tilde p, \tilde q, A_L) \) be the invariants of some genus \( {\operatorname{gen}}(L) \) of even lattices.

A primitive embedding in \( {\operatorname{Emb}}(S, L) \) into some \( L\in {\operatorname{gen}}(L) \) is determined by a tuple \( (H_S, H_Q, \gamma, T, \gamma_K) \) where

1.  \( H_S, H_Q \leq A_S \) are subgroups,
2.  \( \gamma: H_S  { \, \xrightarrow{\sim}\, }H \leq A_L \) is an isometry of subgroups,
3.  \( T \) is an even lattice with \( \operatorname{sig}(T) = (\tilde p, \tilde q) - (p, q) \) and \( A_T = -\delta \) where \( \delta = (A_S \oplus \Gamma_\gamma^\perp)/\Gamma_\gamma \) where \( \Gamma_\gamma \) is the pushout of \( \gamma \) in \( A_S \oplus A_L \), and
4.  \( \gamma_T: A_T  { \, \xrightarrow{\sim}\, }(-\delta) \) is an isometry.
:::

::: remark
This can be used to compute primitive embeddings \( S\hookrightarrow L \) along with \( T = S^{\perp L} \).
:::

::: {.theorem title="{\\cite[Thm. 2.9]{BHPV04}}"}
Let \( S \) be an even lattice and let \( L \) be an even unimodular lattice containing \( U^{\oplus m} \) as a sublattice. If \( \operatorname{rank}S \leq m \) then there exists a primitive embedding \( \iota: S\hookrightarrow L \), If the inequality is strict, then \( \iota \) is unique up to \( {\operatorname{O}}(L) \).
:::

::: theorem
See `\cite[2.2.4]{Sca87}`{=tex}, originally due to James.

Let \( S \) be an even lattice and \( L \) an even unimodular lattice. If \( \operatorname{rank}(S) \leq \mathop{\mathrm{Index}}(L) \), then there is a primitive embedding \( S\hookrightarrow L \) which is unique up to \( {\operatorname{O}}(L) \).
:::

### K3 Embeddings

::: {.proposition title="Embeddings of hyperbolic lattices into the K3 lattice"}
Let \( S \) be an even hyperbolic lattice. If

1.  \( \operatorname{rank}_{\mathbf{Z}}(S) \leq 20 \), and
2.  \( \ell(A_S) \leq 20-\operatorname{rank}_{\mathbf{Z}}(S) \),

Then there exists an embedding \( \iota: S\hookrightarrow {L_{\mathrm{K3}}}  \) which is unique up to \( {\operatorname{O}}( {L_{\mathrm{K3}}} ) \).
:::

::: proof
This follows from `\cite[Cor. 1.13.3]{nikulin1979integer-symmetric}`{=tex}.
:::

::: corollary
If \( S \) is any even hyperbolic lattice with \( \operatorname{rank}S \leq 9 \), then \( S \) embeds uniquely into \(  {L_{\mathrm{K3}}}  \), up to \( {\operatorname{O}}( {L_{\mathrm{K3}}} ) \).
:::

### Embedding direct sums

::: proposition
Let \( L \) be a unimodular lattice. If \( \iota: S\hookrightarrow L \) is a primitive embedding and \( L = \left\langle{e_1,\cdots, e_n}\right\rangle_{\mathbf{Z}} \) is a basis for \( L \) such that \( S = \left\langle{e_1,\cdots, e_k}\right\rangle_{\mathbf{Z}} \), then there is a basis for \( S^{\perp L} \) given by \( T \coloneqq\left\langle{e_{k+1} {}^{ \vee }, \cdots, e_n {}^{ \vee }}\right\rangle_{\mathbf{Z}} \). Moreover, if \( v\in L \) is primitive, then there exists a \( w\in L \) such that \( \beta(v, w) = 1 \).
:::

::: proof
We have \( T \coloneqq\left\langle{e_{k+1} {}^{ \vee }, \cdots, e_n {}^{ \vee }}\right\rangle_{\mathbf{Z}}\subseteq S^{\perp} \) since \( \beta(e_i, e_j {}^{ \vee }) = \delta_{ij} \). To see that \( S^{\perp L} \subseteq T \), let \( v\in S^{\perp L} \subseteq L \). Then \( \beta(v, s) = 0 \) for any \( s\in S = \left\langle{e_1,\cdots, e_k}\right\rangle_{\mathbf{Z}} \), and thus \( v\in \left\langle{e_1,\cdots, e_k}\right\rangle_{\mathbf{Z}}^{\perp L} = \left\langle{e_{k+1} {}^{ \vee }, \cdots, e_n {}^{ \vee }}\right\rangle = T \).

For the latter statement, let \( \left\langle{v}\right\rangle_{\mathbf{Z}}\hookrightarrow L \) be a primitive embedding and extend \( v \) to an \( R \)-basis of \( L \), say \( \left\{{v, e_2, \cdots, e_n}\right\} \). Then take \( w\coloneqq v {}^{ \vee } \).
:::

::: remark
Let \( S\hookrightarrow L \) be a primitive embedding of a lattice into a unimodular lattice, and let \( T\coloneqq S^{\perp L} \). Then \( L \) is an overlattice of \( S \oplus T \) with associated isotropic subgroup \( H_L \coloneqq L/(S \oplus T) \subset A_S \oplus A_T \). Since \( S \hookrightarrow L \) is primitive and \( L \) is unimodular, there is an isomorphism \( (A_S, q_S)  { \, \xrightarrow{\sim}\, }(A_T, -q_S) \). The converse similarly holds, and thus we have:
:::

::: theorem
If \( L \) is a unimodular lattice and \( S \) is a nondegenerate primitive sublattice with orthogonal complement \( T = S^{\perp L} \), there is an isometry \( A_S  { \, \xrightarrow{\sim}\, }A_T(-1) \).
:::

::: proof
See `\cite[Lem. 2.5]{BHPV04}`{=tex}.
:::

::: proposition
Let \( L \) be a unimodular lattice and \( \iota: S \hookrightarrow L \) be a primitively embedded sublattice. Then \( {\left\lvert {{\operatorname{disc}}(S)} \right\rvert} = {\left\lvert {{\operatorname{disc}}(T)} \right\rvert} \), and if \( S \) is unimodular, then \( L \cong S \oplus T \).
:::

::: proof
We have
\[
{\left\lvert {{\operatorname{disc}}(S)} \right\rvert} = {\sharp}A_S = {\sharp}A_T = {\left\lvert {{\operatorname{disc}}(T)} \right\rvert}
.\]
The isometry follows from `\Cref{prop:disc_of_full_rank_sublattice}`{=tex}: since \( S \oplus T \leq L \) is a full-rank sublattice, \( T \) is also unimodular and thus
\[
[L: S \oplus T]^2 = {{\operatorname{disc}}(S \oplus T) \over {\operatorname{disc}}(L)} = {{\operatorname{disc}}(S) \cdot {\operatorname{disc}}(T) \over {\operatorname{disc}}(L)} = 1
.\]
:::

::: lemma
If \( L \) is even and unimodular and \( v^2\neq 0 \), then
\[
\left\{{f\in {\operatorname{O}}(v^\perp) {~\mathrel{\Big\vert}~}{ \left.{{f}} \right|_{{A_{v^\perp}}} } = \operatorname{id}}\right\} 
= \left\{{{ \left.{{f}} \right|_{{v^\perp}} } {~\mathrel{\Big\vert}~}f\in {\operatorname{O}}(L), f(v) = v}\right\} \subseteq {\operatorname{O}}(v^\perp)
.\]
:::

## Splitting Theorems

::: lemma
Let \( U \) be the hyperbolic lattice. Then \( {\operatorname{disc}}(U) = 1, \operatorname{sig}(U) = (1,1) \), and for any primitive embedding \( U \hookrightarrow L \) there is a decomposition \( L \cong U \oplus U^{\perp} \) given by the isometry `\begin{align*}
U &\hookrightarrow U \oplus U^{\perp} \cong L \\
x &\mapsto \beta(e, x)f + \beta(f, x)e + x', \qquad x' \coloneqq x-\beta(e,x)f -\beta(f,x)e,
\end{align*}`{=tex} and one can verify that \( x'\in U^{\perp L} \). Moreover, this also holds with \( U \) replaced by \( U^{\oplus n} \) for any \( n\geq 1 \).
:::

::: remark
In fact, the above statement holds with \( U \) replaced by any unimodular lattice. (TODO: record proof) A useful trick: if \( v \) is isotropic and \( vw = 1 \), then \( \tilde w \coloneqq w - {1\over 2}q(w)x \) is isotropic and \( v,\tilde w \) span a copy of \( U \). One can also then represent any \( n\in {\mathbf{Z}} \), since \( q({1\over 2}n v + \tilde w) = n \).
:::

```{=html}
<!--:::{.corollary}-->
```
```{=html}
<!--Let $L$ be an even unimodular lattice and let $v\in L[0]$ be a nonzero isotropic vector.-->
```
```{=html}
<!--Then $L\iso U \oplus U^{\perp L}$ where $v\mapsto e$.-->
```
```{=html}
<!--:::-->
```
```{=html}
<!--:::{.proof}-->
```
```{=html}
<!--Let $\signature L = (p, q)$ and suppose $p, q \geq 2$.-->
```
```{=html}
<!--By the theorem, there is a primitive embedding $U \injects L$, and thus $L \iso U \oplus U^{\perp}$.-->
```
```{=html}
<!--By the previous lemma, $\Orth(L) \actson I_1(L)$ transitively, so there is an isometry $\psi \in \Orth(L)$ with $\psi(v) = e$.-->
```
```{=html}
<!--If $p,q\geq 1$, since $L$ is unimodular, pick $w\in L$ such that $\beta(v, w) = 1$.-->
```
```{=html}
<!--Set $\tilde w \da w - {\beta(w,w)\over 2}v$, then $\beta(v, \tilde w) = 1$ and $\beta(\tilde w, \tilde w) = 0$.-->
```
```{=html}
<!--Then define the isometry-->
```
```{=html}
<!--\begin{align*}-->
```
```{=html}
<!--\gens{v, \tilde w} &\iso U \\-->
```
```{=html}
<!--v &\mapsto e \\-->
```
```{=html}
<!--\tilde w &\mapsto f-->
```
```{=html}
<!--\end{align*}-->
```
```{=html}
<!--producing a primitively embedded copy of $U \injects L$.-->
```
```{=html}
<!--One thus similarly has $L \iso U \oplus U^{\perp L}$, and $v\mapsto e$ by the above assignment.-->
```
```{=html}
<!--:::-->
```
::: lemma
If \( L \) contains an isotropic element \( v \), then \( v \) can be completed to a copy of \( U \) with \( L = U \oplus M \) for some \( M \) if and only if \( \operatorname{div}_L(v) = 1 \).
:::

## Lifting Problems

### Lifting from embedded sublattices

::: {.theorem title="{\\cite[Cor. 1.5.2]{nikulin1979integer-symmetric}}"}
Let \( S_1, S_2 \hookrightarrow L \) be primitive embeddings with orthogonal complements \( T_1, T_2 \) and let \( \phi: S_1 { \, \xrightarrow{\sim}\, }S_2 \) be an isometry. Then \( \phi \) extends to an isometry \( \widehat{\phi}\in {\operatorname{O}}(L) \) if and only if there exists an isometry \( \psi: T_1 { \, \xrightarrow{\sim}\, }T_2 \) such that the following diagram commutes:

\[\begin{tikzcd}
    {A_{S_1}} && {A_{S_2}} \\
    \\
    {A_{T_1}} && {A_{T_2}}
    \arrow["{\overline{\phi}}", from=1-1, to=1-3]
    \arrow["{\gamma^L_{S_1, T_1}}"', from=1-1, to=3-1]
    \arrow["{\gamma^L_{S_2, T_2}}", from=1-3, to=3-3]
    \arrow["{\overline{\psi}}", from=3-1, to=3-3]
\end{tikzcd}\]
:::

::: corollary
`\label[corollary]{cor:nikulin_extend_isometries_perp}`{=tex} Let \( S_1 = S_2 = S \hookrightarrow L \) a single primitive sublattice in the previous corollary and \( \phi \in {\operatorname{O}}(S) \), and let \( T_1 = T_2 = T \coloneqq S^{\perp L} \). Then \( \phi \) extends to an isometry \( \widehat{\phi}\in {\operatorname{O}}(L) \) if and only if there exists some \( \psi\in {\operatorname{O}}(T) \) such that
\[
{ \left.{{\psi}} \right|_{{A_T}} } \circ \gamma^L_{S, T} = \gamma^L_{S, T} \circ { \left.{{\phi}} \right|_{{A_S}} }
,\]
so the following diagram commutes:

\[\begin{tikzcd}
    {A_S} && {A_S} \\
    \\
    {A_T} && {A_T}
    \arrow["{{ \left.{{\phi}} \right|_{{A_S}} }}", from=1-1, to=1-3]
    \arrow["{\gamma^L_{S, T}}"', from=1-1, to=3-1]
    \arrow["{\gamma^L_{S, T}}", from=1-3, to=3-3]
    \arrow["{{ \left.{{\psi}} \right|_{{A_T}} }}", from=3-1, to=3-3]
\end{tikzcd}\]

In particular, if \( \gamma^L_{S, T}: A_S  { \, \xrightarrow{\sim}\, }A_T \) is an isomorphism, this says that the restrictions of \( \phi \) and \( \psi \) to \( A_S \) and \( A_T \) coincide under the identification \( A_S \cong A_T \).

In other words, there is a surjection
\[
{\operatorname{O}}(L) \twoheadrightarrow\left\{{f\in {\operatorname{O}}(S) \oplus {\operatorname{O}}(T) {~\mathrel{\Big\vert}~}{ \left.{{f}} \right|_{{A_S}} } = { \left.{{f}} \right|_{{A_T}} }}\right\}
.\]
:::

::: theorem
Let \( S \hookrightarrow L \) be a primitive embedding of even lattices where \( L \) is unimodular and write \( T\coloneqq S^{\perp L} \). Then there is a morphism `\begin{align*}
{\operatorname{O}}(L, T) \coloneqq\left\{{f\in {\operatorname{O}}(L) {~\mathrel{\Big\vert}~}{ \left.{{f}} \right|_{{T}} } = \operatorname{id}}\right\} &\to {\operatorname{O}}(S) \\
f &\mapsto { \left.{{f}} \right|_{{S}} }
\end{align*}`{=tex} which induces an isomorphism
\[
{\operatorname{O}}(L, T)  { \, \xrightarrow{\sim}\, }{\operatorname{O}}*(S)
.\]
In other words, any isometry of \( L \) which induces the identity on \( T \) necessarily acts on \( A_S \) and \( A_T \) trivially.
:::

::: proof
To see that \( {\operatorname{O}}(L, T) \subseteq {\operatorname{O}}^*(S) \), let \( f\in {\operatorname{O}}(L) \) with \( { \left.{{f}} \right|_{{T}} } = \operatorname{id}_T \). Since \( T = S^{\perp} \), we have \( A_S = A_T(-1) \), and thus
\[
{ \left.{{f}} \right|_{{A_S}} } = { \left.{{f}} \right|_{{A_S(-1)}} } = { \left.{{f}} \right|_{{A_T}} } = { \left.{{( { \left.{{f}} \right|_{{T}} })}} \right|_{{A_T}} } = { \left.{{\operatorname{id}_T}} \right|_{{A_T}} } = \operatorname{id}_{A_T} = \operatorname{id}_{A_S}
,\]
so \( { \left.{{f}} \right|_{{S}} } \) acts trivially on \( A_S \) and thus \( { \left.{{f}} \right|_{{S}} } \in {\operatorname{O}}^*(S) \).

Conversely, if \( f\in {\operatorname{O}}(S) \) satisfies \( { \left.{{f}} \right|_{{A_S}} } = \operatorname{id}_{A_S} \), define the isometry \( F = f \oplus \operatorname{id}_T \in {\operatorname{O}}(S \oplus T) \). Since \( { \left.{{F}} \right|_{{A_T}} } = \operatorname{id}_{A_T} \), by `\Cref{cor:nikulin_extend_isometries_perp}`{=tex} there is a lift \( \tilde F\in {\operatorname{O}}(L) \), and since \( { \left.{{F}} \right|_{{T}} } = \operatorname{id}_T \), we in fact have \( F\in {\operatorname{O}}(L, T) \).

In this notation, the bijection is thus given by `\begin{align*}
{\operatorname{O}}(L, T) & { \, \xrightarrow{\sim}\, }{\operatorname{O}}^*(S) \\
f &\mapsto { \left.{{f}} \right|_{{S}} } \\
F &\mapsfrom f
\end{align*}`{=tex}
:::

::: {.proposition title="Lifting isometries stabilizing an embedding"}
Let \( S \hookrightarrow L \) be a primitive sublattice of an even unimodular lattice, and define
\[
{\operatorname{O}}(L, S) \coloneqq{\operatorname{Stab}}_{{\operatorname{O}}(L)}(S) = \left\{{f\in {\operatorname{O}}(L) {~\mathrel{\Big\vert}~}f(S) = S}\right\}
.\]
Then
\[
{\operatorname{O}}(T) \twoheadrightarrow{\operatorname{O}}(A_T) \implies {\operatorname{O}}(L, S)\twoheadrightarrow{\operatorname{O}}(S)
,\]
so if \( {\operatorname{O}}_*(A_T) = 0 \), any isometry of \( S \) can be extended to an isometry of \( L \) stabilizing \( S \).
:::

::: proof
Let \( f\in {\operatorname{O}}(S) \), and let \( \phi_L: A_S  { \, \xrightarrow{\sim}\, }A_T(-1) \) be the glue map associated to the primitive embedding \( S\hookrightarrow L \). Since \( {\operatorname{O}}(T) \twoheadrightarrow{\operatorname{O}}(A_T) \), let
\[
\tilde g \coloneqq\phi_L \circ { \left.{{f}} \right|_{{A_S}} } \circ \phi_L^{-1}\in {\operatorname{O}}(A_T)
.\]
Then \( \tilde g = { \left.{{g}} \right|_{{A_T}} } \) for some \( g\in {\operatorname{O}}(T) \), and
\[
\tilde g \circ \phi_L = 
(\phi_L \circ { \left.{{f}} \right|_{{A_S}} } \circ \phi_L^{-1}) \circ \phi_L
= \phi_L \circ { \left.{{f}} \right|_{{A_S}} }
.\]
Thus the isometry \( F \coloneqq f \oplus t\in {\operatorname{O}}(S) \oplus {\operatorname{O}}(T) \) extends to some \( \tilde F\in {\operatorname{O}}(L) \).
:::

::: corollary
Let \( S\hookrightarrow L \) be a primitive embedding into a unimodular lattice and let \( f\in {\operatorname{O}}(S) \). If \( f \) lifts to an element of \( \left\{{F\in {\operatorname{O}}(L) {~\mathrel{\Big\vert}~}{ \left.{{F}} \right|_{{T}} } = \pm \operatorname{id}}\right\} \), then this extension is unique. Such an extension exists if and only if \( f \) induces \( \pm \operatorname{id} \) on \( A_S \).
:::

### Lifting from discriminant groups

::: {.theorem title="{\\cite[Thm. 1.14.2]{nikulin1979integer-symmetric}}"}
Let \( S \) be an even indefinite lattice with \( \ell(S) + 2\leq \operatorname{rank}_{\mathbf{Z}}(S) \). Then \( {\operatorname{O}}_*(A_S) = 0 \), so \( {\operatorname{O}}(S) \twoheadrightarrow{\operatorname{O}}(A_S) \).
:::

::: {.theorem title="{\\cite[Prop. 9.2]{hassettInvolutionsK3Surfaces2024}}"}
Let \( L \) be an even hyperbolic lattice admitting a primitive embedding \( E_8(2) \hookrightarrow L \). If \( \ell(L) \leq 11 \), then \( { \operatorname{cl}}(L) = 1 \) and \( {\operatorname{O}}_*(L) = 0 \).
:::

## Group actions

::: {.lemma title="{\\cite[Lem. 3.2]{grossiSymplecticBirationalTransformations2023}}"}
If \( G \leq {\operatorname{O}}(L) \) is of order 2 which induces an order 2 isometry on \( A_L \), then \( {\left\lvert {{\operatorname{disc}}(L_G)} \right\rvert} = {\left\lvert {{\operatorname{disc}}(L^G)} \right\rvert} \).
:::

### Orbits

::: {.definition title="Set of primitive vectors of a fixed square"}
For a nondegenerate lattice \( L \), define
\[
L[k] \coloneqq\left\{{v\in L {~\mathrel{\Big\vert}~}v^2 = k,\,\, v\text{ is primitive}}\right\}
.\]
:::

::: {.theorem title="Finiteness of orbits of vectors, {\\cite[Thm. 3.6]{kamenovaFamiliesLagrangianFibrations2012}}"}
Let \( L \) be a lattice with \( \operatorname{rank}(L) \geq 7 \). Then \( L[0]/{\operatorname{O}}(L) \) is finite.
:::

::: proof
We sketch the proof given in `\cite[Thm. 3.6]{kamenovaFamiliesLagrangianFibrations2012}`{=tex}.

Let \( d \coloneqq{\left\lvert {{\operatorname{disc}}(L)} \right\rvert} \). Let \( v\in L \) be primitive with \( v^2 = 0 \). Choose \( w\in L \) such that \( \alpha \coloneqq vw \) is minimal. Then \( \alpha \) divides \( d \). Let \( K \coloneqq\left\langle{v, w}\right\rangle_{\mathbf{Z}}\leq L \), then \( {\operatorname{disc}}(K) = v^2 w^2 - (vw)^2 = -\alpha^2 \), which is bounded since \( -d^2 \leq -\alpha^2 \leq 0 \). We have \( {\sharp}K[0] \leq 2\operatorname{rank}(K) = 4 \). There are only finitely many ways of expressing \( L \) as an overlattice of \( K \oplus K^{\perp L} \), since these correspond to isotropic subgroups in \( A_L \), which has size at most \( d \).

Toward a contradiction, if \( L[0]/{\operatorname{O}}(L) \) is infinite, then there are infinitely many non-isomorphic pairs \( (K, K^{\perp L}) \). However, for infinitely many such pairs, we would have \(  \operatorname{Cl}^{{\operatorname{Stab}}}(K) =  \operatorname{Cl}^{\operatorname{Stab}}(K_1^{\perp L}) \) for some \( K_1 \), since there are only finitely many choices for \( K \). This contradicts the finiteness of \(  \operatorname{Cl}^{\operatorname{Stab}}(K) \).
:::

::: {.theorem title="{\\cite[Satz 30.2]{kneserQuadratischeFormen2002a}}"}
`\label[theorem]{thm:finiteness_of_embeddings}`{=tex} Let \( S \) be a nondegenerate lattice. Then given any \( n,d\neq 0 \), there are only finitely many isometry classes of primitive embeddings \( u: S\hookrightarrow L \) where \( L \) is of rank \( n \) and discriminant \( d \).
:::

::: corollary
If \( L \) is any nondegenerate lattice, then \( L[k]/{\operatorname{O}}(L) \) is finite for any \( k \in {\mathbf{Z}} \).
:::

::: proof
Given \( v_i \in L[k] \), let \( S_i \coloneqq\left\langle{v_i}\right\rangle_{\mathbf{Z}} \). This yields an embedding \( u_i: S_i \hookrightarrow L \), of which there are finitely many up to \( {\operatorname{O}}(L) \) by `\Cref{thm:finiteness_of_embeddings}`{=tex}.
:::

::: lemma
Let \( L \) be an even unimodular lattice. If \( \operatorname{sig}(L) \geq (1, 1) \), then for any \( d \), \( L[d]\neq 0 \), i.e. there exists a primitive element of square \( 2d \). If\( \operatorname{sig}(L) \geq (2,2) \), then \( {\operatorname{O}}(L) \) acts transitively on \( L[d] \) for each \( d \), and thus \( L[d]/{\operatorname{O}}(L) \) is a single orbit.
:::

::: proof
This is equivalent to the existence of a primitive embedding \( \left\langle{2d}\right\rangle\hookrightarrow L \), which exists by `\Cref{thm:nikulin_primitive_embedding_unimodular_unique}`{=tex}.
:::

::: {.theorem title="{\\cite[Prop. 3.3]{gritsenkoAbelianisationOrthogonalGroups2008}}"}
Let \( L = U \oplus U_1 \oplus M \coloneqq U \oplus L_1 \). Define
\[
E(L) \coloneqq\left\{{ E_{e, a} {~\mathrel{\Big\vert}~}e,a\in L, e^2 = ea = 0, \operatorname{div}_L(e) = 0}\right\}, \quad E_U(L_1) \coloneqq\left\langle{E_{e, a}, E_{f, a} {~\mathrel{\Big\vert}~}a\in L_1}\right\rangle
.\]

If \( u,v\in L \) are primitive with

-   \( u^2 = v^2 = p \),
-   \( [u^*] = [v^*] \in A_L \),

then there exists a transvection \( \tau\in E_U(L_1) \) with \( \tau(u) = v \).

Moreover, \( E(L) = E_U(L_1) \).
:::

::: remark
This may be Eichler's criterion, see `\cite{eichlerQuadratischeFormenUnd1974}`{=tex}.
:::

::: proof
We just prove the first assertion. Let \( u,v\in L \) with \( u^2=v^2=p \), and choose \( u', v'\in L_1 \) such that \( uu' = vv' = d \). We can find \( \tau\in E_{U_1}(U_2) \) such that \( \tau(u)\in L_1 \), so we can assume \( u,v\in L_1 \). We then take the composition of Eichler transformations
\[
u \xrightarrow{E_{e, u'}} u-de \xrightarrow{E_{f, w}} vide \xrightarrow{E_{e, -v'}} v
,\]
which is a translation by \( w\coloneqq(u-v)/d \) in \( U_1^{\perp L_1} \).
:::

## Characteristic Elements

::: {.definition title="Characteristic elements"}
Let \( L \) be an integral lattice. An element \( c\in L \) is **characteristic** if \( \beta(c,x) = \beta(x,x) \pmod{2{\mathbf{Z}}} \) for every \( x\in L \). A **characteristic covector** is an element \( \xi\in L {}^{ \vee } \) such that \( \beta(\xi, x) = \beta(x,x) \pmod{2{\mathbf{Z}}} \) for all \( x\in L \). We define the set
\[
\chi {}^{ \vee }(L) \coloneqq\left\{{f\in L {}^{ \vee }{~\mathrel{\Big\vert}~}f(v) = \beta(v,v) \, \forall v\in L}\right\}
.\]
Every lattice with odd discriminant contains a characteristic element, and the **\( \sigma \)-invariant** of \( L \) is defined as
\[
\sigma(L) = \beta(c, c) \pmod{8{\mathbf{Z}}}
.\]
It is an additive invariant.
:::

::: example
Let \( X \) be a smooth compact real 4-manifold with intersection form \( (L, \beta) \) on \( H^2(X; {\mathbf{Z}}) \). Then the second Stiefel-Whitney class \( w_2(X) \in H^2(X; { \mathbf{F} }_2) \) is characteristic for \( L_{{ \mathbf{F} }_2} \), so
\[
\beta(v,v) = \beta(w_2(X), v) \qquad \forall v\in L_{{ \mathbf{F} }_2}
.\]

If \( X \) is a smooth complex surface, the first Chern class \( c_1(X) \) is characteristic for \( L \) itself.
:::

::: {.lemma title="{\\cite[Lem. 2.1]{petersNotePrimitiveCohomology2023}}"}
If \( L \) is a lattice with odd discriminant and \( h\in L \) is nonisotropic, then \( h^{\perp L} \) is an even lattice if and only if \( h \) is a characteristic element.
:::

### ?

::: remark
Over \( R = {\mathbf{Z}} \), let \( X_n \) denote the space of rank \( n \) unimodular lattices. There is a moduli space of such lattices given by
\[
X_n  { \, \xrightarrow{\sim}\, }\dcosetl{{\operatorname{SL}}_n({\mathbf{Z}})}{{\operatorname{SL}}_n({\mathbf{R}})}
.\]
:::

[^1]: these lattices arise in the study of elliptic K3 surfaces; see `\cite{geemenRemarksBrauerGroups2004,shinderLequivalenceDegreeFive2020,meinsmaDerivedEquivalenceElliptic2024}`{=tex}. One can obtain a K3 surface with \( {\operatorname{NS}}(X) { \, \xrightarrow{\sim}\, }\Lambda_{n, k} \) for some \( k \) by taking a general K3 surface containing a degree \( n \) elliptic curve.
