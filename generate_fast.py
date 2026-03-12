from PIL import Image, ImageDraw, ImageFilter
import math, os, random, shutil
W,H=1280,720
FRAME_COUNT=180
TEXT='PROMOTIONS'
OUT='/mnt/data/apple_lego_demo/src_frames'
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT, exist_ok=True)
random.seed(7)
FONT={
'A':["01110","10001","10001","11111","10001","10001","10001"],'B':["11110","10001","10001","11110","10001","10001","11110"],'C':["01111","10000","10000","10000","10000","10000","01111"],'D':["11110","10001","10001","10001","10001","10001","11110"],'E':["11111","10000","10000","11110","10000","10000","11111"],'F':["11111","10000","10000","11110","10000","10000","10000"],'G':["01111","10000","10000","10111","10001","10001","01111"],'H':["10001","10001","10001","11111","10001","10001","10001"],'I':["11111","00100","00100","00100","00100","00100","11111"],'J':["00111","00010","00010","00010","10010","10010","01100"],'K':["10001","10010","10100","11000","10100","10010","10001"],'L':["10000","10000","10000","10000","10000","10000","11111"],'M':["10001","11011","10101","10101","10001","10001","10001"],'N':["10001","10001","11001","10101","10011","10001","10001"],'O':["01110","10001","10001","10001","10001","10001","01110"],'P':["11110","10001","10001","11110","10000","10000","10000"],'Q':["01110","10001","10001","10001","10101","10010","01101"],'R':["11110","10001","10001","11110","10100","10010","10001"],'S':["01111","10000","10000","01110","00001","00001","11110"],'T':["11111","00100","00100","00100","00100","00100","00100"],'U':["10001","10001","10001","10001","10001","10001","01110"],'V':["10001","10001","10001","10001","10001","01010","00100"],'W':["10001","10001","10001","10101","10101","10101","01010"],'X':["10001","10001","01010","00100","01010","10001","10001"],'Y':["10001","10001","01010","00100","00100","00100","00100"],'Z':["11111","00001","00010","00100","01000","10000","11111"],}
palette=[(233,57,62),(255,191,46),(32,122,232),(43,180,99),(255,122,32),(114,72,201)]
def eio(t): t=max(0,min(1,t)); return 3*t*t-2*t*t*t
def eoc(t): t=max(0,min(1,t)); return 1-(1-t)**3
def lerp(a,b,t): return a+(b-a)*t
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
# background once
bg=Image.new('RGBA',(W,H),(8,10,18,255))
d=ImageDraw.Draw(bg)
for i,col in enumerate([(18,28,54,255),(10,12,22,255)]):
    d.rectangle((0,i*H//2,W,(i+1)*H//2), fill=col)
glow=Image.new('RGBA',(W,H),(0,0,0,0))
dg=ImageDraw.Draw(glow)
dg.ellipse((150,80,1130,560), fill=(68,108,255,38))
dg.ellipse((360,100,920,520), fill=(255,255,255,18))
glow=glow.filter(ImageFilter.GaussianBlur(70))
bg=Image.alpha_composite(bg,glow)
floor=Image.new('RGBA',(W,H),(0,0,0,0))
ImageDraw.Draw(floor).ellipse((-80,520,W+80,920), fill=(0,0,0,120))
floor=floor.filter(ImageFilter.GaussianBlur(55))
bg=Image.alpha_composite(bg,floor)
# particle layer static positions
particles=[((i*97)%W,(i*53)%H,1+(i%2),18 if i%3 else 28) for i in range(28)]
# bricks definition
scale=13; spacing=2; char_w=5*scale; total_w=len(TEXT)*char_w+(len(TEXT)-1)*spacing*scale; x0=(W-total_w)//2; y0=220
cells=[]; idx=0
for ci,ch in enumerate(TEXT):
    for r,row in enumerate(FONT[ch]):
        for c,bit in enumerate(row):
            if bit=='1':
                x=x0+ci*(char_w+spacing*scale)+c*scale; y=y0+r*scale; color=palette[(idx+r+c+ci)%len(palette)]
                st=idx%4
                if st==0: src=(-260-random.randint(0,140), y+random.randint(-140,140))
                elif st==1: src=(W+220+random.randint(0,140), y+random.randint(-140,140))
                elif st==2: src=(x+random.randint(-220,220), -200-random.randint(0,120))
                else: src=(x+random.randint(-220,220), H+200+random.randint(0,120))
                cells.append({'dest':(x,y),'src':src,'size':scale,'color':color,'delay':idx*0.004,'rot':random.uniform(-18,18)})
                idx+=1
# pre-render bricks
brick_cache={}
for color in palette:
    base=Image.new('RGBA',(scale+24,scale+24),(0,0,0,0)); ox=12; oy=12
    sh=Image.new('RGBA',base.size,(0,0,0,0)); ds=ImageDraw.Draw(sh); ds.rounded_rectangle((ox+1,oy+4,ox+scale+1,oy+scale+4), radius=3, fill=(0,0,0,90)); sh=sh.filter(ImageFilter.GaussianBlur(2)); base=Image.alpha_composite(sh,base)
    dd=ImageDraw.Draw(base); dd.rounded_rectangle((ox,oy,ox+scale,oy+scale), radius=3, fill=color)
    dd.polygon([(ox+scale*0.75,oy),(ox+scale,oy),(ox+scale,oy+scale),(ox+scale*0.88,oy+scale-2),(ox+scale*0.88,oy+2)], fill=shade(color,0.75))
    dd.polygon([(ox,oy+scale*0.72),(ox+scale,oy+scale*0.72),(ox+scale,oy+scale),(ox,oy+scale)], fill=shade(color,0.68))
    hi=Image.new('RGBA',base.size,(0,0,0,0)); dhi=ImageDraw.Draw(hi); dhi.rounded_rectangle((ox+1,oy+1,ox+scale-2,oy+scale*0.45), radius=2, fill=(255,255,255,34)); hi=hi.filter(ImageFilter.GaussianBlur(2)); base=Image.alpha_composite(base,hi); dd=ImageDraw.Draw(base)
    stud_w=max(6,int(scale*0.36)); gap=(scale-2*stud_w)/3; sy=oy+scale*0.2
    for col in range(2):
        sx=ox+gap+col*(stud_w+gap); box=(sx,sy,sx+stud_w,sy+stud_w*0.7); dd.ellipse(box, fill=shade(color,1.08)); dd.ellipse((sx+1,sy+1,sx+stud_w-2,sy+stud_w*0.45), fill=(255,255,255,40)); dd.arc(box,20,200, fill=shade(color,0.8), width=1)
    brick_cache[color]=base
for frame in range(FRAME_COUNT):
    t=frame/(FRAME_COUNT-1)
    img=bg.copy()
    d=ImageDraw.Draw(img)
    for px,py,rr,a in particles:
        yy=(py+int(frame*1.8))%H
        d.ellipse((px,yy,px+rr,yy+rr), fill=(255,255,255,a))
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    pg=eio((t-0.06)/0.8)
    for cell in cells:
        local=eoc((pg-cell['delay'])/0.32)
        sx,sy=cell['src']; dx,dy=cell['dest']; x=lerp(sx,dx,local); y=lerp(sy,dy,local)-math.sin(min(1,local)*math.pi)*12*(1-local)
        if local>0.92: y += math.sin((local-0.92)/0.08*math.pi*2)*1.5*(1-(local-0.92)/0.08)
        brick=brick_cache[cell['color']]
        rot=cell['rot']*(1-local)
        if abs(rot)>0.1: brick=brick.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True)
        layer.alpha_composite(brick,(int(x-12),int(y-12)))
    if t>0.55:
        shine=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(shine); sx=int(lerp(-180,W+180,(t-0.55)/0.35)); ds.polygon([(sx-110,120),(sx-20,120),(sx+220,600),(sx+130,600)], fill=(255,255,255,26)); shine=shine.filter(ImageFilter.GaussianBlur(16)); layer=Image.alpha_composite(layer,shine)
    img=Image.alpha_composite(img,layer)
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); do=ImageDraw.Draw(ov); a=int(255*eio(min(1,t/0.22)))
    do.text((420,82),'Building Promotions', fill=(255,255,255,a)); do.text((356,118),'Scroll-driven frame sequence demo', fill=(220,225,235,int(a*0.72)))
    img=Image.alpha_composite(img,ov)
    img.convert('RGB').save(f'{OUT}/frame_{frame+1:04d}.png', quality=92)
print('done', FRAME_COUNT)
