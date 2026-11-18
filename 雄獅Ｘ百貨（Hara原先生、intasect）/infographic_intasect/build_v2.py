"""v2：p1 Banaverse 資訊圖（Intasect 左／雄獅右，雙渠道）＋ p2 市場規模與潛力"""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/shelley-deck/scripts"))
from PIL import Image  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from pptx.util import Pt  # noqa: E402
from shelley_deck import Deck, text_w, W  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
A = lambda n: os.path.join(HERE, "assets", n)  # noqa: E731
RED, CYAN, GOLD, NAVY = "#C8102E", "#1DB7D3", "#FFC000", "#0A1F44"

d = Deck(theme={"frame": RED}, footer_logos=["brand/accucrazy-dark.png"])


# ================================================================ 修圖：下方渠道標籤換成正確順序（原圖文字抹掉，改用原生文字）
def patch_bottom_labels(src, dst):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    k = w / 1600
    x0, x1, y0, y1 = int(622 * k), int(1322 * k), int(602 * k), int(657 * k)
    px = im.load()
    for y in range(y0, y1):
        a, b = px[x0 - 2, y], px[x1 + 2, y]
        for x in range(x0, x1):
            t = (x - x0) / (x1 - x0)
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    im.save(dst, quality=92)


P1 = A("p1_final.jpg")
patch_bottom_labels(A("p1_v1.jpg"), P1)

# ================================================================ P1
s = d.info("合作示意圖：兩條渠道、一個中心——Intasect 的企業官網 × 騰雲 T-Space × 雄獅",
           label="合作架構", numbered=False,
           banner="日本客人從企業官網走進雄獅，台灣客人從雄獅走進日本地方——中心都是騰雲 T-Space")
IW = 11.4
iw, ih = Image.open(P1).size
IH = IW * ih / iw
IX, IY = (W - IW) / 2, 1.08
s.shapes.add_picture(P1, *[int(v * 914400) for v in (IX, IY, IW, IH)])
k = IW / 1600  # 預覽座標(1600 寬) → 英吋


def at(px_, py_):
    return IX + px_ * k, IY + py_ * k


for cx, txt in [(760, "購買自治體行程・\nIntasect 票券"), (957, "T-Space\n導購頁"), (1172, "雄獅官網\n開設對應團")]:
    x, y = at(cx, 604)
    d.tx(s, x - 0.85, y, 1.7, 0.4, txt, 10, color="#1E2A3A", bold=True, align=PP_ALIGN.CENTER, spacing=1.05)

# 客戶名單（原生文字，確保正確）
ys = IY + IH + 0.05
d.round(s, 0.6, ys, W - 1.2, 0.42, "#F2F6FB", 0.2)
d.round(s, 0.7, ys + 0.085, 1.15, 0.25, RED, 0.5)
d.tx(s, 0.7, ys + 0.085, 1.15, 0.25, "更多合作夥伴", 9, color="white", bold=True, align=PP_ALIGN.CENTER,
     anchor=MSO_ANCHOR.MIDDLE)
names = ["京都府", "三鷹市", "美瑛町觀光協會", "平取町", "占冠村", "小樽堺町通商店街", "有馬溫泉", "河口湖旅館協同組合",
         "福井縣立恐龍博物館", "舊福岡縣公會堂", "祇園祭 函谷鉾", "海洋博美ら海花火大會", "岩岳度假村",
         "阪急阪神百貨店", "高島屋", "近鐵百貨店", "Ryubo 琉球百貨", "唐吉訶德（PPIH）",
         "JR 東日本", "JR 西日本", "JR 九州", "JR 東日本 View Tourism", "JR 東日本企劃", "Toki Air", "富士急行",
         "東方樂園", "東京晴空塔", "三井住友 FG", "SBI", "Sony 銀行", "Sony Payment Services", "Aplus", "野村總研", "Toyota"]
d.tx(s, 1.95, ys + 0.045, W - 2.65, 0.36, "・".join(names), 7.5, color="mid", spacing=1.1,
     anchor=MSO_ANCHOR.MIDDLE)
s.notes_slide.notes_text_frame.text = (
    "客戶名單出處：Intasect 事業紹介資料（2026/10）主要取引先・IntaPay 導入實例；intasect.com 導入事例；"
    "PR TIMES（2025/02 白馬谷 IntaPay、IntaEvent 海洋博花火）；長岡花火、淡路島 Pasona 為 Intasect 提供之合作對象。"
    "資訊圖底圖由 Banaverse（Nano Banana Pro）生成，下方渠道文字與合作夥伴名單為可編輯文字。")

