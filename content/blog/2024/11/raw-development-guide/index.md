+++
title = "The Ultimate Guide to RAW Development: Data-Driven Insights"
description = "RAW現像について、SILKYPIX, Pixelmator Pro, GR IIIx JPEG の比較を行っています。"
date = 2024-11-25
aliases = ["/articles/2024/11/25/raw-development-guide"]

[taxonomies]
tags = ["Photography", "Tech"]
[extra]
social_media_card = "ogp.webp"
+++

## Introduction

I’ve been using SILKYPIX to develop RAW images captured with my RICOH GR IIIx. However, I’ve recently started wondering: _Is it really worth continuing to use this software?_

There are two main reasons for my hesitation:

1. The processing takes a significant amount of time.
2. The preview feature is sluggish, and the software frequently freezes after extended use.

With macOS now supporting RAW files natively, a variety of apps are available for editing these files. To explore my options, I wrote a Python-based image comparison tool and analyzed three images to see how they stack up:

- **Image 1**: A JPEG file developed using the macOS version of SILKYPIX, without any adjustments.
- **Image 2**: A JPEG file developed using Pixelmator Pro, also without adjustments. Pixelmator Pro takes advantage of macOS's native RAW support, ensuring high compatibility and efficient processing of RAW files.
- **Image 3**: A JPEG image saved directly from the GR IIIx at the time of capture, with the "Negative Film" preset applied via Image Control.

私はRICOH GR IIIxで撮影したRAW画像の現像にSILKYPIXを使用してきました。しかし、最近こう考え始めています：このソフトウェアを使い続ける価値は本当にあるのだろうか？
ためらいの主な理由は2つあります。

処理に相当な時間がかかる。
プレビュー機能が遅く、長時間使用すると頻繁にフリーズする。

macOSが現在RAWファイルをネイティブにサポートするようになり、これらのファイルを編集するための様々なアプリが利用可能です。選択肢を探るために、Pythonベースの画像比較ツールを作成し、3つの画像を分析して比較しました。

画像1：macOS版のSILKYPIXを使用して現像したJPEGファイル（調整なし）。
画像2：Pixelmator Proを使用して現像したJPEGファイル（同じく調整なし）。Pixelmator ProはmacOSのネイティブRAWサポートを活用し、RAWファイルの高い互換性と効率的な処理を確保しています。
画像3：撮影時にGR IIIxから直接保存されたJPEG画像で、イメージコントロールを通じて「ネガティブフィルム」プリセットが適用されています。

## 1. Analyzing the JPEG Files Using Data

The image I used for comparison was a park scene with autumn leaves illuminated by the setting sun.
Here are the results from my Python program:

比較に使用した画像は、夕日に照らされた秋の紅葉がある公園の風景です。
以下が私のPythonプログラムからの結果です。


![Result of Comparison](comparison-result.webp)

```bash
❯ python three-image-comparison.py


Image 1 Analysis:
Size: (4000, 6000, 3)
Mean Brightness: 85.267
Standard Deviation: 72.58
Mean Saturation: 113.675
Contrast: 255
File Size(KB): 19070.3955078125


Image 2 Analysis:
Size: (4000, 6000, 3)
Mean Brightness: 66.147
Standard Deviation: 73.611
Mean Saturation: 135.691
Contrast: 255
File Size(KB): 29992.3681640625


Image 3 Analysis:
Size: (4000, 6000, 3)
Mean Brightness: 93.122
Standard Deviation: 74.255
Mean Saturation: 85.623
Contrast: 255
File Size(KB): 13395.0634765625


Comparison Results:
SSIM 1-2: 0.68
SSIM 1-3: 0.847
SSIM 2-3: 0.737
Histogram Correlation 1-2: 0.3822719180861183
Histogram Correlation 1-3: 0.7985840630919663
Histogram Correlation 2-3: 0.13442670111231494
```

## 2. Insights from the Image Comparison

### 2.1. Image Comparison Results

The characteristics of each image based on the data are as follows:

- **SILKYPIX Image**
  - Moderate brightness with a calm tone.
  - Adequate saturation, achieving a balance of vibrancy and naturalness.
  - Stable brightness, resulting in a uniform finish.
- **Pixelmator Pro Image**
  - The darkest output, emphasizing shadows.
  - The highest saturation, focusing on vibrancy.
  - Dynamic tonal changes, creating a dramatic impression.
- **GR IIIx Jpeg Image (Negative Film Style)**
  - The brightest output, with a light and soft tone.
  - The lowest saturation, offering a calm and natural color palette.
  - Moderate brightness variation, providing smooth and natural gradation.

