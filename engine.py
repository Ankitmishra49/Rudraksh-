import pandas as pd
import numpy as np

def add_indicators(df):
    x=df.copy()
    x["ema20"]=x.close.ewm(span=20,adjust=False).mean()
    x["ema50"]=x.close.ewm(span=50,adjust=False).mean()
    tr=pd.concat([(x.high-x.low),(x.high-x.close.shift()).abs(),(x.low-x.close.shift()).abs()],axis=1).max(axis=1)
    x["atr"]=tr.rolling(14).mean()
    return x.dropna()

def pivots(s, n=3):
    v=s.to_numpy(); hi=[]; lo=[]
    for i in range(n,len(v)-n):
        w=v[i-n:i+n+1]
        if v[i] == w.max(): hi.append(i)
        if v[i] == w.min(): lo.append(i)
    return hi,lo

def smt(a,b):
    ah,al=pivots(a.close); bh,bl=pivots(b.close)
    if len(al)<2 or len(bl)<2 or len(ah)<2 or len(bh)<2:
        return "WAIT",0,"Insufficient swing structure"
    ab=a.close.iloc[al[-2:]].to_numpy(); bb=b.close.iloc[bl[-2:]].to_numpy()
    ahv=a.close.iloc[ah[-2:]].to_numpy(); bhv=b.close.iloc[bh[-2:]].to_numpy()
    bull=ab[1]<ab[0] and bb[1]>bb[0]
    bear=ahv[1]>ahv[0] and bhv[1]<bhv[0]
    if bull: return "BUY",0.70,"Bullish SMT divergence"
    if bear: return "SELL",0.70,"Bearish SMT divergence"
    return "WAIT",0,"No confirmed SMT divergence"

def analyze(a,b):
    a=add_indicators(a); b=add_indicators(b)
    side,conf,reason=smt(a,b)
    z=a.iloc[-1]
    trend="BULLISH" if z.ema20>z.ema50 else "BEARISH"
    if side=="BUY" and trend=="BULLISH": conf+=.15
    elif side=="SELL" and trend=="BEARISH": conf+=.15
    elif side!="WAIT": conf-=.10
    conf=max(0,min(.95,conf))
    return {"signal":side,"confidence":round(conf,2),"trend":trend,
            "reason":reason,"price":float(z.close),"atr":float(z.atr),
            "timestamp":str(a.index[-1])}
