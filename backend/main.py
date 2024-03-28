from flask import jsonify, Flask, request
from scrappers import scrapeInternshala, scrapeNaukriDotCom
import json

app = Flask(__name__)

@app.route("/")
def home():
    naukriDotComData = scrapeNaukriDotCom("web developer", 0, "vadodara")
    internShalaData = scrapeInternshala("web developer", "vadodara")
    # naukriDotComData = json.dumps(naukriDotComData.json)
    internShalaData = json.dumps(internShalaData.json, indent=2)
    print("done")
    return internShalaData

if __name__ == "__main__":
    app.run(debug=True)