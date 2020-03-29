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

Last year, I did two quarters (or about 5 months) of undergraduate research, and the purpose of this post is to capture some of the research techniques I developed during that time. One thing that surprised me about research was the sheer amount of material you end up reading, at varying levels of detail. For some topics, there were books with multiple chapters dedicated to it, and others with just a single chapter or section. Some topics could only be found in lecture notes, expository writings, other students' theses or dissertations, and of course, papers and journal articles from sites such as the Arxiv.

Within Mathematics, we are lucky that LaTeX is widely used, and thus most of the written material in our field ends up in PDFs. The problem is that the default "work flow" for reading and skimming these documents results in an unorganized mess in your downloads folder. This proves to be problematic in research, since it is often the case that documents provide valuable definitions, theorems, and results, most of which involve a fair bit of technical detail that can be difficult to reproduce from scratch.  

There are a few contributing factors here - for one, even though most browsers now allow internally previewing PDFs, *most still download the file, regardless of whether or not it is something you may want to keep*. This is compounded by the fact that most PDFs have really, truly awful file names, almost never containing the title of the paper. And although there are many excellent tools for searching for text within PDFs, many do not have the necessary OCR layer attached.

Taken together, this makes quoting and citing resources you've read into a rather tedious process. I would often read a paper and see something interesting but not immediately noteworthy, only to find out days or weeks later that having that exact statement or result would be useful. Going back to find such results often meant individually sifting through tens (eventually hundreds) of PDFs to find the paper again, then skimming anywhere from 10 to 400 pages to find the statement again.

I thus sought to build some kind of process for how I read, parse, and recollect information, subject to the following constraints:

1. PDFs read in a browser shouldn't be downloaded unless manually specified

2. Once manually downloaded, a PDF should have an OCR layer added, allowing the use of tools like `pdfgrep` and the extraction of metadata.

3. Documents need to be roughly separated, based on which of these categories they fall into:
   1. Textbooks
   2. Published, peer-reviewed papers (e.g. from the Arxiv)
   3. Expository notes, lecture notes, and other miscellaneous "unofficial" writing 

4. After being downloaded, documents should be imported into some kind of management software that handles populating metadata, renaming and sorting files, and maintaining a global BibTex file.

5. Everything needs to sync between all of my devices (computers and Android phones/tablets), so I can read and annotate anywhere and always be operating on one single file.

6. Documents need to be read in something that supports adding notes, annotations, and bookmarks.

7. Any annotations and notes put into documents need to be easily searchable, ideally providing a quick way to jump directly to the right spot in the right PDF.

   

To this end, I've been somewhat successful! I'd like to lay out the technical solution here, for anyone looking for something similar.



# Avoiding Automatic PDF Downloads

The first step is controlling what is downloaded -- although this requires manually downloading anything you want to keep, you can at least be assured that everything that **does** end up on your computer is intentional.

