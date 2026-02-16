+++
title = "A Command to Sync EXIF Data with File System Timestamps"
description = "I recently embarked on a journey to digitize my old photographs. Since mypre-digital photos exist only as physical prints, I decided to invest in aPFU scanner to bring these memories into the digital age."
date = 2024-12-30
aliases = ["/articles/2024/12/30/exif-tool"]

[taxonomies]
tags = ["Tech", "Photography"]
[extra]
social_media_card = "ogp.webp"
+++

The scanner&apos;s performance has been impressive - it handled even my old San Francisco business trip photos from 2001 beautifully, producing crisp, clear scans.

## Setting EXIF Information

Unlike photos taken with a digital camera, scanned images don't come with proper EXIF data. To preserve the actual capture dates of these photos, I used exiftool from the command line to set the correct EXIF information:

```bash
# Example: Setting the original capture date
exiftool "-DateTimeOriginal=2001:04:15 10:00:00" photo.jpg
```

This command successfully embeds the correct capture date in the photo's EXIF data.

## The Photo Organization

For managing my photo files, I rely on Hazel, a powerful file organization tool for Mac. Hazel offers some fantastic automation features:

- Filtering based on file creation and modification dates
- Automatic folder organization
- Smart file renaming

However, Hazel has one limitation that's been bugging me: it can't directly read EXIF data. This means that even though I've carefully added the correct capture dates to the EXIF data, I can't use this information for Hazel's automated organization.

## The Solution: adj-photodate Script

To bridge this gap, I created a script that syncs EXIF information with the file system timestamps (creation and modification dates). This enables Hazel to organize photos based on their actual capture dates.

The script provides the following features:

- Syncs `DateTimeOriginal` from EXIF to file system timestamps
- Includes a dry-run mode for previewing changes
- Handles batch processing of multiple files
- Supports recursive directory processing

### Installation

1. Create a file named "adj-photodate" and paste the following script:
   - [adj-photodate](https://gist.github.com/yostos/9c301b2831ad3e810cbb4131586687a7)
2. Make it executable:

   ```bash
   chmod +x adj-photodate
   ```

3. Optionally, move it to your path:

   ```bash
   cp adj-photodate ~/bin/
   ```

   Dependencies:

- bash shell
- exiftool

### Usage

```bash
# Process a single file
./adj-photodate photo.jpg

# Preview changes with dry-run
./adj-photodate -n photo.jpg

# Process all JPEG files in a directory recursively
./adj-photodate -r ~/Pictures/Scanned
```

To see available options:

```bash
./adj-photodate --help
```
