import httpx
import json


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "AppId" : "109",
    "SystemId" : "Naukri"
}

def incrementValueOfKey(dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1

listings = []

class user_data():
    def __init__(self, user_data):
        self.title = user_data["title"]  # string
        self.location = user_data["saved_location_list"]  # list
        self.experience = user_data["experience"]  # int

        self.listings = []

        # Prepare title and location for URL
        self.titleSEOKey = self.title.replace(" ", "-")
        self.title = self.title.replace(" ", "%20")

        # Prepare location for URL
        if len(self.location) > 1:
            self.location_str = "%2C%20".join(self.location)
        else:
            self.location_str = self.location[0]


class ScrapeNaukriDotCom(user_data):
    def __init__(self, user_data):
        super().__init__(user_data)
    
    def scrape(self):
        URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={self.location_str}&keyword={self.title}&pageNo=1&experience={self.experience}&k={self.title}&l={self.location_str}&experience={self.experience}&seoKey={self.titleSEOKey}-jobs-in-{self.location_str}&src=jobsearchDesk&latLong="
        httpxResponse = httpx.get(URL, headers=headers)
        jsonResponse = httpxResponse.json()
        numberOfJobs = int(jsonResponse["noOfJobs"])
        
        noOfPages = (numberOfJobs // 20) + 1
        returnData = {
            "skills": {},
        }
        sumOfSalaries = 0
        numberOfSalariesCalculated = 0

        for page in range(1, noOfPages + 1):
            print(page)
            URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={self.location_str}&keyword={self.title}&pageNo={page}&experience={self.experience}&k={self.title}&l={self.location_str}&experience={self.experience}&seoKey={self.titleSEOKey}-jobs-in-{self.location_str}&src=jobsearchDesk&latLong="

            
            httpxResponse = httpx.get(URL, headers=headersNaukriDotCom)
            jsonResponse = httpxResponse.json()
            jobDetails = jsonResponse["jobDetails"]

            for jobDetail in jobDetails:
                tempListing = {}
                try:
                    tempListing['jobTitle'] = jobDetail["title"]
                    tempListing["skills"] = jobDetail["tagsAndSkills"].lower().split(",")
                    tempListing["jobDetailURL"] = jobDetail["jdURL"]
                    tempListing["salary"] = jobDetail["placeholders"][1]["label"]
                    tempListing["type"] = "job"

                    listings.append(tempListing)
                    # Increment skill counts
                    for skill in tempListing["skills"]:
                        incrementValueOfKey(returnData["skills"], skill)

                    # Process salary
                    salary = jobDetail["placeholders"][1]["label"]
                    if "-" in salary:
                        min_salary, max_salary = salary.split("-")
                        min_salary = int(min_salary.replace(",", "").strip())
                        max_salary = int(max_salary.replace(",", "").strip())
                        avg_salary = (min_salary + max_salary) / 2
                        sumOfSalaries += avg_salary
                        numberOfSalariesCalculated += 1

                except KeyError as err:
                    continue
        
        if numberOfSalariesCalculated > 0:
            returnData["average_salary"] = sumOfSalaries / numberOfSalariesCalculated
        else:
            returnData["average_salary"] = None

        return returnData

if __name__ == "__main__":
    with open('user_info.json', 'r') as file:
        user_data_json = json.load(file)
    
    scraper = ScrapeNaukriDotCom(user_data_json)
    result = scraper.scrape()
    print(json.dumps(result, indent=4))
