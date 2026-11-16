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


NAVY, GOLD, GOLD2 = "#13294B", "#B8975A", "#8C6E3C"


def core_map(s, y=1.3):
    """Core + Add-on architecture: three plug-in add-ons sitting on one core."""
    adds = [("PLAY PACK", PINK, "Visit check-ins · Quests\nStamp Rally · LaLa Capsule\nMatsuri Pass"),
            ("AI PACK", BLUE, "AI Receipt Scan (1 sec)\nAsk LaLa concierge\nFor You picks"),
            ("BUZZ PACK", ORANGE, "Pandora LaLa Buzz\nBuzz Score + AI summary\nReal Talk reviews")]
    d.tx(s, 0.72, y, 6, 0.3, "ADD-ONS  |  experience · switch on when ready", 12, color=GOLD2, bold=True)
    for i, (t, col, body) in enumerate(adds):
        x = 0.72 + i * 3.98
        d.round(s, x, y + 0.38, 3.78, 1.55, "soft", 0.08)
        d.rect(s, x, y + 0.38, 0.09, 1.55, col)
        d.tx(s, x + 0.3, y + 0.5, 3.3, 0.35, t, 15, color=col, bold=True)
        d.tx(s, x + 0.3, y + 0.88, 3.4, 1.0, body, 11.5, bold=True, spacing=1.4)
        d.rect(s, x + 1.79, y + 2.0, 0.2, 0.28, "grey", MSO_SHAPE.DOWN_ARROW)
    cy = y + 2.38
    d.round(s, 0.72, cy, W - 1.44, 2.05, NAVY, 0.06)
    d.tx(s, 1.0, cy + 0.14, 8, 0.35, "CORE  |  LaLa Quest base app · drives footfall and sign-ups", 13, color="#E8D6AE", bold=True)
    cores = [("Member ID + 4 tiers", "QR on home · Rookie → Legend"),
             ("LaLa Park · LPR", "Plate = member · free hours by tier\npoints pay the rest"),
             ("LaLa Go · Bus", "LTH tickets · timetable\nboarding reminders · KLIA shuttle"),
             ("Points + e-Vouchers", "Receipt submission · wallet\ntrip & tenant e-Vouchers")]
    for i, (t, body) in enumerate(cores):
        x = 1.0 + i * 2.95
        d.round(s, x, cy + 0.6, 2.75, 1.25, "#1E3A63", 0.08)
        d.tx(s, x + 0.18, cy + 0.7, 2.5, 0.35, t, 13.5, color="white", bold=True)
        d.tx(s, x + 0.18, cy + 1.07, 2.5, 0.75, body, 10.5, color="#C9D3E0", spacing=1.35)



# ---------------------------------------------------------------- v4 helpers: What's New + scenario demo
SC_NAVY, SC_GOLD, SC_GOLD_L = "#13294B", "#B8975A", "#E8D6AE"
PAGES, PAGE_REFS = {}, []


