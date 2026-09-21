def levels(side, entry, atr, rr=2.0):
    if not atr or side=="WAIT": return None
    if side=="BUY":
        stop=entry-1.5*atr; target=entry+(entry-stop)*rr
    else:
        stop=entry+1.5*atr; target=entry-(stop-entry)*rr
    return {"entry":entry,"stop":stop,"target":target}

def quantity(balance, entry, stop, risk_pct):
    risk_cash=balance*risk_pct
    distance=abs(entry-stop)
    return round(risk_cash/distance,6) if distance else 0
