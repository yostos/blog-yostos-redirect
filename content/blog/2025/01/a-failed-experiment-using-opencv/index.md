+++
title = "A Failed Experiment: Using OpenCV to Read Printed Dates from Scanned Photos"
description = "I recently purchased a scanner and was challenged to see if I could capture the shooting date from the images when digitizing old photos that have dates printed on them."
date = 2025-01-06
aliases = ["/articles/2025/01/06/a-failed-experiment-using-opencv"]

[taxonomies]
tags = ["Tech", "Photography","Python"]
[extra]
social_media_card = "ogp.webp"
+++

### Organizing Old Photographs

I recently purchased a scanner at the end of the year to digitize old photographs. The photographs have dates printed on them, and I've been manually setting these dates in the EXIF information using ExifTool.

I use Hazel to organize image files, and I've already created a tool that updates file creation dates that Hazel can read with the shooting dates from EXIF data. However, since setting EXIF information manually is time-consuming, I explored the possibility of automating this process using OpenCV.

### Date Reading Tool

Below is a script that uses OpenCV to read dates from images and set them using ExifTool.

```python
#!/usr/bin/env python3
from datetime import datetime


def preprocess_image(image_path):
    """
    Extract and process the date stamp portion from the image
    """
    # Load image
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    # Crop the bottom right region
    x1 = int(width * 0.65)
    y1 = int(height * 0.75)
    cropped = img[y1:height, x1:width]

    # Split channels
    b, g, r = cv2.split(cropped)

    # Enhance red channel
    red_emphasis = cv2.subtract(r, cv2.max(b, g))

    # Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(red_emphasis)

    # Strong thresholding
    _, binary = cv2.threshold(enhanced, 30, 255, cv2.THRESH_BINARY)

    # Remove noise
    kernel = np.ones((2,2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Detect and filter contours
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter by area
    mask = np.zeros_like(cleaned)
    min_area = 10
    max_area = 500

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            cv2.drawContours(mask, [contour], -1, (255), -1)

    # Resize to 4x
    result = cv2.resize(mask, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Save debug images
    debug_dir = os.path.join(os.path.dirname(image_path), 'debug')
    os.makedirs(debug_dir, exist_ok=True)

    basename = os.path.basename(image_path)
    cv2.imwrite(os.path.join(debug_dir, f'cropped_{basename}'), cropped)
    cv2.imwrite(os.path.join(debug_dir, f'red_emphasis_{basename}'), red_emphasis)
    cv2.imwrite(os.path.join(debug_dir, f'enhanced_{basename}'), enhanced)
    cv2.imwrite(os.path.join(debug_dir, f'binary_{basename}'), binary)
    cv2.imwrite(os.path.join(debug_dir, f'result_{basename}'), result)

    return result


def extract_date_from_image(image_path):
    """Extract date from image using OCR"""
    # Preprocess image
    processed_image = preprocess_image(image_path)

    # OCR configuration for single line text
    custom_configs = [
        '--psm 6 -c tessedit_char_whitelist="0123456789\' "',  # Uniform text block
        '--psm 7 -c tessedit_char_whitelist="0123456789\' "',  # Single text line
        '--psm 8 -c tessedit_char_whitelist="0123456789\' "',  # Single word
        '--psm 10 -c tessedit_char_whitelist="0123456789\' "'  # Single character
    ]

    for config in custom_configs:
        # Run OCR
        text = pytesseract.image_to_string(processed_image, config=config)
        text = text.strip()
        print(f"OCR result (config={config}): [{text}]")

        # Normalize spaces
        text = ' '.join(text.split())

        # Simple pattern matching
        pattern = r"'?(\d{2})\s*(\d{1,2})\s*(\d{1,2})"
        match = re.search(pattern, text)

        if match:
            try:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))

                # Handle 2000s
                year = 2000 + year if year < 50 else 1900 + year

                if 1 <= month <= 12 and 1 <= day <= 31:
                    return datetime(year, month, day)
            except ValueError:
                continue

    return None


def set_exif_date(image_path, date):
    """Set EXIF date information using ExifTool"""
    if not date:
        print(f"No date found in: {image_path}")
        return False

    date_str = date.strftime("%Y:%m:%d")

    # EXIF tags to set
    exif_tags = [
        "DateTimeOriginal",
        "CreateDate",
        "ModifyDate"
    ]

    command = ["exiftool", "-overwrite_original_in_place"]
    for tag in exif_tags:
        command.extend([f"-{tag}={date_str}"])
    command.append(image_path)

    try:
        subprocess.run(command, check=True, capture_output=True)
        print(f"Date set successfully: {image_path} -> {date_str}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to set EXIF information: {e}")
        return False


def process_images(directory):
    """Process all images in the specified directory"""
    processed = 0
    failed = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            date = extract_date_from_image(image_path)

            if set_exif_date(image_path, date):
                processed += 1
            else:
                failed += 1

    print(f"\nProcessing complete:")
    print(f"Success: {processed}")
    print(f"Failed: {failed}")


def main():
    if len(sys.argv) != 2:
        print("Usage: photodate <image_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Specified path is not a valid directory")
        sys.exit(1)

    process_images(directory)


if __name__ == "__main__":
    main()
```

### Results

I tested the script on 27 scanned photographs.

Out of 27 images, the script only detected dates in 4 images, and among those, only 1 date was correctly recognized.

Well, this isn't practical enough to use.
