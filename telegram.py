import requests

def send(enabled, token, chat_id, message):
    if not enabled or not token or not chat_id: return False
    url=f"https://api.telegram.org/bot{token}/sendMessage"
    r=requests.post(url,json={"chat_id":chat_id,"text":message},timeout=10)
    return r.ok
