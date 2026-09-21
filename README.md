# SMT AI Bot PRO — FINAL

Professional SMT/Smart-Money-style crypto analysis dashboard.

## Included
- Live public market data via CCXT (no exchange key required for market data)
- BTC/USDT + ETH/USDT candle comparison
- SMT divergence detector
- EMA trend filter + ATR risk model
- BUY / SELL / WAIT signal engine
- Paper-trading simulator
- SQLite trade journal
- Telegram alerts
- FastAPI REST API
- Responsive dark dashboard
- Docker deployment
- `.env` configuration

## Important
Default mode is PAPER. No withdrawals are implemented. No profit guarantee is made.
Live order execution is intentionally disabled in this final safe build. You can add a separately audited exchange execution adapter after extensive testing.

## Local run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
uvicorn backend.main:app --reload
```
Open `http://127.0.0.1:8000`

## Telegram
Create a bot with Telegram's official BotFather, put the bot token and chat ID in `.env`, then set `TELEGRAM_ENABLED=true`.

## Docker
```bash
docker compose up --build
```

The engine fetches public candles periodically. It is designed for paper analysis first.
