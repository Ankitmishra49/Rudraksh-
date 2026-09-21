import ccxt
import pandas as pd

def exchange(name):
    cls=getattr(ccxt,name)
    return cls({"enableRateLimit":True})

def candles(ex, symbol, timeframe, limit):
    rows=ex.fetch_ohlcv(symbol,timeframe=timeframe,limit=limit)
    df=pd.DataFrame(rows,columns=["ts","open","high","low","close","volume"])
    df["ts"]=pd.to_datetime(df.ts,unit="ms",utc=True)
    return df.set_index("ts")
