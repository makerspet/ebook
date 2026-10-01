"""Extract 1 fps thumbnails from each source video and tile them into labelled contact sheets.

Output: work/frames/<video>/tNNNN.jpg (one per second) and work/sheets/<video>_NN.jpg
(4x4 tiles, one every 2 s, each labelled with its m:ss timestamp).
Used only for choosing frame timestamps; the book itself extracts full-res frames at build time.
"""
import glob, os, subprocess, sys
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, 'work')
FF = imageio_ffmpeg.get_ffmpeg_exe()
COLS, ROWS, STEP, W = 4, 4, 2, 480

def key(path):
    return os.path.basename(path).split('.')[0]  # e.g. 01_6GtjAB19GP8

def main(pattern='*'):
    font = ImageFont.truetype('arial.ttf', 28)
    os.makedirs(os.path.join(WORK, 'sheets'), exist_ok=True)
    for mp4 in sorted(glob.glob(os.path.join(WORK, 'video', pattern + '.mp4'))):
        k = key(mp4)
        out = os.path.join(WORK, 'frames', k)
        os.makedirs(out, exist_ok=True)
        if not os.listdir(out):
            # frame i of the fps=1 stream (1-based) is sampled at t = i-1 seconds
            subprocess.run([FF, '-loglevel', 'error', '-i', mp4, '-vf', f'fps=1,scale={W}:-2',
                            '-q:v', '4', '-start_number', '0', os.path.join(out, 't%04d.jpg')], check=True)
        frames = sorted(glob.glob(os.path.join(out, 't*.jpg')))[::STEP]
        th = Image.open(frames[0]).size[1]
        per = COLS * ROWS
        for s in range(0, len(frames), per):
            sheet = Image.new('RGB', (COLS * W, ROWS * th), 'black')
            d = ImageDraw.Draw(sheet)
            for i, f in enumerate(frames[s:s + per]):
                t = int(os.path.basename(f)[1:5])
                x, y = (i % COLS) * W, (i // COLS) * th
                sheet.paste(Image.open(f), (x, y))
                label = f'{t // 60}:{t % 60:02d}'
                d.rectangle([x, y, x + 90, y + 36], fill='black')
                d.text((x + 6, y + 2), label, fill='yellow', font=font)
            sheet.save(os.path.join(WORK, 'sheets', f'{k}_{s // per:02d}.jpg'), quality=80)
        print(k, len(frames) * STEP, 's')

if __name__ == '__main__':
    main(*sys.argv[1:])
