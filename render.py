#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page, drawn entirely in code.

One 1024x1024 PNG: a newspaper front page. Masthead names the day
(WEDNESDAY 18 NOVEMBER 2026); the lead is the Gulf escalation; the rest
covers the Kerch Bridge, the Shenzhen three-way summit, the Alaska Senate
race, the Congo Ebola outbreak, the US measles status, Voyager 1, plus a
ticker with the Siberia crash and Cyclone Xavier.

Every fact is as reported on 18 Nov 2026 (Reuters / UN / NASA / PAHO):
- US jets struck a Revolutionary Guard missile site on Qeshm Island;
  Iran answered with drones at US sites in Bahrain and Kuwait.
- Ukraine hit the Kerch Bridge a second day; part of the road span fell.
- Xi, Putin and Trump meet in Shenzhen at APEC.
- Mary Peltola won Alaska's Senate seat; Democrats lead 56-44.
- Ebola in DR Congo: 11,000+ cases, 5,400 deaths.
- The US lost its measles elimination status: 5,412 cases in 2026.
- Voyager 1 reached one light-day from Earth (16 billion miles).
- A Russian military plane crashed in Siberia: 19 dead.
- Category 5 Cyclone Xavier hit the Northern Cook Islands.

Drawn with PIL + DejaVu only; no external images, no network.
Output: entry.png (PNG, 1024x1024, well under 1 MiB).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 242, 233)
INK = (16, 24, 34)
NAVY = (13, 33, 55)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
TEAL = (36, 122, 140)
SAND = (224, 205, 164)
WHITE = (255, 255, 255)
GREY = (90, 96, 104)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, max_w, start, floor=12):
    """Largest font size (<= start, >= floor) that fits max_w."""
    size = start
    while size > floor:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, floor)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(draw, x, y, w, h, accent):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=(60, 60, 60), width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=accent)


def headline(draw, text, x, y, w, size=30, color=INK):
    f = fit(draw, text, BOLD, w, size)
    for i, line in enumerate(wrap(draw, text, f, w)):
        draw.text((x, y + i * int(size * 1.12)), line, font=f, fill=color)
    return y + len(wrap(draw, text, f, w)) * int(size * 1.12)


def subline(draw, text, x, y, w, size=19):
    f = font(REG, size)
    for i, line in enumerate(wrap(draw, text, f, w)):
        draw.text((x, y + i * int(size * 1.35)), line, font=f, fill=(40, 40, 40))
    return y + len(wrap(draw, text, f, w)) * int(size * 1.35)


def starburst(draw, cx, cy, r, color):
    """Explosion flash: 12 spikes + core."""
    for k in range(12):
        a = k * math.pi / 6
        x2 = cx + r * math.cos(a)
        y2 = cy + r * math.sin(a)
        draw.line([cx, cy, x2, y2], fill=color, width=5)
    draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
                 fill=color)


def jet(draw, x, y, s, color, flip=False):
    """Simple jet silhouette (triangle body + wings)."""
    d = -1 if flip else 1
    draw.polygon([(x, y), (x + d * s, y + s * 0.28), (x + d * s * 0.55, y + s * 0.55),
                  (x + d * s * 0.25, y + s * 0.35), (x, y + s * 0.5)], fill=color)


