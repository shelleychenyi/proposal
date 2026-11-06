import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/shelley-deck/scripts"))
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN  # noqa: E402
from shelley_deck import Deck, W, H, _alpha  # noqa: E402

os.chdir(os.path.dirname(os.path.abspath(__file__)))
A = "assets/"
LALA = A + "logo/logo@3x_org.png"
MOP = A + "logo/logo@3x_org_mitsui.png"
TC = "brand/turncloud.png"
BLUE, ORANGE, MINT, PINK, CORAL = "#2B67B0", "#F39A1E", "#22C2A0", "#FF6FA3", "#FF6F61"
IDEA_VIDEO = A + "video/idea_bg.mp4" if os.path.exists(A + "video/idea_bg.mp4") else None

d = Deck(theme={"frame": BLUE, "accent": ORANGE}, footer_logos=[TC])


def phone(s, key, x, y, h, video=True, tag=True):
    """手機框＋Prototype 錄影（poster = 截圖）。回傳寬度。"""
    w = h * 390 / 844
    d.round(s, x - 0.07, y - 0.07, w + 0.14, h + 0.14, "#0E1A33", 0.12)
    poster = A + f"poster/{key}.jpg"
    vid = A + f"video/{key}.mp4" if video else None
    d.movie(s, vid, poster, x, y, w, h)
    if tag:
        d.ai_tag(s, x + 0.08, y + h + 0.14, "Prototype 錄影" if video else "UI 示意")
    return w


def phone_demo(title, label, key, points, banner, photo=None, keys2=None, source=None):
    s = d.info(title, label=label, banner=banner, source=source)
    x = 0.9
    w = phone(s, key, x, 1.3, 4.55)
    x += w + 0.45
    for k in keys2 or []:
        w2 = phone(s, k, x, 1.3, 4.55)
        x += w2 + 0.45
    if photo:
        pw = 9.0 - x
        px, py, pw, ph = d.fit(s, photo, x, 1.3, pw, 4.55)
        d.ai_tag(s, px + 0.1, py + 0.1)
    d.tx(s, 9.35, 1.35, 3.4, 0.35, "畫面重點", 13, color="frame", bold=True)
    gap = min(1.15, 4.6 / max(1, len(points)))
    d.callouts(s, 9.35, 1.85, 3.4, points, gap=gap)
    return s


# ---------------------------------------------------------------- 封面
d.cover("MSP 會員 App\n3.0 改版提案。", "LaLa Quest｜每一次來，都在升級。", "2026.11",
        company="TURN CLOUD TECHNOLOGY SERVICE INC.", logos=[LALA, MOP], image=A + "mock_hero3.jpg")
d.toc([("現況與機會", "機會"), ("標竿學習", "標竿"), ("App 3.0 全貌", "全貌"), ("會員分級", "分級"),
       ("遊戲化設計", "遊戲"), ("AI 功能", "AI"), ("口碑專區 LaLa Buzz", "口碑"), ("落地與 KPI", "落地")])

# ---------------------------------------------------------------- 1 現況與機會
d.divider("現況與機會", "App 有了、會員有了，\n只差一個「每天打開」的理由", key="機會")

s = d.info("一頁看懂：把逛街，變成一場會升級的遊戲", label="Executive Summary",
           banner="不是再多一個優惠券入口，而是讓年輕人「想」打開 App：看得到等級、玩得到東西、問得到答案")
d.columns(s, [("現況", "#8A94A6", "95% 的會員，消費沒被記住",
               "只有 5% 會員用 App 集點\n一種會員：Regular Member\n首頁是一面廣告牆\n遊戲藏在 Profile 第二層"),
              ("解法", BLUE, "LaLa Quest：四件事",
               "Level Up：四級會員\nPlay：簽到、任務、扭蛋\nAsk：AI 管家＋AI 發票集點\nBuzz：網路好評＋Real Talk"),
              ("收益", ORANGE, "集點率 5% → 20%（示意）",
               "每張發票都回到 CRM\n偶爾來 → 每月來\n店家多一個導購入口\n兩館共用一個會員身份")])

