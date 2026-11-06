# ================================================================ 2-1 全體像（漏斗）
p2f = s = page("2-1. 集客施策｜全體像",
               "認知（嚮往）→ 興趣・查證 → 預約・行動 → 分享・再訪。所有施策都導向繁中官方指南與雄獅行程，成效以 Pandora 聲量與 UTM 衡量。",
               "※ 施策組合依方案調整（詳見報價單）。")
layers = [("認知・嚮往", "IG Reels・旅遊 KOC ／ 雄獅×欣傳媒 專訪＋社群", "讓「還不知道長岡」的台灣人看見感動", PINK),
          ("興趣・查證", "Threads 官方帳號 ／ Threads KOC ／ GEO（AI 搜尋）", "「怎麼搶票・怎麼去」被問到時，答案是官方", TNAVY),
          ("預約・行動", "繁中官方指南 ／ 雄獅觀覽席行程 ／ 廣告", "抽選日程・席種・一日遊，把想去變成訂得到", GOLD_T),
          ("分享・再訪", "KOC・UGC 二次利用 ／ 白菊・長岡四季", "8月以外也被想起，接到下一年", "2E9E6A")]
for i, (t, a_, b_, c) in enumerate(layers):
    y = 1.5 + i * 1.08
    W = 8.4 - i * 1.25
    X = 0.45 + i * 0.625
    d.poly(s, [(X, y), (X + W, y), (X + W - 0.62, y + 0.98), (X + 0.62, y + 0.98)], c)
    d.tx(s, X + 0.6, y + 0.06, W - 1.2, 0.38, t, 14, WHITE, True, align="c", font=FONT_ZH)
    d.tx(s, X + 0.6, y + 0.46, W - 1.2, 0.48, a_, 9.5, WHITE, align="c", font=FONT_ZH)
    d.hline(s, X + W - 0.3, y + 0.49, 9.05, y + 0.49, "B8C4D6", 1, dash=True)
    d.rrect(s, 9.05, y + 0.12, 3.85, 0.76, WHITE, c, lw=1.25)
    d.tx(s, 9.18, y + 0.12, 3.6, 0.76, b_, 10, INK, True, anchor="m", font=FONT_ZH)
d.rrect(s, 0.45, 5.9, 12.45, 0.85, "EEF2FA", None)
d.tx(s, 0.65, 5.9, 2.2, 0.85, "Pandora\n月次監測", 12, TNAVY, True, anchor="m", font=FONT_ZH)
d.tx(s, 2.8, 5.9, 10.0, 0.85, "施策前基準值（總聲量 4,770,013）→ 月別聲量・正負面・話題。負面（轉賣・散場等）即時通知，官方帳號與 KOC 立即回應。", 10, INK, anchor="m", font=FONT_ZH, line=1.3)

# ================================================================ 2-2 KOC 的定義（沿用 Hakuba 金字塔頁的圖形）
import copy as _copy
from pptx import Presentation as _P
_HK = _P(os.path.join(os.path.dirname(ROOT), "白馬谷Hakuba Valley", "【中文版】Hakuba Valley 繁體中文市場集客策略提案202610.pptx"))
pkoc = s = page("2-2. KOC 的定義｜台灣資訊發布者的結構",
                "在台灣，發文者的規模決定了觸及範圍與消費者的距離感。本提案的口碑施策全部以「KOC」執行——粉絲 10 萬以下、貼近旅客視角的發布者。",
                None)
for sh in _HK.slides[6].shapes:
    if sh.name in ("TextBox 1", "TextBox 2", "TextBox 63"):
        continue
    s.shapes._spTree.append(_copy.deepcopy(sh._element))
_T = {"TextBox 51": "微網紅・旅遊 KOC。以旅客的視角拍攝花火現場，擴大「想去」。→ 本提案：旅遊 KOC（花火當天同行）",
      "TextBox 55": "在日台灣人・一般旅客的 KOC。攻略與體驗談，是搜尋・比較時的依據。→ 本提案：Threads KOC・IG KOC",
      "TextBox 62": "※ 各層級區分為本公司實務上的參考標準。橘色為本提案定義的 KOC（粉絲 10 萬以下）。",
      "Rounded Rectangle 61": "本提案的 KOC\n粉絲 10萬以下"}
for sh in s.shapes:
    if sh.name in _T and sh.has_text_frame:
        lines = _T[sh.name].split("\n")
        ps = sh.text_frame.paragraphs
        for i, pp in enumerate(ps):
            for j, r in enumerate(pp.runs):
                r.text = lines[i] if (i < len(lines) and j == 0) else ""
    if sh.name == "Rounded Rectangle 57":
        sh.top = int(3.86 * 914400)
        sh.height = int(2.46 * 914400)
    if sh.name in ("TextBox 51", "TextBox 55"):
        sh.width = int(4.55 * 914400)
        sh.height = int(0.75 * 914400)

