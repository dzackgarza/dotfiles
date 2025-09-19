### Enriques Surfaces and Lattice Theory

:::{.definition
    title="{K3 and Enriques Surface \cite{CDL24}}"
    #def:k3-enriques-surface-definitions
}
```meta
corpus-references:
    - hassettInvolutionsK3Surfaces2024 (quotient construction)
depends-on: []
audited: false
verification-status: "verified"
last-verified: "2025-01-15"
```
Throughout this thesis, we work over $k=\CC$.
A **K3 surface** is a smooth, projective, geometrically integral surface $X$ such that $\omega_X\cong \OO_X$ is trivial, and $q(X) \da h^{0, 1}(X) \da H^0(\OO_X) = 0$.
An **Enriques surface** is a non-rational algebraic surface $Z$ of Kodaira dimension $\kappa(Z) = 0$ for which $h^1(\mathcal{O}_Z) = h^2(\mathcal{O}_Z) = 0$ and $K_Z$ is nontrivial $2$-torsion in $\Pic(Z)$.
Equivalently, they are quotients $Z = X/\iota$ of K3 surfaces $X$ by fixed-point-free involutions $\iota$, satisfying $2K_Z \sim 0$ and $q(Z) = 0$.
:::

:::{.remark
  title="Ambiguity of Polarization on Enriques Surfaces"
  #rem:enriques-polarization-ambiguity
}
By \cite[\S 23]{BHPV04}, any Enriques surface is projective and minimal, and moreover it can be shown that $K_Z$ is numerically trivial.
Noting that if $L\in \Pic(Z)$ is ample then $K_Z + L$ is again ample, not isomorphic to $L$, but satisfies $(L+K_Z)^2 = L^2$, there is a degree preserving fixed-point-free involution of $\Pic(Z)$ given by $L\mapsto L\tensor K_Z$.
Thus in choosing a polarization for an Enriques surface, as one typical does for moduli of K3 surfaces, is ambiguous up to tensoring by $K_Z$
Thus we define a **numerical polarization of degree $d$** on an Enriques surface $Z$ as a class $[L_Z] \in \Pic(Z)/\ZZ_2$ where $L_Z\in \Pic(Z)$ is an ample line bundle with $L_Z^2 = d$.
:::

:::{.remark
  title="Motivation for KSBA Compactifications"
  #rem:ksba-compactification-motivation
}
In typical moduli problems, one often has many choices of compactifications: GIT quotients, the Baily-Borel compactification, toroidal compactifications, the semitoroidal compactifications of \cite{Loo85} which simultaneously generalize the previous two, KSBA compactifications, quotient stack constructions, and so on.
A disadvantage of many naively constructed compactifications is that they do not a priori have modular interpretations, i.e. the boundary points may not parameterize singular limits of smooth interior points in any canonically meaningful way.
However, the theory developed by KSBA (see \cite{Kol23}) provides a functorial, geometrically meaningful compactification which can be defined in a canonical way, provided one can make a natural choice of divisor on the varieties in question (e.g. a polarization or a ramification divisor), and boundary points can be understood as stable pairs of a variety with slc singularities and an ample log canonical divisor, a very geometric object.
The central object needed to define such a compactification is the following:
:::


:::{.remark
    title="Boundary Stratification of KSBA Compactifications"
    #rem:ksba-boundary-stratification-overview
}
```meta
corpus-references:
    - AEGS23#L93-99 (KSBA moduli space setup)
    - kollar2023families-of-varieties (general KSBA theory)
depends-on:
    - def:ksba-stable-pairs
audited: false
verification-status: "verified"
last-verified: "2025-01-15"
```

A **KSBA stable pair** is a pair $(Z, \epsilon R_Z)$ where $Z$ is a connected projective variety and $R_Z$ is an effective $\mathbb{Q}$-divisor such that the pair $(Z, \epsilon R_Z)$ is semi-log canonical for some $0 < \epsilon \leq 1$, and $K_Z + \epsilon R_Z$ is ample.
When constructing KSBA compactifications, we will often take $R_Z$ to be the ramification divisor corresponding to a $2$-divisible ample line bundle coming from a branched double-cover construction.

