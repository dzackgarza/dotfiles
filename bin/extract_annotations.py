#!/usr/bin/env python3
import popplerqt5
import sys
import PyQt5
import os
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument


def main():
    total_annotations = 0
    popups = []
    highlights = []
    #
    filename = sys.argv[1]
    realpath = os.path.abspath(filename)
    modtime = os.path.getmtime(realpath)
    # print(filename)
    # print(realpath)
    doc = popplerqt5.Poppler.Document.load(filename)
    booktitle = doc.info('Title')
    bookauthor = doc.info('Author')
    for i in range(doc.numPages()):
        #print("========= PAGE {} =========".format(i+1))
        page = doc.page(i)
        annotations = page.annotations()
        if len(annotations) < 1:
            continue
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        for annotation in annotations:
            if not isinstance(annotation, popplerqt5.Poppler.Annotation):
               continue
            if(isinstance(annotation, popplerqt5.Poppler.TextAnnotation)):
                print("Found popup text.")
                fewer_spaces = ' '.join(annotation.contents().split()).replace("- ", "")
                popups.append(f'{fewer_spaces} (<a href="file:///{realpath}#page={i+1}" target="_blank">{bookauthor} {i+1}</a>)</p>')
            if isinstance(annotation, popplerqt5.Poppler.HighlightAnnotation):
                txt = ""
                # print("Found highlight.")
                quads = annotation.highlightQuads()
                for quad in quads:
                    rect = (quad.points[0].x() * pwidth,
                            quad.points[0].y() * pheight,
                            quad.points[2].x() * pwidth,
                            quad.points[2].y() * pheight)
                    bdy = PyQt5.QtCore.QRectF()
                    bdy.setCoords(*rect)
                    txt += str(page.text(bdy)) + ' '
                fewer_spaces = ' '.join(txt.split()).replace("- ", "")
                highlights.append(f'{fewer_spaces} (<a href="file:///{realpath}#page={i+1}" target="_blank">{bookauthor} {i+1}</a>)</p>')
            total_annotations += 1

    if total_annotations == 0:
        sys.exit()
    with open(f"/home/zack/Notes/Annotations/{booktitle}.html", "w") as fp:
        fp.write(f"<h1>{booktitle}, {bookauthor}</h1>")
        fp.write(f"File Location: <br>{realpath}")
        fp.write("<h2>Notes</h2>")
        fp.write('\n'.join(popups))
        fp.write("<hr>")
        fp.write("<h2>Highlights</h2>")
        fp.write('\n'.join(highlights))
        fp.write("<hr>")
    # if total_annotations > 0:
        # print (str(total_annotations) + " annotation(s) found")
    # else:
        # print ("no annotations found")


if __name__ == "__main__":
    main()
