from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scrappers import scrapeNaukriDotComForKnown
from scrappers import scrapeNaukriDotComForUnknown
from dataCleaning import dataCleaningKnown
from dataCleaning import dataCleaningUnknown
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

        data = scrapeNaukriDotComForKnown()
        # print(f"Scraped data: {data}")
        # ______________________Graph______________________________________

        cleanedData = dataCleaningKnown(data)
        # print(f"Cleaned data: {cleanedData}")
        totalJobs = cleanedData["total_jobs"]

        skillPercentages = [round((value / totalJobs) * 100, 2) for value in cleanedData["skillValues"][:10]]


        topSkillsBar = px.bar(
            x=cleanedData["skills"][:10], 
            y=cleanedData["skillValues"][:10], hover_data={"Percentage": skillPercentages},
            labels={"x": "skills", "y": "frequency"}, 
            color=cleanedData["skills"][:10]
        )
        
        jobPercentages = [round((value / totalJobs) * 100, 2) for value in cleanedData["jobTitleValues"][:10]]

        topJobTitles = px.bar(
            x=cleanedData["jobTitles"][:10], 
            y=cleanedData["jobTitleValues"][:10], 
            labels={"x": "job Titles", "y": "frequency"}, hover_data={"Percentage": jobPercentages},
            color=cleanedData["jobTitles"][:10]
        )
        topJobTitles.update_traces(hovertemplate="Job Title: %{x}<br>Frequency: %{y}<br>Percentage: %{Percentage}%")

        # print(cleanedData["entryLevel"])
        # print(cleanedData["advanceLevel"])

        levelDistribution = px.pie(values=[cleanedData["entryLevel"],cleanedData["advanceLevel"]], names=["Entry Level","Experienced"])
        # ______________________Graph______________________________________

        # ______________________Listings______________________________________
        listings = listingSortedBySkills(data)
        # ______________________Listings______________________________________

        response = {
            "skillGraph": topSkillsBar.to_json(),
            "jobTitleGraph": topJobTitles.to_json(),
            "jobListings": listings,
            "levelDistribution" : levelDistribution.to_json()
        }

        return jsonify(response) 
    
    except Exception as e:
        print("errrrrrrrror")
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/v1/unknown-field-data", methods=["POST"])
def unknown():
    data = request.get_json()
    combination = data["combination"]
    # sites = data["sites"]
    cities = data["cities"]
    # print(type(combination))
    
    data = scrapeNaukriDotComForUnknown(combination,cities)
    cleanedData = dataCleaningUnknown(data)
    # print(cleanedData)


    # Convert data to a list of dictionaries
    noOfJobs = [{'Field': field, 'Total Jobs': count} for field, count in cleanedData["total_jobs_comparision"].items()]
    # Create the figure
    jobComparision = px.bar(noOfJobs, x='Field', y='Total Jobs', title='Total Jobs Comparison')


    # Convert data to a list of dictionaries
    salaries = [{'Field': field, 'Average Salary': count} for field, count in cleanedData["AvgSalary"].items()]

    # Create the figure
    salaryComparision = px.bar(salaries, x='Field', y='Average Salary', title='Average Salary Comparison')



    experience_counts = cleanedData["experience_counts"]

    # Convert data to a list of dictionaries
    jobLevel = []
    for field, counts in experience_counts.items():
        jobLevel.append({'Field': field, 'Experience Level': 'Entry Level', 'Count': counts['entryLevel']})
        jobLevel.append({'Field': field, 'Experience Level': 'Experienced', 'Count': counts['experienced']})

    # Create the figure
    jobLevelComparision = px.bar(jobLevel, x='Field', y='Count', color='Experience Level', barmode='group', title='Experience Level Comparison')

    # fig = px.bar(data, x='Field', y='Count', color='Experience Level', title='Experience Level Comparison')
    topFiveSkills =cleanedData["topFiveSkills"]
    

    response = {
            "noOfJobs": jobComparision.to_json(),
            "jobLevel": jobLevelComparision.to_json(),
            "salaries" : salaryComparision.to_json(),
            "topSkills": topFiveSkills
        }
    
    
    return response
    # return jsonify({'message': 'Data received successfully'})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
