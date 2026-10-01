# Build an Arduino, ROS 2 Self-Driving Robot

Source for the PDF e-book that accompanies the Maker's Pet video course
([YouTube playlist](https://www.youtube.com/watch?v=6GtjAB19GP8&list=PLOSXKDW70aR8uA1IFahSKVuk5ODDfjTZV))
for the BLD-120MM-PACK Arduino/ESP32/ROS 2 LiDAR robot.

The chapters are Markdown files in [book/](book/). The illustrations are frames from the course videos,
referenced by YouTube ID and timestamp, e.g. `![Press the wheel on.](yt:6GtjAB19GP8@2:24)`, and
extracted at build time. See [book/AUTHORING.md](book/AUTHORING.md) for the conventions.

## Build

Requirements: Python 3.10+, Google Chrome, Node.js (for yt-dlp).

```
pip install -r requirements.txt
python tools/fetch_videos.py        # once: downloads the videos into work/ (git-ignored)
python tools/build.py               # build/ebook-draft.pdf, with open questions
python tools/build.py --timestamps  # same, each figure labelled with its timestamp or file name
python tools/build.py --final       # build/ebook.pdf
```

## Reviewing figures

Build with `--timestamps` to label every figure with an orange `VIDEO_ID @ m:ss` link that opens
YouTube at that moment. To change a figure, edit the timestamp (and optional `#crop=x,y,w,h`) in the chapter's `.md`
file and rebuild. `!!! draft` boxes are open questions; they only appear in the draft build.

Helpers: `tools/peek.py` grabs full-resolution frames, `tools/contact_sheets.py` makes timestamped
thumbnail sheets for picking frames, and `tools/preview.py` renders PDF pages to PNG.