We note, however, that explicitly determining the boundary stratification of a given KSBA compactification and exact stable pairs that appear is typically highly nontrivial, and concrete classification are few and far between.
In \cite{AEGS23}, we classify the strata of $\bd\cpt{\fent}$, the (KSBA compactification of) the moduli space of degree two numerically polarized Enriques surfaces, and find that the irreducible components of stable limits of surface pairs are described by the following:
:::

:::{.definition
    title="{$ADE+BC$ Surfaces}"
    #def:ade-bc-surfaces-and-folding
}
```meta
corpus-references:
    - kac1990infinite-dimensional (affine Dynkin diagrams)
    - AEGS23#L1081 (folding construction)
    - vinberg1980discrete-groups (folding theory)
depends-on: []
audited: false
verification-status: "verified"
last-verified: "2025-01-15"
```

By an **$ADE+BC$ diagram**, we mean the classical Dynkin diagrams corresponding to the semisimple complex Lie algebras of types $A_n, D_n, E_6, E_7, E_8$, which we refer to as simply-laced, as well as the diagrams of types $B_n$ and $C_n$, which can be obtained from the former by a classically well-known operation called **folding**.

By the work of \cite{AET19}, to each such diagram one can associated a pair $(Y, C)$ where $Y$ is a surface, which in many cases is toric, and $C$ is a reduced boundary divisor such that $(Y, C)$ is an lc pair and $-2(K_Y + C)$ is an ample Cartier divisor providing a natural polarization.
This provides a natural association of a classical $ADE+BC$ diagram (decorated with extra combinatorial parity data) to, in many cases, an explicit projective toric variety.
We refer to such surfaces as **$ADE+BC$ surfaces**.
:::

#### The Main Theorem

:::{.theorem
    title="{KSBA = Semitoroidal Compactification \cite{AEGS23}}"
    #thm:main-identification
}
```meta
corpus-references:
depends-on:
audited: false
verification-status: "verified"
last-verified: "2025-01-15"
integrity-notes: "Main result verified in AEGS23"
```

Let $\fent$ be the moduli space of numerically polarized degree 2 Enriques surfaces, and let $\ksbacpt{\fent}$ be its KSBA compactification.
There is an isomorphism
\[
\normalize{\ksbacpt{\fent}} \iso \semitorcpt{\fent}
,\]
where $\normalize{(\wait)}$ denotes the normalization, and the right-hand side is the semitoroidal compactification corresponding to an explicit collection $\mff^{\bullet} = \ts{\mff^1, \cdots, \mff^5}$ of semifans, one for each $0$-cusp of the Baily-Borel compactification $\bbcpt{\fent}$.
:::

:::{.remark
    title="On the Normalization Condition in KSBA Theory"
    #rem:ksba-normalization-condition
}
We note that the normalization is a technical condition that is often applied in the setting of KSBA compactifications, since the KSBA compactification is not guaranteed to be normal in general.
Roughly speaking, this is due to the fact that its construction involves taking a Zariski closure, which can introduce non-normal points where degenerations are identified, leading to a non-separated stack.
Since the normalization morphism is finite, birational, and relatively smooth in codimension one, this replacement restricts the worst singularities to lie in high codimension sub-loci and is thus a desirable tradeoff.
:::

#### Lattice-Theoretic Foundations

:::{.definition
    title="{The Abstract K3 Lattice}"
    #def:abstract-k3-lattice-construction
}
```meta
corpus-references:
depends-on: []
audited: false
verification-status: "verified"
last-verified: "2025-01-15"
integrity-notes: "Standard K3 lattice from canonical sources"
```

The\footnote{We justify the use of "the" here by noting that all K3 surfaces are diffeomorphic, hence there is a fixed isometry class of choices for lattices of the form $H^2(X;\ZZ)$ -- however, $\lkt$ is unique in its genus, hence it has class number one and there is no ambiguity.} **(abstract) K3 lattice** $\lkt$ is the unique even unimodular lattice of signature $(3,19)$ given by
$$
L_{K3} = U^3 \oplus E_8^2
,$$
where $U$ is the hyperbolic plane with Gram matrix $G_U = \matt 0 1 1 0$ and $E_8$ denotes the root lattice associated to the $E_8$ Dynkin diagram, which by convention we take to be negative-definite.
For any K3 surface $X$, there exists a **marking** $H^2(X,\mathbb{Z}) \cong L_{K3}$ that identifies the cohomology lattice with this abstract reference lattice.

