---
layout: ''
title: Research Workflow
tags: todo
description: ''
excerpt: ''
header:
  overlay_color: "#333"
toc: true
---

In the last year of my undergraduate degree, I did two quarters [^1] of undergraduate research, and the purpose of this post is to capture some of the research techniques and processes I pieced together during that time. 

One thing that surprised me about the research process was the sheer amount of material one ends up reading. For example, for some topics there were books with multiple chapters dedicated to it, whereas some were covered in a single chapter, section, or even a paragraph. Some topics could only be found in lecture notes, expository writings, theses/dissertations, and of course, papers and journal articles.

It was also surprising how many times I needed results, both small and large, from things I'd previously read, and how difficult it can be to rediscover any particular result. An early example of this for me occurred when I began trying to sort out what was known about the higher homotopy groups of spheres.[^homotopy_wikipedia] [^homotopy_nlab]

I churned through a number of documents, not really knowing what was significant or not. At some point, I found a student's thesis that tabulated the order of certain torsion subgroups of these homotopy groups, and it wasn't until many weeks later that I realized that this was quite a useful thing to have because it included groups in the "unstable" range. Going back and finding that specific document, however, turned out to be quite difficult.

Within Mathematics, we are lucky that LaTeX is widely used, and thus most of the written material in our field ends up in PDFs. The problem then becomes managing a large number of PDFs, plus your own notes or annotations on each one, and being able to find these easily. 

There are a few confounding factors that make this difficult. The first is that browsers tend to download PDFs automatically, even when you are just skimming them within the browser's reader. This quickly leads to a cluttered download folder that contains documents, only some of which may end up containing relevant information. This is compounded by the fact that most PDFs are awfully named, and occasionally lack the OCR layers necessary to search within them.



I thus sought to build some kind of process for how I read, parse, and recollect information, subject to the following constraints:

1. PDFs read in a browser shouldn't be downloaded unless manually specified
2. Documents need to be roughly separated, based on which of these categories they fall into:
   1. Textbooks
   2. Published and peer-reviewed papers (e.g. from the Arxiv)
   3. Expository notes, lecture notes, and other miscellaneous "unofficial" writing 
3. Documents should be imported into some kind of reference management software that handles populating metadata, renaming and sorting files, and maintaining a global BibTex file.
4. Everything needs to sync between all of my devices (computers and Android phones/tablets), so I can read and annotate anywhere, always operating on one single canonical file.
5. Documents need to be read in something that supports adding notes, annotations, and bookmarks.
6. Any annotations and notes put into documents need to be easily searchable, ideally providing a quick way to jump directly to the right spot in the right PDF.


Although it required cobbling together several different tools, I've managed to land on a process that roughly meets these criteria, so I'll try to lay out a rough outline of what my current process it.



# Avoiding Automatic PDF Downloads

The first step is controlling what is downloaded -- although this requires manually downloading anything you want to keep, you can at least be assured that everything that **does** end up on your computer is intentional.

