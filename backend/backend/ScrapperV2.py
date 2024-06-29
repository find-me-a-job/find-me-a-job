import httpx
from selectolax.parser import HTMLParser
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


def scrapeNaukriDotCom(title: str, location: str, experience: int) -> list:
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    
    URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo=1&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
    httpxResponse = httpx.get(URL, headers=headers)
    jsonResponse = httpxResponse.json()
    numberOfJobs = int(jsonResponse["noOfJobs"])
    # if numberOfJobs == int("O"):
    #     return {}
    noOfPages = numberOfJobs//20
    returnData = {
                "skills": {},
            }
    sumOfSalaries = 0
    numberOfSalariesCalculated = 0

    for page in range(1,noOfPages+1):
        print(returnData)
        print(page)
        URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={page}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
        
        httpxResponse = httpx.get(URL, headers=headers)
        jsonResponse = httpxResponse.json()
        jobDetails = jsonResponse["jobDetails"]
        skills = []
        for jobDetail in jobDetails:
            try:
                #skills
                skills = jobDetail["tagsAndSkills"].lower().split(",")
                for skill in skills:
                    incrementValueOfKey(returnData["skills"], skill)
                #average-salary
                # salary = jobDetail["placeholders"][1]["label"]
                # print(salary)
                # if salary != "Not disclosed":
                #     validIndex = salary.index(" ")
                #     salary= salary[:validIndex]
                #     print(salary)
                #     if "-" in salary:
                #         salaryRange = salary.split("-")
                #         average = 0
                #         for i in salaryRange:
                #             i=i.replace(",","")
                #             i= float(i)
                #             average += i
                #         salary = average/2
                #     # print(salary)
                #     # salary = float(salary[salary.index("-") + 1 : -8].strip())

                #     sumOfSalaries += salary
                #     numberOfSalariesCalculated += 1

            except KeyError as err:
                continue
        # if(numberOfSalariesCalculated == 0):
        #     returnData["average-salary"] = 0
        # else:
        #     returnData["average-salary"] = sumOfSalaries / numberOfSalariesCalculated
    
    return returnData
    
if __name__ == "__main__":
    print(scrapeNaukriDotCom(title = "data science analyst", location="", experience=""))