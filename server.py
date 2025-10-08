from flask import Flask
import threading

# --- Tiny Flask server to keep Render awake ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Still alive and training!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Start Flask in a background thread
threading.Thread(target=run_flask, daemon=True).start()
