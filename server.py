from flask import Flask
import threading
import os
import train  # your training script file

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Still alive and training!"

def background_train():
    train.main()  # call your training loop here

def run_flask():
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Start Flask in a background thread
threading.Thread(target=run_flask, daemon=True).start()
