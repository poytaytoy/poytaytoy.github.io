"""Rebuild the checked-in GIF frame atlas. Requires Pillow; not needed by site builds."""
from PIL import Image
from collections import deque
import json
from pathlib import Path
source = Image.open('public/media/donkey-kong-source.gif')
w, h = source.size
frames, delays = [], []
for i in range(source.n_frames):
    source.seek(i)
    frame = source.convert('RGBA').copy()
    pixels = frame.load()
    queue = deque([(x, y) for x in range(w) for y in (0, h-1)] + [(x, y) for y in range(h) for x in (0, w-1)])
    # White gaps enclosed between the arms and torso are background too.
    # Seed below the face to preserve the whites of the eyes.
    queue.extend((x, y) for y in range(h//2, h) for x in range(w)
                 if min(pixels[x, y][:3]) >= 230)
    seen = set()
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        r, g, b, a = pixels[x, y]
        if min(r, g, b) < 230:
            continue
        pixels[x, y] = (r, g, b, 0)
        queue.extend(((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
    if i == 0:
        frame.save('public/media/donkey-kong-poster.png')
    frames.append(frame)
    delays.append(source.info.get('duration', 100))
atlas = Image.new('RGBA', (w*7, h*2))
for i, frame in enumerate(frames):
    atlas.paste(frame, ((i%7)*w, (i//7)*h))
atlas.save('public/media/donkey-kong-frames.webp', quality=94, method=6)
Path('src/lib/kong-frames.json').write_text(json.dumps({'width':w, 'height':h, 'columns':7, 'delays':delays, 'source':'https://tenor.com/view/donkey-kong-gif-9557225'}))
print(f'{len(frames)} frames; {sum(delays)} ms; {Path("public/media/donkey-kong-frames.webp").stat().st_size} bytes')