def draw_gulf(draw, x, y, w, h):
    """Schematic Strait of Hormuz: Iran top, Arabia bottom, Qeshm Island."""
    draw.rectangle([x, y, x + w, y + h], fill=(168, 208, 220))  # sea
    # Iran landmass (top) and Arabian peninsula (bottom): plain trapezoids.
    draw.polygon([(x, y), (x + w, y), (x + w, y + h * 0.36),
                  (x, y + h * 0.30)], fill=SAND)
    draw.polygon([(x, y + h), (x + w, y + h), (x + w, y + h * 0.74),
                  (x, y + h * 0.78)], fill=SAND)
    # Qeshm Island in the strait.
    ix, iy = x + w * 0.52, y + h * 0.52
    draw.ellipse([ix - 34, iy - 12, ix + 34, iy + 12], fill=SAND,
                 outline=INK, width=2)
    starburst(draw, ix, iy - 6, 26, (214, 48, 49))
    # Bahrain + Kuwait markers.
    bx, by = x + w * 0.16, y + h * 0.62
    kx, ky = x + w * 0.30, y + h * 0.30
    for px, py in ((bx, by), (kx, ky)):
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                     outline=WHITE, width=2)
    f = font(BOLD, 20)
    draw.text((ix + 42, iy - 34), "QESHM ISLAND", font=f, fill=INK)
    draw.text((bx + 14, by - 10), "BAHRAIN", font=f, fill=INK)
    draw.text((kx + 14, ky - 26), "KUWAIT", font=f, fill=INK)
    # Jets + drone trail.
    jet(draw, x + w * 0.66, y + h * 0.16, 46, INK)
    jet(draw, x + w * 0.76, y + h * 0.26, 38, INK, flip=True)
    draw.line([kx + 10, ky + 8, bx - 8, by - 6], fill=RED, width=3)
    for t in (0.33, 0.55, 0.77):
        px = kx + 10 + (bx - 18 - kx) * t
        py = ky + 8 + (by - 14 - ky) * t
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    f2 = font(REG, 17)
    draw.text((x + 10, y + h - 26), "STRAIT OF HORMUZ", font=f2, fill=(30, 60, 80))


def draw_bridge(draw, x, y, w, h):
    """Kerch Bridge: deck across, middle span collapsed into the strait."""
    draw.rectangle([x, y, x + w, y + h], fill=(150, 190, 205))  # water
    mid = x + w // 2
    # Two standing spans with a wide gap where the middle span fell.
    draw.rectangle([x + 8, y + h * 0.42, mid - 62, y + h * 0.42 + 10], fill=INK)
    draw.rectangle([mid + 62, y + h * 0.42, x + w - 8, y + h * 0.42 + 10], fill=INK)
    # Towers.
    for tx in (x + w * 0.22, x + w * 0.78):
        draw.rectangle([tx - 5, y + h * 0.12, tx + 5, y + h * 0.42], fill=INK)
    # Fallen span, tilted low in the water.
    draw.polygon([(mid - 56, y + h * 0.62), (mid + 56, y + h * 0.70),
                  (mid + 50, y + h * 0.80), (mid - 62, y + h * 0.72)], fill=(120, 40, 40))
    # Smoke + splash.
    for sx, sy, r in ((mid - 44, y + h * 0.32, 9), (mid + 6, y + h * 0.28, 11),
                      (mid + 42, y + h * 0.34, 8)):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(225, 225, 225),
                     outline=(140, 140, 140))
    draw.arc([mid - 56, y + h * 0.66, mid + 56, y + h * 0.94], 0, 180,
             fill=WHITE, width=3)


