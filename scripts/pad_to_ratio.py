"""Pad an image to an exact aspect ratio without cropping or scaling it.

Usage:
    python3 -I pad_to_ratio.py input.png output.png 16:9
    python3 -I pad_to_ratio.py input.png output.png 9:16

The padding uses the background colour sampled from the top-left corner,
so a render on a plain background simply gets more of the same background.
If the image already has the requested ratio it is saved unchanged.
"""
import sys

import numpy as np
from PIL import Image

if len(sys.argv) != 4:
    sys.exit(__doc__)

src, dst, ratio = sys.argv[1], sys.argv[2], sys.argv[3]
rw, rh = (int(x) for x in ratio.split(":"))

im = Image.open(src).convert("RGB")
a = np.asarray(im).astype(int)
bg = tuple(int(v) for v in a[5:30, 5:30].reshape(-1, 3).mean(axis=0))
w, h = im.size

target_w = round(h * rw / rh)
if target_w == w:
    canvas = im
elif target_w > w:
    canvas = Image.new("RGB", (target_w, h), bg)
    canvas.paste(im, ((target_w - w) // 2, 0))
else:
    target_h = round(w * rh / rw)
    canvas = Image.new("RGB", (w, target_h), bg)
    canvas.paste(im, (0, (target_h - h) // 2))

canvas.save(dst)
print(im.size, "->", canvas.size, "bg", bg)
