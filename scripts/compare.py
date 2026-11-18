"""Compare a reference image with a generated image to check that the
product geometry did not change.

Usage:
    python3 -I compare.py reference.png generated.png side_by_side.png blend.png

Outputs:
    - prints the silhouette IoU and the bounding box of both silhouettes
    - side_by_side.png : reference | generated (half size)
    - blend.png        : 50% overlay of the two images

The silhouette is every pixel that differs from the background colour,
sampled from the top-left corner of each image. The IoU is only a signal:
a soft shadow added by the generator widens the silhouette and lowers the
number even when the product itself is correct. The 50% overlay is what
decides: contours, seams and proportions must line up with no double edges.
"""
import sys

import numpy as np
from PIL import Image

if len(sys.argv) != 5:
    sys.exit(__doc__)

ref = Image.open(sys.argv[1]).convert("RGB")
out = Image.open(sys.argv[2]).convert("RGB").resize(ref.size, Image.LANCZOS)


def mask(im):
    a = np.asarray(im).astype(int)
    bg = a[5:30, 5:30].reshape(-1, 3).mean(axis=0)
    return np.abs(a - bg).sum(axis=2) > 30


m1, m2 = mask(ref), mask(out)
iou = (m1 & m2).sum() / (m1 | m2).sum()
print("IoU silhouette:", round(float(iou), 3))
for name, m in (("reference", m1), ("generated", m2)):
    ys, xs = np.where(m)
    print(name, "bbox", xs.min(), ys.min(), xs.max(), ys.max())

blend = Image.blend(ref, out, 0.5)
side = Image.new("RGB", (ref.width * 2, ref.height))
side.paste(ref, (0, 0))
side.paste(out, (ref.width, 0))
side.resize((side.width // 2, side.height // 2)).save(sys.argv[3])
blend.save(sys.argv[4])
