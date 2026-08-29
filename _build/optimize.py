#!/usr/bin/env python3
"""Nén ảnh trong img/ về WebP, bề ngang tối đa MAXW.

Chạy lại nhiều lần vô hại: ảnh đã đạt chuẩn sẽ bị bỏ qua.
Ảnh gốc vẫn lấy lại được từ lịch sử git nếu cần.
"""
import pathlib, sys
from PIL import Image

MAXW, Q = 900, 78
EXT = ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif')
IMG = pathlib.Path(__file__).resolve().parent.parent / 'img'

def main():
    if not IMG.is_dir():
        sys.exit('không thấy thư mục img/')
    files = sorted(p for p in IMG.iterdir()
                   if p.suffix.lower() in EXT and (p.stem.isdigit() or p.stem == 'plate'))
    before = after = 0
    done = skipped = 0
    for src in files:
        n0 = src.stat().st_size
        before += n0
        try:
            im = Image.open(src)
        except Exception as e:
            print(f'  bỏ qua {src.name}: {e}')
            after += n0
            continue
        w, h = im.size
        if src.suffix.lower() == '.webp' and w <= MAXW:
            after += n0; skipped += 1; continue
        if im.mode in ('P', 'RGBA', 'LA'):
            im = im.convert('RGBA' if 'A' in im.mode or im.mode == 'P' else 'RGB')
        if w > MAXW:
            im = im.resize((MAXW, round(h * MAXW / w)), Image.LANCZOS)
        dst = src.with_suffix('.webp')
        tmp = src.with_suffix('.webp.tmp')
        im.save(tmp, 'WEBP', quality=Q, method=6)
        n1 = tmp.stat().st_size
        if n1 >= n0 and w <= MAXW:
            # ảnh gốc đã nhỏ hơn bản nén, giữ nguyên
            tmp.unlink(); after += n0; skipped += 1; continue
        tmp.replace(dst)
        if dst != src:
            src.unlink()
        after += n1; done += 1
        print(f'  {src.name:14} {n0/1024:8.0f} KB -> {dst.name:14} {n1/1024:7.0f} KB'
              f'  ({w}x{h}' + (f' -> {MAXW}px' if w > MAXW else '') + ')')
    print(f'\n{done} ảnh đã nén, {skipped} bỏ qua vì đã đạt chuẩn')
    print(f'tổng: {before/1024/1024:.1f} MB -> {after/1024/1024:.1f} MB'
          f'  (giảm {100*(before-after)/before:.0f}%)' if before else '')

if __name__ == '__main__':
    main()
