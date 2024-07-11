import httpx
import json
import pickle


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "AppId" : "109",
    "SystemId" : "Naukri"
}

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


def scrapeNaukriDotCom(title: str, location: list, experience: int) -> list:
    listings = []

    # Prepare location for URL
    if len(location) > 1:
        location_str = "%2C%20".join(location)
        
    else:
        location_str = location[0]

    location = location_str
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    
    URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo=1&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
    httpxResponse = httpx.get(URL, headers=headers)
    jsonResponse = httpxResponse.json()
    numberOfJobs = int(jsonResponse["noOfJobs"])
    # if numberOfJobs == int("O"):
    #     return {}
    noOfPages = numberOfJobs//20

    numberOfSalariesCalculated = 0

    for page in range(1,noOfPages+1):
        print((page/noOfPages)*100)
        URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={page}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
        

        httpxResponse = httpx.get(URL, headers=headers)
        jsonResponse = httpxResponse.json()
        jobDetails = jsonResponse["jobDetails"]

        for jobDetail in jobDetails:
            try:
                
                jobTitle = jobDetail["title"]
                companyName = jobDetail["companyName"]
                skills = jobDetail["tagsAndSkills"].lower().split(",")
                jobDetailURL = jobDetail["jdURL"]
                jobDetailURL = "https://www.naukri.com"+jobDetailURL
                jobDescription = jobDetail["jobDescription"]
                salary = jobDetail["placeholders"][1]["label"]
                listingType = "job"
                portal = "Naukri.com"

                tempList = [jobTitle,companyName,skills,jobDetailURL,jobDescription,salary,listingType,portal]

                listings.append(tempList)
            except KeyError as err:
                continue
    # with open("data", "wb") as fp:   #Pickling
    #     pickle.dump(listings, fp)
    return listings

# if __name__ == "__main__":
    
#     with open('user_info.json', 'r') as file:
#         user_data_json = json.load(file)
    
#     title = user_data_json["title"]  # string
#     location = user_data_json["saved_location_list"]  # list
#     experience = user_data_json["experience"]  # int

#     # Prepare title and location for URL
#     titleSEOKey = title.replace(" ", "-")
#     title = title.replace(" ", "%20")

#     # Prepare location for URL
#     if len(location) > 1:
#         location_str = "%2C%20".join(location)
        
#     else:
#         location_str = location[0]

#     location = location_str
#     data = scrapeNaukriDotCom(title, location, experience)
#     with open("data", "wb") as fp:   #Pickling
#         pickle.dump(data, fp)