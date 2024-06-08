#PORT = 5000
from flask import Flask, request
from flask_cors import CORS, cross_origin
from scrappers import scrape
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def home():
    print("home!")
    return

@app.route("/api/v1/test")
def test():
    print("test response from backend!")
    return "return statement of test"

@app.route("/api/v1/known-field-data", methods=["POST"])
def data():
    print("---------------")
    info = json.loads(request.data.decode())
    return json.dumps(scrape(info))
    # return scrape(info=info)

if __name__ == "__main__":
    app.run(debug=True)
#vadodara
#web development