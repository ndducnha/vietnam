#!/bin/sh
# Dựng lại index.html. Chạy sau khi thêm ảnh vào img/ hoặc sửa _build/*.json
cd "$(dirname "$0")" || exit 1
python3 _build/optimize.py || exit 1
python3 _build/assemble.py
