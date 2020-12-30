
while ((i++)); read -r line
do
  convert -size 16x16 canvas:"#${line}" "/home/zack/gitclones/XournalCustom/pixmaps/$[i-1]_palette.png"
done < /home/zack/dotfiles/xournal_palette

cat /home/zack/dotfiles/xournal_palette | awk '{print "0x"tolower($0)"ff,"}' | paste - - - - | xsel --clipboard --input

vim +61 "/home/zack/gitclones/xournal-code/src/xo-misc.c"

cd ~/gitclones/xournal-code && ./autogen.sh && ./configure --prefix=$HOME/gitclones/XournalCustom && make && make install && ~/gitclones/XournalCustom/bin/xournal
