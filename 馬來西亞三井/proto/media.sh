#!/bin/zsh
# Re-capture prototype screenshots + recordings, then make rounded-corner videos/posters for the deck.
set -e
cd "$(dirname $0)/.."
FF=/Users/shelleychen/.claude/skills/shelley-deck/.venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1
python3 proto/capture.py shots
python3 proto/record.py "$@"
for f in assets/video/*.mp4; do b=$(basename $f .mp4); [ $b = idea_bg ] && continue
  $FF -y -loglevel error -i $f -i assets/corner_mask.png -filter_complex "[0:v]scale=780:1688[v];[v][1:v]overlay=0:0,format=yuv420p" -c:v libx264 -crf 20 -movflags +faststart assets/video_r/$b.mp4; done
~/.claude/skills/shelley-deck/.venv/bin/python - <<'PY'
from PIL import Image;import glob,os
m=Image.open("assets/corner_mask.png")
for f in glob.glob("assets/screens/*.png"):
    b=os.path.basename(f)[:-4];im=Image.open(f).convert("RGBA").resize((780,1688),Image.LANCZOS);im.alpha_composite(m);im.convert("RGB").save(f"assets/poster_r/{b}.jpg",quality=90)
print("posters ok")
PY