s = d.info("機會①　95% 的會員，來了卻沒被記住", label="核心與機會",
           banner="大家為了活動與美食而來，但 App 在社群裡幾乎不存在",
           source="Data source: 客戶提供 2026/11；Pandora 實測 2025/11/06–2026/11/05，馬來西亞地區 LaLaport BBCC／MOP 相關貼文 N=7,236（Threads、Instagram）")
d.num_cards(s, [("5%", "用 App 集點的會員", "95% 的消費沒有回到會員身上"),
                ("7,236", "近一年社群貼文", "LaLaport BBCC、MOP 在馬來西亞的聲量"),
                ("0.3%", "提到 App／點數的貼文", "約 20 篇：App 沒有存在感"),
                ("83%", "英文貼文", "介面與語氣都要用馬來西亞英語")], color="frame")
d.tx(s, 0.75, 4.05, 11.8, 1.5,
     "→ 不是會員不夠多，是 App 沒有給他們「每次打開都有收穫」的感覺。\n"
     "→ 年輕人每天在 Shopee 玩小遊戲換 Coins，卻不會為了 1 點 MSP Point 打開商場 App。",
     15, bold=True, spacing=1.7)

s = d.info("機會②　現在的 App，是一本電子版的商場簡介", label="現況盤點",
           banner="功能都有，但每個功能都是「看」，沒有一個是「玩」",
           source="Data source: Mitsui New App guideline；App 實機截圖 2026/11")
d.fit(s, A + "current_app.jpg", 0.6, 1.25, 8.4, 2.6, border=True)
d.ai_tag(s, 0.72, 1.33, "現行 App 實機畫面")
d.tx(s, 9.35, 1.35, 3.4, 0.35, "我們看到的問題", 13, color="frame", bold=True)
d.callouts(s, 9.35, 1.85, 3.4, [("首頁＝廣告牆", "Banner、News、Voucher 都在推，沒有「我」"),
                               ("只有一種會員", "Regular Member，看不到下一步在哪"),
                               ("遊戲藏太深", "Spin & Win 在 Profile 第二層"),
                               ("沒有 AI", "找店、找吃、集點全靠自己")], gap=1.1)
d.table(s, ["現行 Tab", "Mall", "Vouchers", "Home", "Profile", "News"],
        [["3.0 Tab", "Home", "Quest", "Scan（正中間）", "Buzz", "Me"]],
        x=0.6, y=4.25, w=8.4, size=12, row_h=0.5, hot_row=0)

s = d.info("機會③　年輕人早就在這裡：動漫、K-pop、聯名咖啡", label="核心與機會",
           banner="館內本來就是年輕人的主場：ACG Base、Animate Café、Doko Koko、GSC K-pop 放映會",
           source="Data source: Pandora 實測 2025/11/06–2026/11/05，馬來西亞 N=7,236；關鍵字分類、一篇可屬多類")
d.bars(s, [("美食・咖啡", 1594), ("優惠・折扣", 1465), ("節慶・活動", 1374), ("停車・交通", 1204),
           ("動漫 ACG", 1054), ("電影・K-pop", 724), ("親子", 303)], 0.6, 1.4, 7.6, row_h=0.6, hot={4, 5})
d.quote(s, 8.4, 1.4, 4.3, 2.15, "「This mall is secretly\nheaven for anime fans 👀」",
        "@mijuyq Instagram｜2026/07")
d.quote(s, 8.4, 3.75, 4.3, 2.15, "「Lalaport 的 lulu 猪快闪店\n太好逛了，一时没忍住！」",
        "IG Reel｜LuLu 快閃店｜2026/05｜聲量 56,568")

s = d.info("機會④　最痛的停車費，App 早就有解，只是沒人知道", label="Fan Truth",
           banner="把「MSP Member 免費停車」變成等級權益，第一天就讓人感受到 App 的價值",
           source="Data source: Instagram Reel 標註 @lalaport_bbcc（Pandora 聲量 104,838）；官網 MSP Member Free 3 Hours Parking 2026/11–12")
d.quote(s, 0.72, 1.45, 6.0, 2.6, "「你们觉得我的积蓄\n够给这个 parking fee 吗 🙂‍↕️」",
        "IG Reel @lalaport_bbcc 標註｜聲量 104,838，近一年馬來西亞前 10 名")
