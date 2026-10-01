"""Download the source videos (and English captions) into work/video/.

    pip install -r requirements.txt
    python tools/fetch_videos.py

Videos are not committed to git (they're large); the build extracts figure frames from them.
Needs Node.js on PATH (yt-dlp uses it to solve YouTube's JavaScript challenges).
"""
import os, subprocess, sys
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYLIST = 'https://www.youtube.com/playlist?list=PLOSXKDW70aR8uA1IFahSKVuk5ODDfjTZV'
EXTRA = ['7RVY4gUWgz4',   # simulation (ROS2 Gazebo)
         'ZBZORU5--4s',   # earlier upload of "Map your room"
         'jNF1pKFe9b8']   # N20 encoder soldering defect
COMMON = [sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '--sleep-requests', '1',
          '--ffmpeg-location', imageio_ffmpeg.get_ffmpeg_exe(),
          '-f', 'bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]', '--merge-output-format', 'mp4',
          # plain 'en' only: 'en.*' also pulls auto-translations and trips YouTube's rate limit
          '--write-subs', '--sub-langs', 'en', '--sub-format', 'vtt', '--no-overwrites']
out = os.path.join(ROOT, 'work', 'video')
subprocess.run(COMMON + ['-o', os.path.join(out, '%(playlist_index)02d_%(id)s.%(ext)s'), PLAYLIST], check=True)
subprocess.run(COMMON + ['-o', os.path.join(out, 'x_%(id)s.%(ext)s')] +
               [f'https://www.youtube.com/watch?v={v}' for v in EXTRA], check=True)