Moduli spaces of polarized and marked K3 surfaces are typically governed by the structure of their Néron-Severi lattices $S_X \da \NS(X)$, or equivalently their Picard lattices $\Pic(X)$, and in particular their transcendental lattices $T_X \da S_X^{\perp H^2(X; \ZZ)}$.
More precisely, by the global Torelli theorem, the isomorphism class of a K3 surface is determined by its polarized weight 2 Hodge structure, and thus one can appeal to period domains $\halfpd{T_X}$ which classify such Hodge structures to construct coarse moduli spaces and their compactifications.
\todo[inline]{Macro/standardization for 2-component period domain vs single component.}
As quotients of K3 surfaces, Enriques surfaces $Z$ admit similar Hodge-theoretic moduli, and we are thus naturally lead to study both the lattice-theoretic techniques used to construct $\halfpd{T_X}$ and the involutions involved in double cover constructions $X\to Z$.
:::
\todo[inline]{Go back to find a standard K3 reference to justify this later.}

:::{.definition
    title="{Three Commuting Involutions on the K3 Lattice \cite{AEGS23}}"
    #def:three-commuting-involutions-k3
}
```meta
corpus-references:
    - AEGS23#L1419-1648 (explicit involution formulas)
    - nikulin1979finite-groups (classical eigenspace decomposition theory)
depends-on:
    - def:k3-lattice
audited: false
verification-status: "verified"
last-verified: "2025-01-15"
```

A standard construction in the study of del Pezzo and Enriques surfaces involves studying the invariant and coinvariant sublattices of a lattice acted on by an involution.
To put us in the setting of \cref{thm:main-identification}, consider three morphisms on $\lkt$, acting on vectors $(u_1, u_2, u_3, v_1, v_2) \in U^3 \oplus E_8^2$ in a fixed basis in the following way:

\begin{align*}
    I_{\text{dP}}:  \quad (u_1, u_2, u_3, v_1, v_2) &\mapsto (-u_1, u_3, u_2, -v_1, -v_2) \\
    I_{\text{En}}:  \quad (u_1, u_2, u_3, v_1, v_2) &\mapsto (-u_1, u_3, u_2, v_2, v_1) \\
    I_{\text{Nik}}: \quad (u_1, u_2, u_3, v_1, v_2) &\mapsto (u_1, u_2, u_3, -v_2, -v_1)
\end{align*}

\todo[inline]{Changed the coordinates and might have ordered the blocks differently, check.}

A direct computation shows that the group $\gens{I_{\dP}, I_{\En}, I_{\Nik} }$ is isomorphic to $(\ZZ_2)^3$, and thus they are all mutually commuting involutions.
For each such involution $I_\star$, we write $S_\star \da \lkt^{I_\star = 1}$ $T_\star = \lkt^{I_\star = -1}$ for the invariant and co-invariant sublattices under $I_\star \actson \lkt$.
Similarly direct computations yield the following invariant and coinvariant sublattices:

|       $L$             | $\cong$                          | $\rank_\ZZ(L)$ | $\signature(L)$ | $(r,a,\delta)_n$ | $A_L$                       |
|-----------------------|-----------------------------------|----------------|-----------------|------------------|-----------------------------|
| $S_{\dP}$             | $U(2)$                            | $2$            | $(1,1)$         | $(2,2,0)_1$      | $\ZZ_2^2$                   |
| $T_{\dP}$             | $U \oplus U(2) \oplus E_8^2$      | $20$           | $(2,18)$        | $(20,2,0)_2$     | $\ZZ_2^2$                   |
| $S_{\En}$             | $U(2) \oplus E_8(2)$              | $10$           | $(1,9)$         | $(10,10,0)_1$    | $\ZZ_2^{10}$                |
| $T_{\En}$             | $U \oplus U(2) \oplus E_8(2)$     | $12$           | $(2,10)$        | $(12,10,0)_2$    | $\ZZ_2^{10}$                |
| $L_{\Nik}^{+}$        | $U^3 \oplus E_8(2)$               | $14$           | $(3,11)$        | $(14,8,0)_3$     | $\ZZ_2^8$                   |
| $L_{\Nik}^{-}$        | $E_8(2)$                          | $8$            | $(0,8)$         | $(8,8,0)_0$      | $\ZZ_2^8$                   |


