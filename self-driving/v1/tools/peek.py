"""Grab full-resolution frames for close reading: python tools/peek.py VIDEO_ID m:ss [m:ss ...] [--crop x,y,w,h]

Writes work/peek/<VIDEO_ID>_<m-ss>.jpg and prints the paths. Crop is in frame fractions.
"""
import glob, os, subprocess, sys
import imageio_ffmpeg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()


def secs(ts):
    s = 0.0
    for p in ts.split(':'):
        s = s * 60 + float(p)
    return s


args = sys.argv[1:]
crop = None
if '--crop' in args:
    i = args.index('--crop'); crop = [float(v) for v in args[i + 1].split(',')]; del args[i:i + 2]
vid, stamps = args[0], args[1:]
mp4 = glob.glob(os.path.join(ROOT, 'work', 'video', f'*{vid}.mp4'))[0]
os.makedirs(os.path.join(ROOT, 'work', 'peek'), exist_ok=True)
for ts in stamps:
    dst = os.path.join(ROOT, 'work', 'peek', f'{vid}_{ts.replace(":", "-")}' + ('_crop' if crop else '') + '.png')
    subprocess.run([FF, '-loglevel', 'error', '-y', '-ss', f'{secs(ts):.3f}', '-i', mp4, '-frames:v', '1', dst], check=True)
    if crop:
        im = Image.open(dst); W, H = im.size; x, y, w, h = crop
        im.crop((int(x * W), int(y * H), int((x + w) * W), int((y + h) * H))).save(dst)
    print(dst)
