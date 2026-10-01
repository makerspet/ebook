# Authoring conventions

Chapters live in `book/NN-slug.md` and are assembled in file-name order.
`00-*.md` is front matter (no TOC entry); every other file becomes one TOC entry from its `# ` heading.

## Figures from the videos

```markdown
![Caption sentence.](yt:VIDEO_ID@m:ss)
![Caption sentence.](yt:VIDEO_ID@m:ss.s#crop=x,y,w,h)
```

- `VIDEO_ID` is the 11-character YouTube ID; `m:ss` may have a decimal (`2:24.5`).
- `crop` is in fractions of the 1920×1080 frame: left, top, width, height (e.g. `0.25,0.1,0.5,0.6`).
  Use it to zoom into a terminal, a browser address bar, a dialog or a small part on the board.
- To review or fix a frame: open the draft PDF, click the orange `VIDEO_ID @ m:ss` link under the
  figure (opens YouTube at that second), pick a better moment, edit the timestamp, rebuild.
- Two small figures side by side:

  ```markdown
  <div class="pair" markdown="1">
  ![Left.](yt:ID@1:40)
  ![Right.](yt:ID@1:50)
  </div>
  ```

- Ordinary images (`![Caption](https://...)`) work too, e.g. illustrations from makerspet.com or
  the support forum; they are downloaded and cached at build time.

## Chapter shape

```markdown
# 3. Upload the Firmware and Bring Up the Robot

Video: [Step by Step Arduino LiDAR Robot Bringup](https://youtu.be/tKfVU1n5TjA)
{: .video-link }

One or two paragraphs: what you will do, what you need before starting, roughly how long it takes.

## Section per phase of the video
1. Numbered, imperative steps, one action each.
   Commands transcribed exactly from the screen as fenced code blocks.
![Caption.](yt:...)
```

- Voice: the author's (Ilia's) friendly, plain, second-person instructions, as in the narration.
  Write for a beginner; explain briefly *why* where the video only says *what*.
- One figure per meaningful step, not per sentence; typically 12–30 per chapter.
  Prefer frames where the on-screen text overlay is fully visible; the overlays often summarise the step.
- Callouts:
  - `!!! tip`, `!!! note`, `!!! warning` for ordinary advice.
  - `!!! update "Since the video was recorded"` for corrections and additions from the bring-up and
    troubleshooting guide (makerspet.com/blog/bld-120mm-pack/). This keeps the video and the book
    consistent while flagging what changed.
  - `!!! draft "Question for Ilia"` for anything you could not verify or that needs the author's
    decision. Shown in draft builds only.
- Don't invent facts, part numbers, commands or URLs. If the screen is unreadable, say so in a
  `!!! draft` callout rather than guessing.
- Don't paste long passages from third-party pages (Arduino, Docker, Microsoft docs); link to them.

## Building

```
python tools/build.py           # build/ebook-draft.pdf, with figure timestamps
python tools/build.py --final   # build/ebook.pdf
python tools/peek.py VIDEO_ID 1:23 1:25 [--crop x,y,w,h]   # full-res frames into work/peek/
python tools/preview.py build/ebook-draft.pdf 5 12         # PDF pages -> work/preview/*.png
```
