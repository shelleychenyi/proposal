"""Sync deck + prototype into web/ (EN) and web_zh/ (ZH)."""
import json, re, os, shutil, glob, sys
import fitz
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
SITES = [("web", "MSP_App3.0_LaLaQuest_Proposal_EN.pdf", "web_meta_en.json", "en"),
         ("web_zh", "MSP_App3.0_LaLaQuest_提案.pdf", "web_meta.json", "zh")]
IDEA = {"en": ('LaLa Quest<br>Park. Ride. Level up.',
               '<b>Core</b>　Tiers · LPR parking · LaLa Go buses · e-Vouchers<br><b>AI</b>　Instant receipt scan, Ask LaLa, LaLa Buzz reviews<br>'
               '<b>Play</b>　Check-ins, quests, stamps, capsules'),
        "zh": ('LaLa Quest<br>停車、搭車、升級',
               '<b>核心</b>　四級會員・車牌停車・LaLa Go 巴士・e-Voucher<br><b>AI 包</b>　1 秒發票掃描、Ask LaLa、LaLa Buzz 口碑<br>'
               '<b>遊戲包</b>　簽到、任務、集章、扭蛋')}
for site, pdf, meta, lang in SITES:
    A = f"{site}/assets/"
    for f in glob.glob("assets/video_r/*.mp4"): shutil.copy(f, A + "video/")
    for f in glob.glob("assets/poster_r/*.jpg"): shutil.copy(f, A + "img/")
    for f in glob.glob("assets/app/*.jpg"): shutil.copy(f, A + "app/")
    shutil.copy("assets/klia_outlet.jpg", A + "klia_outlet.jpg")
    shutil.copy("proto/app.html", f"{site}/prototype/index.html")
    for f in glob.glob(A + "slides/s-*.jpg"): os.remove(f)
    doc = fitz.open(pdf)
    for i, p in enumerate(doc):
        pix = p.get_pixmap(matrix=fitz.Matrix(1920 / p.rect.width, 1920 / p.rect.width))
        pix.save(A + f"slides/s-{i + 1:02d}.jpg", jpg_quality=85)
    m = json.load(open(meta))
    s = open(f"{site}/index.html").read()
    v = {k: [[a, round(x, 4), round(y, 4), round(w, 4), round(h, 4)] for a, x, y, w, h in L] for k, L in m["video"].items()}
    s = re.sub(r"const VIDEO = \{.*?\};", "const VIDEO = " + json.dumps(v, ensure_ascii=False) + ";", s, flags=re.S)
    s = re.sub(r"const N = \d+,", f"const N = {len(doc)},", s)
    s = re.sub(r"const SPECIAL = \{[^}]*\};", "const SPECIAL = {idea: %d, islands: 0, tiers: %d};" % (m["special"]["idea"], m["special"]["tiers"]), s)
    big, body = IDEA[lang]
    s = re.sub(r'<h1>LaLa Quest<br>.*?<small>', f'<h1>{big}<small>', s)
    s = re.sub(r'<p><b>(Level Up|Core|核心)</b>.*?</p></div>', f'<p>{body}</p></div>', s)
    open(f"{site}/index.html", "w").write(s)
    print(site, len(doc), "slides")
