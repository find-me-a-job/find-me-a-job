from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scrappers import scrapeNaukriDotCom
from dataCleaning import dataCleaning
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
        print(f"Received data: {info}")


        with open('user_info.json', 'r') as file:
            user_info = json.load(file)
        user_info.update(info)
        with open('user_info.json', 'w') as file:
            json.dump(user_info, file, indent=4)

        data = scrapeNaukriDotCom()
        # print(f"Scraped data: {data}")

        cleanedData = dataCleaning(data)
        # print(f"Cleaned data: {cleanedData}")

        topSkillsBar = px.bar(x=cleanedData["skills"][:10], y=cleanedData["values"][:10], labels={"skills": "frequency"}, color=cleanedData["skills"][:10])
        topSkills = pio.to_html(topSkillsBar, full_html=False)
        # print(f"Generated Plotly graph: {topSkills}")

        return topSkills

    except Exception as e:
        print("errrrrrrrror")
        return
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


# #PORT = 5000
# from flask import Flask, request, jsonify,url_for,render_template
# from flask_cors import CORS
# from scrappers import scrapeNaukriDotCom
# from dataCleaning import dataCleaning
# from userTailoredListing import listingSortedBySkills
# import plotly.express as px
# import plotly.io as pio
# import json

# app = Flask(__name__)
# CORS(app)

# @app.route("/")
# def home():
#     return "home"

# @app.route("/api/v1/test", methods=["GET", "POST"])
# def test():
#     print("testprint")
#     return jsonify({"message": "this is a test message"})


# @app.route("/api/v1/known-field-data", methods=["POST"])
# def data():
#     try:
#         info = json.loads(request.data.decode())

#         # Update user_info.json if needed
#         with open('user_info.json', 'r') as file:
#             user_info = json.load(file)
#         user_info.update(info)
#         with open('user_info.json', 'w') as file:
#             json.dump(user_info, file, indent=4)

#         # Example Plotly graph creation
#         data = scrapeNaukriDotCom()
#         cleanedData = dataCleaning(data)
#         topSkillsBar = px.bar(x=cleanedData["skills"][:10], y=cleanedData["values"][:10], labels={"skills": "frequency"}, color=cleanedData["skills"][:10])
#         topSkills = pio.to_html(topSkillsBar, full_html=False)

#         # Render graph.html with Plotly graph
#         return render_template('graph.html', topSkills=topSkills)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  # Return error message with status code 500



# # @app.route("/api/v1/known-field-data", methods=["POST"])
# # def data():
# #     info = json.loads(request.data.decode())
# #     # print(f"info: {info}")

    
# #     with open('user_info.json', 'r') as file:
# #         user_info = json.load(file)
# #     user_info.update(info)
# #     with open('user_info.json', 'w') as file:
# #         json.dump(user_info, file, indent=4)


# #     data = scrapeNaukriDotCom()
# #     cleanedData = dataCleaning(data) #return a dict with 3 keys total_jobs->int, skills->tuple, values->tuple
    
# #     topSkillsBar = px.bar(x=cleanedData["skills"][:10],y=cleanedData["values"][:10], labels={"skills":"frequency"}, color=cleanedData["skills"][:10])
# #     # Generate the HTML representation of the plot
# #     topSkills = pio.to_html(topSkillsBar, full_html=False)

# #     return render_template('graph.html', topSkills=topSkills)



#     # with open("NaukriDotComResponse.json", "w+") as f:
#     #     f.write(str(data))
#     # print(f"==================DATA: {data}=====================")
#     # cleanedData = {}
#     # cleanedData["skills_chart"] = dataCleaning(data)
#     # cleanedData["skills_listings"] = listingSortedBySkills(data)
#     # # print(data)
#     # return jsonify(cleanedData)

# # @app.route("/api/v2/known-field-data", methods=["POST"])
# # def data():
# #     # V2
# #     # New logic for new data format for known field
# #     pass

# @app.route("/api/v1/naukridotcom-data", methods=["POST"])
# def naukriData():
#     info = json.loads(request.data.decode())
#     retObject = jsonify(scrapeNaukriDotCom(title=info["title"], location=info["location"], experience=info["experience"]))
#     return retObject

# if __name__ == "__main__":
#     app.run(host= "0.0.0.0", port=4000, debug=True)