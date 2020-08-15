" Original file is https://github.com/wjakob/wjakob.vim/blob/master/after/syntax/tex.vim
if has('conceal')

  syn match texMathSymbol '\\dash' contained conceal cchar=-
  syn match texMathSymbol '\\tilde' contained conceal cchar=~
  syn match texMathSymbol '\\hat' contained conceal cchar=^
  syn match texMathSymbol '\\bar' contained conceal cchar=¯
  syn match texMathSymbol '\\homotopic' contained conceal cchar=~
  syn match texMathSymbol '\\sim' contained conceal cchar=~
  syn match texMathSymbol '\\union' contained conceal cchar=∪
  syn match texMathSymbol '\\disjoint' contained conceal cchar=∐
  syn match texMathSymbol '\\times' contained conceal cchar=×
  syn match texMathSymbol '\\units' contained conceal cchar=×
  syn match texMathSymbol '\\dual' contained conceal cchar=ⱽ
  syn match texMathSymbol '\\cross' contained conceal cchar=×
  syn match texMathSymbol '\\surjects' contained conceal cchar=↠
  syn match texMathSymbol '\\injects' contained conceal cchar=↣
  syn match texMathSymbol '\\not\\in' contained conceal cchar=∉
  syn match texMathSymbol '\\tensor' contained conceal cchar=⊗
  syn match texMathSymbol '\\oplus' contained conceal cchar=⊕
  syn match texMathSymbol '\\bigoplus' contained conceal cchar=⊕
  syn match texMathSymbol '\\selfmap' contained conceal cchar=⟲
  syn match texMathSymbol '\\actson' contained conceal cchar=⟳
  syn match texMathSymbol '\\iff' contained conceal cchar=⇔
  syn match texMathSymbol '\\semidirect' contained conceal cchar=⋊
  syn match texMathSymbol '\\qed' contained conceal cchar=▧

  syn match texMathSymbol '\\alpha' contained conceal cchar=α
  syn match texMathSymbol '\\beta' contained conceal cchar=β
  syn match texMathSymbol '\\delta' contained conceal cchar=δ
  syn match texMathSymbol '\\Delta' contained conceal cchar=Δ
  syn match texMathSymbol '\\gamma' contained conceal cchar=𝛾
  syn match texMathSymbol '\\mu' contained conceal cchar=μ
  syn match texMathSymbol '\\psi' contained conceal cchar=ψ
  syn match texMathSymbol '\\Psi' contained conceal cchar=Ψ
  syn match texMathSymbol '\\phi' contained conceal cchar=φ
  syn match texMathSymbol '\\rho' contained conceal cchar=ρ
  syn match texMathSymbol '\\ell' contained conceal cchar=ℓ
  syn match texMathSymbol '\\varphi' contained conceal cchar=φ
  syn match texMathSymbol '\\Phi' contained conceal cchar=Φ
  syn match texMathSymbol '\\lambda' contained conceal cchar=λ
  syn match texMathSymbol '\\Lambda' contained conceal cchar=Λ
  syn match texMathSymbol '\\pi' contained conceal cchar=π
  syn match texMathSymbol '\\xi' contained conceal cchar=ξ
  syn match texMathSymbol '\\chi' contained conceal cchar=𝜒
  syn match texMathSymbol '\\eps' contained conceal cchar=ε
  syn match texMathSymbol '\\Sigma' contained conceal cchar=𝚺
  syn match texMathSymbol '\\prod' contained conceal cchar=𝚷
  syn match texMathSymbol '\\sum' contained conceal cchar=𝚺
  syn match texMathSymbol '\\aleph' contained conceal cchar=ℵ
  syn match texMathSymbol '\\textbackslash' contained conceal cchar=\
  syn match texMathSymbol '\\done' contained conceal cchar=✨
  syn match texMathSymbol '\\work' contained conceal cchar=🚩

  syn match texBoldMathText '\\lieg' contained conceal cchar=𝖌
  syn match texBoldMathText '\\lieh' contained conceal cchar=𝖍
  syn match texBoldMathText '\\lies' contained conceal cchar=𝖘
  syn match texBoldMathText '\\lieb' contained conceal cchar=𝖇
  syn match texBoldMathText '\\lien' contained conceal cchar=𝖓
  syn match texBoldMathText '\\mfn' contained conceal cchar=𝖓
  syn match texBoldMathText '\\mfp' contained conceal cchar=𝖕
  syn match texBoldMathText '\\mfq' contained conceal cchar=𝖖
  syn match texBoldMathText '\\mfm' contained conceal cchar=𝖒
  syn match texMathSymbol '\\pr\>' contained conceal cchar=𝔭

  " more reasonably sized symbols that were already defined
  syn match texMathSymbol '\\Rightarrow' contained conceal cchar=⇒
  syn match texMathSymbol '\\Leftarrow' contained conceal cchar=⇐
  syn match texMathSymbol '\\up' contained conceal cchar=↑
  syn match texMathSymbol '\\rightarrow' contained conceal cchar=→
  syn match texMathSymbol '\\to' contained conceal cchar=→
  syn match texMathSymbol '\\mapsvia' contained conceal cchar=→
  syn match texMathSymbol '\\mapsto' contained conceal cchar=→
  syn match texMathSymbol '\\leftarrow' contained conceal cchar=←
  syn match texMathSymbol '\\emptyset' contained conceal cchar=Ø
  syn match texMathSymbol '\\indic' contained conceal cchar=𝟙
  syn match texMathSymbol '\\id' contained conceal cchar=𝟙
  syn match texMathSymbol '\\abs' contained conceal cchar=|
  syn match texMathSymbol '\\theset' contained conceal cchar=  
  syn match texMathSymbol '\\qty' contained conceal cchar=  
  syn match texMathSymbol '\\langle\>\s*' contained conceal cchar=⟨
  syn match texMathSymbol '\s*\\rangle\>' contained conceal cchar=⟩
  syn match texMathSymbol '\\\\' contained conceal cchar=⏎

    " \mathbb characters
  syn match texMathSymbol '\\mathbb{A}' contained conceal cchar=𝔸
  syn match texMathSymbol '\\AA' contained conceal cchar=𝔸
  syn match texMathSymbol '\\mathbb{B}' contained conceal cchar=𝔹
  syn match texMathSymbol '\\mathbb{C}' contained conceal cchar=ℂ
  syn match texMathSymbol '\\mathbb{D}' contained conceal cchar=𝔻
  syn match texMathSymbol '\\mathbb{E}' contained conceal cchar=𝔼
  syn match texMathSymbol '\\Bbb{E}' contained conceal cchar=𝔼
  syn match texMathSymbol '\\mathbb{F}' contained conceal cchar=𝔽
  syn match texMathSymbol '\\mathbb{G}' contained conceal cchar=𝔾
  syn match texMathSymbol '\\mathbb{H}' contained conceal cchar=ℍ
  syn match texMathSymbol '\\mathbb{I}' contained conceal cchar=𝕀
  syn match texMathSymbol '\\mathbb{J}' contained conceal cchar=𝕁
  syn match texMathSymbol '\\mathbb{K}' contained conceal cchar=𝕂
  syn match texMathSymbol '\\mathbb{L}' contained conceal cchar=𝕃
  syn match texMathSymbol '\\mathbb{M}' contained conceal cchar=𝕄
  syn match texMathSymbol '\\mathbb{O}' contained conceal cchar=𝕆
  syn match texMathSymbol '\\mathbb{P}' contained conceal cchar=ℙ
  syn match texMathSymbol '\\mathbb{S}' contained conceal cchar=𝕊
  syn match texMathSymbol '\\mathbb{T}' contained conceal cchar=𝕋
  syn match texMathSymbol '\\mathbb{U}' contained conceal cchar=𝕌
  syn match texMathSymbol '\\mathbb{V}' contained conceal cchar=𝕍
  syn match texMathSymbol '\\mathbb{W}' contained conceal cchar=𝕎
  syn match texMathSymbol '\\mathbb{X}' contained conceal cchar=𝕏
  syn match texMathSymbol '\\mathbb{Y}' contained conceal cchar=𝕐
  syn match texMathSymbol '\\QQ' contained conceal cchar=ℚ
  syn match texMathSymbol '\\RR' contained conceal cchar=ℝ
  syn match texMathSymbol '\\CC' contained conceal cchar=ℂ
  syn match texMathSymbol '\\GG' contained conceal cchar=𝔾
  syn match texMathSymbol '\\DD' contained conceal cchar=𝔻
  syn match texMathSymbol '\\HH' contained conceal cchar=ℍ
  syn match texMathSymbol '\\FF' contained conceal cchar=𝔽
  syn match texMathSymbol '\\ZZ' contained conceal cchar=ℤ
  syn match texMathSymbol '\\PP' contained conceal cchar=ℙ
  syn match texMathSymbol '\\NN' contained conceal cchar=ℕ

  syn match texBoldMathText '\\mA\>' contained conceal cchar=A
  syn match texBoldMathText '\\mB\>' contained conceal cchar=B
  syn match texBoldMathText '\\mC\>' contained conceal cchar=C
  syn match texBoldMathText '\\mD\>' contained conceal cchar=D
  syn match texBoldMathText '\\mE\>' contained conceal cchar=E
  syn match texBoldMathText '\\mF\>' contained conceal cchar=F
  syn match texBoldMathText '\\mG\>' contained conceal cchar=G
  syn match texBoldMathText '\\mH\>' contained conceal cchar=H
  syn match texBoldMathText '\\mI\>' contained conceal cchar=I
  syn match texBoldMathText '\\mJ\>' contained conceal cchar=J
  syn match texBoldMathText '\\mK\>' contained conceal cchar=K
  syn match texBoldMathText '\\mL\>' contained conceal cchar=L
  syn match texBoldMathText '\\mM\>' contained conceal cchar=M
  syn match texBoldMathText '\\mN\>' contained conceal cchar=N
  syn match texBoldMathText '\\mO\>' contained conceal cchar=O
  syn match texBoldMathText '\\mP\>' contained conceal cchar=P
  syn match texBoldMathText '\\mQ\>' contained conceal cchar=Q
  syn match texBoldMathText '\\mR\>' contained conceal cchar=R
  syn match texBoldMathText '\\mS\>' contained conceal cchar=S
  syn match texBoldMathText '\\mT\>' contained conceal cchar=T
  syn match texBoldMathText '\\mU\>' contained conceal cchar=U
  syn match texBoldMathText '\\mV\>' contained conceal cchar=V
  syn match texBoldMathText '\\mW\>' contained conceal cchar=W
  syn match texBoldMathText '\\mX\>' contained conceal cchar=X
  syn match texBoldMathText '\\mY\>' contained conceal cchar=Y
  syn match texBoldMathText '\\mZ\>' contained conceal cchar=Z

  syn match texBoldMathText '\\va\>' contained conceal cchar=a
  syn match texBoldMathText '\\vb\>' contained conceal cchar=b
  syn match texBoldMathText '\\vc\>' contained conceal cchar=c
  syn match texBoldMathText '\\vd\>' contained conceal cchar=d
  syn match texBoldMathText '\\ve\>' contained conceal cchar=e
  syn match texBoldMathText '\\vf\>' contained conceal cchar=f
  syn match texBoldMathText '\\vg\>' contained conceal cchar=g
  syn match texBoldMathText '\\vh\>' contained conceal cchar=h
  syn match texBoldMathText '\\vi\>' contained conceal cchar=i
  syn match texBoldMathText '\\vj\>' contained conceal cchar=j
  syn match texBoldMathText '\\vk\>' contained conceal cchar=k
  syn match texBoldMathText '\\vl\>' contained conceal cchar=l
  syn match texBoldMathText '\\vm\>' contained conceal cchar=m
  syn match texBoldMathText '\\vn\>' contained conceal cchar=n
  syn match texBoldMathText '\\vo\>' contained conceal cchar=o
  syn match texBoldMathText '\\vp\>' contained conceal cchar=p
  syn match texBoldMathText '\\vq\>' contained conceal cchar=q
  syn match texBoldMathText '\\vr\>' contained conceal cchar=r
  syn match texBoldMathText '\\vs\>' contained conceal cchar=s
  syn match texBoldMathText '\\vt\>' contained conceal cchar=t
  syn match texBoldMathText '\\vu\>' contained conceal cchar=u
  syn match texBoldMathText '\\vv\>' contained conceal cchar=v
  syn match texBoldMathText '\\vw\>' contained conceal cchar=w
  syn match texBoldMathText '\\vx\>' contained conceal cchar=x
  syn match texBoldMathText '\\vy\>' contained conceal cchar=y
  syn match texBoldMathText '\\vz\>' contained conceal cchar=z
  " syn match texBoldMathText '\\bar\>' contained conceal cchar=‾

  " \mathcal characters
  syn match texMathSymbol '\\mca' contained conceal cchar=𝓐
  syn match texMathSymbol '\\mathcal{B}' contained conceal cchar=𝓑
  syn match texMathSymbol '\\mathcal B' contained conceal cchar=𝓑
  syn match texMathSymbol '\\mathcal{C}' contained conceal cchar=𝓒
  syn match texMathSymbol '\\mcc' contained conceal cchar=𝓒
  syn match texMathSymbol '\\mathcal{D}' contained conceal cchar=𝓓
  syn match texMathSymbol '\\mcd' contained conceal cchar=𝓓
  syn match texMathSymbol '\\mathcal{E}' contained conceal cchar=𝓔
  syn match texMathSymbol '\\mcf' contained conceal cchar=𝓕
  syn match texMathSymbol '\\mathcal{F}' contained conceal cchar=𝓕
  syn match texMathSymbol '\\mathcal{G}' contained conceal cchar=𝓖
  syn match texMathSymbol '\\mcg' contained conceal cchar=𝓖
  syn match texMathSymbol '\\mathcal{H}' contained conceal cchar=𝓗
  syn match texMathSymbol '\\mch' contained conceal cchar=𝓗
  syn match texMathSymbol '\\mathcal{I}' contained conceal cchar=𝓘
  syn match texMathSymbol '\\mathcal{J}' contained conceal cchar=𝓙
  syn match texMathSymbol '\\mathcal{K}' contained conceal cchar=𝓚
  syn match texMathSymbol '\\mathcal{L}' contained conceal cchar=𝓛
  syn match texMathSymbol '\\mcl' contained conceal cchar=𝓛
  syn match texMathSymbol '\\mathcal{M}' contained conceal cchar=𝓜
  syn match texMathSymbol '\\mathcal M' contained conceal cchar=𝓜
  syn match texMathSymbol '\\mathcal{N}' contained conceal cchar=𝓝
  syn match texMathSymbol '\\mathcal{O}' contained conceal cchar=𝓞
  syn match texMathSymbol '\\OO' contained conceal cchar=𝓞
  syn match texMathSymbol '\\mathcal{P}' contained conceal cchar=𝓟
  syn match texMathSymbol '\\mcp' contained conceal cchar=𝓟
  syn match texMathSymbol '\\mathcal{Q}' contained conceal cchar=𝓠
  syn match texMathSymbol '\\mathcal{R}' contained conceal cchar=𝓡
  syn match texMathSymbol '\\mathcal{S}' contained conceal cchar=𝓢
  syn match texMathSymbol '\\mct' contained conceal cchar=𝓣
  syn match texMathSymbol '\\mathcal{U}' contained conceal cchar=𝓤
  syn match texMathSymbol '\\mathcal{V}' contained conceal cchar=𝓥
  syn match texMathSymbol '\\mathcal{W}' contained conceal cchar=𝓦
  syn match texMathSymbol '\\mathcal{X}' contained conceal cchar=𝓧
  syn match texMathSymbol '\\mathcal{Y}' contained conceal cchar=𝓨
  syn match texMathSymbol '\\mathcal{Z}' contained conceal cchar=𝓩
  syn match texMathSymbol '\\syl' contained conceal cchar=𝓢


  " Simple number super/sub-scripts
  "syn match texMathSymbol '\^t' contained conceal cchar=ᐪ
  "syn match texMathSymbol '\^T' contained conceal cchar=ᐪ
  syn match texMathSymbol '\^0' contained conceal cchar=⁰
  syn match texMathSymbol '\^1' contained conceal cchar=¹
  syn match texMathSymbol '\^2' contained conceal cchar=²
  syn match texMathSymbol '\^3' contained conceal cchar=³
  syn match texMathSymbol '\^4' contained conceal cchar=⁴
  syn match texMathSymbol '\^5' contained conceal cchar=⁵
  syn match texMathSymbol '\^6' contained conceal cchar=⁶
  syn match texMathSymbol '\^7' contained conceal cchar=⁷
  syn match texMathSymbol '\^8' contained conceal cchar=⁸
  syn match texMathSymbol '\^9' contained conceal cchar=⁹

  syn match texMathSymbol '\^{-1}' contained conceal contains=texSuperscripts
  syn match texMathSymbol '\\inv' contained conceal cchar=¹
  syn match texMathSymbol '\^T' contained conceal contains=texSuperscripts
  syn match texMathSymbol '\^{-T}' contained conceal contains=texSuperscripts
  syn match texMathSymbol '\^t' contained conceal contains=texSuperscripts
  syn match texMathSymbol '\^{-t}' contained conceal contains=texSuperscripts
  syn match texSuperscripts '1' contained conceal cchar=¹
  syn match texSuperscripts '-' contained conceal cchar=⁻
  syn match texSuperscripts 'T' contained conceal cchar=ᵀ
  syn match texSuperscripts 't' contained conceal cchar=ᵀ
  syn match texSuperscripts 'i' contained conceal cchar=ⁱ
  syn match texSuperscripts 'n' contained conceal cchar=ⁿ
  syn match texSuperscripts 'o' contained conceal cchar=ᵒ

  syn match texMathSymbol '_0' contained conceal cchar=₀
  syn match texMathSymbol '_1' contained conceal cchar=₁
  syn match texMathSymbol '_2' contained conceal cchar=₂
  syn match texMathSymbol '_3' contained conceal cchar=₃
  syn match texMathSymbol '_4' contained conceal cchar=₄
  syn match texMathSymbol '_5' contained conceal cchar=₅
  syn match texMathSymbol '_6' contained conceal cchar=₆
  syn match texMathSymbol '_7' contained conceal cchar=₇
  syn match texMathSymbol '_8' contained conceal cchar=₈
  syn match texMathSymbol '_9' contained conceal cchar=₉
  syn match texMathSymbol '_i' contained conceal cchar=ᵢ
  syn match texMathSymbol '_o' contained conceal cchar=ₒ

  " logical symbols
  syn match texMathSymbol '\\lor' contained conceal cchar=∨
  syn match texMathSymbol '\\land' contained conceal cchar=∧
  syn match texMathSymbol '\\lnot\>' contained conceal cchar=¬
  syn match texMathSymbol '\\implies' contained conceal cchar=⇒
  syn match texMathSymbol '\\impliedby' contained conceal cchar=⇐
  syn match texMathSymbol '\\geqslant\>' contained conceal cchar=⩾
  syn match texMathSymbol '\\leqslant\>' contained conceal cchar=⩽
  syn match texMathSymbol '\\normal\>' contained conceal cchar=⊴
  syn match texMathSymbol '\\normalneq' contained conceal cchar=⋪
  syn match texMathSymbol '\\subset\>' contained conceal cchar=⊴
  syn match texMathSymbol '\\subseteq' contained conceal cchar=⊆
  syn match texMathSymbol '\\subsetneq' contained conceal cchar=⊊
  syn match texMathSymbol '\\circ' contained conceal cchar=∘

  syn match texMathSymbol '\\intersect' contained conceal cchar=∩
  syn match texMathSymbol '\\int\>' contained conceal cchar=∫

  syn match texStatement '``' contained conceal cchar=“
  syn match texStatement '\'\'' contained conceal cchar=”
  syn match texStatement '\\item\>' contained conceal cchar=•
  syn match texStatement '\\wait' contained conceal cchar=•
  syn match texMathSymbol '\\dd' contained conceal cchar=d
  syn match texDelimiter '\\{' contained conceal cchar={
  syn match texDelimiter '\\}' contained conceal cchar=}
  syn match texMathSymbol '\\setminus\>' contained conceal cchar=\
  syn match texMathSymbol '\\definedas' contained conceal cchar=≔
  syn match texMathSymbol '\\#' contained conceal cchar=#
  "syn match texMathSymbol '\\,' contained conceal cchar=
  "syn match texMathSymbol '\\ ' contained conceal cchar=
  syn match texMathSymbol '\\quad' contained conceal cchar= 
  syn match texMathSymbol '\\sqrt' contained conceal cchar=√
  syn match texMathSymbol '\\not' contained conceal cchar=¬
  syn match texMathSymbol '\\quad' contained conceal cchar=¬
  syn match texMathSymbol '\\over' contained conceal cchar=\
  "syn match texMathSymbol '\\suchthat' contained conceal cchar=϶
  syn match texMathSymbol '\\suchthat\>' contained conceal cchar=|
  syn match texMathSymbol '\\divides' contained conceal cchar=|
  syn match texMathSymbol '\\\!' contained conceal
  "syn match texStatement '\\\[' contained conceal cchar=⟦
  "syn match texStatement '\\\]' contained conceal cchar=⟧

  " hide \text delimiter etc inside math mode
  if !exists("g:tex_nospell") || !g:tex_nospell
    syn region texMathText matchgroup=texStatement start='\\\(\(inter\)\=mathrm\)\s*{'     end='}' concealends keepend contains=@texFoldGroup containedin=texMathMatcher
    syn region texMathText matchgroup=texStatement start='\\\(\(inter\)\=text\|txt\|substack\|parbox\|mbox\)\s*{' end='}' concealends keepend contains=@texFoldGroup,@Spell containedin=texMathMatcher
  else
    syn region texMathText matchgroup=texStatement start='\\\(\(inter\)\=text\|txt\|substack\|parbox\|mbox\|mathrm\)\s*{' end='}' concealends keepend contains=@texFoldGroup containedin=texMathMatcher
  endif

  syn region texBoldMathText matchgroup=texStatement start='\\\(mathbf\|mathrm\|txt\|operatorname\|bm\|symbf\|vector\){' end='}' concealends contains=@texMathZoneGroup containedin=texMathMatcher
  syn cluster texMathZoneGroup add=texBoldMathText

  syn region texBoldItalStyle     matchgroup=texTypeStyle start="\\emph\s*{" end="}" concealends contains=@texItalGroup
  syn region texItalStyle  matchgroup=texTypeStyle start="\\emph\s*{" end="}" concealends contains=@texItalGroup

  set ambiwidth=double
  hi texBoldMathText cterm=bold gui=bold
endif
