var fsPDF=function(c,h){function d(c,a,b){var d=1===arguments.length?c:Array.prototype.join.call(arguments," ");u.push(d);m+=d.length+1}function f(c,a,b){b?k.unshift(m):k.push(m);b=b?1:++q;var f;a&&(f="/Length "+a.length);d(b+" 0 obj\r\n<<"+c+(f?f:"")+">>");a&&(d("stream"),d(a),d("endstream"));d("endobj");return b}var r=[],u=[],k=[],t=[],m=0,q=1,y=c.width,n=c.height,v,w,x;return{toDataURL:function(){var q=btoa,a;d("%PDF-1.6\r\n%\u00ffGenerated by FireShot [http://getfireshot.com]\u00ff");if(h.length){for(var b in h){var p=
h[b],e="http://getfireshot.com/pdf_"+btoa(h[b].a),l;t[e]?l=t[e]:(l=f("/Type/Action/S/URI/URI("+e+")"),t[e]=l);p.nActionId=l}for(a in h){b=h[a];for(var g in b.r){p=b.nActionId;e=b.r[g];l=n-Math.max(0,e[1]);var z=Math.min(c.width,e[0]+e[2]),A=n-Math.min(c.height,e[1]+e[3]),e=[(.75*Math.max(0,e[0])).toFixed(2),(.75*A).toFixed(2),(.75*z).toFixed(2),(.75*l).toFixed(2)].join(" ");r.push(f("/Type/Annot/BS<</W 0 /S /S>>/C[0 1 0]/Subtype/Link/Rect["+e+"]/A "+p+" 0 R"))}}}a="/Type /XObject /Subtype /Image /Width "+
c.width+" /Height "+c.height+" /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode ";g=atob(c.toDataURL("image/jpeg").replace("data:image/jpeg;base64,",""));a=f(a,g);a=f("/ProcSet[/PDF/ImageC]/XObject<</I0 "+a+" 0 R>>");g=f("","q\r\n"+(.75*c.width).toFixed(2)+" 0 0 "+(.75*c.height).toFixed(2)+" 0 "+(.75*(n-c.height)).toFixed(2)+" cm\r\n/I0 Do\r\nQ");b="";r.length&&(b="/Annots["+r.join(" 0 R ")+" 0 R]");v=f("/Type/Page/Parent 1 0 R/MediaBox[0 0 "+(.75*y).toFixed(2)+" "+(.75*n).toFixed(2)+
"]/Contents "+g+" 0 R/Resources "+a+" 0 R"+b);w=f("/Type/Catalog/Pages 1 0 R");f("/Type/Pages /Kids ["+v+" 0 R] /Count 1",null,!0);x=m;d("\r\nxref\r\n0 "+(k.length+1)+"\r\n0000000000 65535 f");for(a=0;a<k.length;++a){for(g=k[a].toString();10>g.length;)g="0"+g;d(g+" 00000 n")}d("trailer\r\n<</Root "+w+" 0 R /Size "+(k.length+1)+">>\r\n");d("startxref\r\n"+x+"\r\n%%%%EOF\r\n");a=u.join("\n");return"data:application/pdf;base64,"+q(a)}}};
