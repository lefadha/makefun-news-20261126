"""Geometry check: every text block inside its tile, nothing taller than the tile."""
import sys

sys.path.insert(0, '/opt/data/makefun/news26/entry')
from PIL import Image, ImageDraw  # noqa: E402

import render as R  # noqa: E402

img = Image.new('RGB', (R.W, R.H))
d = ImageDraw.Draw(img)
gap, gh = 24, 150
gw = (R.RIGHT - R.M - gap) / 2
worst = 0
for i, (kicker, head, detail) in enumerate(R.STORIES):
    hl = R.wrap(d, head, 22, True, gw - 26, serif=True)
    dl = R.wrap(d, detail, 14, False, gw - 26)
    ty = 28 + min(len(hl), 3) * 25 + 2 + min(len(dl), 2) * 17
    worst = max(worst, ty)
    print(f'{i} {kicker:14} head_lines={len(hl)} detail_lines={len(dl)} block={ty}px of {gh}')
print('tile height needed:', worst, 'available', gh, 'OK' if worst <= gh else 'OVERFLOW')
for i, (tag, line) in enumerate(R.WIRE):
    n = R.wrap(d, '· ' + line, 14, False, R.RIGHT - R.M - 104)
    print(f'wire {i} lines={len(n)} width_ok={R.tw(d, "· " + line, 14) <= R.RIGHT - R.M - 104}')
for num, cap in R.FIGURES:
    print('figure', num, 'caption lines', len(R.wrap(d, cap, 15, False, (R.RIGHT - R.M) / 4 - 12)))
print('date width', round(R.tw(d, R.DATE, 50, True, True)), 'of', R.RIGHT - R.M)
