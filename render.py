#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news image (1024x1024 PNG).

Flat editorial infographic, all text rendered here with PIL so nothing is
garbled: a masthead naming the day, a hero panel on the APEC summit in
Shenzhen, six story panels, and a footer strip. Run: python3 render.py
writes entry.png beside this file.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (14, 27, 46)
NAVY2 = (27, 58, 92)
INK = (20, 32, 52)
RED = (192, 57, 43)
GOLD = (217, 164, 65)
TEAL = (31, 122, 140)
MUTED = (74, 88, 110)
WHITE = (255, 255, 255)
SKY_TOP = (27, 58, 92)
SKY_BOT = (232, 134, 46)

DJ = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{DJ}/DejaVuSerif-Bold.ttf"
SANS_B = f"{DJ}/DejaVuSans-Bold.ttf"
SANS = f"{DJ}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def flag(draw, x, y, w, h, kind):
    """Small flat flag on a pole at (x, y) top-left of the flag itself."""
    draw.line([(x, y), (x, y + h + 26)], fill=NAVY, width=3)
    if kind == "china":
        draw.rectangle([x + 3, y, x + 3 + w, y + h], fill=(222, 41, 16))
        for sx, sy in [(10, 8), (22, 11), (24, 20), (12, 22)]:
            draw.regular_polygon((x + 3 + sx, y + sy, 4), 5, fill=(255, 222, 89))
    elif kind == "russia":
        draw.rectangle([x + 3, y, x + 3 + w, y + h // 3], fill=WHITE)
        draw.rectangle([x + 3, y + h // 3, x + 3 + w, y + 2 * h // 3], fill=(0, 57, 166))
        draw.rectangle([x + 3, y + 2 * h // 3, x + 3 + w, y + h], fill=(213, 0, 50))
    elif kind == "usa":
        for i in range(7):
            col = (179, 25, 66) if i % 2 == 0 else WHITE
            draw.rectangle([x + 3, y + i * h // 7, x + 3 + w, y + (i + 1) * h // 7], fill=col)
        draw.rectangle([x + 3, y, x + 3 + w // 2, y + 4 * h // 7], fill=(10, 49, 97))
    elif kind == "india":
        draw.rectangle([x + 3, y, x + 3 + w, y + h // 3], fill=(255, 153, 51))
        draw.rectangle([x + 3, y + h // 3, x + 3 + w, y + 2 * h // 3], fill=WHITE)
        draw.rectangle([x + 3, y + 2 * h // 3, x + 3 + w, y + h], fill=(19, 136, 8))
        draw.ellipse([x + 3 + w // 2 - 6, y + h // 2 - 6, x + 3 + w // 2 + 6, y + h // 2 + 6],
                     outline=(0, 56, 120), width=2)
    elif kind == "japan":
        draw.rectangle([x + 3, y, x + 3 + w, y + h], fill=WHITE)
        draw.ellipse([x + 3 + w // 2 - 8, y + h // 2 - 8, x + 3 + w // 2 + 8, y + h // 2 + 8],
                     fill=(188, 0, 45))


def skyline(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, SKY_TOP, SKY_BOT)
    draw.ellipse([x1 - 90, y0 + 58, x1 - 30, y0 + 118], fill=(224, 82, 42))
    horizon = y1 - 46
    buildings = [(0, 150, 46), (48, 118, 34), (84, 168, 52), (138, 96, 40),
                 (180, 140, 44), (226, 110, 36), (264, 156, 48), (314, 128, 42)]
    for bx, bh, bw in buildings:
        draw.rectangle([x0 + bx, horizon - bh, x0 + bx + bw, horizon], fill=NAVY)
        for wy in range(horizon - bh + 10, horizon - 8, 16):
            for wx in range(x0 + bx + 7, x0 + bx + bw - 6, 14):
                if (wx + wy) % 29 < 15:
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=GOLD)
    draw.rectangle([x0, horizon, x1, y1], fill=(16, 38, 64))
    flag(draw, x0 + 26, y1 - 44, 40, 26, "china")
    flag(draw, x0 + 108, y1 - 44, 40, 26, "russia")
    flag(draw, x0 + 190, y1 - 44, 40, 26, "usa")
    draw.rectangle([x0, y1 - 4, x1, y1], fill=GOLD)


def sea_tanker(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (126, 180, 205), (43, 101, 146))
    cx, cy = x0 + 236, y0 + 26
    for i, r in enumerate([8, 15, 22, 29]):
        col = (255, 196, 66) if i % 2 == 0 else (255, 122, 26)
        for a in range(0, 360, 45):
            px = cx + r * math.cos(math.radians(a))
            py = cy + r * math.sin(math.radians(a))
            draw.line([(cx, cy), (px, py)], fill=col, width=4)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 236, 170))
    wy = y1 - 34
    draw.rectangle([x0, wy, x1, y1], fill=(24, 68, 104))
    draw.rectangle([x0 + 24, wy - 20, x0 + 150, wy], fill=(18, 32, 48))
    for bx in range(x0 + 32, x0 + 146, 20):
        draw.rectangle([bx, wy - 34, bx + 14, wy - 20], fill=(217, 164, 65))
    draw.rectangle([x0 + 156, wy - 14, x0 + 176, wy], fill=(18, 32, 48))
    draw.line([(x0 + 8, wy + 12), (x1 - 8, wy + 12)], fill=(126, 180, 205), width=3)
    draw.line([(x0 + 30, wy + 22), (x1 - 30, wy + 22)], fill=(126, 180, 205), width=2)
    dx, dy = x0 + 168, y0 + 20
    draw.ellipse([dx - 9, dy - 4, dx + 9, dy + 4], fill=NAVY)
    for ox, oy in [(-14, -10), (14, -10), (-14, 8), (14, 8)]:
        draw.line([(dx + ox - 8, dy + oy - 3), (dx + ox + 8, dy + oy + 3)], fill=NAVY, width=3)


def bridge(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (214, 226, 238), (164, 190, 210))
    wy = y1 - 26
    draw.rectangle([x0, wy, x1, y1], fill=(43, 101, 146))
    draw.line([(x0 + 10, wy + 10), (x1 - 10, wy + 10)], fill=(126, 180, 205), width=2)
    deck = y0 + 34
    draw.line([(x0 + 8, deck), (x0 + 120, deck)], fill=NAVY, width=5)
    draw.line([(x0 + 190, deck + 26), (x1 - 8, deck + 26)], fill=NAVY, width=5)
    draw.arc([x0 + 24, deck - 44, x0 + 104, deck + 8], 180, 360, fill=NAVY, width=4)
    draw.arc([x0 + 210, deck - 18, x0 + 290, deck + 34], 180, 360, fill=NAVY, width=4)
    for px in (x0 + 20, x0 + 100, x0 + 220, x0 + 280):
        draw.line([(px, deck), (px, wy)], fill=NAVY, width=4)
    draw.line([(x0 + 120, deck), (x0 + 150, deck + 24)], fill=RED, width=6)
    draw.line([(x0 + 150, deck + 24), (x0 + 190, deck + 26)], fill=RED, width=6)
    for cx, cy, r in [(x0 + 158, y0 + 12, 9), (x0 + 176, y0 + 6, 12), (x0 + 196, y0 + 14, 8)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 128, 138))


def ballot_bars(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 240, 244))
    base = y1 - 22
    draw.rectangle([x0 + 52, base - 34, x0 + 112, base], fill=(31, 92, 168))
    draw.rectangle([x0 + 168, base - 26, x0 + 228, base], fill=(179, 25, 66))
    f = font(SANS_B, 17)
    draw.text((x0 + 74, base + 2), "56", font=f, fill=NAVY)
    draw.text((x0 + 190, base + 2), "44", font=f, fill=NAVY)
    draw.rectangle([x0 + 248, y0 + 14, x0 + 296, y0 + 62], fill=WHITE, outline=NAVY, width=3)
    draw.line([(x0 + 256, y0 + 40), (x0 + 266, y0 + 52), (x0 + 288, y0 + 24)], fill=(19, 136, 8), width=5)


def chip(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 46, 38))
    cx, cy = x0 + 110, y0 + 42
    for i in range(5):
        px = x0 + 52 + i * 28
        draw.line([(px, y0 + 6), (px, y0 + 18)], fill=GOLD, width=4)
        draw.line([(px, y1 - 18), (px, y1 - 6)], fill=GOLD, width=4)
        py = y0 + 10 + i * 16
        draw.line([(x0 + 6, py), (x0 + 18, py)], fill=GOLD, width=4)
        draw.line([(x1 - 18, py), (x1 - 6, py)], fill=GOLD, width=4)
    draw.rectangle([cx - 34, cy - 26, cx + 34, cy + 26], fill=(31, 92, 68), outline=GOLD, width=3)
    draw.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=GOLD)
    draw.line([(x1 - 96, y1 - 14), (x1 - 66, y1 - 34), (x1 - 40, y1 - 22), (x1 - 14, y1 - 52)],
              fill=(46, 204, 113), width=6)
    draw.polygon([(x1 - 14, y1 - 52), (x1 - 30, y1 - 50), (x1 - 16, y1 - 36)], fill=(46, 204, 113))


def cyclone(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 233, 240))
    cx, cy = x0 + 130, y0 + 44
    pts = []
    for a in range(0, 540, 6):
        r = 4 + a * 0.075
        pts.append((cx + r * math.cos(math.radians(a - 90)),
                    cy + r * math.sin(math.radians(a - 90))))
    draw.line(pts, fill=TEAL, width=6)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=NAVY)
    for dx, dy in [(200, 12), (230, 26), (260, 10), (290, 28), (216, 40), (246, 46)]:
        draw.line([(x0 + dx, y0 + dy), (x0 + dx - 3, y0 + dy + 8)], fill=NAVY2, width=3)
    draw.polygon([(x1 - 96, y1), (x1, y1 - 34), (x1, y1)], fill=(222, 184, 120))
    draw.line([(x0 + 12, y1 - 12), (x1 - 12, y1 - 12)], fill=(43, 101, 146), width=3)


def two_flags(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 240, 244))
    flag(draw, x0 + 44, y0 + 12, 84, 52, "india")
    flag(draw, x0 + 182, y0 + 12, 84, 52, "japan")
    f = font(SANS_B, 22)
    draw.text((x0 + 138, y0 + 26), "2+2", font=f, fill=NAVY)


PANELS = [
    ("MIDDLE EAST", "US JETS HIT IRAN SITE AS DRONES FLY OVER GULF",
     "Iran drones target Kuwait and Bahrain; tankers burn in Hormuz.", sea_tanker),
    ("EUROPE", "KERCH BRIDGE HIT \u2014 SPAN COLLAPSES",
     "Ukraine strikes the Crimea link a second day.", bridge),
    ("UNITED STATES", "PELTOLA WINS ALASKA SENATE SEAT",
     "Democrats projected to take the Senate 56\u201344.", ballot_bars),
    ("TECHNOLOGY", "NVIDIA'S RECORD $115.8B QUARTER",
     "Revenue doubles; board rules out Huang's return.", chip),
    ("WEATHER \u00b7 INDIA", "CYCLONE AKVAN BEARS DOWN ON ANDHRA",
     "Landfall expected on the coast around Friday.", cyclone),
    ("ASIA", "INDIA AND JAPAN HOLD 2+2 TALKS",
     "Defence and foreign ministers meet in Tokyo.", two_flags),
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    kicker = font(SANS_B, 19)
    d.text((32, 22), "THE DAY IN ONE IMAGE  \u00b7  WORLD NEWS", font=kicker, fill=GOLD)
    date_f = font(SERIF_B, 50)
    d.text((32, 56), "WEDNESDAY 18 NOVEMBER 2026", font=date_f, fill=WHITE)
    d.rectangle([0, 148, W, 153], fill=GOLD)

    # Hero: APEC Shenzhen
    hero_y, hero_h = 165, 300
    d.rectangle([16, hero_y, W - 16, hero_y + hero_h], fill=WHITE, outline=NAVY, width=2)
    skyline(d, (18, hero_y + 2, 408, hero_y + hero_h - 2))
    tx = 432
    tag_f = font(SANS_B, 16)
    d.text((tx, hero_y + 22), "ASIA-PACIFIC  \u00b7  DIPLOMACY", font=tag_f, fill=RED)
    head_f = font(SANS_B, 40)
    y = text_block(d, (tx, hero_y + 52),
                   wrap(d, "XI AND PUTIN MEET IN SHENZHEN", head_f, W - 16 - tx - 24),
                   head_f, NAVY, leading=46)
    sub_f = font(SANS, 21)
    text_block(d, (tx, y + 14),
               wrap(d, "APEC opens \u2014 trilateral summit with Trump on Thursday.", sub_f, W - 16 - tx - 24),
               sub_f, MUTED, leading=27)
    d.text((tx, hero_y + hero_h - 34), "SHENZHEN, CHINA", font=font(SANS_B, 15), fill=MUTED)

    # Grid: 3 x 2 panels
    pw, ph, gap, gx, gy = 322, 206, 12, 16, 481
    tag_f = font(SANS_B, 13)
    head_f = font(SANS_B, 20)
    cap_f = font(SANS, 14)
    for i, (tag, headline, caption, art) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x = gx + col * (pw + gap)
        y = gy + row * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=WHITE, outline=NAVY, width=2)
        art(d, (x + 2, y + 2, x + pw - 2, y + 86))
        d.text((x + 12, y + 96), tag, font=tag_f, fill=RED)
        hy = text_block(d, (x + 12, y + 118),
                        wrap(d, headline, head_f, pw - 24), head_f, NAVY, leading=23)
        text_block(d, (x + 12, hy + 6),
                   wrap(d, caption, cap_f, pw - 24), cap_f, MUTED, leading=17)

    # Footer strip
    fy = 924
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((32, fy + 14), "ALSO ON THE DAY", font=font(SANS_B, 16), fill=GOLD)
    foot_f = font(SANS, 17)
    d.text((32, fy + 42), "Ebola in DR Congo passes 11,000 cases  \u00b7  US loses measles-free status after 26 years",
           font=foot_f, fill=WHITE)
    d.text((32, fy + 68), "Cold kills displaced people in Gaza tents",
           font=foot_f, fill=WHITE)

    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]} {size} bytes")


if __name__ == "__main__":
    main()
