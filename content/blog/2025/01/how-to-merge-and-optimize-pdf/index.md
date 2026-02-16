+++
title = "How to Merge and Optimize Your PDF Files"
description = "I recently purchased a DJI Neo drone, and in Japan, it's mandatory to register your drone with the Ministry of Land, Infrastructure, Transport and Tourism (MLIT). During registration, you need to submit a user manual that includes both handling instructions and specifications. However, the DJI Neo manual only contains references to specifications on DJI's website. Therefore, for the registration, I needed to merge the user manual with the specifications from the website."
date = 2025-01-10
aliases = ["/articles/2025/01/10/how-to-merge-and-optimize-pdf"]

[taxonomies]
tags = ["Tech","PDF","CLI"]
[extra]
social_media_card = "ogp.webp"
+++

## Bypassing PDF Password Protection

While the DJI Neo user manual is provided in PDF format, it's password-protected, preventing any modifications or merging. Here's how to bypass the password protection on a Mac:

1. Open the PDF in the Preview app
2. Select "Print" from the File menu (note: not "Export")
3. Choose "Save as PDF" and specify the destination

This process will create a new PDF without password protection.

## Merging PDFs

While this can be done with `Ghostscript` (mentioned later), we'll use `pdftk` for its advantages:

- Preserves PDF internal structure (table of contents, bookmarks, links, etc.)
- Operates at the binary level, preventing quality degradation
- (Although not relevant for this case) Offers flexible operations like page rotation and reordering

Here's how to merge PDFs:

```bash
# Install pdftk (on Mac)
brew install pdftk-java


# Merge PDFs
pdftk input1.pdf input2.pdf cat output merged.pdf
```

## PDF Optimization

After merging, I found that the file size exceeded 40MB, which was too large to upload to MLIT's DIPS2.0 (Drone/UAS Information Platform System).

To resolve this, I used Ghostscript for optimization:

```bash
# Install Ghostscript (on Mac)
brew install ghostscript


# Optimize PDF
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```

The `-dPDFSETTINGS` option allows you to adjust the compression level:

- `/screen`: For screen display (72dpi) - smallest file size
- `/ebook`: For e-books (150dpi) - balanced compression
- `/printer`: For printing (300dpi)
- `/prepress`: For high-quality printing (highest quality)

## Making PDF Searchable

Scanned PDFs aren't searchable. Use these Linux/Mac commands for OCR instead of expensive software:

```bash
brew install ocrmypdf
brew install tesseract-lang
# OCR with image optimization
ocrmypdf -l jpn --optimize 3 input.pdf output.pdf
```

## Creating Table of contents

Scanned PDFs often lack a table of contents. Instead of buying expensive PDF software, use these Linux/Mac commands:

```bash
# Install pdftk (on Mac)
brew install pdftk-java
# Extract metadata
pdftk input.pdf dump_data_utf8 > metadata.txt
```

Open metadata.txt in your editor and add bookmark locations in this format:

```text
BookmarkBegin
BookmarkTitle: Chapter 1
BookmarkLevel: 1
BookmarkPageNumber: 1
BookmarkBegin
BookmarkTitle: Chapter 2
BookmarkLevel: 1
BookmarkPageNumber: 10
```

Then apply the metadata to create a PDF with a table of contents:

```bash
# Apply edited metadata
pdftk input.pdf update_info_utf8 metadata.txt output output.pdf
```

## Conclusion

With these steps, I successfully optimized the PDF and completed the drone registration.

However, it seems rather inefficient to require individual manual submissions for DJI drones, which are widely used. This feels like typical bureaucratic red tape.

Finally, while this may only be relevant for Japanese users, I'm sharing the prepared DJI Neo manual that meets DIPS2.0 requirements here: [Download](https://e.pcloud.link/publink/show?code=XZHwGwZuCQmrRb6SFHGinz8MJe1akHv9dF7)
