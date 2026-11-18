"""Core extras (v7): Mission Wall, smart-push journey, receipt submission. Shared by EN + ZH builds."""
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

NAVY, GOLD, GOLD_L, SOFT = "#13294B", "#B8975A", "#E8D6AE", "#F3F1EC"


def add_core_extra(d, lang, phone, A, PAGES):
    T = (lambda en, zh: en) if lang == "en" else (lambda en, zh: zh)
    C = lambda s, x, y, w, h, t, sz, **k: d.tx(s, x, y, w, h, t, sz, align=PP_ALIGN.CENTER, **k)  # noqa: E731

    def still(s, key, x, y, h, tag=None):
        w = h * 390 / 844
        d.round(s, x - 0.06, y - 0.06, w + 0.12, h + 0.12, "#0E1A33", 0.12)
        s.shapes.add_picture(A + f"poster_r/{key}.jpg", *[int(v * 914400) for v in (x, y, w, h)])
        if tag:
            d.ai_tag(s, x + 0.06, y + h + 0.12, tag)
        return w

    # ------------------------------------------------------------ Mission Wall
    s = d.info(T("Mission Wall: every member sees what to do next, and what they get",
                 "任務牆：每位會員都看得到下一步要做什麼、能拿到什麼"),
               label=T("Core | Mission Wall", "核心｜任務牆"),
               banner=T("One campaign, a personal to-do list for every member: come back, spend a little more, level up",
                        "同一檔活動，變成每位會員自己的待辦清單：再來一次、多花一點、升一級"),
               source=T("Mission logic follows the TurnCloud CRM stack (TCRM rules, TGalaxy segments, MA push). Amounts and rewards are illustrative.",
                        "任務邏輯沿用騰雲 CRM（TCRM 規則、TGalaxy 分群、MA 推播）；金額與獎勵皆為示意。"))
    x = 0.9
    w = phone(s, "missions", x, 1.3, 4.35)
    x += w + 0.45
    still(s, "j5", x, 1.3, 4.35, T("UI mock-up", "UI 示意"))
    d.tx(s, 7.15, 1.35, 5.6, 0.35, T("What members see", "會員看到什麼"), 13, color="frame", bold=True)
    pts = [(T("01  Progress at a glance", "01  進度一目了然"), T("Warm-Up, Main Event, Comeback: done, in progress or locked", "暖身、主活動、回訪：完成、進行中、未開放一眼看懂")),
           (T("02  Spend gap + picks", "02  差額＋推薦店家"), T("\"RM80 to go\", with dining picks that close the gap", "「還差 RM80」，附上剛好補齊差額的餐飲推薦")),
           (T("03  Claim in one tap", "03  一鍵領獎"), T("Receipt approved → RM300 reached → RM30 voucher + 300 pts", "發票審核通過 → 達到 RM300 → RM30 券＋300 點")),
           (T("04  Next tier, always in sight", "04  下一級永遠看得到"), T("Senpai is RM620 away: the next goal is never hidden", "距離 Senpai 只差 RM620：下一個目標不會被藏起來")),
           (T("05  Same tab for every campaign", "05  每檔活動同一個入口"), T("Anniversary, Anime, Family, Japanese Style: the Missions tab replaces Bus in the nav bar", "週年慶、動漫、親子、日式：任務分頁取代底部選單的 Bus"))]
    d.callouts(s, 7.15, 1.85, 5.6, pts, gap=0.86)
    PAGES["missions"] = d.n

    # ------------------------------------------------------------ Smart-push journey
    s = d.info(T("Smart push walks each member through the campaign, from invite to next tier",
                 "智慧推播：從邀請到升級，一路陪會員走完整檔活動"),
               label=T("Core | Smart Push Journey", "核心｜推播旅程"),
               banner=T("Every push answers one question: what's in it for me, how far am I, what do I do next",
                        "每一則推播只回答一件事：我能拿到什麼、還差多少、下一步做什麼"),
               source=T("In-app push + notification centre; segments from TGalaxy, journeys in MA, eligibility in TCRM, purchases from POS. Illustrative data.",
                        "App 推播＋通知中心；分群 TGalaxy、旅程 MA、資格判定 TCRM、消費資料 POS。數據為示意。"))
    phases = [(T("Before the campaign", "活動前"), 0, 2), (T("During the campaign", "活動中"), 2, 4), (T("After the campaign", "活動後"), 4, 6)]
    pw = 12.15 / 6
    for nm, a, b in phases:
        d.round(s, 0.6 + a * pw + 0.04, 1.15, (b - a) * pw - 0.08, 0.3, "#E2F4F9", 0.3)
        C(s, 0.6 + a * pw, 1.19, (b - a) * pw, 0.24, nm, 10, bold=True, color="#0E7C9A")
    steps = [("j1", T("Get a VIP invite", "收到 VIP 邀請"), T("Push: Fiesta invite for Explorers", "推播：Explorer 專屬週年慶邀請"), "TGalaxy · MA"),
             ("j2", T("Open the Mission Wall", "打開任務牆"), T("Tasks, spend target and reward", "任務、消費門檻與獎勵"), "APP · MA"),
             ("j3", T("\"RM80 to go\" nudge", "「還差 RM80」提醒"), T("Push with dining picks to close the gap", "推播附上補齊差額的餐飲推薦"), "TGalaxy · MA"),
             ("j4", T("Shop with member QR", "結帳出示會員 QR"), T("The purchase counts toward the mission", "這筆消費自動計入任務"), "POS · APP"),
             ("j5", T("Claim the reward", "領取獎勵"), T("RM300 reached: RM30 + 300 pts", "達到 RM300：RM30 券＋300 點"), "TCRM · APP"),
             ("j6", T("Next-tier nudge", "升級提醒"), T("Senpai is RM620 away", "距離 Senpai 只差 RM620"), "TCRM · MA")]
    ph = 3.05
    phw = ph * 390 / 844
    d.rect(s, 0.6 + pw / 2, 4.86, 12.15 - pw, 0.012, "#9FD3E2")
    for i, (k, ttl, ds, sysn) in enumerate(steps):
        cx = 0.6 + i * pw + pw / 2
        still(s, k, cx - phw / 2, 1.62, ph)
        d.rect(s, cx - 0.07, 4.8, 0.14, 0.14, "#1F6FB8", MSO_SHAPE.OVAL)
        C(s, cx - pw / 2, 4.98, pw, 0.28, ttl, 11.5, bold=True, color=NAVY)
        C(s, cx - pw / 2 + 0.05, 5.25, pw - 0.1, 0.4, ds, 9, color="mid", spacing=1.05)
        d.round(s, cx - 0.62, 5.72, 1.24, 0.24, SOFT, 0.5)
        C(s, cx - 0.62, 5.75, 1.24, 0.2, sysn, 8, bold=True, color="#0E7C9A")
    PAGES["push"] = d.n

    # ------------------------------------------------------------ Receipt submission
    s = d.info(T("Submit Receipt: snap it, submit it, see when the points land",
                 "發票登錄：拍照、送出、隨時看到點數什麼時候入帳"),
               label=T("Core | Receipts", "核心｜發票登錄"),
               banner=T("Receipts capture spend without touching every tenant's POS. Core makes it easy; the AI add-on makes it instant",
                        "發票是不改店家 POS 也能記到消費的方法：核心版讓它好用，AI 加購讓它即時"),
               source=T("Flow benchmarked on a KL mall loyalty app (Pavilion Bukit Jalil \"Submit Spend\", Nov 2026). Review time and amounts are illustrative.",
                        "流程參考吉隆坡商場會員 App（Pavilion Bukit Jalil「Submit Spend」，2026/11）；審核時間與金額為示意。"))
    x = 0.9
    w = phone(s, "receipt", x, 1.3, 4.35)
    x += w + 0.45
    still(s, "rh_ok", x, 1.3, 4.35, T("UI mock-up", "UI 示意"))
    d.tx(s, 7.15, 1.35, 5.6, 0.35, T("The flow", "流程"), 13, color="frame", bold=True)
    pts = [(T("1  Count it toward a mission", "1  先選要計入的活動"), T("Pick the campaign, or skip for points only", "選擇週年慶任務，或只累積點數")),
           (T("2  Quick check", "2  快速確認"), T("One receipt, LaLaport BBCC store, last 7 days", "一張發票、LaLaport BBCC 店家、7 天內")),
           (T("3  Snap every page", "3  每一頁都拍"), T("Auto-capture scanner; add pages, retake or delete", "自動對焦掃描；可加頁、重拍、刪除")),
           (T("4  Track the status", "4  追蹤審核狀態"), T("Pending → approved (+pts) or rejected, with the reason", "審核中 → 通過（入點、計入任務）或退件並說明原因")),
           (T("AI add-on: skip the wait", "AI 加購：不用等"), T("AI Receipt Scan reads it in 1 second, points land instantly", "AI 發票掃描 1 秒讀完，點數立刻入帳"))]
    d.callouts(s, 7.15, 1.85, 5.6, pts, gap=0.86)
    PAGES["receipt"] = d.n