d.rect(s, 7.1, 1.45, 5.6, 2.6, "soft")
d.rect(s, 7.1, 1.45, 5.6, 0.08, ORANGE)
d.tx(s, 7.4, 1.75, 5.0, 0.4, "其實 App 已經有：", 14, color="mid", bold=True)
d.tx(s, 7.4, 2.2, 5.0, 0.8, "MSP Member\nFree 3 Hours Parking", 24, color="frame", bold=True, spacing=1.2)
d.tx(s, 7.4, 3.3, 5.0, 0.6, "但它只是 News 頁裡的一則活動", 13, color="mid")
d.tx(s, 0.75, 4.4, 12, 1.3,
     "3.0 做法：停車時數跟著等級走 —— Rookie 3H → Explorer 4H → Senpai 5H → Legend 全日。\n"
     "首頁會員卡上直接寫「🅿️ 4H free parking」，出場掃一下就扣。", 15, bold=True, spacing=1.7)

s = d.info("三個切角，收斂成一句話", label="切角 → Proposition", banner="Proposition｜每一次來，都在升級。")
d.columns(s, [("切角 1", "dark", "看得到進度", "會員分四級\n進度條天天動\n停車、倍率跟著升"),
              ("切角 2", "dark", "玩得到東西", "每日簽到、館內任務\n集章 Stamp Rally\n數位扭蛋 Capsule"),
              ("切角 3", "dark", "問得到答案", "AI 管家 Ask LaLa\nAI 發票掃描集點\n網路好評 LaLa Buzz")])

d.statement("IDEA", "LaLa Quest\n把逛街變成升級遊戲",
            "Every visit levels you up.\n"
            "Level Up：Rookie → Explorer → Senpai → Legend\n"
            "Play：簽到、任務、集章、扭蛋\n"
            "Ask：AI 管家＋AI 發票集點\n"
            "Buzz：網路好評，一鍵帶你過去",
            image=A + ("idea_poster.jpg" if IDEA_VIDEO else "app/acg_event.jpg"), video=IDEA_VIDEO)

# ---------------------------------------------------------------- 2 標竿
d.divider("標竿學習", "好的會員 App，讓人「想」打開，\n不是「要」打開", key="標竿")
s = d.info("六個標竿：每一個都把會員變成一種「身份」", label="Benchmark",
           banner="借來三件事：看得到的進度（Starbucks）、玩得到的收集（USJ／Shopee）、問得到的答案（Disney）",
           source="Data source: 各品牌官方 App 與公開資訊；Starbucks Rewards 2026/03 三級制（Restaurant Dive）")
d.table(s, ["品牌", "他們怎麼做", "LaLa Quest 借什麼"],
        [["MUJI Passport", "進店打卡也送 MUJI Miles，不買東西也能累積", "每日簽到 Streak、Check-in 任務"],
         ["Disney App", "AI 行程建議、排隊時能玩的小遊戲", "Ask LaLa 幫你排一天"],
         ["Universal Studios", "實體互動收集鑰匙，手機上看分數與收藏", "館內集章 Stamp Rally"],
         ["Starbucks Rewards", "Green／Gold／Reserve 三級，回饋 1x／1.2x／1.7x", "四級會員＋點數倍率"],
         ["Shopee", "Coins＋每日小遊戲，大馬人每天的習慣", "每日一抽 LaLa Capsule"],
         ["Sephora", "Beauty Insider 分級＋會員真實評價", "LaLa Buzz＋Real Talk"]],
        col_w=[1.6, 4.2, 3.2], size=13, row_h=0.62)

# ---------------------------------------------------------------- 3 全貌
d.divider("App 3.0 全貌", "四大支柱、五個 Tab、\n一個更年輕的 LaLaport", key="全貌")
s = d.info("LaLa Quest 四大支柱：升級、玩、問、口碑", label="App 架構",
           banner="四個支柱都導向同一件事：把每一次消費、每一次造訪，記回會員身上")
d.columns(s, [("Level Up", "#1E9C9A", "四級會員", "Rookie／Explorer／\nSenpai／Legend\n停車、倍率、扭蛋次數\n跟著等級升"),
              ("Play", PINK, "遊戲化", "每日簽到 Streak\n館內 Quest 任務\nStamp Rally 集章\nLaLa Capsule 扭蛋"),
              ("Ask", BLUE, "AI 功能", "AI 發票掃描集點\nAsk LaLa 管家\nFor You 個人化首頁"),
              ("Buzz", ORANGE, "口碑專區", "Pandora 爬網路好評\nAI 摘要「大家愛什麼」\nReal Talk 已購分享")])

