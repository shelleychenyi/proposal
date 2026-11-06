# -*- coding: utf-8 -*-
"""四国MaaS 見積明細（Hakuba 12か月プラン明細の様式に準拠）"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "【繁中版】Intasect_長岡花火_台灣市場集客施策_3方案報價明細_202612-202709.xlsx")

F = "Microsoft JhengHei"
NAVY, HEAD, INK, GREY = "16243D", "22406B", "222222", "444444"
SOFT, OPT, GOLD, YEL = "F3F6FB", "E9F9EF", "F5B841", "FFFF00"
thin = Side(style="thin", color="D5DBE5")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

def font(sz=10, b=False, color=INK):
    return Font(name=F, size=sz, bold=b, color=color)

def fill(c):
    return PatternFill("solid", fgColor=c) if c else PatternFill()

def put(ws, ref, v, sz=10, b=False, color=INK, bg=None, fmt=None, wrap=True, h="left", border=True):
    c = ws[ref]
    if not (v is None and type(c).__name__ == "MergedCell"):
        c.value = v
    c.font = font(sz, b, color)
    if bg:
        c.fill = fill(bg)
    if fmt:
        c.number_format = fmt
    c.alignment = Alignment(wrap_text=wrap, vertical="center", horizontal=h)
    if border:
        c.border = BOX
    return c

def band(ws, row, text, sub=None, ncol=6):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncol)
    put(ws, f"A{row}", text, 14, True, "FFFFFF", NAVY, border=False)
    ws.row_dimensions[row].height = 30
    if sub:
        ws.merge_cells(start_row=row + 1, start_column=1, end_row=row + 1, end_column=ncol)
        put(ws, f"A{row+1}", sub, 10, False, "FFFFFF", NAVY, border=False)
        ws.row_dimensions[row + 1].height = 22

def header(ws, row, cols):
    for i, t in enumerate(cols):
        put(ws, f"{L(i+1)}{row}", t, 10, True, "FFFFFF", HEAD, h="center")
    ws.row_dimensions[row].height = 22

YEN = '#,##0;(#,##0);"-"'
INPUT = "0000FF"   # 青字＝入力値

wb = Workbook()
ws = wb.active
ws.title = "3方案比較"
for k, v in {"A": 30, "B": 60, "C": 7, "D": 12, "E": 8, "F": 13, "G": 8, "H": 13, "I": 8, "J": 13, "K": 30}.items():
    ws.column_dimensions[k].width = v
band(ws, 1, "XXX 敬啟　長岡花火｜台灣・繁中圈 Inbound 集客施策　3方案報價",
     "小：口碑基礎／中：認知擴大＋抽選前（推薦）／大：全年展開｜施策期間 2026年12月〜2027年9月（10個月）｜金額皆為日圓・未稅｜2026年11月　Intasect Communications 株式會社", ncol=11)
put(ws, "A4", "■ 方案別報價明細", 12, True, NAVY, border=False)
for c, t in zip("ABCD", ["項目", "內容", "單位", "單價（日圓）"]):
    ws.merge_cells(f"{c}5:{c}6")
    put(ws, f"{c}5", t, 10, True, "FFFFFF", HEAD, h="center")
PLANS = [("E", "F", "小方案｜口碑基礎", "4A6FA5"), ("G", "H", "中方案｜認知擴大＋抽選前（推薦）", "EA336A"), ("I", "J", "大方案｜全年展開", "16243D")]
for q, m, name, col in PLANS:
    ws.merge_cells(f"{q}5:{m}5")
    put(ws, f"{q}5", name, 10, True, "FFFFFF", col, h="center")
    put(ws, f"{m}5", None, 10, True, "FFFFFF", col)
    put(ws, f"{q}6", "數量", 9, True, "FFFFFF", col, h="center")
    put(ws, f"{m}6", "金額（日圓）", 9, True, "FFFFFF", col, h="center")
ws.merge_cells("K5:K6")
put(ws, "K5", "備註", 10, True, "FFFFFF", HEAD, h="center")
ws.row_dimensions[5].height = 24
items = [
    ("聲量監測（Pandora）", "施策前基準值測定、月報 1 本／月（台灣・香港）、LINE 即時通知（關鍵字 4 組・24 小時監測）、轉賣・詐騙・散場等負面貼文發生時通報", "個月", 125000, (10, 10, 10), ""),
    ("Threads 繁中官方帳號經營", "繁中官方帳號「長岡花火 繁中官方（暫稱）」開設・經營。每月 6 篇以上（提交發文行事曆）、留言回覆 30〜100 則／月（不含私訊）、圖片製作 10 張以內／月、官方素材的繁中再編輯", "個月", 300000, (10, 10, 10), "官方名義的範圍需協議"),
    ("Threads KOC 成果保證型", "粉絲 3,000+ 的 KOC 帳號。1,500 字以內的攻略・體驗文＋置入回文 10 則／篇。每篇保證瀏覽 10,000 以上・互動 100 以上・聲量 1,000 以上，未達成免費補發。標示「合作」，原稿事先送審", "篇", 249000, (4, 6, 10), "5個切角：感動／抽選・席種／散場／住宿・回程／長岡四季"),
    ("Instagram UGC（在日台灣人 KOC）", "粉絲 5,000〜10,000 的微型 KOC。招待體驗＋Feed／Reels＋限時動態。8月花火當天與冬・春的長岡。素材授權官方二次利用。標示「合作」", "名", 70000, (0, 6, 10), "交通・住宿・觀覽席為實費"),
    ("GEO（AI 搜尋優化）", "1套（3個月）：新聞 6 本（Yahoo奇摩新聞等保證刊登＋10〜15 家聯播轉載）＋論壇 SEO 文 6 本（Dcard／PTT／Mobile01）＋關鍵字 30 組設計＋AI 搜尋命中保證 3 組。未達成退還該套金額 30％", "套", 2400000, (0, 1, 2), "①購票・觀覽席 ②交通・散場・住宿"),
    ("旅遊 KOL（花火當天同行）", "旅遊・攝影類 KOL。花火當天同行拍攝：Instagram Reels 1 本＋限時動態 2 本＋Threads 1 篇。觸及「還不知道長岡」的新族群。標示「合作」", "名", 200000, (0, 2, 4), "人選事先確認／交通住宿・觀覽席為實費"),
    ("欣傳媒 旅遊特集", "以「一生一次的長岡花火」為題的特集 1 本（企劃・採訪・製作・刊登）、Yahoo 等新聞平台配信、Facebook 推播（含廣告費）。連結觀覽席行程與繁中官方指南", "本", 1000000, (0, 1, 2), "大：＋淡季（冬・春的長岡）特集"),
    ("繁中官方指南 LP 製作", "企劃・構成・繁中文案・設計・實作（PC／手機）。抽選日程・席種比較・散場路線（可離線保存）・住宿與回程・花火的故事・長岡四季。UTM 計測設定", "式", 450000, (0, 1, 1), "網域・與官網的連結方式另議"),
    ("KV・Banner 系列製作", "設計系統（色彩・字體・3種模板）＋季節別 Banner（正三尺玉新年／抽選前準備／安全・正規購票／長岡四季）。Banaverse 生成素材＋正式排版，多尺寸輸出", "式", 300000, (0, 1, 1), "暫定單價：數量確定後定價"),
    ("廣告運用（Meta・Google）", "抽選前（3〜6月）台灣的興趣配信＋8月初東京都內繁中使用者的位置配信。廣告設計・入稿・優化・月報", "個月", 300000, (0, 0, 6), "媒體費另計"),
]
r0 = 7
for i, (a, b, u, p, qs, note) in enumerate(items):
    r = r0 + i
    put(ws, f"A{r}", a, 10, True, INK, SOFT)
    put(ws, f"B{r}", b, 9, False, INK, SOFT)
    put(ws, f"C{r}", u, 10, False, INK, SOFT, h="center")
    put(ws, f"D{r}", p, 10, False, INPUT, SOFT, YEN, h="right")
    for (q, m, *_), n in zip(PLANS, qs):
        put(ws, f"{q}{r}", n, 10, False, INPUT, None, '#,##0;(#,##0);"-"', h="center")
        put(ws, f"{m}{r}", f"=D{r}*{q}{r}", 10, False, INK, None, YEN, h="right")
    put(ws, f"K{r}", note, 9, False, "C0504D" if "暫定" in note else GREY, SOFT)
    ws.row_dimensions[r].height = 60
rl = r0 + len(items) - 1
rT = rl + 1
put(ws, f"A{rT}", "方案合計（未稅）", 11, True, NAVY, GOLD)
for c in "BCDK":
    put(ws, f"{c}{rT}", None, 11, True, NAVY, GOLD)
put(ws, f"B{rT}", "施策期間 2026年12月〜2027年9月（10個月）", 9, True, NAVY, GOLD)
for q, m, *_ in PLANS:
    put(ws, f"{q}{rT}", None, 11, True, NAVY, GOLD)
    put(ws, f"{m}{rT}", f"=SUM({m}{r0}:{m}{rl})", 11, True, NAVY, GOLD, YEN, h="right")
ws.row_dimensions[rT].height = 28
r = rT + 1
put(ws, f"A{r}", "方案目的", 10, True, INK, SOFT)
put(ws, f"B{r}", "共通：Pandora 月次監測確保成效衡量與負面即時應對", 9, False, GREY, SOFT)
for c in "CD":
    put(ws, f"{c}{r}", None, 9, False, INK, SOFT)
aims = ["以 Threads 官方帳號＋KOC，先建立官方的繁中窗口與口碑，累積認知",
        "IG・旅遊 KOL・欣傳媒特集擴大認知，GEO・繁中指南在抽選前接住「想去」的人",
        "GEO 2套・KOC 10篇・KOL 4名・特集 2本・廣告，從認知到預約全年展開"]
for (q, m, *_), t_ in zip(PLANS, aims):
    ws.merge_cells(f"{q}{r}:{m}{r}")
    put(ws, f"{q}{r}", t_, 9, False, INK, None)
    put(ws, f"{m}{r}", None, 9)
put(ws, f"K{r}", None, 9, False, INK, SOFT)
ws.row_dimensions[r].height = 64

r += 2
put(ws, f"A{r}", "■ 另計實費（不含於上述合計）", 12, True, NAVY, border=False)
for a, b, n in [("KOC・KOL 的體驗費用", "KOC・KOL 的交通・住宿・觀覽席（觀覽席由貴單位提供或旅行社方案購入）", "實費"),
                ("廣告媒體費（大方案）", "Meta・Threads 的實際投放金額", "實費"),
                ("官方素材", "官方照片・影片・logo 的使用", "貴單位提供")]:
    r += 1
    put(ws, f"A{r}", a, 10, True, INK, SOFT)
    ws.merge_cells(f"B{r}:J{r}")
    put(ws, f"B{r}", b, 9, False, INK, SOFT)
    put(ws, f"K{r}", n, 9, False, GREY, SOFT)
    ws.row_dimensions[r].height = 30

r += 2
put(ws, f"A{r}", "■ 選購項目（可加購・單價）", 12, True, NAVY, border=False)
r += 1
for c, t_ in zip("ABCD", ["項目", "內容", "單位", "單價（日圓）"]):
    put(ws, f"{c}{r}", t_, 10, True, "FFFFFF", HEAD, h="center")
ws.merge_cells(f"E{r}:K{r}")
put(ws, f"E{r}", "備註", 10, True, "FFFFFF", HEAD, h="center")
for a, b, u, p, n in [("客訴・負面應對", "應對邏輯・步驟設計、回覆文案、後續追蹤（花火前後 7〜8 月）", "個月", 100000, ""),
                      ("繁中 LP 更新・維護", "季節內容更新（年 4 次）、抽選資訊更新、輕微修改", "個月", 80000, "")]:
    r += 1
    put(ws, f"A{r}", a, 10, True, INK, OPT)
    put(ws, f"B{r}", b, 9, False, INK, OPT)
    put(ws, f"C{r}", u, 10, False, INK, OPT, h="center")
    put(ws, f"D{r}", p, 10, False, INPUT, OPT, YEN, h="right")
    ws.merge_cells(f"E{r}:K{r}")
    put(ws, f"E{r}", n, 9, False, GREY, OPT)
    ws.row_dimensions[r].height = 40

r += 2
put(ws, f"A{r}", "■ 保證項目・備註", 12, True, NAVY, border=False)
for n in [
    "・聲量保證：以 Pandora 實測值（2025/10/27〜2026/10/26・台灣＋香港・總聲量 4,770,013）為基準，施策期間內全年聲量 ＋30％（6,201,017）。實施時以施策開始前一日的最新資料為基準值。",
    "・GEO 保證：每套 30 組關鍵字中 3 組於 AI 搜尋（Google AI 概覽・ChatGPT・Gemini）有效顯示。未達成時退還該套金額 30％。",
    "・Threads KOC 保證：每篇瀏覽 10,000 以上・互動（讚＋留言）100 以上・聲量 1,000 以上。未達成時免費補發至達標。",
    "・所有 KOC・KOL 貼文依台灣公平交易委員會規範標示「合作」。人選・原稿事先經貴單位確認。",
    "・「暫定單價」項目（KV・Banner 系列）於數量・尺寸確定後定價。欣傳媒特集以欣傳媒正式報價為準。",
    "・金額皆為日圓・未稅（消費稅另計）。不含廣告媒體費・體驗交通住宿・觀覽席。",
    "・藍字為數量・單價的輸入值，變更後各方案金額與合計自動重新計算。",
]:
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    put(ws, f"A{r}", n, 9, False, GREY, border=False)
ws.freeze_panes = "A7"
ws.sheet_view.zoomScale = 90

wsm = wb.create_sheet("月別預算（中方案）")
mm = ["2026/12", "2027/1", "2027/2", "2027/3", "2027/4", "2027/5", "2027/6", "2027/7", "2027/8", "2027/9"]
wsm.column_dimensions["A"].width = 30
for i in range(len(mm) + 1):
    wsm.column_dimensions[L(i + 2)].width = 12
band(wsm, 1, "中方案｜月別預算配分（日圓・未稅）", "前段（12〜3月）打地基・決定期前就位 → 4〜8月 抽選與出發前集中", ncol=12)
header(wsm, 4, ["項目"] + mm + ["合計"])
alloc = [("聲量監測（Pandora）", [125000] * 10),
         ("Threads 官方帳號", [300000] * 10),
         ("Threads KOC（6篇）", [0, 249000, 0, 249000, 249000, 0, 249000, 249000, 0, 249000]),
         ("IG UGC（6名）", [0, 140000, 0, 0, 0, 0, 0, 0, 280000, 0]),
         ("GEO（1套）", [0, 800000, 800000, 800000, 0, 0, 0, 0, 0, 0]),
         ("繁中官方指南 LP", [0, 225000, 0, 225000, 0, 0, 0, 0, 0, 0]),
         ("KV・Banner 系列", [150000, 150000, 0, 0, 0, 0, 0, 0, 0, 0]),
         ("旅遊 KOL（2名）", [0, 0, 0, 0, 0, 0, 0, 0, 400000, 0]),
         ("欣傳媒 旅遊特集（1本）", [0, 0, 0, 0, 1000000, 0, 0, 0, 0, 0])]
for i, (a, vals) in enumerate(alloc):
    rr = 5 + i
    put(wsm, f"A{rr}", a, 10, True, INK, SOFT)
    for j, v in enumerate(vals):
        put(wsm, f"{L(j+2)}{rr}", v, 10, False, INPUT, None, YEN, h="right")
    put(wsm, f"L{rr}", f"=SUM(B{rr}:K{rr})", 10, True, INK, SOFT, YEN, h="right")
rr = 5 + len(alloc)
put(wsm, f"A{rr}", "月合計", 11, True, NAVY, GOLD)
for j in range(11):
    c = L(j + 2)
    put(wsm, f"{c}{rr}", f"=SUM({c}5:{c}{rr-1})", 10, True, NAVY, GOLD, YEN, h="right")
wsm.merge_cells(start_row=rr + 2, start_column=1, end_row=rr + 2, end_column=12)
put(wsm, f"A{rr+2}", "・合計須與「3方案比較」中方案合計一致。月別配分為建議，可依官方帳號開設時期與抽選日程調整。", 9, False, GREY, border=False)

ws3 = wb.create_sheet("KPI目標")
for k, v in {"A": 24, "B": 26, "C": 24, "D": 24, "E": 24, "F": 26, "G": 20}.items():
    ws3.column_dimensions[k].width = v
band(ws3, 1, "XXX 敬啟　方案別 KPI 一覽", "保證＝寫入契約（未達成有對應措施）／目標值＝依實績設定的努力目標／承諾交付＝一定交付的數量", ncol=7)
header(ws3, 4, ["施策", "KPI 指標", "小方案", "中方案", "大方案", "衡量方式", "區分"])
TAG = {"保證": ("9C5700", "FDF3DC"), "目標值": ("22406B", "EEF2FA"), "承諾交付": ("048F3E", "E9F9EF")}
kpi = [
    ("聲量（全體）", "「長岡花火」全年總聲量", "＋30％（4,770,013 → 6,201,017）", "＋30％（4,770,013 → 6,201,017）", "＋30％（4,770,013 → 6,201,017）", "Pandora", "保證"),
    ("", "8月以外的聲量", "—", "1.5倍（1,226,672 → 1,840,000）", "1.5倍（1,226,672 → 1,840,000）", "Pandora", "目標值"),
    ("", "月報", "10本", "10本", "10本", "提交月報", "承諾交付"),
    ("Threads 官方帳號", "經營期間・發文數", "10個月・60篇以上", "10個月・60篇以上", "10個月・60篇以上", "發文行事曆＋貼文連結", "承諾交付"),
    ("", "粉絲數", "8,000〜10,000人", "8,000〜10,000人", "10,000〜15,000人", "Threads 洞察報告", "目標值"),
    ("", "平均互動率", "4％以上", "4％以上", "4％以上", "Threads 洞察報告", "目標值"),
    ("Threads KOC", "發文數", "4篇", "6篇", "10篇", "貼文連結", "承諾交付"),
    ("", "瀏覽數（每篇 10,000 以上）", "40,000以上", "60,000以上", "100,000以上", "平台數據", "保證"),
    ("", "每篇互動・聲量", "100以上・1,000以上", "100以上・1,000以上", "100以上・1,000以上", "截圖＋Pandora", "保證"),
    ("IG UGC・旅遊 KOL", "KOC・KOL 人數", "—", "IG UGC 6名・KOL 2名", "IG UGC 10名・KOL 4名", "貼文連結", "承諾交付"),
    ("", "觸及（參考值）", "—", "12,000〜30,000", "20,000〜50,000", "IG 洞察報告", "目標值"),
    ("GEO", "新聞・論壇文", "—", "新聞6・論壇6", "新聞12・論壇12", "刊登連結一覽", "承諾交付"),
    ("", "關鍵字設計", "—", "30組", "60組", "關鍵字一覽", "承諾交付"),
    ("", "AI 搜尋命中", "—", "3組", "6組", "月次 AI 搜尋監測", "保證（未達成退還30％）"),
    ("欣傳媒", "旅遊特集", "—", "1本", "2本（＋淡季特集）", "刊登連結＋配信報告", "承諾交付"),
    ("繁中官方指南", "LP 製作", "—", "1式", "1式", "上線網址＋UTM 報表", "承諾交付"),
    ("廣告", "運用・月報", "—", "—", "6個月", "廣告後台報表", "承諾交付"),
]
for i, row in enumerate(kpi):
    rr = 5 + i
    put(ws3, f"A{rr}", row[0], 10, True, INK, SOFT)
    put(ws3, f"B{rr}", row[1], 10, True, INK)
    for j, c in enumerate("CDE"):
        put(ws3, f"{c}{rr}", row[2 + j], 9.5, False, INK, h="center")
    put(ws3, f"F{rr}", row[5], 9, False, INK)
    e = row[6]
    base = "保證" if e.startswith("保證") else e
    put(ws3, f"G{rr}", e, 9.5, True, TAG[base][0], TAG[base][1], h="center")
    ws3.row_dimensions[rr].height = 34
rr = 5 + len(kpi) + 1
for n in ["・「保證」：未達成時的對應寫入契約（GEO：未達成的套退還30％／KOC：免費補發至達標／聲量：追加施策對應）。",
          "・「目標值」：依同類帳號經營實績設定的目標，非契約保證值。以月報確認進度並調整施策。",
          "・「承諾交付」：一定交付的數量・成果物，以貼文連結・刊登連結・截圖記錄交付。",
          "・聲量基準值為 Pandora 實測值（資料期間 2025/10/27〜2026/10/26、關鍵字「長岡花火大會」、台灣＋香港、總聲量 4,770,013）。實施時以施策開始前一日的最新資料為基準值。"]:
    ws3.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=7)
    put(ws3, f"A{rr}", n, 9, False, GREY, border=False)
    rr += 1
for w in wb:
    w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.orientation = "landscape"
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT)
