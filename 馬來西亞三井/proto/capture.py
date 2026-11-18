import asyncio,sys,os,shutil
from playwright.async_api import async_playwright
BASE="file://"+os.path.abspath("proto/app.html")
SHOTS={"home":4,"tiers":2.5,"quest":2.5,"capsule":4.5,"scan":5.5,"ask":5,"buzz":2,"brand":2.5,"realtalk":3.5,"levelup":4.5,"parking":2,"bus":2,"busticket":1.5,"missions":2,"receipt":1.5,"rhist":1.5,"rok":2,"paycode":1.5}
VIDS={"home":12.5,"capsule":6,"scan":6.5,"ask":6,"buzz":5,"brand":4,"realtalk":9,"levelup":5.5,"tiers":3,"quest":3.5,"parking":7.5,"bus":3.5,"busticket":6,"missions":12.5,"receipt":12.5}
async def main(mode):
  async with async_playwright() as p:
    b=await p.chromium.launch(channel="chrome")
    if mode in("shots","all"):
      ctx=await b.new_context(viewport={"width":390,"height":844},device_scale_factor=3)
      for k,t in SHOTS.items():
        pg=await ctx.new_page();await pg.goto(BASE+"?s="+k);await pg.wait_for_timeout(int(t*1000))
        await pg.screenshot(path=f"assets/screens/{k}.png");await pg.close();print("shot",k)
      await ctx.close()
    if mode in("vids","all"):
      for k,t in VIDS.items():
        ctx=await b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,record_video_dir="assets/video_raw/tmp",record_video_size={"width":780,"height":1688})
        pg=await ctx.new_page();await pg.goto(BASE+"?play=1&s="+k);await pg.wait_for_timeout(int(t*1000))
        v=pg.video;await ctx.close();src=await v.path();shutil.move(src,f"assets/video_raw/{k}.webm");print("vid",k)
    await b.close()
asyncio.run(main(sys.argv[1] if len(sys.argv)>1 else "all"))