Since I use a variant of the Chromium browser, I use an extension called [PDF Viewer](https://chrome.google.com/webstore/detail/pdf-viewer/oemmndcbldboiebfnladdacbdfmadadm?hl=en) to accomplish this. It essentially bypasses Chromium's internal PDF viewer, instead rendering files within the browser (using the nice [pdf.js](https://mozilla.github.io/pdf.js/) JavaScript library from Mozilla), entirely preventing the file from being automatically downloaded.

Thus the first part of this workflow is skimming papers within the browser, and then manually downloading anything that looks promising and worth a more detailed read.

*Note: extensions such as Mendeley or Zotero's import tools do not currently seem compatible with this plugin -- however, this workflow obviates the need for either!*

# Adding OCR Layers

There are many ways to go about this, but I've settled on the wonderful [OCRmyPDF tool](https://github.com/jbarlow83/OCRmyPDF). Usage from the command line is extremely simple, generally something along the lines of `ocrmypdf infile.pdf outfile.pdf`.  

Many other OCR solutions miss many of critical features that this tool gets right - for example, it positions the OCR'd text accurately, which is important when it comes to highlighting and extracting annotations correctly down the line. It also maintains the original PDF resolution, whereas other tools tend to degrade the quality. Finally, it's amazingly easy to script with and tends to **just work** on everything thrown at it, which makes it great for automated batch jobs.

There are scripting approaches [described in their documentation](https://ocrmypdf.readthedocs.io/en/latest/batch.html); two excellent options include setting up a cron job that runs a batch job over your entire "Downloads" directory periodically, or setting this folder up as a "hot" watched folder to OCR each new PDF as it comes in. Since I'm on a laptop and like to control battery usage, I opt for the manual approach.



# Separating Document Types

This one's fairly easy -- since every PDF file is now an intentional download, I simply drop them into one of several subfolders as soon as they are downloaded. 

Separation by type is important for me, because I prefer to use [Calibre](https://calibre-ebook.com/) to manage my library of textbooks. It's quite good at automatically pulling good metadata and cover images from the internet, and creates its own organized directory structure that I can point reading applications at.

For papers and lecture notes, I prefer to store these in separately in [Zotero](https://www.zotero.org/). It is excellent at automatically extracting citation information from papers (when they have OCR layers), it can easily export [BibTex](http://www.bibtex.org/) files for your entire library, and (perhaps most importantly) can be set up to automatically index all of the OCR'd text of the documents it sees, allowing for *extremely* quick searches across the full text in all of your documents.



# Importing Into Management Software

As mentioned above, my two primary document managers are [Calibre](https://calibre-ebook.com/) and [Zotero](https://www.zotero.org/). I choose these because there's no real vendor lock-in; I'm able to store my libraries in plain file structures, and these only help sort, organize, search, and enrich what I already have. If both stopped working tomorrow, I would have no issues continuing to use my library directly from the file system.

Calibre is what I use for more general reading, primarily because it is particularly good at populating metadata and covers for textbooks, which makes for a nice display in casual reading applications.

Zotero I use in a slightly odd way - I let it manage files for papers and notes, but also let it *link* to the files managed by Calibre. I primarily use Zotero for its ability to extract annotations and it's excellent search capabilities, including quickly searching the full text of PDFs.

The way I take care of imports is straightforward - documents are thrown in either a "Books" or a "Papers" catch-all folder in my downloads directory as soon as they are downloaded. It's then easy to set Calibre to automatically watch and import from the "Books" folder.

For Zotero, watching folders isn't a built-in feature, and instead requires additionally installing the [Zotfile plugin](http://zotfile.com/). With this installed, I can then point it to the "Papers" folder.

Both behave similarly -- whenever I initiate a library update, both pull all of the PDFs from their respective folders, attempt to download metadata, and then move them into their respective sorted library folders.

There are really two killer features of this plugin, the first being this ability to watch folders, and the second being its astoundingly good annotation extraction (which I'll explain more momentarily). With the plugin installed, it's simply a matter of pointing it to the "Papers" directory to watch.

I thus let Zotero manage all of the files for papers and notes, but it also allows *linking* to external files -- that is, it doesn't manage the actual files, but instead records the location and includes it in its indexing, searching, annotation extraction, BibTex generation, etc. 

Although this may sound slightly complicated, it turns out the be quite easy thanks to [the ZMI plugin for Calibre](https://www.mobileread.com/forums/showthread.php?p=3339192). Although it has to be done manually, this plugin allows you to export all of the information about your library into a file, which can be directly imported into Zotero as a new collection. What's especially compelling is that is records the *file location* for each book, and imports them into Zotero as links (as opposed to copying any files).

# Syncing Between Devices

This one is also quite easy, I simply store Calibre's *Library* folder and a separate *Zotero Library* folder on [Dropbox](https://www.dropbox.com/?landing=dbv2). Syncing between PCs is easy enough with the provided applications, although setup on Linux can be tricky as Dropbox relies on a taskbar/notification icon, which some desktop environments (such as Gnome) are phasing out.

Syncing to Android devices requires something like [DropSync](https://play.google.com/store/apps/details?id=com.ttxapps.dropsync&hl=en_US) to kick off a sync when files change.



# Reading and Adding Annotations

I generally want a mix of two types of annotation - the first is being able to draw a bit on PDFs, since I occasionally like to color-code things (e.g. to quickly visually distinguish the assumptions of a theorem from the results). The second, however, is being able to either highlight chunks of text, or add pop-up notes on the side of the text, both with the intention of being able to digitally search for that text at a later time.

To this end, I've settled on two programs: [Okular](https://okular.kde.org/) on Linux and [Moon+ Reader](https://www.moondownload.com/) on Android. 

Both have the appropriate annotation capabilities, and additionally save your view settings position within a document after it is closed. Another convenience is that, as far as I can tell, the annotations made these applications are actually attached **to** the PDF and show up in other viewers, which is not always the case.



# Annotation Extraction

This is perhaps the crown jewel of this workflow, and at least in my case, makes building and sticking to a slightly complex system absolutely worth it. This feature is provided by the combination of Zotero and  [the Zotfile plugin](http://zotfile.com/). Annotations can be extracted from any individual document, creating an HTML document that contains all highlighted text as well as any notes added in popups. What makes this *especially* compelling is that it also includes a hyperlink that you can click which opens the PDF in your default viewer and jumpts **directly** to the page of that annotation! Moreover, you can select any number of documents and create a joint report, which combines all of the individual reports into a single page.

I simply can't overstate how useful this is - if  