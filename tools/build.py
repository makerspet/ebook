"""Build the e-book PDF from book/*.md.

    python tools/build.py                # draft: open questions (!!! draft) shown
    python tools/build.py --final        # final: no draft notes
    python tools/build.py --timestamps   # also label each figure with its timestamp / file name

Figures are written in Markdown as

    ![Caption text](yt:VIDEO_ID@m:ss.s)
    ![Caption text](yt:VIDEO_ID@m:ss.s#crop=x,y,w,h)     crop as fractions of the frame

The frame is grabbed from work/video/*<VIDEO_ID>.mp4 at build time (download the videos
first, see README). Edit the timestamp and rebuild to swap an illustration.
Ordinary image URLs/paths also work; remote images are cached in work/cache/.
"""
import argparse, glob, hashlib, html, os, re, subprocess, sys, urllib.request

import imageio_ffmpeg
import markdown
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, 'book')
WORK = os.path.join(ROOT, 'work')
OUT = os.path.join(ROOT, 'build')
FF = imageio_ffmpeg.get_ffmpeg_exe()
PAGED_JS = 'https://unpkg.com/pagedjs@0.4.3/dist/paged.polyfill.js'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36'
FIG_WIDTH = 1400  # px; frames are downscaled to keep the PDF small

FIG_RE = re.compile(r'!\[([^\]]*)\]\(yt:([\w-]{11})@([\d:.]+)(?:#crop=([\d.,]+))?\)')


def seconds(ts):
    s = 0.0
    for part in ts.split(':'):
        s = s * 60 + float(part)
    return s


def video_path(vid):
    hits = glob.glob(os.path.join(WORK, 'video', f'*{vid}.mp4'))
    if not hits:
        sys.exit(f'missing video for {vid}; download it into work/video/ (see README)')
    return hits[0]


def grab(vid, ts, crop):
    os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
    name = f'{vid}_{ts.replace(":", "-")}' + (f'_c{hashlib.md5(crop.encode()).hexdigest()[:6]}' if crop else '') + '.jpg'
    dst = os.path.join(OUT, 'img', name)
    if not os.path.exists(dst):
        raw = dst + '.png'
        subprocess.run([FF, '-loglevel', 'error', '-y', '-ss', f'{seconds(ts):.3f}', '-i', video_path(vid),
                        '-frames:v', '1', raw], check=True)
        im = Image.open(raw).convert('RGB')
        if crop:
            x, y, w, h = (float(v) for v in crop.split(','))
            W, H = im.size
            im = im.crop((int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)))
        if im.width > FIG_WIDTH:
            im = im.resize((FIG_WIDTH, round(im.height * FIG_WIDTH / im.width)), Image.LANCZOS)
        im.save(dst, quality=80, optimize=True)
        os.remove(raw)
    return 'img/' + name


def local_image(rel):
    """Copy a local image (path relative to book/) into build/img as a downscaled JPEG."""
    path = os.path.join(BOOK, rel)
    if not os.path.exists(path):
        sys.exit(f'missing image {path}')
    os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
    name = 'local_' + re.sub(r'[^\w.-]', '_', os.path.splitext(rel)[0]) + '.jpg'
    dst = os.path.join(OUT, 'img', name)
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(path):
        im = Image.open(path).convert('RGB')
        if im.width > FIG_WIDTH:
            im = im.resize((FIG_WIDTH, round(im.height * FIG_WIDTH / im.width)), Image.LANCZOS)
        im.save(dst, quality=84, optimize=True)
    return 'img/' + name


def fetch(url):
    os.makedirs(os.path.join(WORK, 'cache'), exist_ok=True)
    dst = os.path.join(WORK, 'cache', hashlib.md5(url.encode()).hexdigest()[:12] + '.jpg')
    if not os.path.exists(dst):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        raw = dst + '.raw'
        with urllib.request.urlopen(req) as r, open(raw, 'wb') as f:
            f.write(r.read())
        im = Image.open(raw).convert('RGB')  # normalise webp/png/gif to jpg
        if im.width > FIG_WIDTH:
            im = im.resize((FIG_WIDTH, round(im.height * FIG_WIDTH / im.width)), Image.LANCZOS)
        im.save(dst, quality=86)
        os.remove(raw)
    return dst


IMG_LINE_RE = re.compile(r'^([ \t]*)!\[([^\]]*)\]\(([^)\s]+)\)[ \t]*$')


