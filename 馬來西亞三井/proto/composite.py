import cv2,numpy as np,sys
def screens(img):
    h,s,v=cv2.split(cv2.cvtColor(img,cv2.COLOR_BGR2HSV))
    m=((h>40)&(h<85)&(s>120)&(v>120)).astype(np.uint8)*255
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m)
    comps=[i for i in range(1,n) if st[i,4]>20000]
    comps.sort(key=lambda i:st[i,0])
    return [(lab==i).astype(np.uint8)*255 for i in comps]
def quad(mask):
    ys,xs=np.nonzero(mask);pts=np.stack([xs,ys],1).astype(np.float32)
    hull=cv2.convexHull(pts).reshape(-1,2)
    # fit 4-gon
    peri=cv2.arcLength(hull,True)
    for e in np.linspace(0.01,0.1,40):
        ap=cv2.approxPolyDP(hull,e*peri,True).reshape(-1,2)
        if len(ap)==4:break
    if len(ap)!=4:
        s=pts.sum(1);d=pts[:,0]-pts[:,1]
        ap=np.array([pts[s.argmin()],pts[d.argmax()],pts[s.argmax()],pts[d.argmin()]])
    # order tl,tr,br,bl
    c=ap.mean(0);ang=np.arctan2(ap[:,1]-c[1],ap[:,0]-c[0]);ap=ap[np.argsort(ang)]
    # argsort from -pi: order tl? ensure start at top-left
    i=np.argmin(ap.sum(1));ap=np.roll(ap,-i,0)
    # angles ascending go tl->tr->br->bl in image coords (y down) 
    return ap.astype(np.float32)
def comp(bg_path,shots,out,expand=1.02):
    img=cv2.imread(bg_path);ms=screens(img);print(out,len(ms),"screens")
    res=img.copy()
    for m,sp in zip(ms,shots):
        q=quad(m);c=q.mean(0);q=(q-c)*expand+c
        sc=cv2.imread(sp);H,W=sc.shape[:2]
        M=cv2.getPerspectiveTransform(np.float32([[0,0],[W,0],[W,H],[0,H]]),q)
        warp=cv2.warpPerspective(sc,M,(img.shape[1],img.shape[0]),flags=cv2.INTER_AREA)
        mm=cv2.dilate(m,np.ones((5,5),np.uint8))
        mm=cv2.GaussianBlur(mm,(5,5),0).astype(np.float32)/255
        res=(res*(1-mm[...,None])+warp*mm[...,None]).astype(np.uint8)
    # despill leftover green
    hh,ss,vv=cv2.split(cv2.cvtColor(res,cv2.COLOR_BGR2HSV))
    sp=((hh>40)&(hh<85)&(ss>140)).astype(np.uint8)
    b,g,r=cv2.split(res);g=np.where(sp,np.maximum(b,r),g).astype(np.uint8);res=cv2.merge([b,g,r])
    cv2.imwrite(out,res,[cv2.IMWRITE_JPEG_QUALITY,92])
S="assets/screens/"
comp("assets/mock_raw/hero3.jpg",[S+"buzz.png",S+"home.png",S+"capsule.png"],"assets/mock_hero3.jpg")
comp("assets/mock_raw/hijab.jpg",[S+"home.png"],"assets/mock_hijab_home.jpg")
comp("assets/mock_raw/ramen.jpg",[S+"scan.png"],"assets/mock_ramen_scan.jpg")
comp("assets/mock_raw/friends.jpg",[S+"capsule.png"],"assets/mock_friends_capsule.jpg")
