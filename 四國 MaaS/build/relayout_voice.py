# -*- coding: utf-8 -*-
"""1-4 口碑分析頁：結論卡片移到上方，Pandora 報告截圖在下方作為佐證。  python3 relayout_voice.py zh|ja"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from pptx.util import Emu

LANG = sys.argv[1]
J = LANG == "ja"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "【XXX御中】四国MaaS 台湾向けインバウンド集客のご提案202611_v2.pptx" if J else
                 "【繁中版】四國MaaS 台灣市場Inbound集客策略提案202611_v2.pptx")
d = Deck(F, font="Meiryo" if J else None)
E = 914400

def title(s):
    for sh in s.shapes:
        if sh.has_text_frame and sh.left < E * 0.1 and sh.top < E * 0.3 and sh.width > E * 8:
            return sh.text_frame.text
    return ""

s = next(sl for sl in d.prs.slides if title(sl).startswith("1-4."))
near = lambda a, b, tol=0.06: abs(a - b) < tol

def place(sh, x, y, w=None, h=None, keep_ratio=False):
    if keep_ratio and w and h:
        ar = sh.width / sh.height
        if w / h > ar:
            nw, nh = h * ar, h
        else:
            nw, nh = w, w / ar
        x, y, w, h = x + (w - nw) / 2, y + (h - nh) / 2, nw, nh
    sh.left, sh.top = Emu(int(x * E)), Emu(int(y * E))
    if w is not None:
        sh.width = Emu(int(w * E))
    if h is not None:
        sh.height = Emu(int(h * E))

CW, CH_, CY = 3.05, 1.18, 1.5
pics = {}
for sh in list(s.shapes):
    x, y, w, h = sh.left / E, sh.top / E, sh.width / E, sh.height / E
    if sh.shape_type == 13:
        if x < 4.5 and y < 3.0:
            pics["stats"] = sh
        elif x < 4.5:
            pics["platform"] = sh
        elif x < 8.6 and y < 3.5:
            pics["trend"] = sh
        elif x < 8.6:
            pics["senti"] = sh
        elif near(y, 5.55, 0.2) and x < 10:
            pics["qr1"] = sh
        elif near(y, 5.55, 0.2):
            pics["qr2"] = sh
        continue
    # 結論卡片（右欄 4 張）
    if x > 8.6 and 1.9 < y < 5.4:
        i = int(round((y - 2.0) / 0.84)) if near(x, 8.65) else int(round((y - 2.04) / 0.84))
        i = max(0, min(3, int((y - 1.95) // 0.84)))
        cx = 0.45 + i * 3.15
        oy = y - (2.0 + i * 0.84)
        if near(x, 8.65) and near(w, 4.3):          # 卡片底
            place(sh, cx, CY, CW, CH_)
        elif near(x, 8.65) and w < 0.1:             # 色條
            place(sh, cx, CY + 0.1, 0.06, CH_ - 0.2)
        elif near(x, 8.8) and oy < 0.2:             # 標題
            place(sh, cx + 0.15, CY + 0.06, CW - 0.22, 0.5)
            sh.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        elif near(x, 8.8):                           # 說明
            place(sh, cx + 0.15, CY + 0.56, CW - 0.22, 0.6)
        continue
    # 調查條件
    if near(y, 1.55) and x < 1:
        place(sh, x, 2.82, None, None)
        continue
    # 紅框摘要
    if near(y, 5.4) and x < 1:
        place(sh, 8.65 + (x - 0.45), 3.27, 4.3 if w > 3 else 4.15, 0.75)
        continue
    # QR 區
    if 5.4 < y < 6.4 and x > 8.6:
        place(sh, x, y - 1.3)
        continue
# 截圖（佐證）
place(pics["stats"], 0.45, 3.27, 4.0, 1.2, keep_ratio=True)
place(pics["trend"], 4.55, 3.27, 4.0, 1.75, keep_ratio=True)
place(pics["platform"], 0.45, 4.6, 4.0, 2.15, keep_ratio=True)
place(pics["senti"], 4.55, 5.1, 4.0, 1.65, keep_ratio=True)
for k in ("qr1", "qr2"):
    sh = pics[k]
    place(sh, sh.left / E, sh.top / E - 1.3)
# 標記：截圖對應的結論編號
tags = [("①", 0.5, 3.3), ("③", 4.6, 3.3), ("④", 0.5, 4.63), ("②", 4.6, 5.13)]
for n, x, y in tags:
    d.circle(s, x, y, 0.34, n.replace("①", "1").replace("②", "2").replace("③", "3").replace("④", "4"), RED, 10)
# 結論→佐證的引導
d.rect(s, 0.45, 2.73, 12.5, 0.02, "D5DBE5")
d.tx(s, 8.65, 5.2, 4.3, 1.5,
     [("佐證資料的讀法" if not J else "根拠データの見方", {"bold": True, "color": NAVY, "size": 10}),
      ("截圖左上的編號，對應上方的結論①〜④。" if not J else "画像左上の番号は、上部の結論①〜④に対応しています。"),
      ("①基本統計　②情緒分布　③聲量趨勢　④平台分布" if not J else "①基本統計　②センチメント分布　③声量推移　④プラットフォーム分布")],
     8.5, INK, line=1.35)
d.save(F)
print("saved", F)
