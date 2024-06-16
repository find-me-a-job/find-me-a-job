#PORT = 5000
from flask import Flask, request
from flask_cors import CORS, cross_origin
from scrappers import scrapeKnownField
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def home():
    return "home"

@app.route("/api/v1/test")
def test():
    return "return string of /api/v1/test"

@app.route("/api/v1/known-field-data", methods=["POST"])
def data():
    info = json.loads(request.data.decode())
    return json.dumps(scrapeKnownField(info))

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=5000, debug=True)