s = d.info("視覺：留住 LaLaport 的藍與 Mitsui 的橘，換上更年輕的語氣", label="Design System",
           banner="品牌色不變、Logo 不動；變的是圓角、漸層、動態，和一口馬來西亞英語")
sw = [(BLUE, "LaLaport Blue", "#2B67B0", "主色・按鈕・導覽"), (ORANGE, "Mitsui Orange", "#F39A1E", "行動・集點・Scan"),
      ("#FEF6E6", "Member Cream", "#FEF6E6", "沿用現行會員卡"), (MINT, "Quest Mint", "#22C2A0", "完成・成功"),
      (PINK, "Matsuri Pink", "#FF6FA3", "活動・ACG")]
for i, (c, n, hx, use) in enumerate(sw):
    x = 0.7 + i * 1.62
    d.round(s, x, 1.4, 1.45, 1.1, c, 0.12)
    d.tx(s, x, 2.6, 1.5, 0.3, n, 11.5, bold=True)
    d.tx(s, x, 2.88, 1.5, 0.3, hx + "\n" + use, 10, color="mid", spacing=1.3)
d.logo(s, LALA, 0.7, 3.85, 0.55)
d.logo(s, MOP, 3.3, 3.88, 0.5)
d.tx(s, 0.7, 4.65, 7.5, 1.2, "字型：Plus Jakarta Sans（圓潤、易讀、支援馬來文）\n圓角 20–24px、卡片漸層、全畫面微動態（進度條、扭蛋、彩帶）",
     12.5, color="mid", spacing=1.6)
d.tx(s, 9.0, 1.35, 3.7, 0.35, "Microcopy：馬來西亞英語", 13, color="frame", bold=True)
mc = ["Jom! 2 quests waiting for you today.", "Ada! Here are 2 picks on L4 👇", "Ask anything, lah…",
      "Done · Shiok!", "Squad up: bring 1 kawan", "🤤 Sedap gila  💸 Worth it"]
for i, t in enumerate(mc):
    d.round(s, 9.0, 1.8 + i * 0.68, 3.7, 0.54, "soft", 0.3)
    d.tx(s, 9.2, 1.92 + i * 0.68, 3.4, 0.3, t, 11.5, bold=True)

phone_demo("首頁：一打開，就知道自己是哪一級、今天能拿什麼", "Home", "home",
           [("會員卡＝進度條", "1,884 pts，再 616 點升 Senpai；停車時數直接寫在卡上"),
            ("5 天連續簽到", "第 7 天送免費扭蛋，用 Streak 養成每天打開"),
            ("四個快捷鍵", "Scan Receipt、Ask LaLa、Capsule、Parking"),
            ("今日任務＋Buzz", "ACG Matsuri 集章進度、網路正夯的店")],
           "首頁從「商場在推什麼」換成「我今天能拿到什麼」", photo=A + "mock_hijab_home.jpg")

# ---------------------------------------------------------------- 4 分級
d.divider("會員分級", "從 Regular Member，\n到 Rookie、Explorer、Senpai、Legend", key="分級")
s = d.info("四個等級：不叫金卡銀卡，叫 Senpai", label="Tier Design",
           banner="用日系動漫語言命名，貼近 LaLaport 的日本 DNA，也是年輕人會想截圖分享的身份",
           source="門檻與權益為試算示意，正式數字依三井會員消費分布調整")
d.table(s, ["等級", "門檻（12 個月）", "點數倍率", "免費停車", "扭蛋", "代表權益"],
        [["Rookie　LV1", "註冊即得", "1x", "3 小時", "1 次／日", "每日簽到、生日禮"],
         ["Explorer　LV2", "RM 1,500 或 12 次造訪", "1.2x", "4 小時", "1 次／日", "生日月雙倍點、聯名咖啡優先訂位"],
         ["Senpai　LV3", "RM 5,000", "1.5x", "5 小時", "2 次／日", "Bon Odori・ACG 活動優先入場、限定扭蛋"],
         ["Legend　LV4", "RM 12,000", "2x", "全日", "3 次／日", "Legend Lounge、年度 Legend Night"]],
        col_w=[1.5, 2.2, 1.1, 1.1, 1.0, 3.6], size=13, row_h=0.7, hot_row=2)
