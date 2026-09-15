# -*- coding: utf-8 -*-
"""v.2 deck: circled numbering + translate pages 16+ to Chinese. Pages 1-15 untouched."""
import os, re
from pptx import Presentation

BASE = "/Users/shelleychen/Documents/提案/SMBC三井住友"
SRC = os.path.join(BASE, "8:28-v.2_編集中【SMCC様】_Visaタッチについて0831_中文版 copy.pptx")
OUT = os.path.join(BASE, "8:28-v.2_編集中【SMCC様】_Visaタッチについて0831_中文版 copy_v.2.pptx")

C = {"01": "①", "02": "②", "03": "③", "04": "④", "05": "⑤",
     "06": "⑥", "07": "⑦", "08": "⑧", "09": "⑨", "10": "⑩"}

prs = Presentation(SRC)

def walk(shapes):
    for sh in shapes:
        if sh.shape_type == 6:
            for sub in walk(sh.shapes):
                yield sub
        elif sh.has_text_frame:
            yield sh

def para_text(para):
    return "".join(r.text for r in para.runs)

def rewrite_para(para, new_text):
    runs = para.runs
    if not runs:
        return
    runs[0].text = new_text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)

# ---- paragraph-level translations (exact match after strip) ----
PARA_EXACT = {
# p18 日台對照
"本提案に出てくる台湾の空港・鉄道・街区を、日本の同等物に対応させた早見表。以降のページはこの対応関係で読めます":
    "把本提案中出現的台灣機場・鐵道・街區，對應到日本同等設施的對照表。之後的頁面都可以用這個對應關係來閱讀",
"台湾": "台灣",
"日本での相当": "日本的對應",
"補足": "補充說明",
"空港": "機場",
"鉄道": "鐵道",
"駅・拠点": "車站・據點",
"街区・道路": "街區・道路",
"桃園国際空港（TPE）": "桃園國際機場（TPE）",
"松山空港（TSA）": "松山機場（TSA）",
"都心から約 40 km。台湾の国際線の主玄関。年 4,780 万人次":
    "距台北市中心約 40 km。台灣國際線的主要門戶。年 4,780 萬人次",
"台北市内にある都市型空港。国際線はほぼ東京・羽田のみ。年 562 万人次":
    "位於台北市區的都市型機場。國際線幾乎只飛東京・羽田。年 562 萬人次",
"≒　京成スカイライナー ／ 東京モノレール": "≒　京成 Skyliner ／ 東京單軌電車",
"台北駅 → 空港 直達 35 分。全 21 駅、乗客はほぼ全員が空港往復":
    "台北車站 → 機場直達 35 分。全線 21 站，乘客幾乎都是機場往返",
"台湾高鐵（高鐵）": "台灣高鐵（高鐵）",
"台北 – 左営 350 km・最速 1 時間 45 分。西部を縦断する幹線":
    "台北 – 左營 350 km・最快 1 小時 45 分。縱貫西部的幹線",
"≒　東京メトロ": "≒　東京 Metro（地下鐵）",
"≒　東京駅": "≒　東京車站",
"台北都市圏の地下鉄網。1 日平均 216 万人次": "台北都會區的地下鐵路網。日均 216 萬人次",
"台北車站（台北駅）": "台北車站",
"在来線・高鐵・地下鉄の三線共構。月間の乗換量 約 1,200 万":
    "台鐵・高鐵・捷運三鐵共構。每月轉乘量約 1,200 萬",
"≒　新幹線の郊外駅 ＋ 空港連絡線の乗換駅": "≒　新幹線郊區站 ＋ 機場聯絡線轉乘站",
"中南部からの旅客はこの駅で空港線に乗り換える": "中南部旅客在這一站轉乘機場線",
"≒　表参道・青山あたり": "≒　表參道・青山一帶",
"松山空港に隣接するオフィス街。海外カード利用頻度が最も高い層":
    "鄰接松山機場的商辦街區。海外刷卡使用頻率最高的客層",
"≒　成田周辺の幹線沿い": "≒　成田周邊的幹道沿線",
"台 4 線と国道 2 号（空港連絡道）が通る、空港手前の必経ルート":
    "台 4 線與國道 2 號（機場聯絡道）經過，機場前的必經路線",
"国道 2 号": "國道 2 號",
"≒　東関東自動車道（空港連絡道）": "≒　東關東自動車道（機場聯絡道）",
"桃園空港への直結道路。バス・タクシー・自家用車の共通ルート":
    "直通桃園機場的道路。巴士・計程車・自駕的共同路線",
"この対応で読むと、本案の中心版位「桃園空港 T1・3F 出国審査待ちエリアの大型ライトボックス」は、日本でいえば「成田の出国審査の列に並んでいる 40 分間、正面に出続ける看板」に相当します。並んでいる人は手持ち無沙汰で、視線が固定される——「どう使うか」を四コマで説明するのに最も適した場所です。":
    "用這個對照來看，本案的核心版位「桃園機場 T1・3F 出境查驗等候區的大型燈箱」，相當於日本「在成田出境審查隊伍中排隊 40 分鐘、正面持續映入眼簾的看板」。排隊的人手上沒事做、視線被固定——是用四格圖解說明「怎麼用」最適合的場所。",
# p33 季節性
"強度は、訪日台湾人の月別需要、祝日、日本の季節要因を総合した相対評価（1～5）。秋（10～11月）は夏休みに次ぐ高需要期。":
    "強度為綜合訪日台灣旅客月別需求、假期與日本季節因素的相對評價（1–5）。秋季（10–11 月）是僅次於暑假的高需求期。",
"出発月と意思決定月を分けて設計": "出發月與決策月分開設計",
"空港・交通媒体は実際の出発月に接触する一方、GEO・口コミは1～2ヶ月前の情報収集段階から展開する。":
    "機場・交通媒體接觸的是實際出發月；GEO・口碑則從出發前 1–2 個月的資訊蒐集階段開始佈局。",
"本案件では、意思決定月に検索・比較接点を整備し、出発月に空港・移動接点で利用方法を再認知させる二段構えが有効。":
    "本案採兩段式設計：在決策月建立搜尋・比較接點，在出發月以機場・移動接點喚起使用方式的再認知。",
"ピークごとの投資優先度": "各高峰的投資優先順序",
"最重要期は7～8月の夏休み。訪日量・若年層比率・新決済受容度が最も高い。":
    "最重要檔期是 7–8 月暑假。訪日量、年輕客群比例與新支付方式接受度都最高。",
"春節・桜シーズンは第2ピーク。人気枠は早期に埋まるため、前倒しで確保する。":
    "春節・櫻花季是第二高峰。熱門版位很早就被訂滿，須提前鎖定。",
"年末年始は話題化に適した時期。GEO・口コミ・動画素材で効率的に接点化する。":
    "年末年初適合話題操作。以 GEO・口碑・影音素材有效率地建立接點。",
"5月は実体広告を抑制": "5 月抑制實體廣告",
"5月は訪日需要が落ち込みやすいため、実体広告は停止し、GEOとPandora監視のみ継続。":
    "5 月訪日需求容易下滑，實體廣告全面暫停，僅持續 GEO 與 Pandora 監測。",
"捻出した予算は、需要が最大化する7～8月の空港ターミナルへ再配分する。":
    "省下的預算重新配置到需求最大化的 7–8 月機場航廈。",
# p34 投放時機
"本ページの月別構成は、媒体配置明細と連動。秋季は認知形成、春節・桜・夏休みは行動化を重視。":
    "本頁的月別構成與媒體排期明細連動。秋季重認知形成，春節・櫻花・暑假重行動轉換。",
"訪日出発強度": "訪日出發強度",
"GEO（プレスリリース＋口コミ記事）": "GEO（新聞稿＋口碑文章）",
"Pandora モニタリング": "Pandora 監測",
"01　地下鉄ネットワーク（6週間）": "①　捷運聯播網（6 週）",
"03　松山空港線 市内バス 車内ポスター": "③　敦化・民生幹線 車內海報",
"03　松山空港線 市内バス 945号 車体": "③　松山機場線 945 車體滿版",
"04　屋外看板（桃園の動線）": "④　戶外看板（桃園動線）",
"05　桃園メトロ 特別列車ポスター 1列": "⑤　桃捷 專車海報 1 列",
"06　空港バス 車体広告（1819＋1840）": "⑥　機場巴士 車體滿版（1819＋1840）",
"07　タクシー 車内スクリーン": "⑦　計程車 車內螢幕",
"08　桃園空港 ターミナル": "⑧　桃園機場 出境區",
"08　松山空港 ターミナル": "⑧　松山機場 出境區",
"09　桃園空港配車 シートカバー": "⑨　桃機排班計程車 椅套",
"10　台湾高鉄（桃園駅・台北駅）": "⑩　台灣高鐵（桃園站・台北站）",
# month labels (p33/p34)
"双十節": "雙十節", "双十": "雙十", "大晦日": "跨年", "冬休み": "寒假",
"桜": "櫻花", "閑散期": "淡季", "夏休み前": "暑假前", "夏休み": "暑假",
"9月26日": "26/09", "1月27日": "27/01",
}

