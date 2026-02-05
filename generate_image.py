#!/usr/bin/env python3
"""
LinkedIn Post Image Generator
Style: Bebas Neue, top-left aligned, key word in red with underline
"""

import os
import ssl
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ssl._create_default_https_context = ssl._create_unverified_context

OUTPUT_DIR = Path(__file__).parent / "output"
ASSETS_DIR = Path(__file__).parent / "assets"
FONT_PATH = ASSETS_DIR / "fonts" / "BebasNeue-Regular.ttf"

# Image settings
IMAGE_SIZE = (1200, 627)  # LinkedIn landscape
FONT_SIZE = 102
LINE_HEIGHT = 90
TEXT_X = 60
TEXT_Y = 60
BRIGHTNESS = 0.5
GRADIENT_WIDTH_PERCENT = 0.6
GRADIENT_ALPHA = 160

# Background images by keyword (real photos from Unsplash)
BACKGROUNDS = {
    'gcc': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200',      # Dubai skyline
    'gulf': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200',
    'dubai': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200',
    'uae': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200',
    'rbi': 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1200',      # Currency/money
    'export': 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1200',
    'credit': 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1200',
    'trade': 'https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=1200',    # Container port
    'goods': 'https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=1200',
    'shipping': 'https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=1200',
    'india': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1200',    # India Gate
    'us': 'https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=1200',       # NYC
    'usa': 'https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=1200',
    'china': 'https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200',       # Shanghai
    'asean': 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1200',    # Singapore
    'fintech': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1200',  # Fintech
    'payment': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1200',     # Digital payment
    'default': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200',  # Earth at night
}


def get_font(size=FONT_SIZE):
    """Load Bebas Neue font."""
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    raise FileNotFoundError(f"Font not found: {FONT_PATH}")


def download_image(url, filename="temp_source.jpg"):
    """Download image from URL."""
    filepath = OUTPUT_DIR / filename
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def find_background(keywords):
    """Find appropriate background based on keywords."""
    text = ' '.join(keywords).lower()
    for key, url in BACKGROUNDS.items():
        if key in text:
            return url
    return BACKGROUNDS['default']


def create_linkedin_image(
    lines_config,
    background_url=None,
    keywords=None,
    output_filename=None
):
    """
    Create LinkedIn post image.

    Args:
        lines_config: List of (text, color) tuples. color is "white" or "red".
                      Red text gets underline.
        background_url: Direct URL to background image (optional)
        keywords: List of keywords to auto-select background (optional)
        output_filename: Output filename

    Returns:
        Path to generated image
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Get background
    if not background_url and keywords:
        background_url = find_background(keywords)
    elif not background_url:
        background_url = BACKGROUNDS['default']

    # Download and process background
    temp_path = download_image(background_url, "temp_bg.jpg")

    if temp_path and temp_path.exists():
        img = Image.open(temp_path)

        # Crop to target aspect ratio
        img_ratio = img.width / img.height
        target_ratio = IMAGE_SIZE[0] / IMAGE_SIZE[1]

        if img_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))

        img = img.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)

        # Darken
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(BRIGHTNESS)
    else:
        # Fallback to dark solid
        img = Image.new('RGB', IMAGE_SIZE, (20, 20, 35))

    # Convert for gradient overlay
    img = img.convert('RGBA')

    # Add gradient on left side
    gradient = Image.new('RGBA', IMAGE_SIZE, (0, 0, 0, 0))
    draw_grad = ImageDraw.Draw(gradient)

    gradient_width = int(IMAGE_SIZE[0] * GRADIENT_WIDTH_PERCENT)
    for x in range(gradient_width):
        alpha = int(GRADIENT_ALPHA * (1 - x / gradient_width))
        draw_grad.line([(x, 0), (x, IMAGE_SIZE[1])], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, gradient)
    img = img.convert('RGB')

    # Draw text
    draw = ImageDraw.Draw(img)
    font = get_font()

    x, y = TEXT_X, TEXT_Y

    for text, color in lines_config:
        text = text.upper()  # Bebas Neue is all caps

        # Shadow
        draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0))

        # Main text
        fill_color = (255, 255, 255) if color == "white" else (220, 38, 38)
        draw.text((x, y), text, font=font, fill=fill_color)

        # Underline for red text
        if color == "red":
            bbox = draw.textbbox((x, y), text, font=font)
            draw.rectangle([x, bbox[3] + 3, bbox[2], bbox[3] + 10], fill=(220, 38, 38))

        y += LINE_HEIGHT

    # Save
    if not output_filename:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"linkedin_image_{timestamp}.jpg"

    output_path = OUTPUT_DIR / output_filename
    img.save(output_path, "JPEG", quality=95)

    # Cleanup
    temp_file = OUTPUT_DIR / "temp_bg.jpg"
    if temp_file.exists():
        temp_file.unlink()

    print(f"✅ Image saved: {output_path}")
    return output_path


# Convenience function for workflow
def generate_post_image(hook_text, emphasis_word, keywords, output_name):
    """
    Generate image from hook text.

    Args:
        hook_text: Full hook text
        emphasis_word: Word to highlight in red (will be on its own line)
        keywords: List of keywords for background selection
        output_name: Output filename
    """
    # Split hook into lines, with emphasis word last
    words = hook_text.replace(emphasis_word, '').strip()

    # Simple split into ~3 lines
    parts = words.split()
    mid = len(parts) // 2

    line1 = ' '.join(parts[:mid])
    line2 = ' '.join(parts[mid:])

    lines_config = [
        (line1, "white"),
        (line2, "white"),
        (emphasis_word, "red"),
    ]

    return create_linkedin_image(
        lines_config=lines_config,
        keywords=keywords,
        output_filename=output_name
    )


if __name__ == "__main__":
    # Example usage
    create_linkedin_image(
        lines_config=[
            ("India-GCC FTA", "white"),
            ("talks officially", "white"),
            ("begin.", "red"),
        ],
        keywords=["gcc", "india", "trade"],
        output_filename="test_image.jpg"
    )
