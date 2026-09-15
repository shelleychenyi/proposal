# -*- coding: utf-8 -*-
"""Generate billboard location maps from OSM tiles with numbered pins."""
import math, os, io, urllib.request, time
from PIL import Image, ImageDraw, ImageFont

CACHE = os.path.join(os.path.dirname(__file__), "tile_cache")
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "SMBC-proposal-map/1.0 (internal one-off document)"}

def tile(z, x, y):
    fp = os.path.join(CACHE, f"{z}_{x}_{y}.png")
    if not os.path.exists(fp):
        url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            open(fp, "wb").write(r.read())
        time.sleep(0.1)
    return Image.open(fp).convert("RGB")

def px(lng, z):  return (lng + 180.0) / 360.0 * 256 * (2 ** z)
def py(lat, z):
    s = math.sin(math.radians(lat))
    return (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * 256 * (2 ** z)

def render(bbox, z):
    lat1, lng1, lat2, lng2 = bbox  # top-left lat/lng, bottom-right
    x0, y0 = px(lng1, z), py(lat1, z)
    x1, y1 = px(lng2, z), py(lat2, z)
    tx0, ty0 = int(x0 // 256), int(y0 // 256)
    tx1, ty1 = int(x1 // 256), int(y1 // 256)
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    canvas = Image.new("RGB", (W, H), "#d8e8f0")
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            try:
                canvas.paste(tile(z, tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))
            except Exception as e:
                print("tile fail", z, tx, ty, e)
    crop = canvas.crop((int(x0 - tx0 * 256), int(y0 - ty0 * 256),
                        int(x1 - tx0 * 256), int(y1 - ty0 * 256)))
    return crop, (x0, y0)

GROUP_COLORS = {1: "#FF5A3C", 2: "#12203F", 3: "#1C7293"}

def draw_pins(img, origin, z, pins, r=26):
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(r * 1.15))
    except Exception:
        font = ImageFont.load_default()
    x0, y0 = origin
    for p in pins:
        x = px(p["lng"], z) - x0 + p.get("dx", 0)
        y = py(p["lat"], z) - y0 + p.get("dy", 0)
        if not (r < x < img.width - r and r < y < img.height - r):
            print("pin out of bounds:", p["n"])
            continue
        col = GROUP_COLORS[p["g"]]
        # soft shadow
        d.ellipse([x - r - 2, y - r + 1, x + r + 2, y + r + 5], fill="#9aa3b0")
        d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline="#ffffff", width=4)
        t = str(p["n"])
        bb = d.textbbox((0, 0), t, font=font)
        d.text((x - (bb[2] - bb[0]) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1]), t, font=font, fill="#ffffff")

def attribution(img):
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except Exception:
        f = ImageFont.load_default()
    t = "© OpenStreetMap contributors"
    bb = d.textbbox((0, 0), t, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    x, y = img.width - w - 14, img.height - h - 10
    d.rectangle([x - 6, y - 4, x + w + 6, y + h + 6], fill=(255, 255, 255, 220))
    d.text((x, y), t, font=f, fill="#6B7A90")

pinsN = [
    dict(n=1, g=1, lat=25.0560, lng=121.2950),
    dict(n=2, g=1, lat=24.9890, lng=121.3128),
    dict(n=3, g=2, lat=25.0332, lng=121.5378, dy=14),
    dict(n=4, g=2, lat=25.0672, lng=121.5297),
    dict(n=5, g=2, lat=25.0468, lng=121.5312, dx=26, dy=-6),
    dict(n=6, g=2, lat=25.0462, lng=121.5148, dx=-14, dy=6),
    dict(n=7, g=2, lat=25.0142, lng=121.4640),
]
pinsS = [
    dict(n=8,  g=3, lat=24.7845, lng=121.0040, dx=16, dy=14),
    dict(n=9,  g=3, lat=24.8040, lng=120.9655, dx=-10, dy=-10),
    dict(n=10, g=3, lat=24.1648, lng=120.6428),
    dict(n=11, g=3, lat=22.9975, lng=120.2120),
    dict(n=12, g=3, lat=22.6605, lng=120.3020),
]

# --- north map: 大台北・桃園, z12, aspect 4.4:2.7 ---
N_BBOX = (25.170, 121.170, 24.898, 121.660)
img, origin = render(N_BBOX, 12)
print("north size", img.size)
draw_pins(img, origin, 12, pinsN, r=30)
attribution(img)
img.save(os.path.join(os.path.dirname(__file__), "map_north.png"))

# --- south map: 全台西部走廊, z8, aspect ~4.4:1.85 wide ---
lat_top, lat_bot = 25.42, 22.30
h = py(lat_bot, 8) - py(lat_top, 8)
target_w = h * (4.4 / 1.85)
lng_c = 120.9
lng_span = target_w / (256 * 2 ** 8 / 360.0)
S_BBOX = (lat_top, lng_c - lng_span / 2, lat_bot, lng_c + lng_span / 2)
print("south bbox", S_BBOX)
img2, origin2 = render(S_BBOX, 8)
print("south size", img2.size)
# coverage box of north map
d = ImageDraw.Draw(img2)
bx0 = px(N_BBOX[1], 8) - origin2[0]; by0 = py(N_BBOX[0], 8) - origin2[1]
bx1 = px(N_BBOX[3], 8) - origin2[0]; by1 = py(N_BBOX[2], 8) - origin2[1]
d.rectangle([bx0, by0, bx1, by1], outline="#FF5A3C", width=4)
try:
    fcjk = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 26)
except Exception:
    fcjk = ImageFont.load_default()
_t = "上圖範圍"
_bb = d.textbbox((0, 0), _t, font=fcjk)
_w, _h = _bb[2]-_bb[0], _bb[3]-_bb[1]
d.rectangle([bx0, by1 + 6, bx0 + _w + 16, by1 + _h + 18], fill="#FFFFFF")
d.text((bx0 + 8 - _bb[0], by1 + 12 - _bb[1]), _t, font=fcjk, fill="#FF5A3C")
draw_pins(img2, origin2, 8, pinsS, r=24)
attribution(img2)
img2.save(os.path.join(os.path.dirname(__file__), "map_south.png"))
print("done")
