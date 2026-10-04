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


def local_image(ref):
    """Copy a local image (path relative to book/, optional #crop=x,y,w,h) into build/img as a JPEG."""
    rel, _, crop = ref.partition('#crop=')
    path = os.path.join(BOOK, rel)
    if not os.path.exists(path):
        sys.exit(f'missing image {path}')
    os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
    name = ('local_' + re.sub(r'[^\w.-]', '_', os.path.splitext(rel)[0])
            + (f'_c{hashlib.md5(crop.encode()).hexdigest()[:6]}' if crop else '') + '.jpg')
    dst = os.path.join(OUT, 'img', name)
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(path):
        im = Image.open(path).convert('RGB')
        if crop:
            x, y, w, h = (float(v) for v in crop.split(','))
            W, H = im.size
            im = im.crop((int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)))
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


def keep_with_figures(body):
    """Keep headings and short lead-in text on the same page as the figure they lead to.

    1. A heading is grouped with what follows it up to and including the first figure, even when
       that figure sits inside step 1 or 2 of a list: the list is split there (numbering continues).
    2. Any other top-level figure is grouped with the short text right before it.
    Groups are capped in size so they always fit on a page.
    """
    from bs4 import BeautifulSoup, NavigableString
    soup = BeautifulSoup(body, 'html.parser')
    MAX_TEXT, MAX_BLOCKS = 700, 4

    def is_fig(el):
        return el.name == 'figure' or (el.name == 'div' and 'pair' in (el.get('class') or []))

    def has_fig(el):
        return is_fig(el) or el.find('figure') is not None

    def is_code(el):
        return el.name == 'pre' or (el.name == 'div' and 'highlight' in (el.get('class') or []))

    def in_keep(el):
        return any('keep' in (p.get('class') or []) for p in el.parents if p.name == 'div')

    def blocks_after(el):
        sib = el.next_sibling
        while sib is not None:
            if not isinstance(sib, NavigableString):
                yield sib
            sib = sib.next_sibling

    def split_list(lst, upto):
        """Move the items after index `upto` of an ol/ul into a new list right after it."""
        items = lst.find_all('li', recursive=False)
        if upto >= len(items) - 1:
            return
        rest = soup.new_tag(lst.name)
        if lst.name == 'ol':
            rest['start'] = str(int(lst.get('start', 1)) + upto + 1)
        for li in items[upto + 1:]:
            rest.append(li.extract())
        lst.insert_after(rest)

    def wrap(els):
        box = soup.new_tag('div', attrs={'class': 'keep'})
        els[0].insert_before(box)
        for el in els:
            box.append(el.extract())

    # 1. headings: heading ... first figure
    for h in soup.find_all(['h2', 'h3'], recursive=False):
        group, size, found = [h], 0, False
        if h.find_previous_sibling() is not None and h.find_previous_sibling().name in ('h2', 'h3'):
            continue  # handled together with the heading above it
        for blk in blocks_after(h):
            if blk.name in ('h2', 'h3') and all(g.name in ('h2', 'h3') for g in group):
                group.append(blk)  # e.g. "## B.9 ..." followed by "### Healthy boot"
                continue
            if blk.name in ('h1', 'h2', 'h3') or len(group) > MAX_BLOCKS or in_keep(blk):
                group = None
                break
            if (is_code(blk) or blk.name == 'table') and not has_fig(blk):
                if size + len(blk.get_text()) <= 2500:  # a code block or table up to about a page
                    group.append(blk)
                    found = True
                else:
                    group = None
                break
            if blk.name in ('ol', 'ul') and not has_fig(blk):
                items = blk.find_all('li', recursive=False)
                if items and size + len(items[0].get_text()) <= MAX_TEXT:
                    split_list(blk, 0)
                    group.append(blk)
                    found = True
                    nxt = blk.find_next_sibling()
                    if nxt is not None and is_fig(nxt):  # a figure right after step 1 joins too
                        group.append(nxt)
                else:
                    group = None
                break
            if is_fig(blk):
                group.append(blk)
                found = True
                break
            if blk.name in ('ol', 'ul') and has_fig(blk):
                items = blk.find_all('li', recursive=False)
                k = next(i for i, li in enumerate(items) if li.find('figure') is not None)
                size += sum(len(li.get_text()) for li in items[:k])
                if k > 2 or size > MAX_TEXT:
                    group = None
                    break
                split_list(blk, k)
                group.append(blk)
                found = True
                break
            if has_fig(blk) or blk.name not in ('p', 'ol', 'ul', 'pre', 'div'):
                group = None
                break
            size += len(blk.get_text())
            if size > MAX_TEXT:
                group = None
                break
            group.append(blk)
        if group and found:
            wrap(group)

    # 2. other top-level figures: short text right before them
    for fig in [c for c in soup.contents if not isinstance(c, NavigableString) and is_fig(c)]:
        lead, size = [], 0
        prev = fig.find_previous_sibling()
        while prev is not None and len(lead) < 3:
            if not (prev.name in ('h2', 'h3', 'p', 'ol', 'ul') or is_code(prev)) or has_fig(prev) or in_keep(prev):
                break
            if prev.name in ('ol', 'ul') and len(prev.get_text()) > MAX_TEXT // 2:
                items = prev.find_all('li', recursive=False)
                if len(items) > 1:  # keep only the last step with the figure
                    split_list(prev, len(items) - 2)
                    prev = prev.find_next_sibling()
            size += len(prev.get_text())
            if size > MAX_TEXT:
                break
            lead.insert(0, prev)
            if prev.name in ('h2', 'h3'):
                break
            prev = prev.find_previous_sibling()
        if lead:
            wrap(lead + [fig])
    return str(soup)


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
        md = markdown.Markdown(extensions=['abbr', 'attr_list', 'def_list', 'footnotes', 'md_in_html', 'tables',
                                           'pymdownx.superfences',  # code fences inside list items
                                           'admonition', 'sane_lists', 'toc'],
                               extension_configs={'toc': {'slugify': lambda v, s: slug(v)}})
        body = md.convert(figures(text, labels))
        body = keep_with_figures(body)
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
    meta = dict(line.split(':', 1) for line in open(os.path.join(BOOK, 'edition.txt'), encoding='utf-8')
                if ':' in line)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    page = (page.replace('{{edition}}', meta['edition']).replace('{{date}}', meta['date'])
                .replace('{{year}}', meta['date'].split()[-1]))
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
