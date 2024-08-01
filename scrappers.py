import httpx
import json
import pickle


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "AppId" : "109",
    "SystemId" : "Naukri"
}

listings = []


def scrapeNaukriDotComForKnown() -> list:
    try:
        with open('user_info.json', 'r') as file:
            print("loading done")
            user_info = json.load(file)
        
    except:
        print("Error!!!")

    title = user_info["title"]
    location = user_info["saved_location_list"]
    experience = user_info["experience"]
    listings = []

    # Prepare location for URL
    if len(location) > 1:
        location_str = "%2C%20".join(location)
        
    elif len(location)==1 :
        location_str = location[0]
    else:
        location_str = None

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
        # print(URL)

        httpxResponse = httpx.get(URL, headers=headers)
        jsonResponse = httpxResponse.json()
        if 'jobDetails' in jsonResponse:
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
                    experience = jobDetail["placeholders"][0]["label"]

                    listingType = "job"
                    portal = "Naukri.com"

                    tempList = [jobTitle,companyName,skills,jobDetailURL,jobDescription,salary,experience,listingType,portal]

                    listings.append(tempList)
                except KeyError as err:
                    continue
        else:
            continue
    # print(listings)
    
    return listings



def scrapeNaukriDotComForUnknown(combinations,cities) -> list:
    
    
    
    listings = []
    location = cities
    combinations = combinations
    experience = ""

    # Prepare location for URL
    if len(location) > 1:
        location_str = "%2C%20".join(location)
        
    elif len(location)==1 :
        location_str = location[0]
    else:
        location_str = None

    location = location_str
    

    for field in combinations:
        # print(combinations)
        title = field
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
            # print(URL)

            httpxResponse = httpx.get(URL, headers=headers)
            jsonResponse = httpxResponse.json()
            if 'jobDetails' in jsonResponse:
                jobDetails = jsonResponse["jobDetails"]
                for jobDetail in jobDetails:

                    try:

                        jobTitle = jobDetail["title"]
                        # companyName = jobDetail["companyName"]
                        skills = jobDetail["tagsAndSkills"].lower().split(",")
                        jobDetailURL = jobDetail["jdURL"]
                        jobDetailURL = "https://www.naukri.com"+jobDetailURL
                        # jobDescription = jobDetail["jobDescription"]
                        salary = jobDetail["placeholders"][1]["label"]
                        experience = jobDetail["placeholders"][0]["label"]

                        listingType = "job"
                        portal = "Naukri.com"

                        tempList = [field,jobTitle,skills,salary,experience,listingType,portal]

                        listings.append(tempList)
                    except KeyError as err:
                        continue
            else:
                continue

        # print(listings)
    # print(listings)
    return listings





# if __name__ == "__main__":
    # scrapeNaukriDotCom()
    
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