From the comparison results, the following observations can be made:

- Based on **SSIM (Structural Similarity Index)**, SILKYPIX and Pixelmator Pro exhibit significantly different structures, with notable differences in brightness and saturation. The GR IIIx Jpeg is relatively similar to SILKYPIX but with more subdued saturation.
- According to the **Histogram Correlation**, SILKYPIX and Pixelmator Pro show distinctly different color distributions. When compared to GR IIIx Jpeg, SILKYPIX has some similarity, while Pixelmator Pro displays significant differences.

ータに基づく各画像の特徴は以下の通りです。

- SILKYPIX画像
  - 穏やかなトーンの適度な明るさ。
  - 適切な彩度で、鮮やかさと自然さのバランスを実現。
  - 安定した明るさにより、均一な仕上がりになっている。
- Pixelmator Pro画像
  - 最も暗い出力で、影を強調。
  - 最も高い彩度で、鮮やかさに焦点。
  - ダイナミックな色調の変化により、ドラマチックな印象を作り出す。
- GR IIIx JPEG画像（ネガティブフィルムスタイル）
  - 最も明るい出力で、明るく柔らかいトーン。
  - 最も低い彩度で、落ち着いた自然な色調を提供。
  - 適度な明るさのバリエーションにより、滑らかで自然なグラデーションを提供。

比較結果から、以下の観察が可能です。

SSIM（構造的類似性指標）に基づくと、SILKYPIXとPixelmator Proは明るさと彩
度に顕著な違いがあり、構造が大きく異なります。GR IIIx JPEGはSILKYPIXと比較的
似ていますが、より控えめな彩度となっています。
ヒストグラム相関によると、SILKYPIXとPixelmator Proは明らかに異なる色分布を示しています。GR IIIx JPEGと比較すると、SILKYPIXにはある程度の類似性がありますが、Pixelmator Proは大きな違いを示しています。

### 2.2. Evaluating RAW Development Apps

Based on the analysis, here’s my evaluation of each tool:

- **SILKYPIX**  
  SILKYPIX delivers vivid colors and a balanced brightness level, making it ideal for landscapes or scenes where vibrant colors are essential. Its versatility makes it suitable for various scenarios.SILKYPIXは鮮やかな色とバランスの取れた明るさのレベルを提供し、鮮やかな色が重要な風景やシーンに理想的。その多様性により、様々なシナリオに適している。

- **Pixelmator Pro**  
  With its darker tones and shadow emphasis, Pixelmator Pro works well for dramatic compositions or print projects. However, additional adjustments might be required for darker areas.より暗いトーンと影の強調により、Pixelmator Proはドラマチックな構図や印刷プロジェクトに適している。ただし、暗い部分には追加の調整が必要な場合がある。

- **GR IIIx JPEG (Negative Film Preset)**  
   The GR IIIx JPEG provides a bright, soft tone with natural colors, making
  it great for everyday photography and relaxed scenes.GR IIIx JPEGは明るく柔
  らかいトーンと自然な色を提供し、日常の写真や落ち着いたシーンに最適。

## 3. Final Thoughts

From this comparison, SILKYPIX proves to be a reliable tool, and the numerical data supports its strengths. Surprisingly, I found myself drawn to the GR IIIx JPEG with the Negative Film preset.

A practical workflow could be to shoot in RAW + JPEG mode, using the JPEGs directly for most situations and turning to SILKYPIX for advanced adjustments when needed.

この比較から、SILKYPIXは信頼性の高いツールであり、数値データがその強みを裏付けています。驚いたことに、ネガティブフィルムプリセットを適用したGR IIIx JPEGに魅力を感じました。
実用的なワークフローとしては、RAW + JPEGモードで撮影し、
ほとんどの状況では直接JPEGを使用し、必要に応じてSILKYPIXを使用して調整することが考えられます。

## Appendix. Python Program for Image Analysis

Here is the Python program I used for this analysis. It’s a quick and simple script, so it includes hard-coded file names for convenience. Feel free to adapt it to your needs.

