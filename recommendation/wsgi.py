from app.routes import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True, timeout=120)