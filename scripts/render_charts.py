"""Render original data charts; no generated robot footage."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,csv,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets";OUT.mkdir(exist_ok=True)
F="/System/Library/Fonts/Supplemental/Arial.ttf"
FB="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def font(n,b=False):return ImageFont.truetype(FB if b else F,n)
BG="#f2f0e9";INK="#172527";MUTED="#5c6c6d";GREEN="#007e6b";BLUE="#636bdf"
data=json.loads((ROOT/"data/reported.json").read_text())
def frame(c,progress=1):
 im=Image.new("RGB",(1280,720),BG);d=ImageDraw.Draw(im)
 d.text((64,42),"DIGDEEP / ROBOT USE LAB",font=font(18,True),fill=MUTED)
 d.text((64,95),"Change the task.",font=font(57,True),fill=INK)
 d.text((64,157),"Watch the winner change.",font=font(57,True),fill=GREEN)
 d.text((64,252),c["label"].upper(),font=font(24,True),fill=INK)
 for y,label,val,col in [(336,"PEAR",c["pear"],GREEN),(454,"pi0.5",c["pi05"],BLUE)]:
  d.text((64,y),label,font=font(30,True),fill=INK)
  d.rounded_rectangle((245,y,1085,y+48),radius=6,fill="#e0e5df")
  w=max(4,840*val/100*progress)
  d.rounded_rectangle((245,y,245+w,y+48),radius=5,fill=col)
  d.text((1112,y+2),f"{val:g}%",font=font(29,True),fill=col)
 d.text((64,568),"SUCCESS RATE (%) / AUTHOR-REPORTED RESULTS",font=font(18,True),fill=MUTED)
 d.text((64,606),"PEAR: LIBERO-only, xhigh. pi0.5: published baseline; not a new matched run.",font=font(18),fill=MUTED)
 d.text((64,646),"Source: PEAR paper, Tables 2-3. Chart animation, no model inference.",font=font(18),fill=MUTED)
 return im
frames=[]
for c in data["conditions"]:
 for i in range(30):frames.append(frame(c,min(1,(i+1)/9)))
frame(data["conditions"][1]).save(OUT/"changed-goal.png")
frame(data["conditions"][0]).save(OUT/"standard-libero.png")
frames[0].save(OUT/"benchmark-switch.gif",save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
with (ROOT/"data/real_trials.csv").open() as h:rows=list(csv.DictReader(h))
im=Image.new("RGB",(1280,850),BG);d=ImageDraw.Draw(im)
d.text((64,42),"DIGDEEP / ROBOT USE LAB",font=font(18,True),fill=MUTED)
d.text((64,96),"18 successes. 12 failures.",font=font(58,True),fill=INK)
d.text((64,177),"Every final-model trial in the paper's real-robot evaluation.",font=font(25),fill=MUTED)
for i,r in enumerate(rows):
 x=64+(i%10)*116;y=252+(i//10)*110
 good=int(r["pear_success"]);col=GREEN if good else "#b66d35"
 d.rounded_rectangle((x,y,x+100,y+90),radius=12,fill=col)
 d.text((x+17,y+12),f"{i+1:02d}",font=font(25,True),fill="white")
 d.text((x+17,y+53),"PASS" if good else "FAIL",font=font(14,True),fill="white")
d.text((64,626),"6 round limits   /   3 unaligned   /   2 toppled   /   1 ball rolled away",font=font(23,True),fill=INK)
d.text((64,685),"Two trials per scene/object. Final model: LIBERO + RoboDojo simulation training.",font=font(19),fill=MUTED)
d.text((64,727),"Source: PEAR paper Table 7. Independent visualization of reported outcomes.",font=font(19),fill=MUTED)
d.text((64,769),"No new robot trials were performed for this analysis.",font=font(19),fill=MUTED)
im.save(OUT/"real-trials.png")
print("Rendered benchmark GIF and three PNG charts.")

