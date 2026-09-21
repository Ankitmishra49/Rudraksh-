#!/bin/sh
python3 -m pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
