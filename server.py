# keep_alive.py
from flask import Flask
import threading
import os
import time
import requests
import train  # your training script file

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Still alive and training!"

def background_train():
    """Run your training loop in the background."""
    try:
        train.main()
    except Exception as e:
        print(f"❌ Training crashed: {e}")
        # Optional: retry logic or graceful exit
        time.sleep(10)

def run_flask():
    """Run the small Flask web server to keep Render happy."""
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    """Continuously ping the app to keep it awake on Render (every 10 min)."""
    # Render automatically provides this environment variable
    host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if not host:
        print("⚠️ No RENDER_EXTERNAL_HOSTNAME found — skipping self-ping.")
        return
    url = f"https://{host}"
    while True:
        try:
            r = requests.get(url)
            print(f"🔁 Self-ping OK ({r.status_code})")
        except Exception as e:
            print(f"⚠️ Self-ping failed: {e}")
        time.sleep(600)  # ping every 10 minutes

if __name__ == "__main__":
    # Start background threads
    threading.Thread(target=background_train, daemon=True).start()
    threading.Thread(target=self_ping, daemon=True).start()
    # Run Flask (main thread)
    run_flask()
