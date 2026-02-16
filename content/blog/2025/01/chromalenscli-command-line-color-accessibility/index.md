+++
title = "ChromaLensCLI: Command Line Color Accessibility Validation"
description = "デザイン入門のようなコースをうけていて「色覚異常の方もいるので気をつけましょうね」とか説明されてんだけど、そんな適当な説明じゃなくちゃんとAccessibilityについて説明しろよと思う。だいたい「気をつける」のでなく、世の中にはちゃんとチェックするツールもあるし・・・・"
date = 2025-01-25
aliases = ["/articles/2025/01/25/chromalenscli-command-line-color-accessibility"]

[taxonomies]
tags = ["Tech", "Software","CLI","Accessibility"]
[extra]
social_media_card = "ogp.webp"
+++

とりあえず色覚異常の方にも画像が正しく認識できてるか確認するためのツール `ChromaLens CLI`を作ってみた。

## ChromaLens CLIの使い方

使い方は、次の通り。

```bash
./chromalens input.jpg output.jpg --type tritanopia
```

これで色覚異常の方が実際どのようにインプットとなる画像が見えているかシミュ
レーションした画像が出力されます。
`type` オプションの指定は次の通りです。

- protanopia (1型色覚)
- deuteranopia (2型色覚)
- tritanopia (3型色覚)

#### ChromeLens CLIの環境設定

以下は、venvでPythonの仮想環境を作って必要なパッケージをインストールする手順です。

```bash
python3 -m venv venv
source venv/bin/activate.fish
pip install numpy Pillow
```

以下が実際のコードです。`chromalens`というファイル名で保管ください。授業中に書いたコードなので、エラー処理などは省いています。

```python
#!/usr/bin/env python3
from PIL import Image


class ColorVisionSimulator:
    MATRICES = {
        'protanopia': np.array([
            [0.567, 0.433, 0.000],
            [0.558, 0.442, 0.000],
            [0.000, 0.242, 0.758]
        ]),
        'deuteranopia': np.array([
            [0.625, 0.375, 0.000],
            [0.700, 0.300, 0.000],
            [0.000, 0.300, 0.700]
        ]),
        'tritanopia': np.array([
            [0.950, 0.050, 0.000],
            [0.000, 0.433, 0.567],
            [0.000, 0.475, 0.525]
        ])
    }


    def simulate(self, image_path, output_path, cvd_type):
        if cvd_type not in self.MATRICES:
            raise ValueError(f"Unsupported CVD type. Choose from: {', '.join(self.MATRICES.keys())}")


        # 画像を読み込み
        img = Image.open(image_path)
        # RGBAの場合はRGBに変換
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # NumPy配列に変換
        img_array = np.array(img)

        # 色変換行列を適用
        matrix = self.MATRICES[cvd_type]
        shape = img_array.shape
        pixels = img_array.reshape(-1, 3)
        converted = np.dot(pixels, matrix.T)

        # 値を0-255の範囲に収める
        converted = np.clip(converted, 0, 255)
        converted = converted.reshape(shape)

        # 画像として保存
        result = Image.fromarray(converted.astype('uint8'), 'RGB')
        result.save(output_path)


def main():
    parser = argparse.ArgumentParser(description='Color Vision Deficiency Simulator')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('output', help='Output image path')
    parser.add_argument('--type', '-t', choices=['protanopia', 'deuteranopia', 'tritanopia'],
                        required=True, help='Type of color vision deficiency')

    args = parser.parse_args()

    simulator = ColorVisionSimulator()
    try:
        simulator.simulate(args.input, args.output, args.type)
        print(f"Simulation complete: {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == '__main__':
    main()
```
