import httpx
from selectolax.parser import HTMLParser
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "AppId" : "109",
    "SystemId" : "Naukri"
}

def scrapeNaukriDotCom(title: str, location: str, experience: int) -> list:
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    
    testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo=1&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
    httpxResponse = httpx.get(testURL, headers=headers)
    # print(resp.text)
    # return
    jsonResponse = httpxResponse.json()
    if(jsonResponse["noOfJobs"] == 0):
        return {}
    print(jsonResponse["jobDetails"])
    returnData = {
                "skills": {},
            }
    jobDetails = jsonResponse["jobDetails"]
    with open("temp.json", "w+") as f:
        f.write(json.dumps(jobDetails))
    skills = []
    sumOfSalaries = 0
    numberOfSalariesCalculated = 0
    for jobDetail in jobDetails:
        try:
            #skills
            skills = jobDetail["tagsAndSkills"].lower().split(",")
            for skill in skills:
                if skill in returnData["skills"]:
                    returnData["skills"][skill] += 1
                else:
                    returnData["skills"][skill] = 1
            #average-salary
            salary = jobDetail["placeholders"][1]["label"]
            if salary != "Not disclosed":
                print(salary)
                salary = float(salary[salary.index("-") + 1 : -8].strip())

                sumOfSalaries += salary
                numberOfSalariesCalculated += 1
            # applicants-to-jobs-ratio

        except KeyError as err:
            continue
    if(numberOfSalariesCalculated == 0):
        returnData["average-salary"] = 0
    else:
        returnData["average-salary"] = sumOfSalaries / numberOfSalariesCalculated
    # with open("skills.json", "w+") as f:
    #     f.write(json.dumps(returnData))
    
    return returnData

