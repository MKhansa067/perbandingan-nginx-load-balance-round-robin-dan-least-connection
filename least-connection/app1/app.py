//skenario delay 2 detik
from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def home():

    print("REQUEST MASUK KE APP1")
    # simulasi server lambat
    time.sleep(2)

    return "Response from APP 1 (DELAY 2s)"

app.run(host='0.0.0.0', port=5000)
