import base64, json, re, pathlib, sys

D = pathlib.Path(__file__).parent
BASE = D / 'baseline.html'          # pristine bundle, never overwritten
SRC = D.parent / 'index.html'       # the built page
IMG_ROOT = D.parent

FACES = [
    ('EB Garamond',    500, 'fonts/garamond500.woff2'),
    ('EB Garamond',    700, 'fonts/garamond700.woff2'),
    ('Be Vietnam Pro', 400, 'fonts/bvp400.woff2'),
    ('Be Vietnam Pro', 500, 'fonts/bvp500.woff2'),
    ('Be Vietnam Pro', 600, 'fonts/bvp600.woff2'),
    ('JetBrains Mono', 500, 'fonts/mono500.woff2'),
]

def fonts_css():
    """Ghi 6 file woff2 ra fonts/ và trả về @font-face trỏ tới chúng.

    Trước đây font nhúng base64 khiến index.html phình 118 KB và phải tải
    xong mới hiện được gì. Tách ra file rời thì font tải song song, được
    trình duyệt cache riêng nên lần vào sau gần như tức thì.
    """
    out_dir = IMG_ROOT / 'fonts'
    out_dir.mkdir(exist_ok=True)
    out, tot = [], 0
    for fam, w, rel in FACES:
        raw = (D / rel).read_bytes(); tot += len(raw)
        name = pathlib.Path(rel).name
        (out_dir / name).write_bytes(raw)
        out.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;"
            "src:url(fonts/%s) format('woff2')}" % (fam, w, name))
    print(f'  fonts: {len(FACES)} file rời trong fonts/, {tot/1024:.1f} KB')
    return '\n'.join(out)


def template_line(lines):
    """Vị trí dòng JSON chứa template. Dò theo thẻ chứ không cố định số dòng,
    vì chỉ cần thêm một dòng vào phần <head> là chỉ số cứng sẽ lệch."""
    for i, l in enumerate(lines):
        if l.lstrip().startswith('<script type="__bundler/template"'):
            return i + 1
    sys.exit('FATAL: không tìm thấy thẻ __bundler/template')

# --- canonical milestone list (edit _build/events.json, never the baseline) ---
events = json.loads((D / 'events.json').read_text(encoding='utf-8'))
n_events = len(events)
if n_events != 81:
    sys.exit(f'FATAL: expected 81 events, got {n_events}')
ids = [e['id'] for e in events]
if ids != list(range(1, 82)):
    sys.exit('FATAL: event ids must run 1..81 with no gaps')
data_block = json.dumps({'events': events}, ensure_ascii=False, indent=2)
print(f'  events: {n_events}, ids 1..81 contiguous')

# --- images: img/<id>.<ext> sitting next to index.html ---
IMG_DIR = IMG_ROOT / 'img'
EXT = ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif')
# img/<id>.<ext> holds the illustration for event <id>.
# The Lạc Long Quân – Âu Cơ plate is not an event, so it lives at img/plate.<ext>.
files, origin_img = {}, ''
if IMG_DIR.is_dir():
    for f in sorted(IMG_DIR.iterdir()):
        if f.suffix.lower() not in EXT:
            continue
        if f.stem == 'plate':
            origin_img = 'img/' + f.name
        elif f.stem.isdigit() and 1 <= int(f.stem) <= 81:
            files[int(f.stem)] = 'img/' + f.name
images = files
missing = [i for i in range(1, 82) if i not in images]
gaps = ', '.join(str(i) for i in missing[:6]) + ('…' if len(missing) > 6 else '')
print(f'  images: {len(images)}/81 events wired, plate={"yes" if origin_img else "no"}'
      + (f', missing {gaps}' if missing else ''))


tpl = (D / 'template.src.html').read_text(encoding='utf-8')
imgsrc = json.loads((D / 'imgsrc.json').read_text(encoding='utf-8'))
missing_src = [i for i in range(1, 82) if str(i) not in imgsrc]
if missing_src:
    sys.exit(f'FATAL: thiếu nguồn ảnh cho {missing_src}')
print(f'  imgsrc: {len(imgsrc)}/81 ảnh có nguồn')

for ph in ('/*__FONTS__*/', '/*__DATA__*/', '/*__IMAGES__*/', '/*__ORIGIN_IMG__*/', '/*__IMGSRC__*/'):
    assert ph in tpl, 'placeholder missing: ' + ph
tpl = (tpl.replace('/*__FONTS__*/', fonts_css())
          .replace('/*__DATA__*/', data_block)
          .replace('/*__IMAGES__*/', json.dumps(images, ensure_ascii=False))
          .replace('/*__ORIGIN_IMG__*/', json.dumps(origin_img, ensure_ascii=False))
          .replace('/*__IMGSRC__*/', json.dumps(imgsrc, ensure_ascii=False, indent=2)))
(D / 'template.html').write_text(tpl, encoding='utf-8')

# --- repack: the bundler escapes "</" so the JSON can't terminate its host <script> ---
lines = BASE.read_text(encoding='utf-8').split('\n')
lines[template_line(lines)] = json.dumps(tpl, ensure_ascii=False).replace('</', '<\\u002F')
SRC.write_text('\n'.join(lines), encoding='utf-8')

# --- verify the round trip parses back identically ---
_out = SRC.read_text(encoding='utf-8').split('\n')
back = json.loads(_out[template_line(_out)])
assert back == tpl, 'FATAL: repack round-trip mismatch'
print(f'  template: {len(tpl)/1024:.1f} KB')
print(f'  index.html: {SRC.stat().st_size/1024:.1f} KB  (round-trip verified)')