# ================================================================ P2 市場規模
s = d.info("規模感：接上 Intasect，雄獅多出一條千萬級受眾的雙向渠道", label="市場潛力", numbered=False,
           banner="台灣旅客每年在日本花 NT$2,500 億——只要接住 0.6%，就是一門 NT$14 億的生意")


def kicker(x, y, text, col=RED):
    d.rect(s, x, y + 0.04, 0.06, 0.2, col)
    d.tx(s, x + 0.14, y, 6, 0.28, text, 11.5, bold=True, color="ink")


# --- Row A：市場有多大
kicker(0.6, 1.12, "市場有多大｜台日雙向旅遊與百貨消費")
cards = [("676", "萬人次", "2025 台灣訪日旅客", "JNTO 確定值，年增 11.9%"),
         ("1.2", "兆日圓", "台灣旅客在日消費", "≈ NT$2,500 億｜觀光廳 2025 確報"),
         ("150", "萬人次", "2025 日本訪台旅客", "來台最大客源市場｜觀光署"),
         ("5.7", "兆日圓", "日本百貨業年營業額", "日本百貨店協會 70 家會員企業")]
cw, gap, cy, ch = (W - 1.2 - 0.3) / 4, 0.1, 1.45, 1.05


def numrun(x, y, w, n, u, col, nsize=28, usize=11):
    tb = d.tx(s, x, y, w, 0.5, n, nsize, color=col, bold=True, font=d.num_font)
    para = tb.text_frame.paragraphs[0]
    r = para.add_run()
    r.text = " " + u
    r.font.size = Pt(usize)
    r.font.bold = True
    r.font.color.rgb = d.col(col)
    r.font.name = d.font
    d._ea(tb, d.font)
    tb.text_frame.paragraphs[0].runs[0].font.name = d.num_font
    return tb


for i, (n, u, l, sub) in enumerate(cards):
    x = 0.6 + i * (cw + gap)
    col = RED if i < 2 else "#0E8BA3"
    d.round(s, x, cy, cw, ch, "#FFF4F5" if i < 2 else "#EEF8FB", 0.1)
    d.rect(s, x, cy + 0.15, 0.06, ch - 0.3, RED if i < 2 else CYAN)
    numrun(x + 0.22, cy + 0.04, cw - 0.3, n, u, col)
    d.tx(s, x + 0.24, cy + 0.56, cw - 0.35, 0.22, l, 10.5, bold=True)
    d.tx(s, x + 0.24, cy + 0.8, cw - 0.35, 0.2, sub, 8, color="mid")

# --- Row B 左：Intasect 網絡可觸及受眾
BY = 2.65
LW = 5.95
d.round(s, 0.6, BY, LW, 6.08 - BY, "#F4F7FB", 0.04)
d.fit(s, A("p2_map.jpg"), 0.62, BY + 0.03, 2.5, 6.08 - BY - 0.06)
d.ai_tag(s, 0.72, 5.72, "AI 示意圖")
bx = 3.2
d.tx(s, bx, BY + 0.12, 3.3, 0.25, "Intasect 網絡可觸及受眾", 11, bold=True)
numrun(bx, BY + 0.36, 3.3, "1,200萬+", "人次／年", RED, nsize=26)
bars = [("百貨免稅購買客", 621, "日本百貨店協會 2025"),
        ("百貨會員（阪急阪神・藤崎・鶴屋）", 230, "提案 v3.0"),
        ("富良野 年遊客", 185, "2024 年度"),
        ("白馬谷 冬季遊客", 130, "2024–25 冬季"),
        ("長岡花火大會 觀覽人數", 34, "2025 有料觀覽")]
y = BY + 0.95
for name, v, src in bars:
    d.tx(s, bx, y, 2.6, 0.22, name, 9, bold=True)
    d.tx(s, bx + 2.0, y + 0.01, 1.3, 0.2, src, 7, color="grey", align=PP_ALIGN.RIGHT)
    bw = 3.25 * v / 621
    d.round(s, bx, y + 0.24, bw, 0.13, RED if v >= 185 else "#E58A97", 0.5)
    d.tx(s, bx + text_w(name, 0.155 * 9 / 11.2, 0.085 * 9 / 11.2) + 0.12, y - 0.03, 0.8, 0.25, f"{v}萬", 11,
         color=RED, bold=True, font=d.num_font)
    y += 0.46