def whats_new(title, label, banner, head, rows):
    """Before → After table that doubles as a feature directory (p.N filled in at the end)."""
    s = d.info(title, label=label, banner=banner)
    X = [(0.6, 1.75), (2.4, 3.3), (6.1, 4.75), (10.95, 1.15), (12.2, 0.6)]
    y0 = 1.25
    d.rect(s, 0.6, y0, 12.15, 0.36, SC_NAVY)
    for i, (x, w) in enumerate(X):
        d.tx(s, x + (0.12 if i < 3 else 0), y0 + 0.08, w, 0.25, head[i], 10.5, color=SC_GOLD_L if i == 2 else "white",
             bold=True, align=PP_ALIGN.LEFT if i < 3 else PP_ALIGN.CENTER)
    rh = 0.535
    for r, (feat, before, after, pkg, key) in enumerate(rows):
        y = y0 + 0.42 + r * rh
        new = "NEW" in pkg
        if r % 2 == 0:
            d.rect(s, 0.6, y, 12.15, rh, "soft")
        if new:
            d.rect(s, 0.6, y, 0.07, rh, SC_GOLD)
        d.tx(s, 0.72, y, 1.65, rh, feat, 12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        d.tx(s, 2.52, y, 3.15, rh, before, 10, color="grey", anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
        d.rect(s, 5.78, y + rh / 2 - 0.09, 0.2, 0.18, SC_GOLD, MSO_SHAPE.RIGHT_ARROW)
        d.tx(s, 6.22, y, 4.65, rh, after, 11, bold=True, color=SC_NAVY, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
        core = pkg.startswith(("Core", "核心"))
        d.round(s, 11.0, y + 0.11, 1.05, rh - 0.22, SC_NAVY if core else SC_GOLD, 0.5)
        d.tx(s, 11.0, y + 0.11, 1.05, rh - 0.22, pkg, 8.5, color="white", bold=True, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
        tb = d.tx(s, 12.2, y, 0.6, rh, "p.", 11, color="frame", bold=True, align=PP_ALIGN.CENTER,
                  anchor=MSO_ANCHOR.MIDDLE)
        PAGE_REFS.append((tb, key))
    return s


def glance(title, label, banner, before_lbl, after_lbl, olds, news, tag_txt):
    """Before/after at a glance: greyed current-app screens (left) vs live App 3.0 recordings (right)."""
    s = d.info(title, label=label, banner=banner)
    oh, nh = 3.35, 3.5
    ow, nw = oh * 390 / 844, nh * 390 / 844
    # BEFORE panel
    d.round(s, 0.6, 1.3, 3.55, 4.75, "#ECEAE6", 0.06)
    d.tx(s, 0.6, 1.42, 3.55, 0.3, before_lbl, 12, color="grey", bold=True, align=PP_ALIGN.CENTER)
    x = 0.6 + (3.55 - (2 * ow + 0.2)) / 2
    for img, cap in olds:
        d.round(s, x - 0.05, 1.95 - 0.05, ow + 0.1, oh + 0.1, "#B9B5AE", 0.1)
        d.cover_pic(s, A + f"old/{img}.jpg", x, 1.95, ow, oh)
        d.tx(s, x - 0.15, 1.95 + oh + 0.12, ow + 0.3, 0.45, cap, 9.5, color="grey", align=PP_ALIGN.CENTER, spacing=1.1)
        x += ow + 0.2
    # arrow
    d.rect(s, 4.3, 3.45, 0.42, 0.55, SC_GOLD, MSO_SHAPE.CHEVRON)
    # AFTER panel
    d.round(s, 4.85, 1.3, 7.9, 4.75, SC_NAVY, 0.04)
    d.tx(s, 4.85, 1.42, 7.9, 0.3, after_lbl, 12, color=SC_GOLD_L, bold=True, align=PP_ALIGN.CENTER)
    gap = (7.9 - 4 * nw) / 5
    x = 4.85 + gap
    for key, cap, pill in news:
        phone(s, key, x, 1.85, nh, tag=False)
        d.tx(s, x - 0.25, 1.85 + nh + 0.12, nw + 0.5, 0.3, cap, 10.5, color="white", bold=True, align=PP_ALIGN.CENTER)
        if pill:
            d.round(s, x + nw / 2 - 0.35, 1.85 + nh + 0.44, 0.7, 0.2, SC_GOLD, 0.5)
            d.tx(s, x + nw / 2 - 0.35, 1.85 + nh + 0.44, 0.7, 0.2, pill, 8, color="white", bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        x += nw + gap
    return s


def scene(title, label, banner, photo, phones, beats, stats=None, chip=None, source=None, video=None):
    """Scenario demo: scene photo + story strip (time-stamped beats) + prototype recordings (+ big stats)."""
    s = d.info(title, label=label, banner=banner, source=source)
    pw_phone = 4.55 * 390 / 844
    phones_w = len(phones) * pw_phone + (len(phones) - 1) * 0.3
    stats_w = 3.2 if stats else 0
    pw = 12.15 - 0.4 - phones_w - (stats_w + 0.4 if stats else 0)
    if video:  # Banaverse scene clip (AI tag + chip burned in by proto/scene_video.py)
        d.movie(s, A + f"video_r/{video}.mp4", A + f"poster_r/{video}.jpg", 0.6, 1.3, pw, 2.95)
        META["video"].setdefault(d.n, []).append([video, 0.6, 1.3, pw, 2.95])
        chip = None
    else:
        d.cover_pic(s, photo, 0.6, 1.3, pw, 2.95)
        d.ai_tag(s, 0.7, 1.38)
    if chip:
        d.tag(s, 0.6, 3.83, chip, col=SC_GOLD, size=10.5, h=0.42)
    d.round(s, 0.6, 4.33, pw, 1.55, SC_NAVY, 0.06)
    cw = (pw - 0.2) / len(beats)
    for i, (t, line) in enumerate(beats):
        x = 0.7 + i * cw
        d.tx(s, x + 0.15, 4.45, cw - 0.3, 0.3, t, 11.5, color=SC_GOLD_L, bold=True)
        d.tx(s, x + 0.15, 4.78, cw - 0.3, 1.05, line, 10.5, color="white", spacing=1.25)
        if i:
            d.rect(s, x, 4.5, 0.012, 1.2, "#3A5378")
    x = 0.6 + pw + 0.4
    for k in phones:
        phone(s, k, x, 1.3, 4.55)
        x += pw_phone + 0.3
    if stats:
        x += 0.1
        hh = (4.6 - 0.15 * (len(stats) - 1)) / len(stats)
        for i, (big, lab) in enumerate(stats):
            y = 1.3 + i * (hh + 0.15)
            d.round(s, x, y, stats_w, hh, "soft", 0.08)
            d.rect(s, x, y, 0.07, hh, SC_GOLD)
            d.tx(s, x + 0.3, y + 0.18, stats_w - 0.4, 0.6, big, 26, color=SC_NAVY, bold=True)
            d.tx(s, x + 0.3, y + 0.85, stats_w - 0.4, 0.6, lab, 11, color="mid", bold=True, spacing=1.2)
    return s


def addon_overview(title, label, banner, groups, source=None):
    """All add-on features on one page: one row per pack, each feature with its app mock-up."""
    s = d.info(title, label=label, banner=banner, source=source)
    y = 1.25
    for name, col, sub, items in groups:
        d.round(s, 0.6, y, 12.15, 0.34, col, 0.5)
        d.tx(s, 0.85, y + 0.06, 11.6, 0.25, name + "   " + sub, 11.5, color="white", bold=True)
        cy = y + 0.42
        for i, (img, kind, t, desc) in enumerate(items):
            x = 0.6 + i * 3.06
            d.round(s, x, cy, 2.94, 1.95, "soft", 0.06)
            if kind == "phone":
                d.fit(s, A + f"poster_r/{img}.jpg", x + 0.12, cy + 0.1, 0.82, 1.75)
                tx0 = x + 1.05
            else:
                d.cover_pic(s, A + img, x + 0.1, cy + 0.1, 0.86, 1.75)
                tx0 = x + 1.08
            d.tx(s, tx0, cy + 0.16, 2.94 - (tx0 - x) - 0.1, 0.5, t, 12.5, color=col, bold=True, spacing=1.05)
            d.tx(s, tx0, cy + 0.72, 2.94 - (tx0 - x) - 0.12, 1.2, desc, 10, color="mid", spacing=1.25)
        y = cy + 2.07
    return s


def fill_page_refs():
    for tb, key in PAGE_REFS:
        tb.text_frame.paragraphs[0].runs[0].text = "p.%d" % PAGES[key]


# ---------------------------------------------------------------- Cover
d.cover("MSP App 3.0\nRenewal Proposal.", "LaLa Quest | Every visit levels you up.", "Nov 2026",
        company="TURN CLOUD TECHNOLOGY SERVICE INC.", logos=[LALA, MOP], image=A + "mock_hero3.jpg")
d.toc([("Insights", "機會"), ("Benchmarks", "標竿"), ("App 3.0 Overview", "全貌"), ("Core · Member Tiers", "分級"),
       ("Core · LaLa Park", "停車"), ("Core · LaLa Go", "巴士"), ("Add-ons · AI + Play", "加購"),
       ("Rollout & KPI", "落地")])

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

s = d.info("At a glance: a core that brings people in, add-ons that make them stay",
           label="Executive Summary",
           banner="Core first: parking, buses and tiers give every visitor a reason to sign up on day one")
d.columns(s, [("Insight", "#8A94A6", "Love is there, traffic tools aren't",
               "3,696 posts, 90.7% positive\nTop complaint: parking\nLTH + KLIA bring travellers\n"
               "Only 5% earn points in-app"),
              ("Solution", BLUE, "Core + 2 add-ons",
               "Core: tiers, LPR parking\nCore: LaLa Go bus tickets\nCore: points + e-Vouchers\n"
               "Add-ons: AI (+ Buzz) · Play"),
              ("Return", ORANGE, "More visits, more members",
               "Every plate = a member\nEvery bus ticket = mall spend\nPoint earning 5% → 20%\n"
               "One ID across all malls")])

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
           banner="Characters and games speak to this crowd: a natural Play add-on once the core is live",
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

s = d.info("Insight 3  The #1 complaint is parking, and the fix is hidden in News",
           label="Pandora Insight | Current App",
           banner="Malaysian malls already park by licence plate: link LPR to membership and parking becomes a sign-up reason",
           source=PSRC + " App screenshots, Nov 2026.")
d.fit(s, PD + "i_negative.png", 0.6, 1.28, 6.1, 3.28, border=True)
d.tx(s, 0.75, 4.72, 5.9, 1.3, "Pandora negative summary: parking is pricey, car park entrances get closed,\n"
     "weak signal makes QR payment hard.\n→ 3.0: register your plate, cameras do the rest;\n"
     "free hours by tier (3H → all day), points pay the rest.", 11.5, bold=True, spacing=1.45)
d.fit(s, A + "current_app.jpg", 7.0, 1.28, 5.75, 1.78, border=True)
d.ai_tag(s, 7.1, 1.36, "Current app screenshots")
d.callouts(s, 7.0, 3.3, 5.75, [("Home = ad wall", "Banners, News and Vouchers all push; there's no \"me\""),
                               ("Free parking buried in News", "MSP Member Free 3H Parking is just one post"),
                               ("Paper tickets, no plate link", "Parking isn't tied to the member ID or points")],
           gap=0.9)

s = d.info("Insight 4  Travellers pass through: LTH buses and the KLIA shuttle",
           label="Desk Research | Transport",
           banner="Bus waiting time is mall time: sell the ticket in-app, attach an e-Voucher, remind them to board",
           source="Data source: busonlineticket.com LaLaport Transportation Hub page (Nov 2026); "
                  "railtravelstation.com, MOP KLIA Sepang shuttle info. Timetables to be confirmed with operators.")
d.num_cards(s, [("8", "Bus operators at LTH", "LG1 East Atrium, LaLaport BBCC.\nKL ⇄ Singapore & Johor Bahru,\n"
                 "departures about 06:30–23:45."),
                ("~10 min", "MOP ⇄ KLIA free shuttle", "KLIA T1 ~10 min, klia2 ~20 min.\nTransit passengers and\n"
                 "tourists on a layover."),
                ("0", "Linked to the mall today", "Tickets sit on third-party sites;\nno member ID, no voucher,\n"
                 "no reminder to shop first.")], y=1.35, h=2.55)
d.fit(s, A + "app/lth_bay.jpg", 0.72, 4.05, 3.2, 2.0)
d.ai_tag(s, 0.82, 4.12)
d.callouts(s, 4.2, 4.1, 8.4, [("Travellers arrive early", "Cross-border coaches ask you to come early: 30–90 min to fill"),
                              ("They need a nudge, not an ad", "\"30 min to boarding, RM10 voucher still unused\" turns waiting into spending")],
           gap=0.95)

d.statement("IDEA", "LaLa Quest\nPark. Ride. Level up.",
            "Every visit levels you up.\n"
            "Core: tiers · LPR parking · LaLa Go buses · e-Vouchers\n"
            "AI add-on: instant receipt scan, Ask LaLa, LaLa Buzz reviews\n"
            "Play add-on: check-ins, quests, stamp rallies, capsules",
            image=A + ("idea_poster.jpg" if IDEA_VIDEO else "app/acg_event.jpg"), video=IDEA_VIDEO)
META["special"]["idea"] = d.n

# ---------------------------------------------------------------- 2 Benchmarks
d.divider("Benchmarks", "Great member apps make people WANT to open them,\nnot HAVE to.", key="標竿")
s = d.info("Eight benchmarks: utility gets them in, identity keeps them", label="Benchmark",
           banner="We borrow: plate-based parking (1 Utama, Sunway), visible progress (Starbucks), collecting (USJ / Shopee)",
           source="Data source: official brand apps and public information; 1 Utama ONECARD LPR page (Nov 2026); "
                  "Starbucks Rewards 3-tier model, Mar 2026 (Restaurant Dive)")
d.table(s, ["Brand", "What they do", "What LaLa Quest borrows"],
        [["1 Utama ONECARD", "Register up to 2 plates; LPR opens the gate, e-wallet pays", "Core: LaLa Park plate login"],
         ["Sunway Smart Parking", "Ticketless entry & exit by plate, paid in the app", "Core: pay-at-exit, no ticket"],
         ["MUJI Passport", "Earn MUJI Miles just for checking in, no purchase needed", "Play: visit check-ins"],
         ["Disney App", "AI itinerary tips; mini-games while you queue", "AI: Ask LaLa plans your day"],
         ["Universal Studios", "Collect keys physically, track score in the app", "Play: in-mall Stamp Rally"],
         ["Starbucks Rewards", "Green / Gold / Reserve: 1x / 1.2x / 1.7x rewards", "Core: 4 tiers + multipliers"],
         ["Shopee", "Coins + daily mini-games, a daily Malaysian habit", "Play: daily LaLa Capsule"],
         ["Sephora", "Beauty Insider tiers + verified member reviews", "AI: LaLa Buzz + Real Talk"]],
        col_w=[2.1, 4.6, 2.9], size=12, row_h=0.52)

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
      "LaLa Go trip card: departure, bay, countdown;\nAI add-on: \"Plan my Saturday\";\n"
      "queue times for hot restaurants.",
      "Disney turns a visit into \"my plan\": LaLa Quest does the same for shoppers and travellers")
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
      "Parking hours, bus vouchers, collab merch\nas a reward ladder;\n"
      "full-screen Level Up celebration.",
      "Starbucks went back to 3 tiers in 2026: tiers + ladder is proven design")
bench("Shopee: the \"open it every day\" rhythm Malaysians know", "Shopee MY",
      ["shopee_1.jpg", "shopee_4.jpg", "shopee_5.jpg"],
      [("Strong campaign feel", "11.11, Payday Sale, countdowns, bold visuals"),
       ("ShopeeVIP", "Paid membership: free shipping, deals, vouchers"),
       ("Live + big prizes", "RM11 Million Vouchers, celebrity live streams")],
      "Ride the familiar Payday and 11.11 rhythm;\nMOP KLIA \"Payday Reward\" e-Vouchers;\n"
      "Play add-on: daily Capsule = LaLa's Coins.",
      "No need to educate the market: young Malaysians already open apps daily to claim stuff")
bench("Sephora: tier = discount, and AI picks your gifts", "Sephora",
      ["sephora_1.jpg", "sephora_4.jpg", "sephora_5.jpg"],
      [("Tiers map to discounts", "Insider 10% / VIB 15% / Rouge 20%"),
       ("Shareable Wish List", "Share your saved list with friends"),
       ("AI Beauty Chat", "Ask \"gifts under $200\", get picks")],
      "Rookie → Legend perks in one picture;\nAI add-on: Ask LaLa recommends by chat;\n"
      "AI add-on: LaLa Buzz borrows Sephora's review culture.",
      "Sephora shows the upgrade path: tiers first, then AI and reviews on top")

# ---------------------------------------------------------------- 3 Overview
d.divider("App 3.0", "A core that brings people in,\nadd-ons that make them stay.", key="全貌")
glance("App 3.0 at a glance: from a news board to an app that works for me", "What's New | At a Glance",
       "Same members, a whole new app: every screen now starts with me, my car, my trip, my level",
       "BEFORE · today's MSP app", "AFTER · App 3.0 (prototype recordings)",
       [("home", "Banners first;\nmember info buried"), ("news", "Promos & news,\nnothing personal")],
       [("home", "My card, car & trip", None), ("tiers", "4 tiers + characters", None),
        ("parking", "LaLa Park", "NEW"), ("busticket", "LaLa Go", "NEW")], "")
whats_new("What's new in App 3.0: 8 upgrades, 5 brand-new features", "What's New | Before → After",
          "From an app that pushes mall news to an app that parks my car, books my bus and levels me up",
          ["Feature", "Before · current app", "After · App 3.0", "Package", "Demo"],
          [("Home", "Banners and News push; no \"me\"", "My card, my car, my trip, all on one screen", "Core", "home"),
           ("Membership", "Perks hard to see; no reason to level up", "4 tiers + characters; perks grow with every visit", "Core", "tiers"),
           ("Parking", "Paper tickets; free 3H buried in News", "LaLa Park: plate = member, free hours by tier, points pay, gate opens", "Core · NEW", "park"),
           ("Bus & shuttle", "Tickets on third-party sites, no link to the mall", "LaLa Go: in-app tickets + RM10 e-Voucher + boarding reminders; KLIA shuttle", "Core · NEW", "go"),
           ("Points & vouchers", "Only 5% of members earn in-app", "Points pay parking and buses; tenant + trip e-Vouchers in one wallet", "Core", "home"),
           ("Play", "—", "Visit check-ins, quests, Stamp Rally, LaLa Capsule", "Play · NEW", "play"),
           ("AI", "—", "1-sec receipt scan, Ask LaLa concierge, For You picks", "AI · NEW", "ai"),
           ("Reviews", "Scattered on IG and Threads, invisible in the app", "LaLa Buzz: Pandora Buzz Score + Real Talk reviews", "AI · NEW", "buzz")])
phone_demo("Home: my card, my car, my trip, all on one screen", "Home", "home",
           [("Card = QR + tier", "At checkout, staff scan the QR on home (video, right)"),
            ("My car, live", "LPR spotted WXY 1234 at P2: 2h 31m free left"),
            ("My trip", "Bus to Singapore 3:30 PM, Bay 3, RM10 voucher to spend"),
            ("What's On gallery", "Swipe today's events and promos at the bottom of home (video)")],
           "Home moves from \"what the mall is pushing\" to \"who I am and what I get today\"", clip="checkout")
PAGES["home"] = d.n

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
mc = ["Jom! Your car is parked, 2h 31m free.", "30 min to boarding, still got RM10 lah", "Ask anything, lah…",
      "Done · Shiok!", "Squad up: bring 1 kawan", "Drive safe, see you again!"]
for i, t in enumerate(mc):
    d.round(s, 9.0, 1.8 + i * 0.68, 3.7, 0.54, "soft", 0.3)
    d.tx(s, 9.2, 1.92 + i * 0.68, 3.4, 0.3, t, 11.5, bold=True)

# ---------------------------------------------------------------- 4 Tiers (core)
d.divider("Member Tiers", "Core 1 | From Regular Member\nto Rookie, Explorer, Senpai, Legend.", key="分級")
s = d.info("Four tiers, four LaLas: members grow their own character", label="Core | Tier Characters",
           banner="No gold or silver cards: each level brings new gear, more parking hours and a badge worth a screenshot",
           source="Characters are AI concept designs; can extend into stickers, capsule figures and in-mall installations")
TIERS = [("rookie", "#8F8A80", "ROOKIE", "LV1 | On sign-up", "1x points · 3H parking\nTrip e-Vouchers"),
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
PAGES["tiers"] = d.n

s = d.info("Tier perks: parking hours and bus points grow with your level", label="Core | Tier Design",
           banner="Parking is the perk everyone understands: it turns \"level up\" into hours saved every visit",
           source="Thresholds and perks are illustrative; final numbers to be set from Mitsui member spending and car park data")
d.table(s, ["Tier", "Threshold (12 months)", "Points", "Free parking (LPR)", "Bus ticket pts", "Signature perks"],
        [["Rookie  LV1", "On sign-up", "1x", "3 hours", "1x", "Trip e-Vouchers, birthday gift"],
         ["Explorer  LV2", "RM 1,500 or 12 visits", "1.2x", "4 hours", "1.2x", "Birthday 2x points, 2nd plate"],
         ["Senpai  LV3", "RM 5,000", "1.5x", "5 hours", "1.5x", "Priority entry to Bon Odori & ACG events"],
         ["Legend  LV4", "RM 12,000", "2x", "All day", "2x", "Legend Lounge, reserved bays, Legend Night"]],
        col_w=[1.5, 2.3, 0.9, 1.75, 1.3, 2.75], size=12.5, row_h=0.7, hot_row=2)
d.tx(s, 0.75, 5.2, 12, 0.6, "★ Visits count too: reach Explorer with 12 visits. With Play add-on, each tier also unlocks "
     "more capsule draws (1 / 1 / 2 / 3 a day).", 13, bold=True, color="frame")

phone_demo("Tier page: four cards stacked, the next level always in sight", "Core | Tier", "tierflow",
           [("Stacked cards", "Four tier cards stacked like a wallet; Legend black-gold"),
            ("Perks at a glance", "Multiplier, LPR parking hours, bus points, event entry"),
            ("Level-up moment", "Senpai unlocked: 4H → 5H parking, 1.5x points"),
            ("In the mall", "The moment it happens, with friends (video, right)")],
           "Showing members \"where's next\" works better than giving more points",
           clip="lvscene")

# ---------------------------------------------------------------- 5 LaLa Park (core)
d.divider("LaLa Park", "Core 2 | Register your plate once.\nThe gate knows you're a member.", key="停車")
scene("LaLa Park: drive in, shop all afternoon, drive out. The gate just opens", "Core | LaLa Park · Scenario Demo",
      "Every driver gets a reason to register, and every visit gets logged",
      A + "app/lpr_gate.jpg", ["parking"],
      [("Sat 2:14 PM", "Drive in. The camera reads WXY 1234: \"4H free started\""),
       ("5:12 PM", "Shopping, makan, a movie. Free time left is always on screen"),
       ("Exit", "4H free taken off, 800 pts pay the rest. Gate opens, no ticket")],
      stats=[("0 tickets", "Your plate is your member card"), ("3H → all day", "Free parking grows with your tier"),
             ("100 pts = RM1", "Points pay the parking fee")],
      video="park_scene_en", source="Parking hours, rates and point values are illustrative; car park integration via API with Mitsui's LPR system")
PAGES["park"] = d.n

# ---------------------------------------------------------------- 6 LaLa Go (core)
d.divider("LaLa Go", "Core 3 | Buy the bus ticket in the app.\nSpend the wait in the mall.", key="巴士")
scene("LaLa Go: book the bus, get RM10 to spend, never miss boarding", "Core | LaLa Go · Scenario Demo",
      "Waiting time becomes mall time: every passenger walks past the shops with a voucher in hand",
      A + "app/lth_bay.jpg", ["bus", "busticket"],
      [("1:30 PM", "Book the 3:30 PM coach to Singapore in the app, +RM10 e-Voucher"),
       ("3:00 PM", "Push: \"30 min to boarding, RM10 still unused!\" Bubble tea, sorted"),
       ("3:20 PM", "Show the QR at Bay 3 and board. Points land after the trip")],
      chip="Also at MOP: free KLIA shuttle + \"catch my flight\"",
      video="go_scene_en", source="Operators, fares and timetables are illustrative; tickets via operator booking APIs (busonlineticket.com network at LTH)")
PAGES["go"] = d.n

# ---------------------------------------------------------------- 7 Add-ons (AI + Play)
d.divider("Add-ons", "AI + Play | Plug in when ready:\nsmarter visits first, more reasons to return next.", key="加購")
addon_overview("Add-ons at a glance: 8 features, AI first, then Play", "Add-ons | Overview",
               "Plug in when ready: AI makes every visit smarter, Play gives members a reason to come back",
               [("AI PACK", "#1E3A63", "·  smarter visits  ·  LaLa Buzz now part of AI", [
                   ("scan", "phone", "AI Receipt Scan", "Snap a receipt, points in 1.2 sec; tier multiplier applied"),
                   ("ask", "phone", "Ask LaLa + For You", "AI concierge in Malaysian English: food, shops, exits, day plans"),
                   ("buzz", "phone", "LaLa Buzz", "Pandora reads 3,696+ real posts: Buzz Score, AI summary, hot tags"),
                   ("brand", "phone", "Tenant page + Real Talk", "92% love it, real posts, one tap to go; verified reviews +20 pts")]),
                ("PLAY PACK", "#B8975A", "·  more reasons to come back", [
                   ("home_play", "phone", "Visit check-ins + Quests", "Check in on visit days for points; Makan & Squad quests for XP"),
                   ("quest", "phone", "Stamp Rally", "The floor plan becomes a treasure map: 5 stamps = Matsuri capsule"),
                   ("capsule", "phone", "LaLa Capsule", "One free draw a day, 24 characters a series, trade with kawan"),
                   ("app/acg_event.jpg", "photo", "Matsuri Season Pass", "ACG Matsuri, Bon Odori, Raya, CNY: seasonal passes + events")])],
               source="App screens are prototype captures; Matsuri photo is an AI mock-up")

phone_demo("AI Receipt Scan: finish your ramen, snap, points in", "Add-on · AI | Receipt Scan", "scan",
           [("Instant AI read", "Shop, amount and time captured in 1.2 sec"),
            ("Tier multiplier applied", "Explorer 1.2x: RM28.90 → +35 pts"),
            ("Quests move forward", "With Play add-on: Makan Quest done")],
           "Receipt scanning captures 95% of spending without touching any tenant's POS",
           photo=A + "mock_ramen_scan.jpg")
PAGES["ai"] = d.n

phone_demo("Ask LaLa: ask the mall like you'd ask a friend", "Add-on · AI | Ask LaLa", "ask",
           [("Chat in Malaysian English", "\"Jom makan! Any halal ramen under RM15?\""),
            ("Answers take you there", "With Buzz score and walking time; tap Go"),
            ("Knows your car and trip", "\"Nearest exit?\" uses your LaLa Park session")],
           "Ask LaLa runs on an LLM + tenant data + core parking and bus data: answers you can walk to")

scene("LaLa Buzz: see what everyone's loving, then walk straight in", "Add-on · AI | LaLa Buzz · Scenario Demo",
      "Powered by Pandora: real posts become the reason to visit, and Real Talk keeps the love in the app",
      A + "app/ramen.jpg", ["buzz", "brand"],
      [("Fri night", "Scroll Buzz: Akiba Ramen ★4.8 · 92% love it · ▲32% this week"),
       ("Sat noon", "Tap \"Take me there\": L4, 2-min walk. Creamy paitan, as promised"),
       ("After", "Snap the receipt, post a Real Talk review, +20 pts")],
      chip="Powered by Pandora · 3,696 real posts",
      source="Data source: Pandora social listening, LaLaport BBCC, 3 May–31 Oct 2026, N=3,696 (Instagram, Threads)")
PAGES["buzz"] = d.n

phone_demo("Stamp Rally: the mall floor plan becomes a treasure map", "Add-on · Play | Stamp Rally", "quest",
           [("Floor-map stamps", "L4 Garden Dining, L2 ACG Base, L1 Doko Koko"),
            ("40m away", "Location hints guide you to the next stop"),
            ("Collect for exclusives", "5 stamps = Matsuri capsule + 300 XP")],
           "Stamp rallies are a Japanese mall classic; in-app, they measure traffic on every floor",
           photo=A + "app/acg_event.jpg")
PAGES["play"] = d.n

phone_demo("LaLa Capsule: one free draw a day, and a reason to collect", "Add-on · Play | Capsule", "capsule",
           [("One free draw daily", "From check-ins; higher tiers draw more"),
            ("24 per series", "Durian-chan, Ramen-kun… originals, can become figures"),
            ("Trade with kawan", "Swap duplicates with friends: built-in sharing")],
           "Capsules turn points into collectibles: digital collecting, physical rewards, back to the mall",
           photo=A + "mock_friends_capsule.jpg")

# ---------------------------------------------------------------- 10 Rollout
d.divider("Rollout & KPI", "Core first, add-ons when ready:\nactivation, timeline, roles, KPIs.", key="落地")
d.social_idea("A", "MOP KLIA Sepang × Travellers", "Transit Quest: a layover at the outlet, a member for life",
              "LaLa Go shows the free KLIA shuttle and pings travellers when to leave for their flight. "
              "Download = 30-day Explorer trial + RM10 e-Voucher + Tourist Privilege Pass, so one-time "
              "visitors still become members. (AI mock-up)", A + "klia_outlet.jpg")
d.social_idea("B", "LaLaport BBCC × ACG (with Play add-on)", "ACG Season Pass: ACG Matsuri becomes an in-app season",
              "Once Play Pack is on: stamp rallies, collab café quests, KLP48 Theatre check-ins. Members who drive in "
              "get +1H parking during Matsuri weekend; complete the pass for exclusive capsules. (AI mock-up)",
              A + "app/acg_event.jpg")

s = d.info("Launch the core first, then plug in add-ons season by season", label="Timeline",
           banner="Phase 0 is all core: tiers, LPR parking and LaLa Go go live together; add-ons follow on demand")
d.timeline(s, 1.8, ["Jan 2027", "Apr 2027", "Jul 2027", "Oct 2027", "Jan 2028"],
           [("P0 Core | Tiers · Park · Go · Vouchers", 0, 0.4),
            ("Add-on | AI Pack: LaLa Buzz (Pandora)", 0.3, 0.6),
            ("Add-on | AI Pack: Receipt Scan · Ask LaLa", 0.45, 0.8),
            ("Add-on | Play Pack (Quests · Capsule · Matsuri)", 0.6, 1.0)])
d.table(s, ["", "Mitsui Shopping Park", "TurnCloud"],
        [["Content", "Tier perks, car park rules, tenant vouchers", "UI/UX, prototype, localised copy"],
         ["System", "App, member data, car park LPR + bus partners", "Tier engine, LPR & bus API links, add-ons"],
         ["Data", "Thresholds, parking & voucher budget", "Pandora listening, CRM dashboard"]],
        y=3.85, col_w=[1.1, 4.0, 4.4], size=12, row_h=0.5)

s = d.info("KPI: core moves traffic and sign-ups, add-ons move engagement", label="KPI",
           banner="Every layer is measurable: core data in Phase 0 decides which add-on to switch on first",
           source="Targets are illustrative; final targets to be calibrated with Mitsui's member base, car park and app data")
d.table(s, ["Metric", "Package", "Today", "Phase 0 (3 months)", "12 months (illustrative)"],
        [["Plates registered (LaLa Park)", "Core", "—", "15,000", "60,000"],
         ["Bus tickets sold in-app (LaLa Go)", "Core", "0", "3,000 / month", "10,000 / month"],
         ["Trip e-Vouchers redeemed", "Core", "0", "40%", "55%"],
         ["Members earning points in-app", "Core", "5%", "10%", "20%"],
         ["Avg. monthly visits", "Core", "—", "+0.2", "+0.6"],
         ["MAU / members", "Add-ons", "—", "20%", "35%"],
         ["Real Talk posts per month", "Add-ons", "0", "—", "3,000"]],
        col_w=[3.6, 1.2, 1.1, 2.0, 2.2], size=12.5, row_h=0.56, hot_row=0)

from mkt_section import add_marketing  # noqa: E402
add_marketing(d, "en")

d.closing("Every visit levels you up.",
          "Next Steps\n1  Nov: confirm the Core scope and tier perks (incl. parking hours)\n"
          "2  Dec: car park LPR + bus operator API workshop; prototype test with 20 members\n"
          "3  Jan 2027: Phase 0 Core development kicks off",
          logos=[TC])
fill_page_refs()
d.save("MSP_App3.0_LaLaQuest_Proposal_EN.pptx")
META["n"] = d.n
import json  # noqa: E402
json.dump(META, open("web_meta_en.json", "w"))
