import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert("RGB") for f in files]
W = max(i.size[0] for i in ims)
H = sum(i.size[1] for i in ims) + 8 * len(ims)
s = Image.new("RGB", (W, H), (200, 200, 200)); y = 0
for i in ims:
    s.paste(i, (0, y)); y += i.size[1] + 8
s.save(out)
