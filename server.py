from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Still alive and training!"

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