d.tx(s, 0.75, 5.2, 12, 0.6, "★ 「次數」也能升級：Explorer 可用 12 次造訪達成 —— 學生、年輕上班族不用花大錢，常來就能升。",
     13.5, bold=True, color="frame")


phone_demo("等級頁：四張卡疊在一起，下一級永遠看得到", "Tier", "tiers",
           [("卡片疊疊樂", "四級會員卡像錢包一樣疊著，Legend 黑金卡最吸睛"),
            ("權益對照表", "倍率、停車、扭蛋、活動入場，一眼看懂"),
            ("三種升級方式", "消費掃發票、到館簽到、完成任務")],
           "讓會員知道「下一步在哪」，比給更多點數更有用",
           keys2=["levelup"])

# ---------------------------------------------------------------- 5 遊戲化
d.divider("遊戲化設計", "每天、每週、每季，\n都有一個回來的理由", key="遊戲")
s = d.info("三層迴圈：每天簽到、每週任務、每季祭典", label="Game Loop",
           banner="小獎勵天天給、大獎勵跟著檔期走：把 Bon Odori、ACG Matsuri 變成 App 裡的「季賽」")
d.flow(s, [("DAILY", "#1E9C9A", "簽到 Streak", "每天 +10 pts\n連續 7 天送扭蛋\n斷了可用點數補簽"),
           ("WEEKLY", BLUE, "Quest 任務", "Makan Quest：試 2 家新店\nSquad Quest：帶 1 個 kawan\n完成給 XP"),
           ("SEASONAL", PINK, "Matsuri Pass", "Bon Odori・ACG Matsuri・\nRaya・CNY・Deepavali\n館內集章 Stamp Rally"),
           ("COLLECT", ORANGE, "LaLa Capsule", "24 隻一系列\n稀有款可跟朋友交換\n集滿換實體公仔")])

phone_demo("Stamp Rally：把館內動線，變成一張尋寶地圖", "Quest", "quest",
           [("樓層地圖集章", "L4 Garden Dining、L2 ACG Base、L1 Doko Koko"),
            ("離你 40m", "定位提示下一站，帶動跨樓層人流"),
            ("集滿換限定", "5 章換 Matsuri 限定扭蛋＋300 XP")],
           "集章是日本商場最熟悉的玩法，搬進 App 就能量化每一層的人流",
           photo=A + "app/acg_event.jpg")

phone_demo("LaLa Capsule：每天一抽，抽到的是「想收集」的心", "Capsule", "capsule",
           [("每日免費一抽", "簽到送、等級越高次數越多"),
            ("24 隻一系列", "Durian-chan、Ramen-kun…原創角色，可做成實體公仔"),
            ("Trade with kawan", "重複的可以跟朋友交換，自帶社群擴散")],
           "扭蛋把「點數」變成「收藏」：數位收集，實體兌換，再回到館內",
           photo=A + "mock_friends_capsule.jpg")

# ---------------------------------------------------------------- 6 AI
d.divider("AI 功能", "拍發票、問管家、看推薦：\n三個 AI 各解一個麻煩", key="AI")
s = d.info("三個 AI 功能：讓集點從「麻煩」變成「順手」", label="AI Features",
           banner="5% 集點率的最大原因是麻煩：AI 把每一步縮短到一秒")
d.columns(s, [("AI Receipt Scan", ORANGE, "拍一張，1 秒入點",
               "AI 讀店名、金額、時間\n自動對應店家與任務\n防重複、防竄改"),
              ("Ask LaLa", BLUE, "你的 AI 逛街管家",
               "英文／馬來文／中文都能問\n找吃、找店、找停車出口\n幫你排一天行程"),
              ("For You", MINT, "每個人的首頁不一樣",
               "依等級、喜好、歷史推薦\nACG 粉看到聯名咖啡\n家庭客看到親子活動")])

