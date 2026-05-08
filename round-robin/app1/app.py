from flask import Flask
#import time
app = Flask(__name__)

@app.route('/')
def home():

    print("REQUEST MASUK KE APP1")

    #time sleep(2)
    #time sleep(5)
    return "Response from APP 1"

app.run(host='0.0.0.0', port=5000)
