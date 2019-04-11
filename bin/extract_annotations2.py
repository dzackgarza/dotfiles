#!/usr/bin/env python3
import popplerqt5
import sys
import PyQt5
import os
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument


def main():
    filename = sys.argv[1]
    realpath = os.path.abspath(filename)
    modtime = os.path.getmtime(realpath)
    # print(filename)
    # print(realpath)
    outstring = ""
    doc = popplerqt5.Poppler.Document.load(filename)
    booktitle = doc.info('Title')
    bookauthor = doc.info('Author')
    total_annotations = 0
    outstring += f"<h1>{booktitle}, {bookauthor}</h1>\n"
    popups = []
    highlights = []
    for i in range(doc.numPages()):
        #print("========= PAGE {} =========".format(i+1))
        page = doc.page(i)
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        if len(annotation) < 1:
            continue
        for annotation in annotations:
            if not isinstance(annotation, popplerqt5.Poppler.Annotation):
               continue
            total_annotations += 1
            txt = ""
            if isinstance(annotation, popplerqt5.Poppler.HighlightAnnotation):
                quads = annotation.highlightQuads()
                for quad in quads:
                    rect = (quad.points[0].x() * pwidth,
                            quad.points[0].y() * pheight,
                            quad.points[2].x() * pwidth,
                            quad.points[2].y() * pheight)
                    bdy = PyQt5.QtCore.QRectF()
                    bdy.setCoords(*rect)
                    txt += str(page.text(bdy)) + ' '
            if(isinstance(annotation, popplerqt5.Poppler.TextAnnotation)):
               txt += annotation.contents()
            fewer_spaces = ' '.join(txt.split()).replace("- ", "")
            highlights.append(f'{fewer_spaces} (<a href="file:///{realpath}#page={i+1}" target="_blank">{bookauthor} {i+1}</a>)</p>\n')

    outstring += "<hr>\n"
    with open(f"/home/zack/Notes/Annotations/{booktitle}.html", "w") as fp:
        fp.write(outstring)
    # if total_annotations > 0:
        # print (str(total_annotations) + " annotation(s) found")
    # else:
        # print ("no annotations found")


if __name__ == "__main__":
    main()