d.tx(s, bx, y - 0.02, 3.3, 0.2, "＋IntaPay 4 萬店舖・年流通 2,500 億日圓（受眾為單純加總，示意）", 7,
     color="mid", spacing=1.2)

# --- Row B 右：試算
RX = 0.6 + LW + 0.2
RWD = W - 0.6 - RX
d.tx(s, RX, BY + 0.02, RWD, 0.3, "生意有多大｜導流試算（示意）", 11.5, bold=True)
tbl = s.shapes.add_table(7, 3, *[int(v * 914400) for v in (RX, BY + 0.36, RWD, 2.03)]).table
cols = [2.6, (RWD - 2.6) / 2, (RWD - 2.6) / 2]
for i, c in enumerate(cols):
    tbl.columns[i].width = int(c * 914400)
rows = [("", "Year 1｜起步", "Year 3｜擴大"),
        ("合作官網數", "30 家", "150 家"),
        ("渠道① Banner 曝光", "3,600 萬次", "1.8 億次"),
        ("渠道① LionTrip 新會員", "2.9 萬人", "14.4 萬人"),
        ("渠道② 自治體團 成行", "9,000 人", "2.25 萬人"),
        ("渠道② Intasect 票券", "2.25 萬張", "6.75 萬張"),
        ("預估 GMV", "NT$5 億", "NT$14 億")]
from pptx.dml.color import RGBColor  # noqa: E402
for r, row in enumerate(rows):
    tbl.rows[r].height = int(0.29 * 914400)
    for c, v in enumerate(row):
        cell = tbl.cell(r, c)
        cell.margin_left = cell.margin_right = int(0.1 * 914400)
        cell.margin_top = cell.margin_bottom = 0
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.fill.solid()
        head, last = r == 0, r == len(rows) - 1
        cell.fill.fore_color.rgb = RGBColor.from_string(
            (NAVY if head else RED if last else ("FFFFFF" if r % 2 else "F4F7FB")).lstrip("#"))
        tf = cell.text_frame
        tf.text = v
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
        f = p.runs[0].font if p.runs else None
        if f:
            f.size = Pt(12 if last and c else 9.5)
            f.bold = head or last or c == 2
            f.color.rgb = RGBColor.from_string("FFFFFF" if head or last else ("C8102E" if c == 2 else "1E1A1D"))
            f.name = d.font
        d._ea(cell, d.font)

# 三張亮點卡
hy, hh = 5.17, 0.91
hl = [("NT$14億", "Year 3 年 GMV", "台灣旅客在日消費的 0.6%"),
      ("1.8億次", "品牌曝光／年", "≈ 媒體價值 NT$2,700 萬"),
      ("14.4萬", "LionTrip 日本新會員", "日本人成為雄獅國際會員")]
hw = (RWD - 0.2) / 3
for i, (n, l, sub) in enumerate(hl):
    x = RX + i * (hw + 0.1)
    d.round(s, x, hy, hw, hh, [RED, GOLD, CYAN][i], 0.1)
    fg = "white" if i != 1 else NAVY
    d.tx(s, x, hy + 0.04, hw, 0.42, n, 20, color=fg, bold=True, align=PP_ALIGN.CENTER, font=d.num_font)
    d.tx(s, x, hy + 0.44, hw, 0.22, l, 9.5, color=fg, bold=True, align=PP_ALIGN.CENTER)
    d.tx(s, x, hy + 0.66, hw, 0.2, sub, 7.5, color=fg, align=PP_ALIGN.CENTER)

d.tx(s, 0.6, 6.12, W - 1.2, 0.3,
     "Data source：JNTO 2025 確定值；觀光廳 2025 訪日外國人消費動向確報；交通部觀光署 2025；日本百貨店協會 2025；北海道新聞（富良野 2024 年度）；"
     "白馬村 2024–25 冬季；長岡花火 2025。試算假設（示意）：每站月曝光 10 萬、CTR 0.4%、LP→App 20%、LP→訂單 1%（客單 NT$4 萬）；"
     "雄獅赴日約 45 萬人中 2%／5% 選購自治體團（NT$4.5 萬）、5%／15% 購買票券（NT$2,000）；CPM NT$150。",
     6.5, color="grey", spacing=1.05)

d.save(os.path.join(HERE, "Intasect合作示意_infographic_v2.pptx"))