phone_demo("AI 發票掃描：吃完拉麵，順手一拍就入點", "AI Receipt Scan", "scan",
           [("AI 即時辨識", "店名、金額、時間自動抓，1.2 秒完成"),
            ("等級倍率自動算", "Explorer 1.2x：RM28.90 → +35 pts"),
            ("順便推進任務", "Makan Quest 完成＋提示寫 Real Talk")],
           "拍發票是唯一不用改店家 POS 就能把 95% 消費記回來的方法",
           photo=A + "mock_ramen_scan.jpg")

phone_demo("Ask LaLa：像問朋友一樣問商場", "Ask LaLa", "ask",
           [("用馬來西亞英語聊", "「Jom makan! Any halal ramen under RM15?」"),
            ("答案帶你過去", "附 Buzz 評分、步行時間，按 Go 導航"),
            ("順便推任務", "提醒掃發票完成 Makan Quest")],
           "Ask LaLa 背後是 LLM＋館內店家資料＋Pandora 口碑：問得到，也走得到")

# ---------------------------------------------------------------- 7 口碑
d.divider("口碑專區 LaLa Buzz", "網路上的好評，搬進 App；\n館內的真心話，留在 App", key="口碑")
s = d.info("LaLa Buzz：Pandora 找好評、AI 寫摘要、顧客寫 Real Talk", label="How it works",
           banner="不用店家自己寫廣告：網友已經在幫他們說好話，我們只是把它放到對的地方")
d.flow(s, [("① 爬取", "#15325E", "Pandora", "每日爬 IG、Threads\n公開貼文\n依店家歸類"),
           ("② 篩選", BLUE, "AI 好評判定", "正向情緒、與店家相關\n去除業配、廣告\n保留原文連結"),
           ("③ 呈現", ORANGE, "Buzz Score", "AI 摘要「大家愛什麼」\n熱門標籤、趨勢 ▲\n一鍵導航、領券"),
           ("④ 回寫", MINT, "Real Talk", "已購認證才能寫\n寫一篇 +20 pts\n回到 Buzz Score")])

s = d.info("Pandora 實測：馬來西亞網友，已經在幫店家寫好評", label="Pandora 實測",
           banner="這些是真實貼文：LaLa Buzz 上線第一天，就有內容可以放",
           source="Data source: Pandora 實測 2025/11/06–2026/11/05，馬來西亞地區；括號為提及篇數")
d.bars(s, [("ACG Base", 223), ("KLP48 劇場", 99), ("Doko Koko Café", 98), ("Pokémon", 71),
           ("Animate", 57), ("MINISO", 42), ("Akiba Ramen", 12)], 0.6, 1.35, 6.4, row_h=0.6, hot={2, 4, 6},
       name_w=1.9)
d.quote(s, 7.3, 1.35, 5.4, 1.4, "「Found a hidden ramen gem in KL 🍜」", "@yuumi_kato｜Akiba Ramen｜IG 2026/08")
d.quote(s, 7.3, 2.9, 5.4, 1.4, "「The food was so well themed!」", "@fayejimeno｜Doko Koko Café｜IG 2026/08")
d.quote(s, 7.3, 4.45, 5.4, 1.4, "「Play area is RIGHT by the tables」", "@mymamapicks｜親子咖啡｜IG 2026/09")

phone_demo("Buzz 首頁：大家最近在愛什麼，一頁看完", "LaLa Buzz", "buzz",
           [("Buzz of the Week", "本週聲量最高的店或活動"),
            ("分類切換", "Makan、ACG、Outlet、Family"),
            ("Buzz Score＋趨勢", "★4.8、128 篇、▲32%：好不好、紅不紅都看得到")],
           "顧客進館前先滑 Buzz，就知道今天要去哪一家", photo=A + "mock_hero3.jpg")

phone_demo("店家頁：AI 摘要＋網友原話，決定要不要過去", "LaLa Buzz", "brand",
           [("92% love it", "AI 判定的好評比例與篇數"),
            ("大家愛什麼", "Creamy paitan、Value for money…自動生成標籤"),
            ("Web Buzz／Real Talk", "網路原文附來源；館內已購者的真心話"),
            ("Take me there", "一鍵導航，或寫 Real Talk 拿 +20 pts")],
           "從「看到好評」到「走進店裡」，只差一個按鈕", keys2=["realtalk"])