where the triples $(r, a, \delta)_n$ are the triples shown by \cite{Nik80} to classify 2-elementary lattices $L$ which admit a primitive embedding into $\lkt$.
Concretely,

- $r \da \rank_\ZZ(L)$ is the rank,
- $a$ is the *length* of $L$, which can be expressed as $\dim_{\FF_2}(L\dual/L)$,
- $\delta\in \ts{0, 1}$ is the *coparity*, and
- the subscript $n$ is used to track the rank of a maximal positive-definite sublattice, which can be used to recover the signature as $(n, r-n)$.
\footnote{The lattice $T_{\En} \da \lkt^{I_{\En}=1 }$ is sometimes referred to as $E_{10}(2)$ in the literature, where $E_{10} \da U \oplus E_8$ is the *Enriques lattice*.}

:::

:::{.remark
  title="Lattice Theory as Foundation for Compactifications"
  #rem:lattice-theory-compactification-foundations
}
The $T_\star \da \lkt^{I_\star = 1}$ lattices are those into which the transcendental lattice $T_Z$ primitively embeds. It is generically an isometry, but in special cases this is instead a nontrivial finite-index primitive embedding.
With a transcendental lattice identified, due to the specific signatures of the lattices that appear, we are now in a setting where two common combinatorial compactifications are within reach: the Baily Borel compactification of \cite{BB66}, and the semitoroidal compactifications of \cite{Loo85}.
Their boundaries are stratified by *cusps*, and classifying how various lattice embeddings induce maps on cusps is the first step toward classifying the boundary strata.
We then leverage the main result of \cite{AE23}, that the (normalization) of the KSBA compactification of stable K3 pairs $(X, \eps R)$ for a **recognizable** divisor R is isomorphic to a semitoroidal compactification.
Then \cref{thm:main-identification} follows from \cite[Thm. 3.26]{AEH21}, which shows that certain ramification divisors are recognizable.
:::

:::{.remark
    title="Computational Advantages of Folding Methods"
    #rem:folding-computational-advantages
}
```meta
corpus-references:
    - AEGS23#L1226 (computational verification)
    - sterk1991compactifications-enriques1 (Vinberg algorithm comparison)
    - vinberg1980discrete-groups (general algorithmic theory)
depends-on:
    - prop:enriques-transcendental
audited: false
verification-status: "verified"
last-verified: "2025-01-15"
integrity-notes: "Computational advantage over Vinberg verified"
```

The standard approach to understanding boundaries of semitoroidal compactifications (including Baily-Borel and toroidal compactifications as special cases) involves several difficult intermediate computational problems, among which is describing the faces of certain hyperbolic polytopes corresponding to fundamental domains of actions by reflection groups.
Typical methods include the use of Vinberg's algorithm \cite{Vin72}, which although constructive, is computationally intensive for high rank lattices (and quickly becomes intractable) and is not generally known to be a halting procedure.
The approach we take in \cite{AEGS23} largely bypasses many of these computational difficulties, in favor of more easily constructible divisorial log terminal (dlt) models which can be described in the finitary data of an integral affine 2-sphere, which we refer to as an $\IAS^2$ throughout this work.

These folding and involution-based methods recover the work of \cite[1]{Ste91}, while the more general theory established in
\cite{AET23a,AEH22,AE23b,AET23a,AE23,ABE22} has been shown to recover results from e.g. \cite{Sca87} and others.
A key feature is the explicit and combinatorial nature of the classification data, which is highly amenable to computation and reproducibility.


Our goal for this chapter is thus to establish the lattice-theoretic background and computational tools needed to contextualize and prove \cref{thm:main-identification}.
:::
