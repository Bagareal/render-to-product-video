"""Extract frames from a video and tile them into one contact sheet.

Usage:
    python3 -I contact_sheet.py video.mp4 sheet.png 2

The last argument is frames per second to extract (2 = one frame every
0.5 s). Each tile is labelled with its timestamp. Requires ffmpeg on PATH.
"""
import glob
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

if len(sys.argv) != 4:
    sys.exit(__doc__)

video, out, fps = sys.argv[1], sys.argv[2], float(sys.argv[3])
tmp = tempfile.mkdtemp()
subprocess.run(
    ["ffmpeg", "-v", "error", "-i", video, "-vf", f"fps={fps},scale=640:-1",
     os.path.join(tmp, "f_%04d.png")],
    check=True,
)
files = sorted(glob.glob(os.path.join(tmp, "f_*.png")))
if not files:
    sys.exit("no frames extracted")

tiles = [Image.open(f).convert("RGB") for f in files]
w, h = tiles[0].size
cols = 4
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, h * rows))
for i, tile in enumerate(tiles):
    ImageDraw.Draw(tile).text((6, 4), f"{i / fps:.1f}s", fill=(255, 40, 40))
    sheet.paste(tile, ((i % cols) * w, (i // cols) * h))
sheet.save(out)
print(len(tiles), "frames ->", out, sheet.size)
