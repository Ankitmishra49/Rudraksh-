import os, sqlite3, threading, time
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.market import exchange,candles
from backend.engine import analyze
from backend.risk import levels,quantity
from backend.telegram import send

load_dotenv()
app=FastAPI(title="SMT AI Bot PRO",version="2.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

DB="smt_bot.db"; STATE={"analysis":None,"error":None,"last_alert":""}

def db():
    c=sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS trades(
      id INTEGER PRIMARY KEY, created_at TEXT, symbol TEXT, side TEXT,
      entry REAL, stop REAL, target REAL, quantity REAL, status TEXT)""")
    c.commit(); return c

def config():
    return {
      "mode":os.getenv("MODE","paper"),
      "exchange":os.getenv("EXCHANGE","binance"),
      "a":os.getenv("SYMBOL_A","BTC/USDT"),
      "b":os.getenv("SYMBOL_B","ETH/USDT"),
      "timeframe":os.getenv("TIMEFRAME","15m"),
      "risk":float(os.getenv("RISK_PER_TRADE","0.01"))
    }

def scan():
    ex=exchange(config()["exchange"])
    a=candles(ex,config()["a"],config()["timeframe"],int(os.getenv("LOOKBACK","250")))
    b=candles(ex,config()["b"],config()["timeframe"],int(os.getenv("LOOKBACK","250")))
    result=analyze(a,b)
    lv=levels(result["signal"],result["price"],result["atr"],float(os.getenv("RR","2")))
    if lv:
        result["levels"]=lv
        result["quantity"]=quantity(float(os.getenv("INITIAL_BALANCE","100000")),lv["entry"],lv["stop"],config()["risk"])
    STATE["analysis"]=result; STATE["error"]=None
    if result["signal"]!="WAIT" and result["confidence"]>=.70:
        stamp=result["timestamp"]+result["signal"]
        if STATE["last_alert"]!=stamp:
            msg=(f"SMT SIGNAL\\n{config()['a']} vs {config()['b']}\\n"
                 f"{result['signal']} | confidence {result['confidence']:.0%}\\n"
                 f"Entry: {result['price']:.4f}\\nReason: {result['reason']}")
            send(os.getenv("TELEGRAM_ENABLED","false").lower()=="true",
                 os.getenv("TELEGRAM_BOT_TOKEN",""),os.getenv("TELEGRAM_CHAT_ID",""),msg)
            STATE["last_alert"]=stamp

def worker():
    while True:
        try: scan()
        except Exception as e: STATE["error"]=str(e)
        time.sleep(int(os.getenv("POLL_SECONDS","30")))

@app.on_event("startup")
def startup():
    db().close()
    threading.Thread(target=worker,daemon=True).start()

@app.get("/api/health")
def health(): return {"status":"online","mode":config()["mode"],"error":STATE["error"]}

@app.get("/api/config")
def get_config(): return config()

@app.get("/api/analysis")
def analysis(): return STATE

@app.post("/api/paper/open")
def paper_open(payload:dict):
    c=db()
    c.execute("""INSERT INTO trades(created_at,symbol,side,entry,stop,target,quantity,status)
      VALUES(?,?,?,?,?,?,?,?)""",(datetime.now(timezone.utc).isoformat(),payload["symbol"],
      payload["side"],payload["entry"],payload["stop"],payload["target"],payload["quantity"],"OPEN"))
    c.commit(); tid=c.execute("SELECT last_insert_rowid()").fetchone()[0]; c.close()
    return {"ok":True,"trade_id":tid}

@app.get("/api/trades")
def trades():
    c=db(); rows=c.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 100").fetchall(); c.close()
    cols=["id","created_at","symbol","side","entry","stop","target","quantity","status"]
    return [dict(zip(cols,r)) for r in rows]
