"""Draws the launcher icon (a brass compass rose on an old map) as .ico and .png. Original
artwork, no game logos. Needs Pillow.
usage: make_uncharted_icon.py launcher/uncharted.ico launcher/uncharted.png"""
import math
import sys
from PIL import Image, ImageDraw, ImageFilter

S = 1024  # drawn large, scaled down for every icon size
C = S / 2


def polar(angle, radius):
    a = math.radians(angle - 90)
    return C + radius * math.cos(a), C + radius * math.sin(a)


def draw():
    image = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((24, 24, S - 24, S - 24), radius=190, fill=255)

    # Old map paper: warm parchment, darker towards the edges.
    paper = Image.new('RGBA', (S, S))
    pd = ImageDraw.Draw(paper)
    for r in range(int(C * 1.45), 0, -4):
        t = r / (C * 1.45)
        pd.ellipse((C - r, C - r, C + r, C + r),
                   fill=(int(206 - 120 * t ** 1.6), int(170 - 110 * t ** 1.6), int(112 - 80 * t ** 1.6), 255))
    # faint map lines: a coast and a dotted route
    lines = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines)
    coast = [(60 + i * 30, 760 + 60 * math.sin(i / 3.2) + 25 * math.sin(i / 1.3)) for i in range(32)]
    ld.line(coast, fill=(92, 58, 30, 120), width=10, joint='curve')
    for i in range(14):
        x, y = 150 + i * 52, 260 + 40 * math.sin(i / 2.0)
        ld.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(120, 40, 20, 110))
    paper.alpha_composite(lines.filter(ImageFilter.GaussianBlur(2)))

    rose = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rose)
    brass, brass_dark, ink = (214, 165, 72, 255), (142, 98, 34, 255), (40, 26, 16, 255)
    rd.ellipse((C - 360, C - 360, C + 360, C + 360), outline=ink, width=16)
    rd.ellipse((C - 330, C - 330, C + 330, C + 330), outline=brass_dark, width=8)
    for tick in range(0, 360, 10):
        inner = 300 if tick % 90 else 270
        rd.line((polar(tick, inner), polar(tick, 330)), fill=ink, width=8 if tick % 30 else 12)
    # eight points: long cardinal points, short diagonals; each point lit on one side
    for angle, length, width in [(a, 300, 64) for a in (0, 90, 180, 270)] + [(a, 190, 46) for a in (45, 135, 225, 315)]:
        tip, left, right = polar(angle, length), polar(angle - 90, width), polar(angle + 90, width)
        rd.polygon([tip, left, (C, C)], fill=brass)
        rd.polygon([tip, right, (C, C)], fill=brass_dark)
        rd.line([tip, left, (C, C), right, tip], fill=ink, width=6)
    rd.ellipse((C - 44, C - 44, C + 44, C + 44), fill=brass, outline=ink, width=8)
    rd.ellipse((C - 14, C - 14, C + 14, C + 14), fill=ink)
    shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    shadow.paste((20, 10, 4, 150), (0, 0), rose.split()[3].filter(ImageFilter.GaussianBlur(18)))
    paper.alpha_composite(shadow, (10, 14))
    paper.alpha_composite(rose)

    image.paste(paper, (0, 0), mask)
    border = ImageDraw.Draw(image)
    border.rounded_rectangle((24, 24, S - 24, S - 24), radius=190, outline=(58, 36, 20, 255), width=26)
    return image


big = draw()
big.resize((256, 256), Image.LANCZOS).save(
    sys.argv[1], sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
big.resize((128, 128), Image.LANCZOS).save(sys.argv[2])
