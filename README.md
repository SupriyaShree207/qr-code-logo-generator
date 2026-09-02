# QR Code Generator with Embedded Logo

A simple Python script that generates a scannable QR code with a logo placed in the center. Uses high error correction so the code still scans correctly even with part of it covered by the logo.

## Requirements

- Python 3.7+
- `qrcode[pil]` and `pillow`

Install dependencies:

```bash
pip install qrcode[pil] pillow
```

## Usage

```bash
python qr_with_logo.py --data "https://example.com" --logo logo.png --output qr_output.png
```

### Options

| Flag | Description | Default |
|---|---|---|
| `--data` | Text or URL to encode (required) | — |
| `--logo` | Path to the logo image file (required) | — |
| `--output` | Output file name | `qr_with_logo.png` |
| `--logo-ratio` | Logo size as a fraction of QR width (0.15–0.3 recommended) | `0.25` |
| `--box-size` | Pixel size of each QR module (controls resolution) | `10` |
| `--fill-color` | QR code color | `black` |
| `--back-color` | Background color | `white` |

### Example with custom options

```bash
python qr_with_logo.py --data "https://yourwebsite.com" --logo logo.png --output my_qr.png --logo-ratio 0.2 --fill-color darkblue --back-color white
```

## Tips

- Keep the logo ratio at or below 0.3 (30%) so the QR code stays scannable.
- A PNG logo with a transparent background looks cleanest.
- Always test the final QR code with a phone camera before printing or publishing it.
- Higher `--box-size` values produce a larger, higher-resolution image, useful for printing.

## License

MIT