s = d.info("真實性三道關：只放好評，但每一則都是真的", label="Trust & Safety",
           banner="好評專區不是洗評價：來源公開、已購認證、AI＋人工雙審")
d.columns(s, [("關卡 1", "#15325E", "來源公開", "Web Buzz 每一則都附\n原貼文連結與日期\n業配標記自動排除"),
              ("關卡 2", ORANGE, "已購認證", "Real Talk 必須先掃發票\nVerified purchase ✓\n一張發票只能寫一次"),
              ("關卡 3", MINT, "AI＋人工審核", "AI 先擋不當內容、個資\n商場小編每日複核\n店家可申請回覆")])

# ---------------------------------------------------------------- 8 落地
d.divider("落地與 KPI", "Activation、時程、分工、KPI", key="落地")
d.social_idea("A", "LaLaport BBCC × ACG", "ACG Season Pass：把 ACG Matsuri 變成 App 裡的季賽",
              "每季一張 Season Pass：集章、聯名咖啡任務、KLP48 劇場打卡；完成可換限定扭蛋與活動優先入場。"
              "（AI 示意圖）", A + "app/acg_event.jpg")
d.social_idea("B", "MOP KLIA Sepang × 旅客", "Transit Quest：轉機前 3 小時，在 Outlet 升一級",
              "接 Batik Air 合作與 Tourist Privilege Pass：旅客下載即升 Explorer 試用 30 天、"
              "KLIA 轉乘專屬任務與退稅提醒，讓一次性的旅客也留下會員資料。（AI 示意圖）", A + "klia_outlet.jpg")

s = d.info("先上最痛的三件事，再把遊戲一層層加上去", label="時程",
           banner="Phase 0 先解決「集點麻煩」，Phase 1 再讓人「想玩」")
d.timeline(s, 1.8, ["2027/01", "2027/04", "2027/07", "2027/10", "2028/01"],
           [("P0｜分級＋AI 發票＋Buzz 唯讀", 0, 0.33),
            ("P1｜Quest・Capsule・Ask LaLa", 0.25, 0.6),
            ("P2｜Matsuri Pass・Real Talk", 0.5, 0.85),
            ("P3｜KLIA Transit・For You", 0.72, 1.0)])
d.table(s, ["", "三井 Mitsui Shopping Park", "騰雲 TurnCloud"],
        [["內容", "等級權益、活動檔期、店家合作", "UI/UX 設計、Prototype、文案在地化"],
         ["系統", "既有 App／會員資料提供", "分級引擎、AI 發票、Ask LaLa、遊戲模組"],
         ["數據", "門檻與權益決策", "Pandora 口碑爬取、Buzz Score、CRM 儀表板"]],
        y=3.85, col_w=[1.0, 4.0, 4.0], size=12.5, row_h=0.5)

s = d.info("KPI：一年內，把集點率從 5% 拉到 20%", label="KPI",
           banner="每一層都看得到數字：Phase 0 的數據，就是 Phase 1 權益調整的依據",
           source="目標值為試算示意，正式目標依三井現有會員數與 App 數據校正")
d.table(s, ["指標", "現況", "Phase 0（3 個月）", "上線 12 個月（示意）"],
        [["App 集點會員比例", "5%", "10%", "20%"],
         ["MAU／會員數", "—", "20%", "35%"],
         ["每月發票登錄筆數", "—", "20,000", "60,000"],
         ["平均月造訪次數", "—", "+0.2 次", "+0.6 次"],
         ["Real Talk 分享則數／月", "0", "500", "3,000"],
         ["Explorer 以上會員占比", "—", "15%", "30%"]],
        col_w=[3.0, 1.6, 2.4, 2.6], size=14, row_h=0.6, hot_row=0)

d.closing("每一次來，都在升級。",
          "Next Step\n① 11 月：確認四級門檻與權益方向\n② 12 月：Prototype 使用者測試（20 位 18–34 歲會員）\n"
          "③ 2027/01：Phase 0 開發啟動（分級＋AI 發票＋Buzz）",
          logos=[TC])
d.save("MSP_App3.0_LaLaQuest_提案.pptx")
