"""
Generate a QR code with a logo embedded in the center.

Usage:
    python qr_with_logo.py --data "https://example.com" --logo logo.png --output qr_output.png

Requirements:
    pip install qrcode[pil] pillow
"""

import argparse
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image


def generate_qr_with_logo(
    data: str,
    logo_path: str,
    output_path: str = "qr_with_logo.png",
    logo_size_ratio: float = 0.25,
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
):
    """
    Generate a QR code with a logo placed in the center.

    Args:
        data: The text/URL to encode in the QR code.
        logo_path: Path to the logo image file.
        output_path: Where to save the resulting QR code image.
        logo_size_ratio: Logo size as a fraction of the QR code width (keep <= 0.3
                          so enough of the QR code remains scannable).
        box_size: Pixel size of each QR "box" (controls overall resolution).
        border: Width of the white border around the QR code, in boxes.
        fill_color: Color of the QR code modules.
        back_color: Background color of the QR code.
    """
    # High error correction (~30% recoverable) is required so the QR code
    # still scans correctly even with a logo covering part of the center.
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    # Open and prepare the logo
    logo = Image.open(logo_path)
    if logo.mode != "RGBA":
        logo = logo.convert("RGBA")

    qr_width, qr_height = qr_img.size
    logo_max_size = int(min(qr_width, qr_height) * logo_size_ratio)

    # Resize logo, preserving aspect ratio
    logo.thumbnail((logo_max_size, logo_max_size), Image.LANCZOS)

    # Add a white padded box behind the logo so it stands out clearly
    padding = int(logo.size[0] * 0.12)
    box_size_px = (logo.size[0] + padding * 2, logo.size[1] + padding * 2)
    logo_box = Image.new("RGBA", box_size_px, (255, 255, 255, 255))
    logo_box.paste(logo, (padding, padding), logo)

    # Calculate center position and paste onto the QR code
    pos = (
        (qr_width - logo_box.size[0]) // 2,
        (qr_height - logo_box.size[1]) // 2,
    )
    qr_img.paste(logo_box, pos, logo_box)

    qr_img.save(output_path)
    print(f"QR code saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a QR code with an embedded logo.")
    parser.add_argument("--data", required=True, help="Text or URL to encode")
    parser.add_argument("--logo", required=True, help="Path to the logo image")
    parser.add_argument("--output", default="qr_with_logo.png", help="Output file path")
    parser.add_argument("--logo-ratio", type=float, default=0.25, help="Logo size ratio (0.15-0.3 recommended)")
    parser.add_argument("--box-size", type=int, default=10, help="Pixel size of each QR module")
    parser.add_argument("--fill-color", default="black", help="QR code color")
    parser.add_argument("--back-color", default="white", help="Background color")

    args = parser.parse_args()

    generate_qr_with_logo(
        data=args.data,
        logo_path=args.logo,
        output_path=args.output,
        logo_size_ratio=args.logo_ratio,
        box_size=args.box_size,
        fill_color=args.fill_color,
        back_color=args.back_color,
    )
