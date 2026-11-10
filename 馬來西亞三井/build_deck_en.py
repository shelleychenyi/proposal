"""English version of the MSP App 3.0 / LaLa Quest proposal (same structure & slide numbers as build_deck.py)."""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/shelley-deck/scripts"))
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from shelley_deck import Deck, W, H  # noqa: E402

os.chdir(os.path.dirname(os.path.abspath(__file__)))
A = "assets/"
LALA = A + "logo/logo@3x_org.png"
MOP = A + "logo/logo@3x_org_mitsui.png"
TC = "brand/turncloud.png"
BLUE, ORANGE, MINT, PINK, CORAL = "#2B67B0", "#F39A1E", "#22C2A0", "#FF6FA3", "#FF6F61"
IDEA_VIDEO = A + "video/idea_bg.mp4" if os.path.exists(A + "video/idea_bg.mp4") else None
AI = "AI mock-up"


class DeckEN(Deck):
    def toc(self, sections):
        self.sections = list(sections)
        s = self._new()
        self.tx(s, 1.11, 0.27, 6, 0.6, "Contents", 24, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        per_col = (len(sections) + 1) // 2
        for i, (t, _) in enumerate(sections):
            x, y = 0.95 + (i // per_col) * 6.1, 1.55 + (i % per_col) * 1.2
            self.tx(s, x, y, 0.8, 0.6, f"{i + 1}.", 26, color="cyan", bold=True, font=self.num_font)
            self.tx(s, x + 0.7, y + 0.05, 5.2, 0.6, t, 22, bold=True)
        self.foot(s)
        return s

    def ai_tag(self, s, x, y, text=AI):
        return super().ai_tag(s, x, y, text)


META = {"video": {}, "special": {}}
d = DeckEN(theme={"frame": BLUE, "accent": ORANGE}, footer_logos=[TC])


def phone(s, key, x, y, h, video=True, tag=True):
    w = h * 390 / 844
    d.round(s, x - 0.07, y - 0.07, w + 0.14, h + 0.14, "#0E1A33", 0.12)
    poster = A + f"poster_r/{key}.jpg"
    vid = A + f"video_r/{key}.mp4" if video else None
    d.movie(s, vid, poster, x, y, w, h)
    if video:
        META["video"].setdefault(d.n, []).append([key, x, y, w, h])
    if tag:
        d.ai_tag(s, x + 0.08, y + h + 0.14, "Prototype recording" if video else "UI mock-up")
    return w


def ugc(s, key, x, y, w, h, cap=None):
    px, py, pw, ph = d.fit(s, A + f"ugc/{key}_c.png", x, y, w, h - (0.3 if cap else 0), border=True)
    if cap:
        d.tx(s, x, py + ph + 0.06, w, 0.25, cap, 9, color="grey", align=PP_ALIGN.CENTER)
    return px, py, pw, ph


def bench(title, brand, shots, good, borrow, banner):
    s = d.info(title, label="Benchmark | " + brand, banner=banner,
               source="Data source: official App Store screenshots (Nov 2026)")
    for i, f in enumerate(shots):
        d.fit(s, A + f"bench/{f}", 0.6 + i * 2.32, 1.3, 2.2, 4.75, border=True)
    d.tx(s, 7.75, 1.3, 5.0, 0.35, "What they do well", 13, color="frame", bold=True)
    d.callouts(s, 7.75, 1.75, 5.0, good, gap=0.92)
    yb = 1.75 + 0.92 * len(good) + 0.05
    d.rect(s, 7.75, yb, 5.0, 0.02, "line")
    d.tx(s, 7.75, yb + 0.15, 5.0, 0.35, "What LaLa Quest borrows", 13, color=ORANGE, bold=True)
    d.tx(s, 7.75, yb + 0.55, 5.0, 1.3, borrow, 12, bold=True, spacing=1.45)
    return s


def phone_demo(title, label, key, points, banner, photo=None, keys2=None, source=None, clip=None):
    s = d.info(title, label=label, banner=banner, source=source)
    x = 0.9
    w = phone(s, key, x, 1.3, 4.55)
    x += w + 0.45
    for k in keys2 or []:
        w2 = phone(s, k, x, 1.3, 4.55)
        x += w2 + 0.45
    if clip:
        pw = 9.0 - x
        ph = pw * 9 / 16
        py = 1.3 + (4.55 - ph) / 2
        d.movie(s, A + f"video_r/{clip}.mp4", A + f"poster_r/{clip}.jpg", x, py, pw, ph)
        META["video"].setdefault(d.n, []).append([clip, x, py, pw, ph])
        d.ai_tag(s, x, py + ph + 0.12, "AI mock-up video")
    elif photo:
        pw = 9.0 - x
        px, py, pw, ph = d.fit(s, photo, x, 1.3, pw, 4.55)
        d.ai_tag(s, px + 0.1, py + 0.1)
    d.tx(s, 9.35, 1.35, 3.4, 0.35, "Key features", 13, color="frame", bold=True)
    gap = min(1.15, 4.6 / max(1, len(points)))
    d.callouts(s, 9.35, 1.85, 3.4, points, gap=gap)
    return s


# ---------------------------------------------------------------- Cover
d.cover("MSP App 3.0\nRenewal Proposal.", "LaLa Quest | Every visit levels you up.", "Nov 2026",
        company="TURN CLOUD TECHNOLOGY SERVICE INC.", logos=[LALA, MOP], image=A + "mock_hero3.jpg")
d.toc([("Insights", "機會"), ("Benchmarks", "標竿"), ("App 3.0 Overview", "全貌"), ("Member Tiers", "分級"),
       ("Gamification", "遊戲"), ("AI Features", "AI"), ("LaLa Buzz", "口碑"), ("Rollout & KPI", "落地")])

# ---------------------------------------------------------------- 1 Insights
PD = A + "pandora/"
PSRC = ("Data source: Pandora social listening report \"Lalaport&BBCC\", 3 May–31 Oct 2026, N=3,696 "
        "(Instagram, Threads). Scan the QR code for the full report.")


def qr_pair(s, x, y, size=1.05, gap=0.35, label=True):
    for i, (k, nm) in enumerate([("volume", "Volume Report"), ("insight", "Insight Report")]):
        xx = x + i * (size + gap)
        d.fit(s, PD + f"qr_{k}.png", xx, y, size, size, border=True)
        if label:
            d.tx(s, xx - 0.2, y + size + 0.04, size + 0.4, 0.25, nm, 9, color="mid", bold=True,
                 align=PP_ALIGN.CENTER)


d.divider("Insights", "People love LaLaport.\nThe app just hasn't caught that love yet.", key="機會")

s = d.info("At a glance: turn shopping into a game you level up in", label="Executive Summary",
           banner="Not another voucher portal: give young people a reason to WANT to open the app")
d.columns(s, [("Insight", "#8A94A6", "Huge buzz, app misses it",
               "3,696 posts, 90.7% positive\nYoung fans of ACG & K-pop\n"
               "Only 5% earn points in-app\nParking fix hidden in News"),
              ("Solution", BLUE, "LaLa Quest: four pillars",
               "Level Up: 4 tiers + monsters\nPlay: check-ins, quests\n"
               "Ask: AI concierge + receipts\nBuzz: Pandora + Real Talk"),
              ("Return", ORANGE, "Point earning 5% → 20%",
               "Every receipt back to CRM\nOccasional → monthly visits\nNew traffic for tenants\n"
               "One ID across both malls")])

s = d.info("Insight 1  People love LaLaport: 3,696 posts, 9 in 10 positive", label="Pandora Volume Report",
           banner="The love is there. What's missing is an app that turns it into membership value", source=PSRC)
d.fit(s, PD + "v_stats.png", 0.6, 1.28, 6.3, 2.0, border=True)
d.fit(s, PD + "i_sentdist.png", 0.6, 3.38, 6.3, 2.7, border=True)
d.tx(s, 7.35, 1.3, 5.4, 0.3, "What Pandora tells us", 13, color="frame", bold=True)
for i, (big, lab, desc) in enumerate([("90.7%", "Positive sentiment", "Very Positive 28.1% + Positive 62.6%; only 1.2% negative"),
                                      ("5.1M", "Total engagement", "1.65M likes, 20K comments; 1.2M+ in August alone"),
                                      ("5%", "Members earning in-app", "The buzz lives on social, not in the app (client data)")]):
    y = 1.75 + i * 0.95
    d.tx(s, 7.35, y, 1.9, 0.6, big, 28, color=ORANGE if i == 2 else "frame", bold=True)
    d.tx(s, 9.3, y + 0.02, 3.5, 0.3, lab, 13, bold=True)
    d.tx(s, 9.3, y + 0.33, 3.5, 0.5, desc, 10.5, color="mid")
d.rect(s, 7.35, 4.65, 5.4, 0.02, "line")
d.tx(s, 7.35, 4.8, 2.2, 1.0, "Scan for the\nfull Pandora\nreports →", 12.5, bold=True, color="frame", spacing=1.35)
qr_pair(s, 9.35, 4.75, size=1.0, gap=0.4)

s = d.info("Insight 2  Young crowds come for ACG, K-pop and movies", label="Pandora Insight Report",
           banner="Gamification and characters speak to this crowd: ACG Base, Photoism, GSC fan events, Bon Odori",
           source=PSRC)
d.fit(s, PD + "i_keyword.png", 0.6, 1.28, 6.2, 3.08, border=True)
d.callouts(s, 0.75, 4.55, 6.0, [("ACG home ground", "ACG Base, Ani-One POP, Doko Koko collab café, Anime Fest"),
                                ("K-pop + movies", "Photoism idol frames, GSC Chiikawa / Crayon Shin-chan fan events")],
           gap=0.72)
d.fit(s, PD + "i_positive.png", 7.05, 1.28, 5.7, 3.08, border=True)
d.tx(s, 7.05, 4.5, 4.4, 1.4, "Pandora AI positive summary:\n\"LaLaport BBCC is KL's pop-culture hub.\"\n"
     "These fans collect, check in and chase limited drops: the ideal users for a gamified membership.",
     11.5, bold=True, spacing=1.45)
d.fit(s, PD + "qr_insight.png", 11.65, 4.5, 0.95, 0.95, border=True)
d.tx(s, 11.4, 5.47, 1.45, 0.25, "Insight Report", 9, color="mid", bold=True, align=PP_ALIGN.CENTER)

s = d.info("Insight 3  Complaints are about parking: the app has a fix, hidden in News",
           label="Pandora Insight | Current App",
           banner="Make free parking a tier perk and put the member QR on the home screen: value from day one",
           source=PSRC + " App screenshots, Nov 2026.")
d.fit(s, PD + "i_negative.png", 0.6, 1.28, 6.1, 3.28, border=True)
d.tx(s, 0.75, 4.72, 5.9, 1.3, "Pandora negative summary: parking is pricey, car park entrances get closed,\n"
     "weak signal makes QR payment hard.\n→ 3.0: parking hours grow with your tier (3H → all day);\n"
     "member QR right on the home screen.", 11.5, bold=True, spacing=1.45)
d.fit(s, A + "current_app.jpg", 7.0, 1.28, 5.75, 1.78, border=True)
d.ai_tag(s, 7.1, 1.36, "Current app screenshots")
d.callouts(s, 7.0, 3.3, 5.75, [("Home = ad wall", "Banners, News and Vouchers all push; there's no \"me\""),
                               ("Free parking buried in News", "MSP Member Free 3H Parking is just one post"),
                               ("One tier, games hidden", "Regular Member only; Spin & Win is two levels deep")],
           gap=0.9)

d.statement("IDEA", "LaLa Quest\nShop. Play. Level up.",
            "Every visit levels you up.\n"
            "Level Up: Rookie → Explorer → Senpai → Legend\n"
            "Play: check-ins, quests, stamp rallies, capsules\n"
            "Ask: AI concierge + AI receipt scan\n"
            "Buzz: Pandora-picked reviews, one tap to go",
            image=A + ("idea_poster.jpg" if IDEA_VIDEO else "app/acg_event.jpg"), video=IDEA_VIDEO)
META["special"]["idea"] = d.n

# ---------------------------------------------------------------- 2 Benchmarks
d.divider("Benchmarks", "Great member apps make people WANT to open them,\nnot HAVE to.", key="標竿")
s = d.info("Six benchmarks: each turns membership into an identity", label="Benchmark",
           banner="We borrow: visible progress (Starbucks), collecting (USJ / Shopee), answers on tap (Disney)",
           source="Data source: official brand apps and public information; Starbucks Rewards 3-tier model, "
                  "Mar 2026 (Restaurant Dive)")
d.table(s, ["Brand", "What they do", "What LaLa Quest borrows"],
        [["MUJI Passport", "Earn MUJI Miles just for checking in, no purchase needed", "Daily check-in streaks"],
         ["Disney App", "AI itinerary tips; mini-games while you queue", "Ask LaLa plans your day"],
         ["Universal Studios", "Collect keys physically, track score in the app", "In-mall Stamp Rally"],
         ["Starbucks Rewards", "Green / Gold / Reserve: 1x / 1.2x / 1.7x rewards", "4 tiers + point multipliers"],
         ["Shopee", "Coins + daily mini-games, a daily Malaysian habit", "Daily LaLa Capsule draw"],
         ["Sephora", "Beauty Insider tiers + verified member reviews", "LaLa Buzz + Real Talk"]],
        col_w=[1.8, 4.6, 3.2], size=12.5, row_h=0.62)

bench("MUJI: the member card is the home screen; rules in one line", "MUJI",
      ["muji_2.jpg", "muji_3.jpg", "muji_5.jpg"],
      [("Opens on the barcode", "First screen = member card + points"),
       ("Dead-simple rules", "\"¥100 = 1 pt, 1 pt = ¥1\""),
       ("Member Week = festival", "10% off for all members, on a set calendar")],
      "Member card + points on the first screen;\npoint rules in one line of Malaysian English;\n"
      "Bon Odori and Raya as \"Member Weeks\".",
      "MUJI proves it: card on home + simple rules = higher usage")
bench("Disney: the app plans your day; wait times become info", "Disney",
      ["disney_3.jpg", "disney_4.jpg", "disney_5.jpg"],
      [("Live wait times", "Queue length and next show time at a glance"),
       ("My Plans itinerary", "Bookings, dining and shows in one day plan"),
       ("Interactive map", "Tap rides, restaurants and toilets on the map")],
      "Ask LaLa: \"Plan my Saturday\";\nqueue times for hot restaurants + collab café booking;\n"
      "floor map linked to the Stamp Rally.",
      "Disney turns a visit into \"my plan\": LaLa Quest does the same with AI")
bench("USJ: the map is the hero; timed passes build anticipation", "Universal Studios Japan",
      ["usj_3.jpg", "usj_4.jpg", "usj_5.jpg"],
      [("Wait-time ranking", "Sorted by minutes, quickest ride on top"),
       ("Full park map", "Rides pinned on an illustrated map"),
       ("e-Pass / lottery", "Enter hot zones by app draw, builds hype")],
      "ACG Matsuri, KLP48 Theatre, collab cafés:\ndraw \"priority entry\" passes in the app;\n"
      "Senpai and above get double odds.",
      "USJ proves it: limited + lottery = people open the app every day")
bench("Starbucks: a clear reward ladder, a surprise at every scan", "Starbucks Rewards",
      ["starbucks_2.jpg", "starbucks_3.jpg", "starbucks_5.jpg"],
      [("Reward ladder", "25★, 100★, 200★… each step is clear"),
       ("Scan to pay & earn", "Paying = earning, in one action"),
       ("\"Yay!\" animation", "A celebration after checkout")],
      "Capsules, parking, collab merch as a reward ladder;\n+35 pts animation after AI receipt scan;\n"
      "full-screen Level Up celebration.",
      "Starbucks went back to 3 tiers in 2026: tiers + ladder is proven design")
bench("Shopee: the \"open it every day\" rhythm Malaysians know", "Shopee MY",
      ["shopee_1.jpg", "shopee_4.jpg", "shopee_5.jpg"],
      [("Strong campaign feel", "11.11, Payday Sale, countdowns, bold visuals"),
       ("ShopeeVIP", "Paid membership: free shipping, deals, vouchers"),
       ("Live + big prizes", "RM11 Million Vouchers, celebrity live streams")],
      "Ride the familiar Payday and 11.11 rhythm;\nMOP KLIA \"Payday Reward\" as a Quest;\n"
      "daily Capsule = LaLa's Shopee Coins.",
      "No need to educate the market: young Malaysians already open apps daily to claim stuff")
bench("Sephora: tier = discount, and AI picks your gifts", "Sephora",
      ["sephora_1.jpg", "sephora_4.jpg", "sephora_5.jpg"],
      [("Tiers map to discounts", "Insider 10% / VIB 15% / Rouge 20%"),
       ("Shareable Wish List", "Share your saved list with friends"),
       ("AI Beauty Chat", "Ask \"gifts under $200\", get picks")],
      "Rookie → Legend perks in one picture;\nAsk LaLa recommends shops and gifts by chat;\n"
      "Real Talk + Buzz borrow Sephora's review culture.",
      "Sephora is the best all-in-one model: tiers + AI + reviews")

# ---------------------------------------------------------------- 3 Overview
d.divider("App 3.0", "One main colour, four pillars:\na younger, more premium LaLaport.", key="全貌")
phone_demo("Home: open it and see my card, my QR and my monster", "Home", "home",
           [("Card = QR + tier", "At checkout, staff scan the QR on home (video, right)"),
            ("My monster", "Tier character lives on the card; new outfit each level"),
            ("Progress & perks", "616 pts to Senpai; 4H free parking, 1.2x points"),
            ("Check-in + shortcuts", "5-day streak; Scan Receipt, Ask LaLa, Capsule, Parking")],
           "Home moves from \"what the mall is pushing\" to \"who I am and what I get today\"", clip="checkout")

s = d.info("Four pillars of LaLa Quest: Level Up, Play, Ask, Buzz", label="App Structure",
           banner="All four pillars lead to one thing: every visit and every purchase counts towards membership")
d.cover_pic(s, A + "world/sky.jpg", 0.54, 1.08, W - 1.08, 5.3)
ISL = [("levelup", "#1E9C9A", "Level Up Island", "4 tiers: parking, multipliers, capsules grow"),
       ("play", PINK, "Play Island", "Check-in · Quests · Stamps · LaLa Capsule"),
       ("ask", BLUE, "Ask Island", "AI receipt scan · Ask LaLa · For You"),
       ("buzz", ORANGE, "Buzz Island", "Pandora reviews + Real Talk")]
for i, (k, col, name, desc) in enumerate(ISL):
    cx = 0.75 + i * 3.02
    yoff = [0.0, 0.35, 0.0, 0.35][i]
    d.fit(s, A + f"world/{k}_s.png", cx, 1.2 + yoff, 2.85, 2.95)
    d.round(s, cx + 0.2, 4.35 + yoff * 0.5, 2.45, 0.42, col, 0.5)
    d.tx(s, cx + 0.2, 4.41 + yoff * 0.5, 2.45, 0.3, name, 14, color="white", bold=True, align=PP_ALIGN.CENTER)
    d.round(s, cx + 0.05, 4.85 + yoff * 0.5, 2.75, 0.62, "white", 0.25)
    d.tx(s, cx + 0.15, 4.95 + yoff * 0.5, 2.55, 0.5, desc, 10.5, color="ink", bold=True, align=PP_ALIGN.CENTER)
d.ai_tag(s, 0.7, 1.2, "AI mock-up | interactive in web version")
META["special"]["islands"] = d.n

s = d.info("Visual: one main colour and a touch of champagne gold", label="Design System",
           banner="Clean like the official site: midnight navy leads, gold only for tiers and highlights")
sw = [("#13294B", "Midnight Navy", "Main colour · cards · nav"), ("#B8975A", "Champagne Gold", "Tiers · highlights · pts"),
      ("#F6F3EE", "Ivory", "Background · white space"), ("#E6E0D6", "Pearl", "Lines · dividers"),
      ("#1A1F2B", "Ink", "Text")]
for i, (c, n, use) in enumerate(sw):
    x = 0.7 + i * 1.62
    d.round(s, x, 1.4, 1.45, 1.1, c, 0.12)
    d.tx(s, x, 2.6, 1.5, 0.3, n, 11.5, bold=True)
    d.tx(s, x, 2.88, 1.55, 0.3, c + "\n" + use, 10, color="mid", spacing=1.3)
d.logo(s, LALA, 0.7, 3.85, 0.55)
d.logo(s, MOP, 3.3, 3.88, 0.5)
d.tx(s, 0.7, 4.65, 7.6, 1.2, "Fonts: Cormorant Garamond (headlines, luxury serif) + Plus Jakarta Sans (body, readable, "
     "supports Malay)\nLine icons instead of emoji; gold only on tiers, points and the QR frame",
     12, color="mid", spacing=1.55)
d.tx(s, 9.0, 1.35, 3.7, 0.35, "Microcopy: Malaysian English", 13, color="frame", bold=True)
mc = ["Jom! 2 quests waiting for you today.", "Ada! Here are 2 picks on L4", "Ask anything, lah…",
      "Done · Shiok!", "Squad up: bring 1 kawan", "Sedap gila · Worth it"]
for i, t in enumerate(mc):
    d.round(s, 9.0, 1.8 + i * 0.68, 3.7, 0.54, "soft", 0.3)
    d.tx(s, 9.2, 1.92 + i * 0.68, 3.4, 0.3, t, 11.5, bold=True)

# ---------------------------------------------------------------- 4 Tiers
d.divider("Member Tiers", "From Regular Member\nto Rookie, Explorer, Senpai, Legend.", key="分級")
s = d.info("Four tiers, four LaLas: members grow their own character", label="Tier Characters",
           banner="No gold or silver cards: each level brings new gear and a badge worth a screenshot",
           source="Characters are AI concept designs; can extend into stickers, capsule figures and in-mall installations")
TIERS = [("rookie", "#8F8A80", "ROOKIE", "LV1 | On sign-up", "1x points · 3H parking\n1 draw a day"),
         ("explorer", "#13294B", "EXPLORER", "LV2 | RM1,500 or 12 visits", "1.2x points · 4H parking\nBirthday 2x points"),
         ("senpai", "#B8975A", "SENPAI", "LV3 | RM5,000", "1.5x points · 5H parking\nPriority event entry"),
         ("legend", "#0B1A30", "LEGEND", "LV4 | RM12,000", "2x points · all-day parking\nLegend Lounge")]
for i, (k, col, nm, th, perk) in enumerate(TIERS):
    x = 0.72 + i * 3.02
    d.round(s, x, 1.25, 2.8, 4.75, "soft", 0.08)
    d.rect(s, x, 1.25, 2.8, 0.09, col)
    d.fit(s, A + f"world/char_{k}_s.png", x + 0.25, 1.45, 2.3, 2.25)
    d.tx(s, x, 3.8, 2.8, 0.45, nm, 22, color=col, bold=True, align=PP_ALIGN.CENTER, font="Arial Black")
    d.tx(s, x, 4.32, 2.8, 0.3, th, 11.5, color="mid", bold=True, align=PP_ALIGN.CENTER)
    d.tx(s, x + 0.15, 4.8, 2.5, 0.9, perk, 12.5, bold=True, align=PP_ALIGN.CENTER, spacing=1.5)
    if i < 3:
        d.rect(s, x + 2.84, 3.4, 0.14, 0.24, "grey", MSO_SHAPE.RIGHT_ARROW)
d.ai_tag(s, 0.82, 1.38)
META["special"]["tiers"] = d.n

s = d.info("Tier perks: not \"Gold\", but \"Senpai\"", label="Tier Design",
           banner="Anime-style names match LaLaport's Japanese DNA, and give young members an identity to share",
           source="Thresholds and perks are illustrative; final numbers to be set from Mitsui member spending data")
d.table(s, ["Tier", "Threshold (12 months)", "Points", "Free parking", "Capsule", "Signature perks"],
        [["Rookie  LV1", "On sign-up", "1x", "3 hours", "1 / day", "Daily check-in, birthday gift"],
         ["Explorer  LV2", "RM 1,500 or 12 visits", "1.2x", "4 hours", "1 / day", "Birthday 2x points, collab café priority booking"],
         ["Senpai  LV3", "RM 5,000", "1.5x", "5 hours", "2 / day", "Priority entry to Bon Odori & ACG events, exclusive capsules"],
         ["Legend  LV4", "RM 12,000", "2x", "All day", "3 / day", "Legend Lounge, annual Legend Night"]],
        col_w=[1.5, 2.3, 0.9, 1.25, 1.0, 3.55], size=12.5, row_h=0.7, hot_row=2)
d.tx(s, 0.75, 5.2, 12, 0.6, "★ Visits count too: reach Explorer with 12 visits. Students and young workers level up "
     "by coming often, not by spending big.", 13, bold=True, color="frame")

phone_demo("Tier page: four cards stacked, the next level always in sight", "Tier", "tiers",
           [("Stacked cards", "Four tier cards stacked like a wallet; Legend black-gold"),
            ("Perks at a glance", "Multiplier, parking, capsules, event entry"),
            ("Three ways to level up", "Scan receipts, check in at the mall, finish quests")],
           "Showing members \"where's next\" works better than giving more points",
           keys2=["levelup"])

# ---------------------------------------------------------------- 5 Gamification
d.divider("Gamification", "Every day, every week, every season:\na reason to come back.", key="遊戲")
s = d.info("Three loops: daily check-in, weekly quests, seasonal festivals", label="Game Loop",
           banner="Small rewards daily, big rewards by season: Bon Odori and ACG Matsuri become in-app \"seasons\"")
d.flow(s, [("DAILY", "#1E9C9A", "Check-in Streak", "+10 pts every day\n7-day streak = free capsule\nMissed a day? Use points"),
           ("WEEKLY", BLUE, "Quests", "Makan Quest: try 2 new spots\nSquad Quest: bring 1 kawan\nEarn XP"),
           ("SEASONAL", PINK, "Matsuri Pass", "Bon Odori · ACG Matsuri ·\nRaya · CNY · Deepavali\nIn-mall Stamp Rally"),
           ("COLLECT", ORANGE, "LaLa Capsule", "24 characters per series\nTrade rare ones with friends\nComplete a set = real figure")])

phone_demo("Stamp Rally: the mall floor plan becomes a treasure map", "Quest", "quest",
           [("Floor-map stamps", "L4 Garden Dining, L2 ACG Base, L1 Doko Koko"),
            ("40m away", "Location hints guide you to the next stop"),
            ("Collect for exclusives", "5 stamps = Matsuri capsule + 300 XP")],
           "Stamp rallies are a Japanese mall classic; in-app, they measure traffic on every floor",
           photo=A + "app/acg_event.jpg")

phone_demo("LaLa Capsule: one free draw a day, and a reason to collect", "Capsule", "capsule",
           [("One free draw daily", "From check-ins; higher tiers draw more"),
            ("24 per series", "Durian-chan, Ramen-kun… originals, can become figures"),
            ("Trade with kawan", "Swap duplicates with friends: built-in sharing")],
           "Capsules turn points into collectibles: digital collecting, physical rewards, back to the mall",
           photo=A + "mock_friends_capsule.jpg")

# ---------------------------------------------------------------- 6 AI
d.divider("AI Features", "Snap receipts, ask a concierge, get picks:\nthree AIs, three hassles solved.", key="AI")
s = d.info("Three AI features: from \"a hassle\" to \"no-brainer\"", label="AI Features",
           banner="The #1 reason for a 5% earning rate is hassle: AI cuts every step down to one second")
d.columns(s, [("AI Receipt Scan", ORANGE, "One snap, instant points",
               "AI reads shop, amount and time\nMatches tenants and quests\nBlocks duplicates and edits"),
              ("Ask LaLa", BLUE, "Your AI concierge",
               "Ask in English, Malay or Chinese\nFind food, shops, parking exits\nPlans your day for you"),
              ("For You", MINT, "A home made for you",
               "Picks by tier, taste and history\nACG fans see collab cafés\nFamilies see kids' events")])

phone_demo("AI Receipt Scan: finish your ramen, snap, points in", "AI Receipt Scan", "scan",
           [("Instant AI read", "Shop, amount and time captured in 1.2 sec"),
            ("Tier multiplier applied", "Explorer 1.2x: RM28.90 → +35 pts"),
            ("Quests move forward", "Makan Quest done + prompt to write Real Talk")],
           "Receipt scanning captures 95% of spending without touching any tenant's POS",
           photo=A + "mock_ramen_scan.jpg")

phone_demo("Ask LaLa: ask the mall like you'd ask a friend", "Ask LaLa", "ask",
           [("Chat in Malaysian English", "\"Jom makan! Any halal ramen under RM15?\""),
            ("Answers take you there", "With Buzz score and walking time; tap Go"),
            ("Nudges quests", "Reminds you to scan the receipt for Makan Quest")],
           "Ask LaLa runs on an LLM + tenant data + Pandora social listening: answers you can walk to")

# ---------------------------------------------------------------- 7 Buzz
d.divider("LaLa Buzz", "Bring the online love into the app;\nkeep in-mall Real Talk in the app.", key="口碑")
s = d.info("Pandora is LaLa Buzz's brain: collect, judge, summarise, daily",
           label="How it works | Powered by Pandora",
           banner="No ads to write: Pandora finds what people already praise and shows it when customers decide")
d.flow(s, [("1 Collect", "#13294B", "Pandora listening", "Daily crawl of public IG,\nThreads and Facebook posts\nSorted by tenant & event"),
           ("2 Judge", "#1E3A63", "Pandora AI sentiment", "5-level sentiment analysis\nChecks the post is really\nabout that tenant; drops ads"),
           ("3 Show", "#B8975A", "Buzz Score + summary", "\"92% love it\" ratio\nWhat people love, hot tags\nOne tap to navigate or claim"),
           ("4 Feed back", "#8C6E3C", "Real Talk", "Verified buyers only\n+20 pts per post\nFlows back into Pandora")])

s = d.info("Pandora: one engine, reports for the mall, LaLa Buzz for shoppers", label="Our Product | Pandora",
           banner="These are real Pandora reports for LaLaport BBCC: LaLa Buzz has data from day one",
           source=PSRC)
STEP = [("v_stats.png", "1 Volume", "3,696 posts, 5.1M engagement\n→ \"128 posts ▲32%\" in the app"),
        ("i_sentdist_c.png", "2 Sentiment", "90.7% positive, 1.2% negative\n→ \"92% love it\" in the app"),
        ("i_positive.png", "3 Summary", "AI reads posts, writes the gist\n→ AI summary and tags in the app")]
for i, (f, t, desc) in enumerate(STEP):
    x = 0.6 + i * 3.05
    d.round(s, x, 1.28, 2.85, 4.75, "soft", 0.06)
    d.tx(s, x + 0.15, 1.4, 2.6, 0.35, t, 14, color="frame", bold=True)
    d.fit(s, PD + f, x + 0.12, 1.85, 2.61, 2.1, border=True)
    d.tx(s, x + 0.15, 4.1, 2.6, 0.9, desc, 11, bold=True, spacing=1.5)
    if i < 2:
        d.rect(s, x + 2.88, 3.0, 0.14, 0.24, "grey", MSO_SHAPE.RIGHT_ARROW)
d.rect(s, 9.7, 3.0, 0.14, 0.24, ORANGE, MSO_SHAPE.RIGHT_ARROW)
phone(s, "brand", 10.05, 1.3, 4.0, video=False, tag=False)
d.tx(s, 9.85, 5.42, 2.3, 0.3, "LaLa Buzz tenant page", 10, color="mid", bold=True, align=PP_ALIGN.CENTER)
d.fit(s, PD + "qr_insight.png", 12.2, 1.3, 0.8, 0.8, border=True)
d.tx(s, 12.0, 2.12, 1.2, 0.25, "See report", 9, color="mid", bold=True, align=PP_ALIGN.CENTER)

s = d.info("Pandora test: Malaysians are already writing great reviews", label="Pandora Test",
           banner="These are real posts: LaLa Buzz has content to show on day one",
           source="Data source: Pandora test, 6 Nov 2025–5 Nov 2026, Malaysia; numbers are post mentions")
d.bars(s, [("ACG Base", 223), ("KLP48 Theatre", 99), ("Doko Koko Café", 98), ("Pokémon", 71),
           ("Animate", 57), ("MINISO", 42), ("Akiba Ramen", 12)], 0.6, 1.35, 5.6, row_h=0.62, hot={2, 4, 6},
       name_w=1.7, size=11, unit="posts")
ugc(s, "akiba", 6.35, 1.25, 2.05, 4.85, "Akiba Ramen | 629 likes")
ugc(s, "dokokoko", 8.5, 1.25, 2.05, 4.85, "Doko Koko Café | 4,585 likes")
ugc(s, "kidscafe", 10.65, 1.25, 2.05, 4.85, "Ngam Ngam | family café")

phone_demo("Buzz home: what everyone's loving lately, on one page", "LaLa Buzz", "buzz",
           [("Buzz of the Week", "The most-talked-about shop or event"),
            ("Category tabs", "Makan, ACG, Outlet, Family"),
            ("Buzz Score + trend", "★4.8, 128 posts, ▲32%: how good, how hot")],
           "Shoppers scroll Buzz before arriving and know exactly where to go", photo=A + "mock_hero3.jpg")

phone_demo("Tenant page: AI summary + real posts help people decide", "LaLa Buzz", "brand",
           [("92% love it", "Positive ratio and post count, judged by Pandora AI"),
            ("What people love", "Creamy paitan, Value for money… auto tags"),
            ("Web Buzz / Real Talk", "Online posts with source; verified in-mall reviews"),
            ("Take me there", "One-tap navigation, or write Real Talk for +20 pts")],
           "From \"seeing a good review\" to \"walking in\": just one button", keys2=["realtalk"])

s = d.info("Three trust gates: only good reviews, but every one is real", label="Trust & Safety",
           banner="Not review-washing: public sources, verified purchases, AI + human moderation")
d.columns(s, [("Gate 1", "#15325E", "Public sources", "Every Web Buzz post links\nto the original and date\nSponsored posts auto-excluded"),
              ("Gate 2", ORANGE, "Verified purchase", "Real Talk needs a scanned receipt\nVerified purchase ✓\nOne receipt, one review"),
              ("Gate 3", MINT, "AI + human review", "AI blocks abuse and personal data\nMall team reviews daily\nTenants can reply")])

# ---------------------------------------------------------------- 8 Rollout
d.divider("Rollout & KPI", "Activation, timeline, roles, KPIs.", key="落地")
d.social_idea("A", "LaLaport BBCC × ACG", "ACG Season Pass: ACG Matsuri becomes an in-app season",
              "One Season Pass per season: stamp rallies, collab café quests, KLP48 Theatre check-ins. "
              "Complete it for exclusive capsules and priority event entry. (AI mock-up)", A + "app/acg_event.jpg")
d.social_idea("B", "MOP KLIA Sepang × Travellers", "Transit Quest: level up at the outlet in a 3-hour layover",
              "With Batik Air and the Tourist Privilege Pass: travellers get a 30-day Explorer trial on download, "
              "KLIA transit quests and tax-refund reminders, so one-time visitors still become members. (AI mock-up)",
              A + "klia_outlet.jpg")

s = d.info("Fix the three biggest pains first, then layer on the games", label="Timeline",
           banner="Phase 0 removes the hassle of earning points; Phase 1 makes people want to play")
d.timeline(s, 1.8, ["Jan 2027", "Apr 2027", "Jul 2027", "Oct 2027", "Jan 2028"],
           [("P0 | Tiers + AI receipts + Buzz (read-only)", 0, 0.33),
            ("P1 | Quests · Capsule · Ask LaLa", 0.25, 0.6),
            ("P2 | Matsuri Pass · Real Talk", 0.5, 0.85),
            ("P3 | KLIA Transit · For You", 0.72, 1.0)])
d.table(s, ["", "Mitsui Shopping Park", "TurnCloud"],
        [["Content", "Tier perks, campaign calendar, tenant deals", "UI/UX, prototype, localised copy"],
         ["System", "Existing app and member data", "Tier engine, AI receipts, Ask LaLa, game modules"],
         ["Data", "Thresholds and perk decisions", "Pandora listening, Buzz Score, CRM dashboard"]],
        y=3.85, col_w=[1.1, 4.0, 4.4], size=12, row_h=0.5)

s = d.info("KPI: from 5% to 20% of members earning points in one year", label="KPI",
           banner="Every layer is measurable: Phase 0 data drives the Phase 1 perk tuning",
           source="Targets are illustrative; final targets to be calibrated with Mitsui's member base and app data")
d.table(s, ["Metric", "Today", "Phase 0 (3 months)", "12 months live (illustrative)"],
        [["Members earning points in-app", "5%", "10%", "20%"],
         ["MAU / members", "—", "20%", "35%"],
         ["Receipts logged per month", "—", "20,000", "60,000"],
         ["Avg. monthly visits", "—", "+0.2", "+0.6"],
         ["Real Talk posts per month", "0", "500", "3,000"],
         ["Members at Explorer or above", "—", "15%", "30%"]],
        col_w=[3.4, 1.4, 2.4, 2.9], size=14, row_h=0.6, hot_row=0)

d.closing("Every visit levels you up.",
          "Next Steps\n1  Nov: confirm the four tier thresholds and perks\n"
          "2  Dec: prototype user testing (20 members aged 18–34)\n"
          "3  Jan 2027: Phase 0 development kicks off (tiers + AI receipts + Buzz)",
          logos=[TC])
d.save("MSP_App3.0_LaLaQuest_Proposal_EN.pptx")
import json  # noqa: E402
json.dump(META, open("web_meta_en.json", "w"))
