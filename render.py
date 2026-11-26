"""Draw 26 November 2026's world news as one poster.

Every line comes from our own scan of 41 wire feeds (news26/scan_out.txt), items
timestamped 26 Nov 2026 00:00-02:00 GMT. Nothing invented: each tile carries the
outlet's own subject, the numbers are the ones the wire gave.

Re-authored in this run's session so the poster's authorship is visible in the
transcript that ships with the entry bundle.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 30
RIGHT = W - M
PAPER = (250, 248, 243)
INK = (18, 20, 19)
SOFT = (86, 90, 84)
FAINT = (134, 138, 130)
RED = (168, 34, 30)
BLUE = (24, 48, 96)
RULE = (176, 170, 156)
PANEL = (255, 255, 252)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

DATE = "THURSDAY 26 NOVEMBER 2026"
TAG = "THE WORLD IN ONE DAY"

FIGURES = [
    ("31", "killed in Cairo fuel-truck fire"),
    ("20%", "US tariff set on Singapore goods"),
    ("13", "more trading partners targeted"),
    ("3.25%", "Bank of Korea base rate raised"),
]

STORIES = [
    ("MIDDLE EAST", "Iran war widens: blasts in Sanaa, missiles over Riyadh",
     "Explosions in Yemen's capital; Saudi air defences intercepted missiles."),
    ("TRADE", "US sets tariffs of up to 20% on Singapore and 13 partners",
     "Vietnam says it is working with Washington to close its deal fast."),
    ("SYRIA", "ISIL suicide attacks kill Syrian security personnel",
     "Several bombings in one morning; two security staff among the dead."),
    ("EGYPT", "Cairo fuel-truck fire kills at least 31",
     "Truck overturned on a busy highway outside the capital, then burned."),
    ("UNITED STATES", "Storm forces first postponement of Macy's parade",
     "Thanksgiving Day parade moved to Saturday, unprecedented in its history."),
    ("ASIA", "Bank of Korea raises rates to 3.25%",
     "Seoul resumes tightening; BOJ's Tamura hints at faster hikes ahead."),
]

WIRE = [
    ("ISRAEL", "Judges recommend prosecutors drop the Netanyahu case."),
    ("ZAMBIA", "Government bans protest against removing term limits."),
    ("SCIENCE", "Images reveal the crater left by the DART strike."),
    ("AUSTRALIA", "Anthropic's first data centre wins environmental approval."),
]

FOOT = "41 wire feeds scanned · 33 items · Thursday 26 November 2026, 00:00-02:00 GMT · edition one"


def font(size, bold=False, serif=False):
    if serif:
        return ImageFont.truetype(FSB if bold else F, size)
    return ImageFont.truetype(FB if bold else F, size)


def tw(d, s, size, bold=False, serif=False):
    return d.textlength(s, font=font(size, bold, serif))


def wrap(d, text, size, bold, maxw, serif=False):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, size, bold, serif) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def put(d, x, y, s, size, fill, bold=False, serif=False):
    d.text((x, y), s, font=font(size, bold, serif), fill=fill)


def build(out="/opt/data/makefun/news26/entry/entry.png", scale=2):
    w, h = W * scale, H * scale
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    S = scale

    # masthead ------------------------------------------------------------
    put(d, M * S, 32 * S, TAG, 16 * S, SOFT, bold=True)
    put(d, (RIGHT - tw(d, "ONE PAGE · 26.11.2026", 16 * S, True)) * S, 32 * S,
        "ONE PAGE · 26.11.2026", 16 * S, SOFT, True)
    put(d, M * S, 54 * S, DATE, 50 * S, INK, bold=True, serif=True)
    d.rectangle([M * S, 118 * S, RIGHT * S, 123 * S], fill=RED)

    # figure strip --------------------------------------------------------
    y = 140 * S
    col = (RIGHT - M) / 4
    for i, (num, cap) in enumerate(FIGURES):
        x = M * S + i * col * S
        put(d, x, y, num, 56 * S, RED, bold=True, serif=True)
        for j, ln in enumerate(wrap(d, cap, 15 * S, False, col - 12 * S)[:3]):
            put(d, x, y + (60 + j * 18) * S, ln, 15 * S, SOFT)
    d.rectangle([M * S, 222 * S, RIGHT * S, 223 * S], fill=RULE)

    # story grid: 2 x 3, every tile the same height ------------------------
    gx0, gy0 = M, 240
    gap, gh = 24, 150
    gw = (RIGHT - M - gap) / 2
    for i, (kicker, head, detail) in enumerate(STORIES):
        cx = gx0 + (i % 2) * (gw + gap)
        cy = gy0 + (i // 2) * (gh + 16)
        d.rectangle([cx * S, cy * S, (cx + gw) * S, (cy + gh) * S], fill=PANEL)
        d.rectangle([cx * S, cy * S, (cx + 4) * S, (cy + gh) * S], fill=BLUE)
        put(d, (cx + 14) * S, (cy + 9) * S, kicker, 14 * S, BLUE, bold=True)
        ty = cy + 28
        for ln in wrap(d, head, 22 * S, True, gw - 26 * S, serif=True)[:3]:
            put(d, (cx + 14) * S, ty * S, ln, 22 * S, INK, bold=True, serif=True)
            ty += 25
        ty += 2
        for ln in wrap(d, detail, 14 * S, False, gw - 26 * S)[:2]:
            put(d, (cx + 14) * S, ty * S, ln, 14 * S, SOFT)
            ty += 17

    # wire column ---------------------------------------------------------
    wy = gy0 + 3 * (gh + 16) + 6
    d.rectangle([M * S, wy * S, RIGHT * S, (wy + 1) * S], fill=RULE)
    put(d, M * S, (wy + 10) * S, "ALSO ON THE WIRES", 15 * S, RED, bold=True)
    yy = wy + 34
    for tag, line in WIRE:
        put(d, M * S, yy * S, tag, 14 * S, BLUE, bold=True)
        put(d, (M + 104) * S, yy * S, "· " + line, 14 * S, INK)
        yy += 30

    # footer --------------------------------------------------------------
    d.rectangle([M * S, 970 * S, RIGHT * S, 971 * S], fill=RULE)
    put(d, M * S, 976 * S, FOOT, 12 * S, FAINT)

    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
