"""Crop Banaverse scene clips to the deck's scene-photo box and burn in the AI tag + chip (per language).
Outputs assets/video_r/<key>_<lang>.mp4 and assets/poster_r/<key>_<lang>.jpg."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FF = os.path.expanduser("~/.claude/skills/shelley-deck/.venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1")
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
W = 1280
# key: (raw file, box aspect w/h, vertical crop bias 0..1, chips per lang)
SCENES = {
    "park_scene": ("assets/video_raw/park_scene_raw.mp4", 5.95 / 2.95, 0.55, {"en": None, "zh": None}),
    "go_scene": ("assets/video_raw/go_scene_raw.mp4", 7.25 / 2.95, 0.35,
                 {"en": "Also at MOP: free KLIA shuttle + \"catch my flight\"", "zh": "MOP：機場免費接駁時刻＋趕飛機提醒"}),
}
TAG = {"en": "AI mock-up video", "zh": "AI 示意影片"}


def overlay(w, h, lang, chip, path):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 22, index=1)
    t = TAG[lang]
    tw = dr.textlength(t, font=f)
    dr.rounded_rectangle([18, 16, 18 + tw + 36, 16 + 40], radius=20, fill=(0, 0, 0, 230))
    dr.text((36, 23), t, font=f, fill="white")
    if chip:
        f2 = ImageFont.truetype(FONT, 26, index=1)
        cw = dr.textlength(chip, font=f2)
        dr.rectangle([0, h - 70, cw + 60, h], fill=(184, 151, 90, 240))
        dr.text((30, h - 54), chip, font=f2, fill="white")
    im.save(path)


for key, (raw, ar, bias, chips) in SCENES.items():
    h = int(round(W / ar / 2) * 2)
    y = int((720 - h) * bias)
    for lang, chip in chips.items():
        ov = f"/tmp/ov_{key}_{lang}.png"
        overlay(W, h, lang, chip, ov)
        out = f"assets/video_r/{key}_{lang}.mp4"
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-i", ov, "-filter_complex",
                        f"[0:v]crop={W}:{h}:0:{y}[v];[v][1:v]overlay=0:0,format=yuv420p", "-an", "-c:v", "libx264",
                        "-crf", "21", "-movflags", "+faststart", out], check=True)
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "0.3", "-i", out, "-frames:v", "1", "-q:v", "3",
                        f"assets/poster_r/{key}_{lang}.jpg"], check=True)
        print(out, h)
