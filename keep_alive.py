from flask import Flask
from threading import Thread
import requests
import time
import random
import os
from logger_config import setup_logger

# Logger initialisieren
logger = setup_logger(__name__)

app = Flask(__name__)

KEEP_ALIVE_URL = os.getenv("URL_KEEP_ALIVE")

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def self_ping():
    """Pingt die eigene Replit-URL in zufälligen Intervallen, um den Server aktiv zu halten."""
    while True:
        try:
            response = requests.get(KEEP_ALIVE_URL)
            logger.info("Pinged self to stay awake! Status:", response.status_code)
        except Exception as e:
            logger.error(f"Ping failed: {e}")

        # Zufällige Wartezeit zwischen 1 und 5 Minuten
        sleep_time = random.randint(60, 300)
        logger.info(f"Nächster Ping in {sleep_time} Sekunden...")
        time.sleep(sleep_time)

def emergency_wakeup():
    """Prüft alle 30 Sekunden, ob der Server down ist, und pingt ihn zur Reaktivierung."""
    while True:
        time.sleep(30)  # Prüft alle 30 Sekunden
        
        try:
            response = requests.get(KEEP_ALIVE_URL, timeout=5)
            if response.status_code == 200:
                continue  # Alles gut, nichts tun
        except:
            logger.warning("WARNUNG: Server scheint down zu sein! Versuche Selbst-Reaktivierung...")
            os.system(f"curl {KEEP_ALIVE_URL} > /dev/null 2>&1")

# Starte alles beim Import dieser Datei
# Prüft, ob der Code in Replit läuft (z. B. durch eine Umgebungsvariable)
RUN_KEEP_ALIVE = os.getenv("RUN_KEEP_ALIVE", "false").lower() == "true"

if RUN_KEEP_ALIVE:
    logger.info("🚀 Keep-Alive aktiviert (Replit-Umgebung erkannt)")
    keep_alive()
    Thread(target=self_ping, daemon=True).start()
    Thread(target=emergency_wakeup, daemon=True).start()
else:
    logger.info("🛑 Keep-Alive deaktiviert (Lokale Umgebung erkannt)")