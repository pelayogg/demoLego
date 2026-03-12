from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, os, random
W, H = 1280, 720
FRAME_COUNT = 180
TEXT = 'PROMOTIONS'
OUT = '/mnt/data/apple_lego_demo/src_frames'
os.makedirs(OUT, exist_ok=True)
random.seed(7)
FONT = {
'A':["01110","10001","10001","11111","10001","10001","10001"],'B':["11110","10001","10001","11110","10001","10001","11110"],'C':["01111","10000","10000","10000","10000","10000","01111"],'D':["11110","10001","10001","10001","10001","10001","11110"],'E':["11111","10000","10000","11110","10000","10000","11111"],'F':["11111","10000","10000","11110","10000","10000","10000"],'G':["01111","10000","10000","10111","10001","10001","01111"],'H':["10001","10001","10001","11111","10001","10001","10001"],'I':["11111","00100","00100","00100","00100","00100","11111"],'J':["00111","00010","00010","00010","10010","10010","01100"],'K':["10001","10010","10100","11000","10100","10010","10001"],'L':["10000","10000","10000","10000","10000","10000","11111"],'M':["10001","11011","10101","10101","10001","10001","10001"],'N':["10001","10001","11001","10101","10011","10001","10001"],'O':["01110","10001","10001","10001","10001","10001","01110"],'P':["11110","10001","10001","11110","10000","10000","10000"],'Q':["01110","10001","10001","10001","10101","10010","01101"],'R':["11110","10001","10001","11110","10100","10010","10001"],'S':["01111","10000","10000","01110","00001","00001","11110"],'T':["11111","00100","00100","00100","00100","00100","00100"],'U':["10001","10001","10001","10001","10001","10001","01110"],'V':["10001","10001","10001","10001","10001","01010","00100"],'W':["10001","10001","10001","10101","10101","10101","01010"],'X':["10001","10001","01010","00100","01010","10001","10001"],'Y':["10001","10001","01010","00100","00100","00100","00100"],'Z':["11111","00001","00010","00100","01000","10000","11111"],
}
palette=[(233,57,62),(255,191,46),(32,122,232),(43,180,99),(255,122,32),(114,72,201)]
def ease_out_cubic(t): t=max(0,min(1,t)); return 1-(1-t)**3
def ease_in_out(t): t=max(0,min(1,t)); return 3*t*t-2*t*t*t
def lerp(a,b,t): return a+(b-a)*t
def build_positions(text):
    scale=13; spacing=2; char_w=5*scale; total_w=len(text)*char_w+(len(text)-1)*spacing*scale; x0=(W-total_w)//2; y0=220; cells=[]; idx=0
    for ci,ch in enumerate(text):
        for r,row in enumerate(FONT[ch]):
            for c,bit in enumerate(row):
                if bit=='1':
                    x=x0+ci*(char_w+spacing*scale)+c*scale; y=y0+r*scale; color=palette[(idx+r+c+ci)%len(palette)]
                    cells.append({'dest':(x,y),'size':scale,'color':color,'delay':idx*0.004,'source_type':idx%4,'rot':random.uniform(-18,18)}); idx+=1
    return cells
