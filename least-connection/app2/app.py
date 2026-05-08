from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():

    print("REQUEST MASUK KE APP2")

    return "Response from APP 2"

app.run(host='0.0.0.0', port=5000)