This is useful because not everything I read ends up being relevant -- perhaps I open a PDF to skim it based on a keyword search on the [arXiv](https://arxiv.org/archive/math), which ends up being too far afield to be useful to my particular research project. In this case, I would not want such a document mixed in with documents I'd consider potentially useful.

To accomplish this, I use an extension called [PDF Viewer](https://chrome.google.com/webstore/detail/pdf-viewer/oemmndcbldboiebfnladdacbdfmadadm?hl=en) in Chromium. It bypasses the browser's internal PDF viewer, which prevents any automatic downloading of PDFs, and instead renders them directly in the browser (using the [pdf.js](https://mozilla.github.io/pdf.js/) JavaScript library from Mozilla).[^pdfjs_note]

Thus, the first part of my workflow is skimming papers within the browser, and then manually downloading anything that looks promising and worth a more detailed read.

# Adding OCR Layers

There are many ways to go about this, but I've settled on the wonderful [OCRmyPDF tool](https://github.com/jbarlow83/OCRmyPDF). Usage from the command line is extremely simple, generally something along the lines of `ocrmypdf infile.pdf outfile.pdf`.  

Many other OCR solutions miss many of critical features that this tool gets right -- for example, it positions the OCR'd text accurately, which is important when it comes to highlighting and extracting annotations correctly down the line. It also maintains the original PDF resolution, whereas other tools tend to degrade the quality. Finally, it's easy to script with and tends to **just work** on everything thrown at it, which makes it great for automated batch jobs.

There are scripting approaches [described in their documentation](https://ocrmypdf.readthedocs.io/en/latest/batch.html); two excellent options include setting up a cron job that runs a batch job over your entire "Downloads" directory periodically, or setting this folder up as a "hot" watched folder to OCR each new PDF as it comes in. Since I'm on a laptop and like to control battery usage, I opt to just manually run this on individual PDFs I download.



# Separating Document Types

This one's fairly easy -- since every PDF file is now an intentional download, I simply drop them into one of several subfolders as soon as they are downloaded. 

Separation by type is important for me, because I prefer to use [Calibre](https://calibre-ebook.com/) to manage textbooks. It's quite good at automatically pulling high-quality metadata and cover images from the internet, and creates its own organized directory structure that I can store on Dropbox and point PDF readers to.

For papers and lecture notes, I prefer to store these in separately in [Zotero](https://www.zotero.org/). It is excellent at automatically extracting citation information from papers (when OCR layers are present), it can easily export [BibTex](http://www.bibtex.org/) files for your entire library, and (perhaps most importantly) can be set up to automatically index all document text and annotations. This allows for *extremely* quick searches across the full text content of everything imported.



# Importing Into Management Software

As mentioned above, my two primary document managers are [Calibre](https://calibre-ebook.com/) and [Zotero](https://www.zotero.org/). I choose these because there's no real lock-in; I'm able to store my libraries in plain directory structures, so these primarily help sort, organize, search, and enrich the metadata of what I already have. If both stopped working tomorrow, I would have no issues continuing to use my library directly from the file system.

I tend to use Calibre for more general reading, primarily because it is particularly good at populating metadata and covers for textbooks. This makes for a nice display in casual reading applications.

Zotero I use in a slightly odd way -- I let it manage files for papers and notes, but also let it *link* to the files managed by Calibre. 

Zotero is slightly onerous to use, but has three killer features that make it worth the effort:

- Excellent metadata extraction for papers,
- Maintains a global, automatically updated BibTeX file using the [Better BibTeX plugin](https://github.com/retorquere/zotero-better-bibtex), and
- Excellent annotation extraction and report generation using the [Zotfile plugin](http://zotfile.com/).

Moreover, it has decent internal organizational capabilities using hierarchical "collections", which allows  aliasing items in many separate collections that all reference a single, canonical source file/reference. It also allows linking items to existing files, instead of importing the PDFs files into the directory structure Zotero maintains. In my use case, this lets me hand off papers and notes to Zotero to manage, while also linking to textbooks and other files managed by other software without disturbing their file structures, while also populating reference information.

The way I take care of imports is straightforward - documents are thrown in either a "Books" or a "Papers" catch-all folder in my downloads directory as soon as they are downloaded. It's then easy to set Calibre to automatically watch and import from the "Books" folder. Zotero does not seem to have any "watch folder" features available, and thus requires manually dragging and dropping files from my "Papers" folder directly into the Zotero GUI. Fortunately, once this is done, Zotero copies the file into its internal directory structure and generally populates metadata and reference data automatically.

Thus Zotero manages the "Papers" folder, and it is easy to separately import links to specific textbooks I am working on. This involves navigating to the proper folder in Calibre, then holding **Ctrl-Shift** while dragging it into the main collection in the Zotero GUI. This links the file (instead of copying it in), and then can be set to automatically attempt to pull in metadata and reference information.

# Syncing Between Devices

This one is also quite easy, I simply store Calibre's *Library* folder and (separately) Zotero's *Library* folder on [Dropbox](https://www.dropbox.com/?landing=dbv2). Syncing between PCs is easy enough with the provided applications, although setup on Linux can be tricky as Dropbox relies on a taskbar/notification icon, which some desktop environments (such as Gnome) are phasing out.

Syncing to Android devices requires something like [DropSync](https://play.google.com/store/apps/details?id=com.ttxapps.dropsync&hl=en_US) to kick off a sync to internal storage or your SD card when files are updated or changed.

# Reading and Adding Annotations

I generally want a mix of two types of annotation -- the first freehand drawing, since I occasionally like to color-code things (e.g. to visually distinguish the assumptions of a theorem from the results). The second is being able to either highlight chunks of text or add pop-up notes on the side of the text, both with the intention of being able to digitally search for that text later.

To this end, I've settled on two programs: [Okular](https://okular.kde.org/) on Linux and [Moon+ Reader](https://www.moondownload.com/) on Android. 

Both have the required annotation capabilities, and additionally save your view settings position within a document after it is closed. Thus when a document is reopened, it immediately jumps to the last page viewed, which is quite handy.  Another convenience is that (as far as I can tell) the annotations made with these applications are actually **attached to the PDF** and show up in other viewers, which has not been the case with other viewers I've tried.

# Annotation Extraction

This is perhaps the crown jewel of this workflow, and at least in my case, makes building and sticking to a slightly convoluted setup absolutely worth it. 

This feature is provided by the combination of Zotero and  [the Zotfile plugin](http://zotfile.com/). Annotations can be extracted from any individual document, creating an HTML page that contains all highlighted text and all notes added via pop-up annotations. What makes this *especially* compelling is that it also includes clickable hyperlinks which open the associated PDF jump **directly** to the page of that annotation! 

If desired, you can also select a number of documents and create a joint report, which combines all of the individual reports into a single page.

I can not overstate how useful this is -- if you are diligent about annotating and highlighting definitions, theorems, results, or problems within the PDFs you read, you can quickly hit `Ctrl-F` within Zotero to find a term, which will return the extracted annotation report, which allows you to jump directly into the PDF at the right spot, all in a matter of seconds. 

Subsequently, since your PDFs are OCR'd, you can easily copy-paste text out of it, or use something like the [MathPix snipping tool](https://mathpix.com/) to extract LaTeX for an equation. Since the citation information will already be in your global BibTeX file, it then becomes easy to simply look up the key and cite appropriately.

# Conclusion



[^1]: Around five months
[^homotopy_wikipedia]: For an overview of this fundamental problem, see [https://en.wikipedia.org/wiki/Homotopy_groups_of_spheres](https://en.wikipedia.org/wiki/Homotopy_groups_of_spheres)

[^homotopy_nlab]: For a slightly more involved treatment, see [https://ncatlab.org/nlab/show/homotopy+groups+of+spheres](https://ncatlab.org/nlab/show/homotopy+groups+of+spheres)
[^pdfjs_note]: Browser extensions such as Mendeley or Zotero do not currently seem compatible with this plugin -- however, with this setup, I've rarely needed to actually use these connectors. When I do need them, it's easy to disable to PDFViewer plugin temporarily. 