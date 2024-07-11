#PORT = 5000
from flask import Flask, request, jsonify
from flask_cors import CORS
from scrappers import scrapeNaukriDotCom
from dataCleaning import dataCleaning
from userTailoredListing import listingSortedBySkills
# from scrappersV2 import scrapeNaukriDotCom
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "home"

@app.route("/api/v1/test", methods=["GET", "POST"])
def test():
    print("testprint")
    return jsonify({"message": "this is a test message"})

@app.route("/api/v1/known-field-data", methods=["POST"])
def data():
    info = json.loads(request.data.decode())
    print(f"info: {info}")
    data = scrapeNaukriDotCom(info["title"], info["saved_location_list"], info["experience"])
    # with open("NaukriDotComResponse.json", "w+") as f:
    #     f.write(str(data))
    print(f"==================DATA: {data}=====================")
    cleanedData = {}
    cleanedData["skills_chart"] = dataCleaning(data)
    cleanedData["skills_listings"] = listingSortedBySkills(data)
    # print(data)
    return jsonify(cleanedData)

# @app.route("/api/v2/known-field-data", methods=["POST"])
# def data():
#     # V2
#     # New logic for new data format for known field
#     pass

@app.route("/api/v1/naukridotcom-data", methods=["POST"])
def naukriData():
    info = json.loads(request.data.decode())
    retObject = jsonify(scrapeNaukriDotCom(title=info["title"], location=info["location"], experience=info["experience"]))
    return retObject

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=4000, debug=True)