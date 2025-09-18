#!/data/data/com.termux/files/usr/bin/python3
# sms_forwarder.py
# Kirim SMS masuk ke Telegram bot

import subprocess, json, time, requests, os

BOT_TOKEN = "7990219519:AAGvhE-1_31JzJmWqNyjdMtmi2dZzfgPXHM"   # <<< isi token bot Telegram
CHAT_ID   = "7218474722"     # <<< isi chat id kamu
INTERVAL  = 5                          # jeda cek sms (detik)
STATE_FILE = "/data/data/com.termux/files/home/.last_sms_id"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Gagal kirim:", e)

def get_sms():
    p = subprocess.run(["termux-sms-list", "-l", "10"], capture_output=True, text=True)
    if p.returncode != 0:
        return []
    try:
        return json.loads(p.stdout)
    except:
        return []

def load_last_id():
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE).read().strip()
    return None

def save_last_id(sid):
    with open(STATE_FILE, "w") as f:
        f.write(str(sid))

def main():
    last_id = load_last_id()
    print("SMS Forwarder jalan... cek setiap", INTERVAL, "detik")
    while True:
        msgs = get_sms()
        for m in reversed(msgs):  # urut lama -> baru
            sid = str(m.get("id"))
            if last_id is None or sid > last_id:
                frm = m.get("address") or m.get("from")
                body = m.get("body") or m.get("text")
                tgl  = m.get("date")
                pesan = f"📩 SMS Baru\nDari: {frm}\nIsi: {body}\nTgl: {tgl}"
                send_telegram(pesan)
                save_last_id(sid)
                last_id = sid
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
