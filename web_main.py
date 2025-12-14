import threading
import time
from web_app import create_app

def start_flask(app):
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    app = create_app()

    t = threading.Thread(target=start_flask, args=(app,), daemon=True)
    t.start()

    print("Flask started → http://127.0.0.1:5000")

    # Keep thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing...")
