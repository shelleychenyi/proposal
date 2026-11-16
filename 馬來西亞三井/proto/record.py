import asyncio,os,base64,subprocess,sys
from playwright.async_api import async_playwright
FF="/Users/shelleychen/.claude/skills/shelley-deck/.venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
BASE="file://"+os.path.abspath("proto/app.html")
VIDS={"home":12.5,"capsule":6,"scan":6.5,"ask":6,"buzz":5,"brand":4,"realtalk":9,"levelup":6,"tiers":7,"quest":3.5,"parking":7.5,"bus":3.5,"busticket":6}
if len(sys.argv)>1: VIDS={k:VIDS[k] for k in sys.argv[1:]}
FPS=30
async def rec(b,k,t):
  ctx=await b.new_context(viewport={"width":780,"height":1688},device_scale_factor=1)
  pg=await ctx.new_page();cdp=await ctx.new_cdp_session(pg)
  frames=[]
  async def on(ev):
    frames.append((ev["metadata"]["timestamp"],base64.b64decode(ev["data"])))
    try: await cdp.send("Page.screencastFrameAck",{"sessionId":ev["sessionId"]})
    except Exception: pass
  cdp.on("Page.screencastFrame",lambda ev:asyncio.ensure_future(on(ev)))
  await pg.goto(BASE+"?z=2&s="+k);await pg.wait_for_timeout(600)  # fonts/images
  await cdp.send("Page.startScreencast",{"format":"jpeg","quality":92,"maxWidth":780,"maxHeight":1688,"everyNthFrame":1})
  await pg.evaluate("location.search='?z=2&play=1&s=%s'"%k)
  await pg.wait_for_timeout(int(t*1000)+400)
  await cdp.send("Page.stopScreencast");await ctx.close()
  frames.sort(key=lambda x:x[0]);frames=frames[2:] if len(frames)>4 else frames
  t0=frames[0][0];n=int(t*FPS);out=f"assets/video/{k}.mp4"
  p=subprocess.Popen([FF,"-y","-loglevel","error","-f","image2pipe","-r",str(FPS),"-i","-","-vf","scale=780:1688,format=yuv420p","-c:v","libx264","-crf","20","-movflags","+faststart",out],stdin=subprocess.PIPE)
  j=0
  for i in range(n):
    ts=t0+i/FPS
    while j+1<len(frames) and frames[j+1][0]<=ts: j+=1
    p.stdin.write(frames[j][1])
  p.stdin.close();p.wait();print(k,len(frames),"frames")
async def main():
  os.makedirs("assets/video",exist_ok=True)
  async with async_playwright() as p:
    b=await p.chromium.launch(channel="chrome",args=["--window-size=780,1688"])
    for k,t in VIDS.items(): await rec(b,k,t)
    await b.close()
asyncio.run(main())
