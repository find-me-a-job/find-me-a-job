from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scrappers import scrapeNaukriDotCom
from dataCleaning import dataCleaning
from userTailoredListing import listingSortedBySkills
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "home"

@app.route("/api/v1/test", methods=["GET", "POST"])
def test():
    return jsonify({"message": "this is a test message"})


@app.route("/api/v1/known-field-data", methods=["POST"])
def data():
    try:
        info = json.loads(request.data.decode())
        # print(f"Received data: {info}")

        with open('user_info.json', 'r') as file:
            user_info = json.load(file)
        user_info.update(info)
        with open('user_info.json', 'w') as file:
            json.dump(user_info, file, indent=4)

        data = scrapeNaukriDotCom()
        # print(f"Scraped data: {data}")
        # ______________________Graph______________________________________

        cleanedData = dataCleaning(data)
        # print(f"Cleaned data: {cleanedData}")

        topSkillsBar = px.bar(
            x=cleanedData["skills"][:10], 
            y=cleanedData["skillValues"][:10], 
            labels={"x": "skills", "y": "frequency"}, 
            color=cleanedData["skills"][:10]
        )
        topJobTitles = px.bar(
            x=cleanedData["jobTitles"][:10], 
            y=cleanedData["jobTitleValues"][:10], 
            labels={"x": "job Titles", "y": "frequency"}, 
            color=cleanedData["jobTitles"][:10]
        )
        # ______________________Graph______________________________________

        # ______________________Listings______________________________________
        listings = listingSortedBySkills(data)

        # print(listings)




        # ______________________Listings______________________________________

        response = {
            "skillGraph": topSkillsBar.to_json(),
            "jobTitleGraph": topJobTitles.to_json(),
            "jobListings": listings

        }

        return jsonify(response)

        
    except Exception as e:
        print("errrrrrrrror")
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500



@app.route("/api/v1/naukridotcom-data", methods=["POST"])
def naukriData():
    info = json.loads(request.data.decode())
    retObject = jsonify(scrapeNaukriDotCom(
        title=info["title"], 
        location=info["location"], 
        experience=info["experience"]
    ))
    return retObject

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
