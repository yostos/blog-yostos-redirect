+++
title = "コマンドラインで画像のExif修正"
description = "デジカメの日付の設定を間違えたので、Exifの日付をコマンドラインで一括修正する方法を見つけました。"
date = 2024-08-23
aliases = ["/articles/2024/08/23/Exiftool"]

[taxonomies]
tags = ["Tech", "Photography", "CLI"]
[extra]
social_media_card = "ogp.webp"
+++

デジカメの日付の設定を間違えExifの日付を修正したかったが、
AppStoreから余計なアプリをインストールしたくなかったので、Homebrewでexiftoolをインストールして修正。

```bash
# Install exiftool using Homebrew
brew install exiftool

# Confirm dates of exif
exiftool R0000001.jpg
    ExifTool Version Number         : 12.76
    File Name                       : R0000001.JPG
    Directory                       : .
    File Size                       : 12 MB
    File Modification Date/Time     : 2024:08:26 12:42:29+09:00
    File Access Date/Time           : 2024:08:26 12:43:26+09:00
    File Inode Change Date/Time     : 2024:08:26 12:43:24+09:00
    File Permissions                : -rwx------
    File Type                       : JPEG
    File Type Extension             : jpg
    MIME Type                       : image/jpeg
    Exif Byte Order                 : Little-endian (Intel, II)
    (Output truncated for brevity)

# Modify dates of exif
exiftool -Alldates='2024:08:23 12:11:00' -overwrite_original ./*
```
