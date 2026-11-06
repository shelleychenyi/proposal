import cv2,numpy as np,sys
from composite import screens
def rect_quad(m):
    cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);c=max(cnts,key=cv2.contourArea)
    r=cv2.minAreaRect(c);(cx,cy),(w,h),a=r
    if w>h: w,h=h,w;a+=90
    box=cv2.boxPoints(((cx,cy),(w,h),a))
    # order tl,tr,br,bl
    s=box.sum(1);d=box[:,0]-box[:,1]
    return np.float32([box[s.argmin()],box[d.argmax()],box[s.argmax()],box[d.argmin()]])
def comp(bg,shots,out):
    img=cv2.imread(bg);ms=screens(img);print(out,len(ms));res=img.astype(np.float32)
    for m,sp in zip(ms,shots):
        q=rect_quad(m);sc=cv2.imread(sp);H,W=sc.shape[:2]
        M=cv2.getPerspectiveTransform(np.float32([[0,0],[W,0],[W,H],[0,H]]),q)
        warp=cv2.warpPerspective(sc,M,(img.shape[1],img.shape[0]),flags=cv2.INTER_AREA).astype(np.float32)
        mm=cv2.dilate(m,np.ones((3,3),np.uint8));mm=cv2.GaussianBlur(mm,(3,3),0).astype(np.float32)/255
        # subtle glass glare: diagonal gradient
        yy,xx=np.mgrid[0:img.shape[0],0:img.shape[1]].astype(np.float32)
        x0,y0=q[0];x1,y1=q[2];t=((xx-x0)/(x1-x0+1e-6)+(yy-y0)/(y1-y0+1e-6))/2
        glare=np.clip(1-np.abs(t-0.25)*6,0,1)*18
        warp=np.clip(warp+glare[...,None],0,255)
        res=res*(1-mm[...,None])+warp*mm[...,None]
    res=res.astype(np.uint8)
    hh,ss,vv=cv2.split(cv2.cvtColor(res,cv2.COLOR_BGR2HSV));sp=((hh>40)&(hh<85)&(ss>140))
    b,g,r=cv2.split(res);g=np.where(sp,np.maximum(b,r),g).astype(np.uint8);res=cv2.merge([b,g,r])
    cv2.imwrite(out,res,[cv2.IMWRITE_JPEG_QUALITY,92])
S="assets/screens/"
comp("assets/mock_raw/hero3_v2.jpg",[S+"buzz.png",S+"home.png",S+"capsule.png"],"assets/mock_hero3.jpg")
comp("assets/mock_raw/hijab_v2.jpg",[S+"home.png"],"assets/mock_hijab_home.jpg")
comp("assets/mock_raw/ramen.jpg",[S+"scan.png"],"assets/mock_ramen_scan.jpg")
comp("assets/mock_raw/friends.jpg",[S+"capsule.png"],"assets/mock_friends_capsule.jpg")