def figures(md_text, labels):
    """Turn every image that sits on a line of its own into a captioned <figure>.

    yt: references become frames extracted from the video. A figure keeps its line's
    indentation so that it stays inside the list item it belongs to.
    """
    out = []
    for line in md_text.split('\n'):
        m = IMG_LINE_RE.match(line)
        if not m:
            out.append(line)
            continue
        indent, cap, src = m.groups()
        chip = ''
        y = FIG_RE.match(f'![]({src})')
        if y:
            _, vid, ts, crop = y.groups()
            src = grab(vid, ts, crop)
            if labels:
                chip = (f'<a class="ts" href="https://youtu.be/{vid}?t={int(seconds(ts))}">{vid} @ {ts}'
                        f'{" crop " + crop if crop else ""}</a>')
        elif not re.match(r'https?://', src):  # a local image, e.g. a hand-picked frame in book/frames/
            label = src
            src = local_image(src)
            if labels:
                chip = f'<span class="ts">{html.escape(label)}</span>'
        cap_html = markdown.markdown(cap)[3:-4] if cap else ''
        fig = (f'{indent}<figure><img src="{src}" alt="{html.escape(cap)}">'
               f'<figcaption>{cap_html}{chip}</figcaption></figure>')
        out.append(fig if indent else f'\n{fig}\n')  # top-level figures must be HTML blocks
    return '\n'.join(out)


def remote_images(html_text):
    def sub_url(url):
        return f'src="file:///{fetch(url).replace(os.sep, "/")}"'
    return re.sub(r'<img([^>]*?) src="(https?://[^"]+)"', lambda m: f'<img{m.group(1)} ' + sub_url(m.group(2)), html_text)


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def build(draft, labels):
    os.makedirs(OUT, exist_ok=True)
    files = sorted(glob.glob(os.path.join(BOOK, '[0-9]*.md')))
    chapters, toc = [], []
    for path in files:
        text = open(path, encoding='utf-8').read()
        if not draft:
            text = re.sub(r'(?s)<!--.*?-->', '', text)
        md = markdown.Markdown(extensions=['extra', 'admonition', 'sane_lists', 'toc'],
                               extension_configs={'toc': {'slugify': lambda v, s: slug(v)}})
        body = md.convert(figures(text, labels))
        kind = 'front' if os.path.basename(path).startswith('00') else 'chapter'
        m = re.search(r'<h1 id="([^"]+)">(.*?)</h1>', body)
        if m and kind == 'chapter':
            toc.append((m.group(1), re.sub('<[^>]+>', '', m.group(2))))
            # move "3." / "Appendix B." into data-num so the running header shows just the title
            n = re.match(r'((?:Appendix [A-Z]|\d+)\.)\s+(.*)', m.group(2), re.S)
            if n:
                body = body.replace(m.group(0), f'<h1 id="{m.group(1)}" data-num="{n.group(1)}">{n.group(2)}</h1>', 1)
        chapters.append(f'<section class="{kind}">\n{body}\n</section>')
    toc_html = '\n'.join(f'<li><a href="#{a}"><span class="t">{html.escape(t)}</span><span class="dots"></span><span class="pn"></span></a></li>' for a, t in toc)
    tpl = open(os.path.join(BOOK, 'template.html'), encoding='utf-8').read()
    page = (tpl.replace('{{css}}', open(os.path.join(BOOK, 'style.css'), encoding='utf-8').read())
               .replace('{{toc}}', toc_html)
               .replace('{{body}}', '\n'.join(chapters))
               .replace('{{draft}}', 'draft' if draft else 'final')
               .replace('{{pagedjs}}', PAGED_JS))
    page = re.sub(r'src="yt:([\w-]{11})@([\d:.]+)(?:#crop=([\d.,]+))?"',  # cover image in the template
                  lambda m: f'src="{grab(*m.groups())}"', page)
    page = page.replace('src="assets/', f'src="file:///{BOOK.replace(os.sep, "/")}/assets/')  # cover art
    page = remote_images(page)
    name = 'ebook-draft' if draft else 'ebook'
    html_path = os.path.join(OUT, name + '.html')
    open(html_path, 'w', encoding='utf-8').write(page)
    pdf_path = os.path.join(OUT, name + '.pdf')
    render_pdf(html_path, pdf_path)
    print('wrote', pdf_path)


def render_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome')
        page = browser.new_page()
        page.goto('file:///' + html_path.replace(os.sep, '/'))
        page.wait_for_function('window.__pagedDone === true', timeout=300_000)
        # paged.js target-counter() is unreliable, so number the TOC from the laid-out pages
        page.evaluate("""() => document.querySelectorAll('.toc a').forEach(a => {
            const el = document.getElementById(decodeURIComponent(a.hash.slice(1)));
            const pg = el && el.closest('.pagedjs_page');
            if (pg) a.querySelector('.pn').textContent = pg.dataset.pageNumber;
        })""")
        page.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        browser.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--final', action='store_true', help='omit draft notes')
    ap.add_argument('--timestamps', action='store_true',
                    help='label each figure with its video timestamp or file name')
    a = ap.parse_args()
    build(draft=not a.final, labels=a.timestamps)
