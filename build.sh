#!/bin/sh
# Rebuild index.html from _build/ after adding images to img/ or editing _build/extras.json
cd "$(dirname "$0")" && python3 _build/assemble.py
