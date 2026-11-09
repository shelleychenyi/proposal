import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/shelley-deck/scripts"))
from shelley_deck import Deck  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FM_LOGO = os.path.join(HERE, "assets", "familymart-logo.png")
SRC = "Source: Pandora vs. Opview side-by-side test, keyword \"FamilyMart (全家便利商店)\", 2025/12/22–12/30"

d = Deck(font="Arial", theme={"frame": "#0A8F3C"},
         footer_logos=["brand/accucrazy-dark.png", FM_LOGO])

# 1 ── Cover
d.cover("FamilyMart Taiwan\nSuccess Story.",
        "Pandora social listening: from noisy data\nto real-time, action-ready insight.", "2026.11",
        logos=["brand/accucrazy-dark.png"])

# 2 ── Pain points
s = d.info("The challenge: lots of data, very little signal", label="Pain Points",
           banner="FamilyMart did not need more data. It needed data it could trust and act on, fast.")
d.columns(s, [
    ("Noise", "#1DB7D3", "Brand mentions buried in irrelevant posts",
     "Generic keyword matching pulls in unrelated chatter.\n"
     "Exclusion lists hit their limit almost immediately.\n"
     "The first page of results is already a mix of unrelated posts."),
    ("Misreads", "navy", "Wrong sentiment, wrong decisions",
     "A post praising a product is flagged negative because of one small complaint.\n"
     "No weighting means the overall mood is misjudged."),
    ("Blind spots", "frame", "Missing the channels where customers talk",
     "Legacy tools barely cover Threads, Dcard and PTT.\n"
     "Comment replies counted as posts inflate volume.\n"
     "Teams react after a story has already spread."),
])

# 3 ── What we delivered
s = d.info("What we delivered: one AI platform, from listening to action", label="Our Solution",
           banner="From \"what are people saying?\" to \"what should we do next?\" in one workflow.")
d.flow(s, [
    ("1  LISTEN", "#1DB7D3", "Pandora\nSocial Listening",
     "Hybrid AI search that understands context, not just keywords.\nBrand-specific DataLake for voice & insight reports."),
    ("2  ALERT", "navy", "War Room\n+ 24/7 LINE Alerts",
     "Custom thresholds for buzz, sentiment and negative comments.\nThreads patrolled 24/7, with hot posts sent to LINE."),
    ("3  ANALYZE", "dark", "Ask in\nPlain Language",
     "AI agents (orchestrated by \"Stacey\") answer questions on the data.\nDaily positive/negative report, plus a newsroom tracker for press coverage."),
    ("4  ACT", "frame", "Content\nin Minutes",
     "Moana writes word-of-mouth copy.\nBanana Split creates matching visuals.\nInsight becomes campaigns in minutes."),
], y=1.45, h=4.3)

# 4 ── Results
s = d.info("The results: 12.4× more posts, and full coverage where it matters", label="Results",
           banner="FamilyMart sees what customers actually say, on every channel, before it trends.",
           source=SRC + ". Original posts only (comment replies excluded).")
d.num_cards(s, [
    ("12.4×", "More original posts", "3,366 vs. 272 posts captured in the same 9 days."),
    ("100%", "Original posts", "Every result is its own post. 47% of the legacy tool's results were replies."),
    ("54.1×", "Coverage on Threads", "2,868 vs. 53 posts, on the fastest-growing channel."),
], y=1.35, h=2.15)
d.tx(s, 0.72, 3.7, 6, 0.3, "Original posts by channel: Pandora vs. legacy tool", 12, bold=True)
d.bars(s, [("Threads", 2868), ("Threads (legacy)", 53), ("Facebook", 242), ("Facebook (legacy)", 28),
           ("Dcard", 166), ("Dcard (legacy)", 2)],
       0.72, 4.0, 7.6, row_h=0.3, hot={0, 2, 4}, unit="", name_w=1.9, size=10)
d.tx(s, 8.6, 3.95, 4.1, 2.1,
     "Dcard: 83×   PTT: 45×   Facebook: 8.6×\n\n"
     "More coverage means early warning signs, competitor moves and product buzz all come to the surface.",
     11.5, color="mid", spacing=1.5)

# 5 ── Takeaways for Philippine convenience stores
d.closing("Hear every customer. Act before it trends.",
          "What this means for a Philippine convenience store chain\n"
          "①  Track your brand, competitors and promos on Facebook, TikTok & more\n"
          "②  Catch complaints early with a War Room and real-time alerts\n"
          "③  Turn insight into local content with AI agents\n\n"
          "Next step: 2-week pilot listening report on your brand vs. key competitors",
          logos=["brand/turncloud.png", "brand/accucrazy-white.png"])

d.save(os.path.join(HERE, "FamilyMart_Pandora_CaseStudy_EN.pptx"))
print("saved")
