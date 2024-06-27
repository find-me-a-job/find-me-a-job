#PORT = 5000
from flask import Flask, request, jsonify
from flask_cors import CORS
from scrappers import scrapeKnownField, testScrapper
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def home():
    return "home"

@app.route("/api/v1/test")
def test():
    print("tsetprint")
    return testScrapper()

@app.route("/api/v1/known-field-data", methods=["POST"])
def data():
    info = json.loads(request.data.decode())
    return jsonify(scrapeKnownField(info))

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=5000, debug=True)