def scrapeInternshala(profile="", location="", experience=0):
    def get_html(page):
        if(experience == 0):
            # Fresher
            url = f"https://internshala.com/fresher-jobs/{profile}-jobs-in-{location}/page-{page}"
        else:
            url = f"https://internshala.com/fresher-jobs/{profile}-jobs-in-{location}/experience-{experience}/page-{page}"
        resp = httpx.get(url, headers=headers)
        return HTMLParser(resp.text)
    webpage = get_html(1)
    number_of_pages = int(webpage.css_first("span#total_pages").text())
    salaryList = []
    skills = []
    skillsDict = {}
    applicants = []
    for page_number in range(1, number_of_pages):
        print("page", page_number, "/", number_of_pages)
        webpage = get_html(page_number);
        salaries = webpage.css("span.desktop")
        # return
        listingCards = webpage.css_first(f"#internship_list_container_{page_number}")
        if(listingCards is None):
            print("listing container was not found in the html so early returning!")
            str = webpage.html
            with open("output.txt", 'w+') as f:
                f.write(str)
            return
        else:
            listingCards = listingCards.iter()
        listingLinks = []
        for listingCard in listingCards:
            try:
                listingLinks.append("https://internshala.com" + listingCard.attributes['data-href'] + '/')
            except KeyError:
                print(KeyError, "data-href attribute was not found in listing div")
                continue
        totalListingsVisitedForSkills = 0
        skillsNotFound = 0
        number_of_applicants = 0
        number_of_listings_scrapped_for_number_of_applicants = 0
        # Scrapping Skills #
        for url in listingLinks:
            listingPage = HTMLParser(httpx.get(url, headers=headers).text)
            # skillsExtractedRaw = listingPage.css("span.round_tabs")
            skillsRawHTML = listingPage.css("span.round_tabs")
            totalListingsVisitedForSkills += 1
            # Number of applicants
            # number_of_applicants_on_current_listing
            if(len(skillsRawHTML) == 0):
                print("LENGTH OF SKILLS_RAW_HTML WAS 0 - No skills div found.")
                skillsNotFound += 1
                continue
            skills_for_current_listing = list(map(lambda x: x.text().strip().lower(), skillsRawHTML))
            skills.append(skills_for_current_listing)

            # Applicants
            try:
                number_of_applicants_in_current_listing = listingPage.css_first(".applications_message").text()[:-11].strip()
                if(number_of_applicants_in_current_listing == "1000+"):
                    number_of_applicants_in_current_listing = 1000
                number_of_applicants += int(number_of_applicants_in_current_listing)
                number_of_listings_scrapped_for_number_of_applicants += 1
            except Exception as e:
                print("something went wrong while scrapping number of applicants")
                print(e)
                print("-->", number_of_applicants_in_current_listing)
                print("---------------XXXXXXXXXXXXXXXXXXXXXXXXXX---------------")
            # Skills new format
            for skill in skills_for_current_listing:
                if(skill in skillsDict):
                    skillsDict[skill] += 1
                else:
                    skillsDict[skill] = 1
        print("totalListingsVisitedForSkills :", totalListingsVisitedForSkills, " / ", "skillsNotFound :", skillsNotFound)
        for i in salaries:
            if(i.text().strip() == "Competitive salary"):
                continue
            salaryRange = i.text().strip()[2:]
            endIndexForFirstNumber = len(salaryRange)
            startIndexForSecondNumber = len(salaryRange)
            secondNumber = 0
            divideFactor = 2
            try:
                endIndexForFirstNumber = salaryRange.index("-")
                startIndexForSecondNumber = endIndexForFirstNumber + 2
                secondNumber = int(salaryRange[startIndexForSecondNumber:].strip().replace(",", ""))
            except ValueError as e:
                divideFactor = 1
            firstNumber = int(salaryRange[0:endIndexForFirstNumber].strip().replace(",", ""))
            averageSalary = (firstNumber + secondNumber) // divideFactor
            salaryList.append(averageSalary)
    sumOfSalaries = 0
    for i in salaryList:
        sumOfSalaries += i
    if(len(salaryList) > 0):
        averageSalary = sumOfSalaries/len(salaryList)
    else:
        print("why is salaryList's length 0????")
        print(salaryList)
        print("------------------------------------")
    
    print(skillsDict)

    with open("skillsDict.json", "w+") as f:
        f.write(json.dumps(skillsDict))

    sorted_items = sorted(skillsDict.items(), key=lambda x: x[1], reverse=True)

    skillsSortedByFrequency = [item[0] for item in sorted_items]

    # skillsDict = sorted(skillsDict, reverse=False)
    # Returing data
    applicants_ratio_to_jobs_ratio = number_of_applicants / number_of_listings_scrapped_for_number_of_applicants
    returnData = {}
    returnData["skills"] = skillsDict
    returnData["average-salary"] = averageSalary
    returnData["applicants-to-jobs-ratio"] = applicants_ratio_to_jobs_ratio
    with open("temp.json", "w+") as f:
        f.write(json.dumps(web_development))
    
    return returnData
    

def scrape(info: dict) -> json:
    internshalaData = scrapeInternshala(profile=info["title"], location=info["location"], experience=info["experience"])
    # naukriDotComData = scrapeNaukriDotCom(info["title"], info["experience"], info["location"])
    # response = internshalaData + naukriDotComData
    # response = json.dumps(response)
    # return response
    return json.dumps(internshalaData)

if __name__ == "__main__":
    # web_development = scrapeInternshala("web-development", "", 0)
    # data_science = scrapeInternshala("data_science", "", 0)
    # cyber_security = scrapeInternshala("cyber-security", "", 0)
    # cloud_computing = scrapeInternshala("cloud-computing", "", 0)

    # print(web_development)
    # # print(data_science)
    # # print(cyber_security)
    # print(cloud_computing)

    data = {}
    data["web_development"] = scrapeNaukriDotCom("web-development", "", 0)
    data["data_science"] = scrapeNaukriDotCom("data_science", "", 0)
    data["cyber_security"] = scrapeNaukriDotCom("cyber-security", "", 0)
    data["cloud_computing"] = scrapeNaukriDotCom("cloud-computing", "", 0)

    with open("output.json", "a+") as f:
        f.write(json.dumps(data))