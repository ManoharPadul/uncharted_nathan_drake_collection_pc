"""Draws the Bloodborne icon (a blood moon over gothic spires) as .ico and .png. Needs Pillow.
usage: make_icon.py launcher/bloodborne.ico launcher/bloodborne.png"""
import sys
from PIL import Image, ImageDraw, ImageFilter

S = 1024  # drawn large, scaled down for every icon size


def spire(d, x, base, width, height, color):
    """A tower with a pointed roof and a small finial."""
    roof = height * 0.45
    d.rectangle((x - width / 2, base - height + roof, x + width / 2, base), fill=color)
    d.polygon([(x - width / 2 - width * 0.08, base - height + roof), (x, base - height),
               (x + width / 2 + width * 0.08, base - height + roof)], fill=color)
    d.line((x, base - height, x, base - height - width * 0.6), fill=color, width=max(2, int(width * 0.12)))


def draw():
    image = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((24, 24, S - 24, S - 24), radius=190, fill=255)

    sky = Image.new('RGBA', (S, S))
    sd = ImageDraw.Draw(sky)
    for y in range(S):
        t = y / S
        sd.line((0, y, S, y), fill=(int(40 - 22 * t), int(16 - 8 * t), int(18 - 9 * t), 255))

    glow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((170, 90, 854, 774), fill=(170, 30, 30, 150))
    sky.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))

    moon = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    md = ImageDraw.Draw(moon)
    cx, cy, r = 512, 410, 270
    for i in range(r, 0, -2):
        t = i / r
        md.ellipse((cx - i, cy - i, cx + i, cy + i),
                   fill=(int(150 + 70 * (1 - t)), int(28 + 40 * (1 - t) ** 2), int(26 + 20 * (1 - t) ** 2), 255))
    sky.alpha_composite(moon)

    city = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(city)
    ink = (10, 8, 8, 255)
    base = S - 24
    cd.rectangle((24, 800, S - 24, base), fill=ink)
    for x, w, h in ((90, 60, 330), (175, 44, 250), (250, 70, 400), (340, 52, 300),
                    (684, 52, 300), (774, 70, 400), (849, 44, 250), (934, 60, 330)):
        spire(cd, x, base, w, h, ink)
    # the cathedral in the middle: a wide hall, two towers and the great spire
    cd.rectangle((400, 640, 624, base), fill=ink)
    spire(cd, 430, base, 64, 520, ink)
    spire(cd, 594, base, 64, 520, ink)
    spire(cd, 512, base, 110, 720, ink)
    # pointed windows lit by the moon
    for x in (465, 559):
        cd.rounded_rectangle((x - 14, 760, x + 14, 850), radius=14, fill=(120, 26, 22, 255))
    sky.alpha_composite(city)

    image.paste(sky, (0, 0), mask)
    border = ImageDraw.Draw(image)
    border.rounded_rectangle((24, 24, S - 24, S - 24), radius=190, outline=(200, 169, 106, 255), width=22)
    return image


big = draw()
big.resize((256, 256), Image.LANCZOS).save(
    sys.argv[1], sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
big.resize((128, 128), Image.LANCZOS).save(sys.argv[2])
