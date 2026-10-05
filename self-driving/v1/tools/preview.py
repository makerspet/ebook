"""Render PDF pages to PNG for a quick look: python tools/preview.py build/ebook-draft.pdf [first] [last]"""
import os, sys
import fitz

pdf = fitz.open(sys.argv[1])
first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
last = int(sys.argv[3]) if len(sys.argv) > 3 else pdf.page_count
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'work', 'preview')
os.makedirs(out, exist_ok=True)
print(pdf.page_count, 'pages')
for i in range(first - 1, min(last, pdf.page_count)):
    p = os.path.join(out, f'p{i + 1:03d}.png')
    pdf[i].get_pixmap(dpi=60).save(p)
    print(p)
