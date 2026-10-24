"""Render the self-hosted profile banner with Pillow."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 1120, 350
FONT = '/usr/share/fonts/TTF/DejaVuSans.ttf'
title = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans-Bold.ttf', 66)
small = ImageFont.truetype(FONT, 12)
body = ImageFont.truetype(FONT, 21)
mark = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans-Bold.ttf', 50)
bg = Image.new('RGB', (W, H))
pixels = bg.load()
for y in range(H):
    for x in range(W):
        glow = math.exp(-(((x - 916) / 235) ** 2 + ((y - 165) / 210) ** 2))
        pixels[x, y] = (int(11 + 29 * glow), int(15 + 6 * glow), int(24 + 10 * glow))
d = ImageDraw.Draw(bg)
for x in range(23, W, 28):
    for y in range(22, H, 28):
        d.point((x, y), fill=(33, 36, 47))
d.rounded_rectangle((1, 1, W-2, H-2), radius=20, outline='#33303b')
d.line((47, 46, 73, 46), fill='#ff735c', width=2)
d.text((86, 37), 'DEVELOPER  /  BUILDER  /  TINKERER', font=small, fill='#b5b9c9')
d.text((43, 92), "hey, i'm Red.", font=title, fill='#f4f2f5')
d.line((48, 269, 710, 269), fill='#2d303d')
d.text((48, 289), 'BASED IN CURIOSITY. BUILT WITH CODE.', font=small, fill='#8e94a9')
cx, cy = 911, 163
for r in (64, 94, 124):
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline='#49323b')
d.rounded_rectangle((cx-43,cy-43,cx+43,cy+43),radius=22,fill='#191c29',outline='#ff735c',width=2)
d.text((cx,cy-3),'R',font=mark,fill='#ff9a80',anchor='mm')
d.text((870, 308), '< / >', font=body, fill='#a5807e')
phrases = ['building for the web.', 'exploring AI & automation.']
frames = []
for frame in range(100):
    im = bg.copy()
    draw = ImageDraw.Draw(im)
    phrase = phrases[frame // 50]
    phase = frame % 50
    length = min(len(phrase), int(phase*1.4)) if phase < 39 else max(0,len(phrase)-(phase-39)*3)
    text = phrase[:length]
    draw.text((49, 202), '> ', font=body, fill='#ff735c')
    draw.text((79, 202), text, font=body, fill='#c4cadb')
    if frame % 8 < 5:
        end = 79 + draw.textlength(text, font=body)
        draw.rectangle((end+4, 205, end+14, 225), fill='#ff735c')
    for i, radius in enumerate((64, 94, 124)):
        angle = frame/100*math.tau*(1 if i != 1 else -1)+i*2.1
        x, y = cx+radius*math.cos(angle), cy+radius*math.sin(angle)
        for size,color in ((10,'#35222d'),(6,'#6f393c'),(3,'#ffac89')):
            draw.ellipse((x-size,y-size,x+size,y+size),fill=color)
    frames.append(im.quantize(colors=96))
frames[0].save(ROOT/'assets/header.gif',save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=1)
frames[26].convert('RGB').save('/tmp/github-profile-header-preview.png')
print(f'Generated {len(frames)} frames; {(ROOT/"assets/header.gif").stat().st_size:,} bytes')
