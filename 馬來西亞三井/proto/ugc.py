import asyncio
from playwright.async_api import async_playwright
P={"akiba":"reel/DcAAyTgvNHp","dokokoko":"reel/Dbk9CzWJYM2","animate":"reel/DaSmTfGPfjN","kidscafe":"reel/DdnZpiXz1lE","parking":"reel/DZXA8iSTzgm","lulu":"reel/DY4OtwOzqb6","acgbase":"p/DdQ4FRqBBwN"}
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(channel="chrome");ctx=await b.new_context(viewport={"width":420,"height":1000},device_scale_factor=2,locale="en-US")
    for k,u in P.items():
      pg=await ctx.new_page();await pg.goto(f"https://www.instagram.com/{u}/embed/captioned/",wait_until="networkidle",timeout=45000)
      await pg.wait_for_timeout(2500)
      el=await pg.query_selector(".EmbeddedMedia, .Embed, body")
      h=await pg.evaluate("document.body.scrollHeight");print(k,h)
      await pg.screenshot(path=f"assets/ugc/{k}.png",full_page=True);await pg.close()
    await b.close()
asyncio.run(m())
