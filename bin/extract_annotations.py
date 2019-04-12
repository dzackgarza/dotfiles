#!/usr/bin/env python3
import popplerqt5
import sys
import PyQt5
import os
import time

def cleanString(somestr):
    fewer_spaces = ' '.join(somestr.split()).replace("- ", "").translate(str.maketrans({"(": r"\(", ")": r"\)", ".": r"\.", "_": r"\_", "*": r"\*"}))
    return(fewer_spaces)

def main():
    popups = []
    highlights = []
    filenames = []
    dates = []
    #
    filename = sys.argv[1]
    realpath = os.path.abspath(filename)
    # modtime = os.path.getmtime(realpath)
    # print(filename)
    # print(realpath)
    doc = popplerqt5.Poppler.Document.load(filename)
    booktitle = doc.info('Title')
    bookauthor = doc.info('Author')
    print(f"Parsing book: {booktitle}")
    for i in range(doc.numPages()):
        page = doc.page(i)
        annotations = page.annotations()
        if len(annotations) < 1:
            continue
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        for annotation in annotations:
            if not isinstance(annotation, popplerqt5.Poppler.Annotation):
               continue
            dates.append(annotation.modificationDate().toPyDateTime())
            if(isinstance(annotation, popplerqt5.Poppler.TextAnnotation)):
                # print("Found popup text.")
                fewer_spaces = cleanString(annotation.contents())
                popups.append(f'- {fewer_spaces} (<a href="file:///{realpath}#page={i+1}" target="_blank">{bookauthor} {i+1}</a>)')
            if isinstance(annotation, popplerqt5.Poppler.InkAnnotation):
                bdy = annotation.boundary()
                rect_tmp = bdy.getCoords()
                rect = (rect_tmp[0] * pwidth,
                        rect_tmp[1] * pheight,
                        rect_tmp[2] * pwidth,
                        rect_tmp[3] * pheight)
                bdy2 = PyQt5.QtCore.QRectF()
                bdy2.setCoords(*rect)
                txt = str(page.text(bdy2)) + ' '
                fewer_spaces = cleanString(txt)
                highlights.append(f'- {fewer_spaces} (<a href="file:///{realpath}#page={i+1}" target="_blank">{bookauthor} {i+1}</a>)')
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
                fewer_spaces = cleanString(txt)
                highlights.append(f'- {fewer_spaces} (<a href="file:///{realpath}#page={i+1}" target="_blank">{bookauthor} {i+1}</a>)')
            # print(f"Found annotation on page {i+1}")

    total_annotations = len(popups) + len(highlights)
    if total_annotations < 1:
        sys.exit()

    with open("/home/zack/Notes/Annotations/books_annotated.log", "a") as fp:
        fp.write(realpath + '\n')

    modtime = max(dates)
    outdate = modtime.strftime('%m/%d/%Y')
    outfilename = f"/home/zack/Notes/Annotations/{booktitle}.md"
    with open(outfilename, "w") as fp:
        fp.write(f"# {outdate}: {booktitle} ({bookauthor})\n\n")
        fp.write(f"<a href='file:///{realpath}' target='_blank'>{realpath}</a>\n\n")
        fp.write(f"Last Annotation: {outdate}\n\n")
        if len(popups) > 0:
            fp.write("## Notes\n\n")
            fp.write('\n'.join(popups))
            fp.write("<hr>\n\n")
        if len(highlights) > 0:
            fp.write("## Highlights\n\n")
            fp.write('\n'.join(highlights))
            fp.write("<hr>\n\n")
    setutime = time.mktime(modtime.timetuple())
    os.utime(outfilename, (setutime, setutime))
    print(f"Written to {outfilename}")

    # if total_annotations > 0:
        # print (str(total_annotations) + " annotation(s) found")
    # else:
        # print ("no annotations found")


if __name__ == "__main__":
    main()
