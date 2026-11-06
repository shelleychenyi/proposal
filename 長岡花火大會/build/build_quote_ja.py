# -*- coding: utf-8 -*-
"""四国MaaS 見積明細（Hakuba 12か月プラン明細の様式に準拠）"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "【インタセクト】XXX様_長岡花火_台湾向け集客施策_3プランお見積り_202611.xlsx")

F = "Meiryo"
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
ws.title = "3プラン比較"
for k, v in {"A": 30, "B": 60, "C": 7, "D": 12, "E": 8, "F": 13, "G": 8, "H": 13, "I": 8, "J": 13, "K": 30}.items():
    ws.column_dimensions[k].width = v
band(ws, 1, "XXX様　長岡花火 台湾・繁体字圏向け集客施策　3プランのお見積り",
     "小：口コミ基盤／中：認知拡大＋抽選前（推奨）／大：通年展開｜施策期間 2026年12月〜2027年9月（10か月）｜金額はすべて日本円・税別｜2026年11月　インタセクト・コミュニケーションズ株式会社", ncol=11)
put(ws, "A4", "■ プラン別お見積り明細", 12, True, NAVY, border=False)
for c, t in zip("ABCD", ["項目", "内容", "単位", "単価（円）"]):
    ws.merge_cells(f"{c}5:{c}6")
    put(ws, f"{c}5", t, 10, True, "FFFFFF", HEAD, h="center")
PLANS = [("E", "F", "小プラン｜口コミ基盤", "4A6FA5"), ("G", "H", "中プラン｜認知拡大＋抽選前（推奨）", "EA336A"), ("I", "J", "大プラン｜通年展開", "16243D")]
for q, m, name, col in PLANS:
    ws.merge_cells(f"{q}5:{m}5")
    put(ws, f"{q}5", name, 10, True, "FFFFFF", col, h="center")
    put(ws, f"{m}5", None, 10, True, "FFFFFF", col)
    put(ws, f"{q}6", "数量", 9, True, "FFFFFF", col, h="center")
    put(ws, f"{m}6", "金額（円）", 9, True, "FFFFFF", col, h="center")
ws.merge_cells("K5:K6")
put(ws, "K5", "備考", 10, True, "FFFFFF", HEAD, h="center")
ws.row_dimensions[5].height = 24
items = [
    ("声量モニタリング（Pandora）", "施策前の基準値測定、月次レポート1本／月（台湾・香港）、LINE即時通知（キーワード4組・24時間監視）、転売・詐欺・終演後の混雑などネガティブ投稿発生時の通報", "か月", 125000, (10, 10, 10), ""),
    ("Threads公式アカウント運用", "繁体字公式アカウント「長岡花火 繁中官方（仮称）」の開設・運用。月6投稿以上（投稿カレンダー提出）、コメント返信30〜100件／月（DM対応は含まない）、画像制作10点以内／月、公式素材の繁体字再編集", "か月", 300000, (10, 10, 10), "公式名義の範囲は要協議"),
    ("Threads KOC 成果保証型", "フォロワー3,000+のKOCアカウント。1,500字以内の攻略・体験投稿＋コメント10件／本。1本あたり閲覧数10,000以上・エンゲージメント100以上・言及量1,000以上を保証、未達時は無償で追加投稿。「合作」表記、原稿は事前確認", "本", 249000, (4, 6, 10), "5つの切り口：感動／抽選・席種／宿泊・交通／日帰り／長岡の四季"),
    ("IG KOC（在日台湾人・フォロワー5,000〜1万）", "フォロワー5,000〜10,000の在日台湾人KOC。招待体験＋フィード／リール＋ストーリーズ。8月の花火当日と冬・春の長岡。素材は公式で二次活用。「合作」表記", "名", 70000, (0, 6, 10), "交通・宿泊・観覧席は実費"),
    ("GEO（AI検索対策）", "1セット（3か月）：ニュース記事6本（Yahoo奇摩ニュース等の掲載保証＋10〜15媒体への転載）＋SEO掲示板記事6本（Dcard／PTT／Mobile01）＋キーワード30組設計＋AI検索掲載3組保証。未達時は当該セット金額の30％を返金", "セット", 2400000, (0, 1, 2), "①認知・旅程 ②チケット・交通"),
    ("旅行KOC（フォロワー1〜10万・花火当日同行）", "旅行・写真系KOC（フォロワー1〜10万）。花火当日に同行撮影：Instagramリール1本＋ストーリーズ2本＋Threads投稿1本。「まだ長岡を知らない」層へリーチ。「合作」表記", "名", 200000, (0, 2, 4), "人選は事前確認／交通・宿泊・観覧席は実費"),
    ("雄獅×欣傳媒 インタビュー記事＋SNS", "欣傳媒インタビュー記事1本（企画・取材・執筆・撮影・掲載）、欣傳媒Facebook・Instagram配信（広告費込み）、Yahoo・LINE TODAY等への転載。記事から雄獅の観覧席付きツアーと繁体字公式ガイドへ誘導", "本", 1000000, (0, 1, 2), "大：＋閑散期（冬・春の長岡）記事／仮単価：欣傳媒の正式見積により確定"),
    ("繁体字公式ガイドLP制作", "企画・構成・繁体字コピー・デザイン・実装（PC／スマートフォン）。抽選日程・席種比較・終演後ルート（オフライン保存可）・宿泊と帰路・花火の物語・長岡の四季。UTM計測設定", "式", 450000, (0, 1, 1), "ドメイン・公式サイトとの連携方法は別途協議"),
    ("KV・バナー制作", "デザインシステム（色・書体・3種テンプレート）＋季節別バナー（正三尺玉の新年／抽選前の準備／安全・正規購入／長岡の四季）。Banaverse生成素材＋正式レイアウト、複数サイズ書き出し", "式", 300000, (0, 1, 1), "仮単価：数量確定後に確定"),
    ("広告運用（Meta・Google）", "抽選前（3〜6月）の台湾向け興味関心配信＋8月初旬の東京都内・繁体字ユーザーへの位置情報配信。広告設計・入稿・最適化・月次レポート", "か月", 300000, (0, 0, 6), "媒体費は別途"),
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
    put(ws, f"K{r}", note, 9, False, "C0504D" if "仮単価" in note else GREY, SOFT)
    ws.row_dimensions[r].height = 60
rl = r0 + len(items) - 1
rT = rl + 1
put(ws, f"A{rT}", "プラン合計（税別）", 11, True, NAVY, GOLD)
for c in "BCDK":
    put(ws, f"{c}{rT}", None, 11, True, NAVY, GOLD)
put(ws, f"B{rT}", "施策期間 2026年12月〜2027年9月（10か月）", 9, True, NAVY, GOLD)
for q, m, *_ in PLANS:
    put(ws, f"{q}{rT}", None, 11, True, NAVY, GOLD)
    put(ws, f"{m}{rT}", f"=SUM({m}{r0}:{m}{rl})", 11, True, NAVY, GOLD, YEN, h="right")
ws.row_dimensions[rT].height = 28
r = rT + 1
put(ws, f"A{r}", "プランの狙い", 10, True, INK, SOFT)
put(ws, f"B{r}", "共通：Pandoraの月次モニタリングで効果測定とネガティブ対応を確保", 9, False, GREY, SOFT)
for c in "CD":
    put(ws, f"{c}{r}", None, 9, False, INK, SOFT)
aims = ["Threads公式アカウント＋KOCで、まず公式の繁体字窓口と口コミをつくり認知を積み上げる",
        "IG KOC・旅行KOC・雄獅×欣傳媒で認知を広げ、GEO・繁体字ガイドで抽選前の「行きたい」を受け止める",
        "GEO2セット・Threads KOC10本・旅行KOC4名・欣傳媒記事2本・広告まで通年で展開"]
for (q, m, *_), t_ in zip(PLANS, aims):
    ws.merge_cells(f"{q}{r}:{m}{r}")
    put(ws, f"{q}{r}", t_, 9, False, INK, None)
    put(ws, f"{m}{r}", None, 9)
put(ws, f"K{r}", None, 9, False, INK, SOFT)
ws.row_dimensions[r].height = 64

r += 2
put(ws, f"A{r}", "■ 別途実費（上記合計に含まず）", 12, True, NAVY, border=False)
for a, b, n in [("KOCの体験費用", "KOCの交通・宿泊・観覧席（観覧席は貴会ご提供または旅行会社プランで購入）", "実費"),
                ("広告媒体費（大）", "Meta・Googleへの実投下額", "実費"),
                ("公式素材", "公式写真・映像・ロゴの使用", "貴会ご提供を想定")]:
    r += 1
    put(ws, f"A{r}", a, 10, True, INK, SOFT)
    ws.merge_cells(f"B{r}:J{r}")
    put(ws, f"B{r}", b, 9, False, INK, SOFT)
    put(ws, f"K{r}", n, 9, False, GREY, SOFT)
    ws.row_dimensions[r].height = 30

r += 2
put(ws, f"A{r}", "■ オプション（各プランに追加可能・単価）", 12, True, NAVY, border=False)
r += 1
for c, t_ in zip("ABCD", ["項目", "内容", "単位", "単価（円）"]):
    put(ws, f"{c}{r}", t_, 10, True, "FFFFFF", HEAD, h="center")
ws.merge_cells(f"E{r}:K{r}")
put(ws, f"E{r}", "備考", 10, True, "FFFFFF", HEAD, h="center")
for a, b, u, p, n in [("ネガティブ・クレーム対応", "対応ロジック・手順設計、返信文案、フォローアップ（花火前後の7〜8月）", "か月", 100000, ""),
                      ("繁体字LP 保守・更新", "季節コンテンツ更新（年4回）、抽選情報の更新、軽微な修正", "か月", 80000, "")]:
    r += 1
    put(ws, f"A{r}", a, 10, True, INK, OPT)
    put(ws, f"B{r}", b, 9, False, INK, OPT)
    put(ws, f"C{r}", u, 10, False, INK, OPT, h="center")
    put(ws, f"D{r}", p, 10, False, INPUT, OPT, YEN, h="right")
    ws.merge_cells(f"E{r}:K{r}")
    put(ws, f"E{r}", n, 9, False, GREY, OPT)
    ws.row_dimensions[r].height = 40

r += 2
put(ws, f"A{r}", "■ 保証項目・備考", 12, True, NAVY, border=False)
for n in [
    "・声量保証：Pandora実測値（2025/10/27〜2026/10/26・台湾＋香港・総言及量4,770,013）を基準に、施策期間の年間声量＋30％（6,201,017）。実施時は施策開始前日までの最新データを基準値とする。",
    "・GEO保証：各セット30組のキーワードのうち3組が、AI検索（Google AI Overview・ChatGPT・Gemini）に有効に表示されることを保証。未達成の場合は当該セット金額の30％を返金。",
    "・Threads KOC保証：1本あたり閲覧数10,000以上・エンゲージメント（いいね＋コメント）100以上・言及量1,000以上。未達成の場合は保証値に達するまで無償で追加投稿。",
    "・すべてのKOC投稿は、台湾・公平交易委員会の規範に従い「合作」を表記。人選・原稿は実施前に貴会へ確認。",
    "・「仮単価」の項目（KV・バナー制作、雄獅×欣傳媒）は、数量の確定および欣傳媒の正式見積により金額を確定します。",
    "・金額はすべて日本円・税別（消費税は別途）。媒体費・体験時の交通・宿泊・観覧席は含まない。",
    "・青字は数量・単価の入力値です。変更すると各プランの金額・合計が自動で再計算されます。",
]:
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    put(ws, f"A{r}", n, 9, False, GREY, border=False)
ws.freeze_panes = "A7"
ws.sheet_view.zoomScale = 90

wsm = wb.create_sheet("月別予算（中プラン）")
mm = ["2026/12", "2027/1", "2027/2", "2027/3", "2027/4", "2027/5", "2027/6", "2027/7", "2027/8", "2027/9"]
wsm.column_dimensions["A"].width = 30
for i in range(len(mm) + 1):
    wsm.column_dimensions[L(i + 2)].width = 12
band(wsm, 1, "中プラン｜月別予算配分（日本円・税別）", "前半（12〜3月）で基盤づくり・抽選前に整備 → 4〜8月は抽選・出発前に集中", ncol=12)
header(wsm, 4, ["項目"] + mm + ["合計"])
alloc = [("声量モニタリング（Pandora）", [125000] * 10),
         ("Threads公式アカウント", [300000] * 10),
         ("Threads KOC（6本）", [0, 249000, 0, 249000, 249000, 0, 249000, 249000, 0, 249000]),
         ("IG KOC（6名）", [0, 140000, 0, 0, 0, 0, 0, 0, 280000, 0]),
         ("GEO（1セット）", [0, 800000, 800000, 800000, 0, 0, 0, 0, 0, 0]),
         ("繁体字公式ガイドLP", [0, 225000, 0, 225000, 0, 0, 0, 0, 0, 0]),
         ("KV・バナー", [150000, 150000, 0, 0, 0, 0, 0, 0, 0, 0]),
         ("旅行KOC（2名）", [0, 0, 0, 0, 0, 0, 0, 0, 400000, 0]),
         ("雄獅×欣傳媒 記事（1本）", [0, 0, 0, 0, 1000000, 0, 0, 0, 0, 0])]
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
put(wsm, f"A{rr+2}", "・合計は「3プラン比較」の中プラン合計と一致。月別配分は目安であり、公式アカウント開設時期と抽選日程に応じて調整可能。", 9, False, GREY, border=False)

ws3 = wb.create_sheet("KPI目標")
for k, v in {"A": 24, "B": 26, "C": 24, "D": 24, "E": 24, "F": 26, "G": 20}.items():
    ws3.column_dimensions[k].width = v
band(ws3, 1, "XXX様　プラン別 KPI目標一覧", "保証＝契約に明記（未達時の措置あり）／目標値＝実績に基づく努力目標／承諾交付＝必ず納品する数量", ncol=7)
header(ws3, 4, ["施策", "KPI指標", "小プラン", "中プラン", "大プラン", "測定方法", "区分"])
TAG = {"保証": ("9C5700", "FDF3DC"), "目標値": ("22406B", "EEF2FA"), "承諾交付": ("048F3E", "E9F9EF")}
kpi = [
    ("声量（全体）", "「長岡花火」の年間総言及量", "＋30％（4,770,013 → 6,201,017）", "＋30％（4,770,013 → 6,201,017）", "＋30％（4,770,013 → 6,201,017）", "Pandora", "保証"),
    ("", "8月以外の声量", "—", "1.5倍（1,226,672 → 1,840,000）", "1.5倍（1,226,672 → 1,840,000）", "Pandora", "目標値"),
    ("", "月次レポート", "10本", "10本", "10本", "レポート提出", "承諾交付"),
    ("Threads公式アカウント", "運用期間・投稿数", "10か月・60本以上", "10か月・60本以上", "10か月・60本以上", "投稿カレンダー＋投稿リンク", "承諾交付"),
    ("", "フォロワー数", "8,000〜10,000人", "8,000〜10,000人", "10,000〜15,000人", "Threadsインサイト", "目標値"),
    ("", "平均エンゲージメント率", "4％以上", "4％以上", "4％以上", "Threadsインサイト", "目標値"),
    ("Threads KOC", "投稿数", "4本", "6本", "10本", "投稿リンク", "承諾交付"),
    ("", "閲覧数（1本あたり10,000以上）", "40,000以上", "60,000以上", "100,000以上", "プラットフォーム数値", "保証"),
    ("", "1本あたりエンゲージメント・言及量", "100以上・1,000以上", "100以上・1,000以上", "100以上・1,000以上", "スクリーンショット＋Pandora", "保証"),
    ("IG KOC・旅行KOC", "KOC人数", "—", "IG KOC 6名・旅行KOC 2名", "IG KOC 10名・旅行KOC 4名", "投稿リンク", "承諾交付"),
    ("", "リーチ（参考値）", "—", "12,000〜30,000", "20,000〜50,000", "IGインサイト", "目標値"),
    ("GEO", "ニュース・掲示板記事", "—", "ニュース6・掲示板6", "ニュース12・掲示板12", "掲載リンク一覧", "承諾交付"),
    ("", "キーワード設計", "—", "30組", "60組", "キーワード一覧", "承諾交付"),
    ("", "AI検索掲載", "—", "3組", "6組", "月次AI検索モニタリング", "保証（未達時30％返金）"),
    ("雄獅×欣傳媒", "インタビュー記事＋SNS配信", "—", "1本", "2本（＋閑散期記事）", "掲載リンク＋配信レポート", "承諾交付"),
    ("繁体字公式ガイド", "LP制作", "—", "1式", "1式", "公開URL＋UTMレポート", "承諾交付"),
    ("広告", "運用・月次レポート", "—", "—", "6か月", "広告管理画面レポート", "承諾交付"),
]
for i, row in enumerate(kpi):
    rr = 5 + i
    put(ws3, f"A{rr}", row[0], 10, True, INK, SOFT)
    put(ws3, f"B{rr}", row[1], 10, True, INK)
    for j, c in enumerate("CDE"):
        put(ws3, f"{c}{rr}", row[2 + j], 9.5, False, INK, h="center")
    put(ws3, f"F{rr}", row[5], 9, False, INK)
    e = row[6]
    base = "保証" if e.startswith("保証") else e
    put(ws3, f"G{rr}", e, 9.5, True, TAG[base][0], TAG[base][1], h="center")
    ws3.row_dimensions[rr].height = 34
rr = 5 + len(kpi) + 1
for n in ["・「保証」：未達成時の対応を契約書に明記（GEO：未達のセットは金額の30％を返金／KOC：保証値に達するまで無償で追加投稿／声量：施策の追加実施で対応）。",
          "・「目標値」：同種アカウントの運用実績にもとづく目標。契約上の保証値ではなく、月次レポートで進捗を確認し施策を調整。",
          "・「承諾交付」：必ず納品する数量・成果物。投稿リンク・掲載リンク・スクリーンショットで交付を記録。",
          "・声量の基準値はPandora実測値（データ期間 2025/10/27〜2026/10/26、キーワード「長岡花火大會」、台湾＋香港、総言及量4,770,013）。実施時は施策開始前日までの最新データを基準値とする。"]:
    ws3.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=7)
    put(ws3, f"A{rr}", n, 9, False, GREY, border=False)
    rr += 1
for w in wb:
    w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.orientation = "landscape"
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT)