cells=build_positions(TEXT)
for i,cell in enumerate(cells):
    dx,dy=cell['dest']; st=cell['source_type']
    if st==0: src=(-180-random.randint(0,120), dy-40+random.randint(-120,120))
    elif st==1: src=(W+180+random.randint(0,120), dy+random.randint(-120,120))
    elif st==2: src=(dx+random.randint(-220,220), -180-random.randint(0,120))
    else: src=(dx+random.randint(-220,220), H+180+random.randint(0,120))
    cell['src']=src
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def draw_brick(base,x,y,s,color,rot=0.0):
    brick=Image.new('RGBA',(s+20,s+20),(0,0,0,0)); ox=10; oy=10
    shadow=Image.new('RGBA',brick.size,(0,0,0,0)); ds=ImageDraw.Draw(shadow)
    ds.rounded_rectangle((ox+1,oy+4,ox+s+1,oy+s+4), radius=max(2,s//4), fill=(0,0,0,90)); shadow=shadow.filter(ImageFilter.GaussianBlur(radius=max(1,s//8)))
    brick=Image.alpha_composite(shadow,brick); d=ImageDraw.Draw(brick)
    d.rounded_rectangle((ox,oy,ox+s,oy+s), radius=max(2,s//4), fill=color)
    d.polygon([(ox+s*0.75,oy),(ox+s,oy),(ox+s,oy+s),(ox+s*0.88,oy+s-2),(ox+s*0.88,oy+2)], fill=shade(color,0.75))
    d.polygon([(ox,oy+s*0.72),(ox+s,oy+s*0.72),(ox+s,oy+s),(ox,oy+s)], fill=shade(color,0.68))
    top=Image.new('RGBA',brick.size,(0,0,0,0)); dt=ImageDraw.Draw(top); dt.rounded_rectangle((ox+1,oy+1,ox+s-2,oy+s*0.45), radius=max(2,s//5), fill=(255,255,255,34)); top=top.filter(ImageFilter.GaussianBlur(radius=2)); brick=Image.alpha_composite(brick,top); d=ImageDraw.Draw(brick)
    stud_w=max(6,int(s*0.36)); gap=(s-2*stud_w)/3; sy=oy+s*0.2
    for col in range(2):
        sx=ox+gap+col*(stud_w+gap); box=(sx,sy,sx+stud_w,sy+stud_w*0.7)
        d.ellipse(box, fill=shade(color,1.08)); d.ellipse((sx+1,sy+1,sx+stud_w-2,sy+stud_w*0.45), fill=(255,255,255,40)); d.arc(box,20,200, fill=shade(color,0.8), width=1)
    if abs(rot)>0.1: brick=brick.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True)
    base.alpha_composite(brick,(int(x-10),int(y-10)))
for frame in range(FRAME_COUNT):
    t=frame/(FRAME_COUNT-1)
    img=Image.new('RGBA',(W,H),(8,10,18,255))
    bg=Image.new('RGBA',(W,H),(0,0,0,0)); p=bg.load()
    for yy in range(H):
        top=yy/H
        for xx in range(W): p[xx,yy]=(int(8+12*(1-top)),int(10+14*(1-top)),int(18+30*(1-top)),255)
    img=Image.alpha_composite(img,bg)
    glow=Image.new('RGBA',(W,H),(0,0,0,0)); dg=ImageDraw.Draw(glow); gy=int(330-40*math.cos(t*math.pi)); dg.ellipse((W*0.18,gy-180,W*0.82,gy+220), fill=(70,110,255,40)); dg.ellipse((W*0.32,120,W*0.68,540), fill=(255,255,255,22)); glow=glow.filter(ImageFilter.GaussianBlur(60)); img=Image.alpha_composite(img,glow)
    floor=Image.new('RGBA',(W,H),(0,0,0,0)); df=ImageDraw.Draw(floor); df.ellipse((-120,500,W+120,900), fill=(0,0,0,110)); floor=floor.filter(ImageFilter.GaussianBlur(50)); img=Image.alpha_composite(img,floor)
    d=ImageDraw.Draw(img)
    for q in range(28):
        px=(q*97)%W; py=int((q*53+frame*1.8)%H); rr=1+(q%2); a=18 if q%3 else 28; d.ellipse((px,py,px+rr,py+rr), fill=(255,255,255,a))
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); pg=ease_in_out((t-0.06)/0.8)
    for cell in cells:
        local=ease_out_cubic((pg-cell['delay'])/0.32); sx,sy=cell['src']; dx,dy=cell['dest']; overs=math.sin(min(1,local)*math.pi)*12*(1-local); x=lerp(sx,dx,local); y=lerp(sy,dy,local)-overs; rot=cell['rot']*(1-local)
        if local>0.92: y += math.sin((local-0.92)/0.08*math.pi*2)*1.8*(1-(local-0.92)/0.08)
        draw_brick(layer,x,y,cell['size'],cell['color'],rot)
    if t>0.55:
        shine=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(shine); sx=int(lerp(-200,W+200,(t-0.55)/0.35)); ds.polygon([(sx-120,120),(sx-20,120),(sx+220,600),(sx+120,600)], fill=(255,255,255,28)); shine=shine.filter(ImageFilter.GaussianBlur(18)); layer=Image.alpha_composite(layer,shine)
    img=Image.alpha_composite(img,layer)
    overlay=Image.new('RGBA',(W,H),(0,0,0,0)); do=ImageDraw.Draw(overlay); ta=int(255*ease_in_out(min(1,t/0.22)))
    if ta>0:
        do.text((W//2-225,80),'Building Promotions', fill=(255,255,255,ta)); do.text((W//2-300,116),'Scroll-driven frame sequence demo', fill=(220,225,235,int(ta*0.75)))
    img=Image.alpha_composite(img,overlay)
    vign=Image.new('L',(W,H),0); dv=ImageDraw.Draw(vign); dv.ellipse((-160,-100,W+160,H+160), fill=190); vign=ImageChops.invert(vign).filter(ImageFilter.GaussianBlur(90)); vv=Image.new('RGBA',(W,H),(0,0,0,120)); img=Image.composite(vv,img,vign)
    img.convert('RGB').save(os.path.join(OUT,f'frame_{frame+1:04d}.png'), quality=95)
print('Generated', FRAME_COUNT)
