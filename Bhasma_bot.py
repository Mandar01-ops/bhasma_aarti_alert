import requests
import time
import webbrowser
from bs4 import BeautifulSoup
import os


HOME_URL = "https://www.shrimahakaleshwar.mp.gov.in/"
SERVICES_URL = "https://www.shrimahakaleshwar.mp.gov.in/services"
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
CHECK_INTERVAL=30

def send_telegram(msg):
    api=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(api, params={
        "chat_id":CHAT_ID,
        "text":msg
    })

def check_home_page():
    r = requests.get(HOME_URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator=" ").lower()

    if "bhasma" in text and "book now" in text:
        return True

    return False

def check_services_page():
    r = requests.get(SERVICES_URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href", "")
        label = a.get_text(" ").lower()

        if "bhasma" in label and "book" in label and href:
            return href

    return None

print("Monitoring ONLY Bhasma Aarti booking...")
send_telegram("Bhasma Aarti booking is NOT open yet (test message)")
alerted=False

while True:
    try:
        if check_home_page():
            msg = "Bhasma Aarti booking OPEN (Home Page)"
            print(msg)
            send_telegram(msg)
            webbrowser.open(HOME_URL)
            break

        link = check_services_page()
        if link and not alerted:
            msg = f"Bhasma Aarti booking OPEN (Services Page)\n{link}"
            print(msg)
            send_telegram(msg)
            webbrowser.open(link)
            break

        print("Still not open...")

    except Exception as e:
        print("Error:", e)
    time.sleep(CHECK_INTERVAL)
