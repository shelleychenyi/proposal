"""Stills for the in-app push journey page (deck): proto/journey.py -> assets/screens/j_*.png + poster_r/j_*.jpg"""
import asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
B = "file://" + os.path.abspath("proto/app.html")
J = {"j1": "s=home&push=invite", "j2": "s=missions", "j3": "s=missions&y=250&push=gap", "j4": "s=paycode",
     "j5": "s=missions&y=250&claim=1", "j6": "s=tiers&push=tier", "rc_got": "s=receipt&got=1&y=330", "rc_cam": "s=receipt&cam=1",
     "rh_ok": "s=rhist&st=ok&push=approved"}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        c = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3)
        for k, qs in J.items():
            pg = await c.new_page(); await pg.goto(B + "?" + qs); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f"assets/screens/{k}.png"); await pg.close()
        await b.close()
    m = Image.open("assets/corner_mask.png")
    for k in J:
        im = Image.open(f"assets/screens/{k}.png").convert("RGBA").resize((780, 1688), Image.LANCZOS); im.alpha_composite(m)
        im.convert("RGB").save(f"assets/poster_r/{k}.jpg", quality=90)
    print("journey ok")
asyncio.run(main())
