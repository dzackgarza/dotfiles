var macs = require("/home/zack/.mume/mathjax_config.js").TeX.Macros
as  = Object.entries(macs).map(a => `\\newcommand{\\${a[0]}}[${a[1][1]}]{${a[1][0]}}`)
require('fs').writeFile("/home/zack/Dropbox/Document Archive/Latex/latexmacs.tex", as.join('\n'), a => a)