def draw_flags(draw, x, y, w, h):
    """Three small flags: China, Russia, USA."""
    fw, fh = (w - 24) // 3, 52
    # China: red + stars.
    cx = x
    draw.rectangle([cx, y, cx + fw, y + fh], fill=(222, 41, 16))
    draw.text((cx + 8, y + 6), "\u2605", font=font(BOLD, 26), fill=(255, 222, 0))
    for sx, sy in ((cx + 34, y + 8), (cx + 44, y + 18), (cx + 40, y + 30), (cx + 30, y + 34)):
        draw.text((sx, sy), "\u2605", font=font(BOLD, 11), fill=(255, 222, 0))
    # Russia: white / blue / red.
    rx = x + fw + 12
    draw.rectangle([rx, y, rx + fw, y + fh], fill=WHITE, outline=INK, width=1)
    draw.rectangle([rx, y + fh // 3, rx + fw, y + 2 * fh // 3], fill=(0, 57, 166))
    draw.rectangle([rx, y + 2 * fh // 3, rx + fw, y + fh], fill=(213, 0, 50))
    # USA: stripes + canton.
    ux = x + 2 * (fw + 12)
    for i in range(7):
        draw.rectangle([ux, y + i * (fh // 7), ux + fw, y + (i + 1) * (fh // 7)],
                       fill=RED if i % 2 == 0 else WHITE)
    draw.rectangle([ux, y, ux + fw * 0.45, y + fh * 0.55], fill=(30, 40, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([ux + 5 + c * 9, y + 5 + r * 9, ux + 9 + c * 9, y + 9 + r * 9],
                         fill=WHITE)


def draw_ballot(draw, x, y, s):
    """Ballot box with a star."""
    draw.rectangle([x, y + s * 0.25, x + s, y + s], fill=(200, 170, 120),
                   outline=INK, width=3)
    draw.rectangle([x + s * 0.12, y, x + s * 0.88, y + s * 0.30], fill=INK)
    draw.rectangle([x + s * 0.38, y + s * 0.08, x + s * 0.62, y + s * 0.20],
                   fill=PAPER)
    draw.text((x + s * 0.28, y + s * 0.42), "\u2605", font=font(BOLD, int(s * 0.42)),
              fill=NAVY)


def draw_virus(draw, x, y, r):
    """Spiked virus ball."""
    for k in range(10):
        a = k * math.pi / 5
        x2 = x + (r + 12) * math.cos(a)
        y2 = y + (r + 12) * math.sin(a)
        draw.line([x, y, x2, y2], fill=RED, width=4)
        draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=RED)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(150, 30, 30))
    draw.ellipse([x - r * 0.45, y - r * 0.5, x - r * 0.1, y - r * 0.15],
                 fill=(200, 90, 90))


def draw_measles(draw, x, y, s):
    """Red spots on a face outline (rash)."""
    draw.ellipse([x, y, x + s, y + s], outline=INK, width=4)
    for px, py, r in ((0.3, 0.3, 9), (0.62, 0.25, 11), (0.45, 0.55, 10),
                      (0.68, 0.6, 8), (0.28, 0.62, 7), (0.5, 0.78, 6)):
        draw.ellipse([x + s * px - r, y + s * py - r, x + s * px + r, y + s * py + r],
                     fill=RED)


def draw_voyager(draw, x, y, w, h):
    """Starfield, gold probe dish, Earth far below."""
    draw.rectangle([x, y, x + w, y + h], fill=(8, 14, 34))
    import random
    rng = random.Random(18112026)
    for _ in range(60):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        r = rng.choice((1, 1, 2))
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
    cx, cy = x + w // 2, y + h // 2 - 6
    draw.polygon([(cx - 34, cy - 26), (cx + 34, cy - 26), (cx, cy + 6)],
                 outline=GOLD, width=3)
    draw.line([cx, cy + 6, cx + 44, cy + 34], fill=GOLD, width=3)
    draw.ellipse([cx + 38, cy + 28, cx + 52, cy + 42], fill=GOLD)
    draw.line([cx, cy + 6, cx - 30, cy + 30], fill=GOLD, width=2)
    draw.ellipse([x + w - 46, y + h - 40, x + w - 10, y + h - 4],
                 fill=(70, 130, 200))


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    f_title = fit(d, "THE WORLD IN ONE DAY", BOLD, W - 40, 46)
    d.text(((W - d.textlength("THE WORLD IN ONE DAY", font=f_title)) / 2, 12),
           "THE WORLD IN ONE DAY", font=f_title, fill=WHITE)
    f_date = fit(d, "WEDNESDAY  \u00b7  18 NOVEMBER 2026", BOLD, W - 40, 30)
    d.text(((W - d.textlength("WEDNESDAY  \u00b7  18 NOVEMBER 2026", font=f_date)) / 2, 66),
           "WEDNESDAY  \u00b7  18 NOVEMBER 2026", font=f_date, fill=GOLD)

    # ---- Lead: Gulf escalation ----
    lx, ly, lw, lh = 12, 130, 600, 430
    panel(d, lx, ly, lw, lh, RED)
    draw_gulf(d, lx + 10, ly + 10, lw - 20, 250)
    hy = headline(d, "U.S. STRIKES QESHM ISLAND", lx + 16, ly + 276, lw - 32, 36)
    subline(d, "Iran answers with drones on U.S. bases in Bahrain and Kuwait.",
            lx + 16, hy + 6, lw - 32, 20)
    subline(d, "Gulf on edge as strikes and counter-strikes spread.",
            lx + 16, hy + 62, lw - 32, 20)

    # ---- Right top: Kerch Bridge ----
    rx, ry, rw, rh = 624, 130, 388, 212
    panel(d, rx, ry, rw, rh, TEAL)
    draw_bridge(d, rx + 10, ry + 10, rw - 20, 96)
    hy = headline(d, "KERCH BRIDGE HIT AGAIN", rx + 14, ry + 114, rw - 28, 26)
    subline(d, "Second day of strikes; part of the road span falls into the strait.",
            rx + 14, hy + 4, rw - 28, 17)

    # ---- Right bottom: Shenzhen summit ----
    sx, sy, sw, sh = 624, 354, 388, 206
    panel(d, sx, sy, sw, sh, GOLD)
    draw_flags(d, sx + 14, sy + 12, sw - 28, 52)
    hy = headline(d, "XI \u00b7 PUTIN \u00b7 TRUMP MEET", sx + 14, sy + 76, sw - 28, 26)
    subline(d, "Three-way talks open in Shenzhen as APEC leaders gather.",
            sx + 14, hy + 4, sw - 28, 17)

    # ---- Bottom row: four stories ----
    by, bh = 572, 316
    bx0 = [12, 266, 520, 774]
    bw = 238
    stories = [
        (NAVY, "PELTOLA WINS ALASKA",
         "Democrat takes the Senate seat; party leads 56\u201344.", "ballot",
         "ALASKA \u00b7 USA"),
        (RED, "EBOLA SURGES IN CONGO",
         "Outbreak passes 11,000 cases; 5,400 dead.", "virus",
         "DR CONGO \u00b7 AFRICA"),
        (RED, "U.S. LOSES MEASLES-FREE STATUS",
         "5,412 cases in 2026 \u2014 the most since 1991.", "measles",
         "UNITED STATES"),
        (NAVY, "VOYAGER 1: ONE LIGHT-DAY",
         "Probe reaches 16 billion miles from Earth.", "voyager",
         "DEEP SPACE"),
    ]
    for (accent, head, sub, kind, tag), bx in zip(stories, bx0):
        panel(d, bx, by, bw, bh, accent)
        if kind == "voyager":
            draw_voyager(d, bx + 10, by + 16, bw - 20, 110)
        elif kind == "ballot":
            draw_ballot(d, bx + bw // 2 - 34, by + 30, 68)
        elif kind == "virus":
            draw_virus(d, bx + bw // 2, by + 72, 34)
        elif kind == "measles":
            draw_measles(d, bx + bw // 2 - 34, by + 30, 68)
        hy = headline(d, head, bx + 12, by + 140, bw - 24, 24)
        subline(d, sub, bx + 12, hy + 4, bw - 24, 16)
        f_tag = font(BOLD, 14)
        d.text((bx + 12, by + bh - 28), tag, font=f_tag, fill=GREY)

    # ---- Ticker ----
    d.rectangle([12, 900, 1012, 952], fill=(30, 30, 30))
    f_tick = fit(d, "ALSO: Russian military plane crashes in Siberia, 19 dead  \u00b7  "
                    "Cyclone Xavier, Category 5, hits the Cook Islands",
                 BOLD, 980, 20)
    d.text((22, 918), "ALSO: Russian military plane crashes in Siberia, 19 dead  \u00b7  "
                       "Cyclone Xavier, Category 5, hits the Cook Islands",
           font=f_tick, fill=WHITE)

    # ---- Footer ----
    d.rectangle([0, 964, W, H], fill=NAVY)
    f_foot = fit(d, "ALL STORIES REPORTED ON 18 NOVEMBER 2026", BOLD, W - 40, 24)
    d.text(((W - d.textlength("ALL STORIES REPORTED ON 18 NOVEMBER 2026", font=f_foot)) / 2, 982),
           "ALL STORIES REPORTED ON 18 NOVEMBER 2026", font=f_foot, fill=GOLD)

    im.save(OUT, "PNG")
    print(f"{OUT}: {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
