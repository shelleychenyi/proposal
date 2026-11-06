import cv2,numpy as np,sys
def key(src,out,thr=70,soft=40):
    img=cv2.imread(src).astype(np.float32);h,w=img.shape[:2]
    corners=np.concatenate([img[:20,:20].reshape(-1,3),img[:20,-20:].reshape(-1,3),img[-20:,:20].reshape(-1,3),img[-20:,-20:].reshape(-1,3)])
    bg=np.median(corners,0)
    # local bg estimate (gradient bg): blur of image where close to bg
    d=np.linalg.norm(img-bg,axis=2)
    near=(d<thr+30).astype(np.uint8)
    # connected-to-border region
    n,lab=cv2.connectedComponents(near)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bgmask=np.isin(lab,list(border))
    # chroma-ish distance: magenta-ness = (r+b)/2 - g
    a=np.clip((d-thr)/soft,0,1)
    alpha=a  # global key (handles enclosed bg)
    alpha=cv2.GaussianBlur(alpha.astype(np.float32),(3,3),0)
    # despill: where partially transparent pull toward neutral
    b,g,r=cv2.split(img);m=np.minimum(r,b);sp=np.clip(m-g,0,None)*(1-alpha)
    b=b-sp*0.8;r=r-sp*0.8
    rgba=cv2.merge([np.clip(b,0,255),np.clip(g,0,255),np.clip(r,0,255),alpha*255]).astype(np.uint8)
    ys,xs=np.nonzero(alpha>0.05);rgba=rgba[max(0,ys.min()-10):ys.max()+10,max(0,xs.min()-10):xs.max()+10]
    cv2.imwrite(out,rgba);print(out,rgba.shape)
for k in ["levelup","play","ask","buzz","tiers"]:
    key(f"assets/world/raw_{k}.jpg",f"assets/world/{k}.png")