# run-level substring replacements
RUN_PAIRS = [("01–04", "①–④"), ("05–07", "⑤–⑦"), ("廣告 05 機場捷運", "廣告 ⑤ 機場捷運")]
for nn, c in C.items():
    for rom in ("Ⅰ", "Ⅱ", "Ⅲ"):
        RUN_PAIRS.append((f"{nn}-{rom}", f"{c}-{rom}"))

# p16 transport-name prefixes
P16_PAIRS = [
    ("捷運・計程車・市區公車", "①捷運・⑦計程車・③市區公車"),
    ("機場捷運（A1 → A12／A13）", "⑤機場捷運（A1 → A12／A13）"),
    ("機場巴士 1819／1840", "⑥機場巴士 1819／1840"),
    ("計程車・自駕（國道 2 號）", "⑦計程車・自駕（國道 2 號）"),
    ("機場捷運 A18 → A12", "⑤機場捷運 A18 → A12"),
    ("高鐵（西部走廊）", "⑩高鐵（西部走廊）"),
]

num_prefix = re.compile(r"^(0[1-9]|10)(?=　)")

for idx, slide in enumerate(prs.slides, 1):
    if idx <= 15:
        continue
    for sh in walk(slide.shapes):
        for para in sh.text_frame.paragraphs:
            t = para_text(para)
            ts = t.strip()
            # 1. exact paragraph translation
            if ts in PARA_EXACT:
                rewrite_para(para, PARA_EXACT[ts])
                t = para_text(para)
            # 2. p16-specific
            if idx == 16:
                for a, b in P16_PAIRS:
                    if a in t and not t.startswith(("①", "⑤", "⑥", "⑦", "⑩")):
                        for r in para.runs:
                            if a in r.text:
                                r.text = r.text.replace(a, b)
                        t = para_text(para)
                if t.strip() == "高鐵":
                    rewrite_para(para, "⑩高鐵")
                    t = para_text(para)
                for pre, mark in [("機場巴士 1819", "⑥"), ("計程車・自駕", "⑦")]:
                    if t.startswith(pre) and para.runs:
                        para.runs[0].text = mark + para.runs[0].text
                        t = para_text(para)
            # 3. chip "08" on p17
            if idx == 17 and t.strip() == "08":
                rewrite_para(para, "⑧")
                t = para_text(para)
            # 4. run substrings
            for r in para.runs:
                for a, b in RUN_PAIRS:
                    if a in r.text:
                        r.text = r.text.replace(a, b)
            # 5. leading NN　 -> circled
            t = para_text(para)
            m = num_prefix.match(t)
            if m:
                nn = m.group(1)
                first = para.runs[0]
                if first.text.startswith(nn):
                    first.text = C[nn] + first.text[len(nn):]
                t = para_text(para)

prs.save(OUT)
print("saved", OUT)

# leftover kana check
import zipfile
prs2 = Presentation(OUT)
kana = re.compile(r"[぀-ゟ゠-ヿ]")
def walk2(shapes):
    for sh in shapes:
        if sh.shape_type == 6:
            for sub in walk2(sh.shapes):
                yield sub
        elif sh.has_text_frame:
            yield sh
for i, s in enumerate(prs2.slides, 1):
    if i <= 15:
        continue
    for sh in walk2(s.shapes):
        for para in sh.text_frame.paragraphs:
            t = "".join(r.text for r in para.runs)
            tt = t.replace("・", "")
            if kana.search(tt):
                print("LEFTOVER", i, repr(t[:80]))