```python
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def compare_three_images(image1_path, image2_path, image3_path, output_path=None):
    """
    Compare three images and analyze them using various metrics


    Parameters:
    image1_path (str): Path to first image
    image2_path (str): Path to second image
    image3_path (str): Path to third image
    output_path (str): Path to save comparison results (optional)


    Returns:
    dict: Comparison metrics
    """
    # Load images
    img1 = cv2.imread(image1_path, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(image2_path, cv2.IMREAD_UNCHANGED)
    img3 = cv2.imread(image3_path, cv2.IMREAD_UNCHANGED)


    if img1 is None or img2 is None or img3 is None:
        raise ValueError("Failed to load one or more images")


    # Normalize to 8-bit if necessary for visualization
    def normalize_to_8bit(img):
        if img.dtype != np.uint8:
            return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return img


    img1_8bit = normalize_to_8bit(img1)
    img2_8bit = normalize_to_8bit(img2)
    img3_8bit = normalize_to_8bit(img3)


    # Convert to grayscale for SSIM
    gray1 = cv2.cvtColor(img1_8bit, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2_8bit, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(img3_8bit, cv2.COLOR_BGR2GRAY)


    # Calculate SSIM between each pair
    ssim_1_2 = ssim(gray1, gray2)
    ssim_1_3 = ssim(gray1, gray3)
    ssim_2_3 = ssim(gray2, gray3)


    # Compare histograms between each pair
    def calculate_hist_correlation(img1, img2):
        hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)


    hist_corr_1_2 = calculate_hist_correlation(img1_8bit, img2_8bit)
    hist_corr_1_3 = calculate_hist_correlation(img1_8bit, img3_8bit)
    hist_corr_2_3 = calculate_hist_correlation(img2_8bit, img3_8bit)


    # Visualization
    plt.figure(figsize=(15, 10))


    # Images
    plt.subplot(231)
    plt.imshow(cv2.cvtColor(img1_8bit, cv2.COLOR_BGR2RGB))
    plt.title("Image 1")
    plt.axis("off")


    plt.subplot(232)
    plt.imshow(cv2.cvtColor(img2_8bit, cv2.COLOR_BGR2RGB))
    plt.title("Image 2")
    plt.axis("off")


    plt.subplot(233)
    plt.imshow(cv2.cvtColor(img3_8bit, cv2.COLOR_BGR2RGB))
    plt.title("Image 3")
    plt.axis("off")


    # Histograms
    plt.subplot(234)
    plt.hist(img1_8bit.ravel(), 256, [0, 256])
    plt.title("Histogram - Image 1")


    plt.subplot(235)
    plt.hist(img2_8bit.ravel(), 256, [0, 256])
    plt.title("Histogram - Image 2")


    plt.subplot(236)
    plt.hist(img3_8bit.ravel(), 256, [0, 256])
    plt.title("Histogram - Image 3")


    if output_path:
        plt.savefig(output_path)


    plt.close()


    return {
        "SSIM 1-2": ssim_1_2,
        "SSIM 1-3": ssim_1_3,
        "SSIM 2-3": ssim_2_3,
        "Histogram Correlation 1-2": hist_corr_1_2,
        "Histogram Correlation 1-3": hist_corr_1_3,
        "Histogram Correlation 2-3": hist_corr_2_3,
        "Size": img1.shape,
        "Bit Depth 1": str(img1.dtype),
        "Bit Depth 2": str(img2.dtype),
        "Bit Depth 3": str(img3.dtype),
    }


def analyze_image(image_path):
    """
    Analyze one image


    Parameters:
    image_path (str): path to the image


    Returns:
    dict: results of analysis
    """
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    return {
        "Size": img.shape,
        "Mean Brightness": np.mean(img),
        "Standard Deviation": np.std(img),
        "Mean Saturation": np.mean(hsv[:, :, 1]),
        "Contrast": np.max(img) - np.min(img),
        "File Size(KB)": os.path.getsize(image_path) / 1024,  # KB単位
    }


def format_results(results_dict):
    """
    Format the results dictionary for better readability
    """
    formatted = {}
    for key, value in results_dict.items():
        if isinstance(value, (np.float64, np.float32)):
            formatted[key] = float(round(value, 3))
        elif isinstance(value, np.uint8):
            formatted[key] = int(value)
        else:
            formatted[key] = value
    return formatted


if __name__ == "__main__":
    # Compare three images
    results = compare_three_images(
        "image1.jpg", "image2.jpg", "image3.jpg", "comparison_result.png"
    )


    # Analyze each image
    images = ["image1.jpg", "image2.jpg", "image3.jpg"]
    for i, image_path in enumerate(images, 1):
        analysis = analyze_image(image_path)
        print(f"\nImage {i} Analysis:")
        for key, value in format_results(analysis).items():
            print(f"{key}: {value}")


    print("\nComparison Results:")
    for key, value in format_results(results).items():
        print(f"{key}: {value}")

```
