import httpx
from selectolax.parser import HTMLParser
import json

headersNaukriDotCom = {
    "Postman-Token": "2a1a92ef-6cb8-4afd-9aef-c619374fabc2",
    "Cookie": "J=0; _t_ds=7fc9e31719439797-387fc9e3-07fc9e3; ak_bmsc=FE0BCD76CA64EC6D4C2FDE3E0682BC91~000000000000000000000000000000~YAAQnEU5F9PvSQ+QAQAA/0qJWhiV/rNyLpFIvLFILyQcuhzvsGacvIB8IAbWYNpehdQeoac1mkdZtodWRK9N8zEdhEAwXdYdoPzudDbrYHU6SgnDptUR/Cvqk9+HnXcJem0wKKbRLl68v63iVtphgEKAaNTyWcToZX8P/IDOUJBn5NGR3q2FewmGLVk+3v7J9x3CFlKzxvXZAXB5AExssi66NqUITHTBRxqWGQti43fNUSEWERmCwriC9Vkr+HShlIrkzYpw2+RuFzSXOEkpS1tG2PEbPKu2lJ0z7Uej/5fKaDvPCFZEX7w93eeNDftgr4mm/YDIoNypjYKMHjCTCQYsa9gWybIbhOQucKrj399rTVP7BCGJX65Me1dRhJ3cYaGrg/Vl3uPlnc+o; bm_sv=97FB75357B01A6C025C7A31B5C5CB734~YAAQH/naF1cUIk+QAQAAWIqbWhjlVSj1DwEEBYwgietiEPS79agf8sa82i++/NXMugRQcN/vRI5QUHMmgqtDstaJJe3qrqjMs3E44v7JNOT0qv96ad3FhU6L+XnIGzeJ6WFbR5O8Ay9k9Z+tWN94aQDCK6UerlJW/NJptfN6OgicI/YsgKgWjmk+avpjL8aTlTA+hfnTaXPrkZr+AOsnYHpK5FVagyyCDtcyLxdMIhViGjWNapILbHk16X++O1VI~1",
    "User-Agent": "PostmanRuntime/7.39.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Connection": "keep-alive",
    "AppId": "109",
    "SystemId": "Naukri",
    "Host": "www.naukri.com"
}

normalHeaders = {
    "User-Agent": "PostmanRuntime/7.39.0",
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
    httpxResponse = httpx.get(URL, headers=headersNaukriDotCom)
    jsonResponse = httpxResponse.json()
    numberOfJobs = int(jsonResponse["noOfJobs"])
    noOfPages = numberOfJobs//20
    listings = []
    fieldKnownData = {}

    for page in range(1,noOfPages+1):
        print(page)
        URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={page}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
        
        httpxResponse = httpx.get(URL, headers=headersNaukriDotCom)
        jsonResponse = httpxResponse.json()
        jobDetails = jsonResponse["jobDetails"]

        for jobDetail in jobDetails:
            listingData = []
            try:
                
                listingData.append(jobDetail["title"])
                listingData.append(jobDetail["tagsAndSkills"].lower().split(","))
                listingData.append(jobDetail["jdURL"])
                listingData.append(jobDetail["placeholders"][1]["label"])
                listingData.append("job")

                listings.append(listingData)
                # for skill in skills:
                #     incrementValueOfKey(returnData["skills"], skill)
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

            except KeyError:
                continue
        # if(numberOfSalariesCalculated == 0):
        #     returnData["average-salary"] = 0
        # else:
        #     returnData["average-salary"] = sumOfSalaries / numberOfSalariesCalculated
    
    return {"df-data": listings, "known-field-data": fieldKnownData}

# tempListing['jobTitle'] = jobDetail["title"]
# tempListing["skills"] = jobDetail["tagsAndSkills"].lower().split(",")
# tempListing["jobDetailURL"] = jobDetail["jdURL"]
# tempListing["salary"] = jobDetail["placeholders"][1]["label"]
# tempListing["type"] = "job"



def scrapeInternshala(profile="", location="", experience=0):
    profile = profile.replace(" ", "-")
    def get_html(page):
        if(experience == 0):
            # Fresher
            url = f"https://internshala.com/fresher-jobs/{profile}-jobs-in-{location}/page-{page}"
            
        else:
            url = f"https://internshala.com/jobs/{profile}-jobs-in-{location}/experience-{experience}/page-{page}"
        resp = httpx.get(url, headers=normalHeaders)
        return HTMLParser(resp.text)
    webpage = get_html(1)
    number_of_pages = int(webpage.css_first("span#total_pages").text())
    salaryList = []
    averageSalary = 0
    skills = []
    skillsDict = {}
    applicants = []
    number_of_applicants = 0
    number_of_listings_scrapped_for_number_of_applicants = 0
    for page_number in range(1, number_of_pages):
        # # This if block is here for debugging. It would take a really long time to scrape so many pages so i limit it to only 1 page here.
        # if page_number > 1:
        #     break
        print("page", page_number, "/", number_of_pages)
        webpage = get_html(page_number);
        salaries = webpage.css("span.desktop")
        # return
        listingCards = webpage.css_first(f"#internship_list_container_{page_number}")
        if(listingCards is None):
            print("listing container was not found in the html so early returning!")
            str = webpage.html
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
        # Scrapping Skills #
        for url in listingLinks:
            listingPage = HTMLParser(httpx.get(url, headers=normalHeaders).text)
            # skillsExtractedRaw = listingPage.css("span.round_tabs")
            skillsRawHTML = listingPage.css("span.round_tabs")
            totalListingsVisitedForSkills += 1
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
            # Skills new format
            for skill in skills_for_current_listing:
                incrementValueOfKey(skillsDict, skill)
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
    
    print(skillsDict)


    sorted_items = sorted(skillsDict.items(), key=lambda x: x[1], reverse=True)

    skillsSortedByFrequency = [item[0] for item in sorted_items]

    applicants_to_jobs_ratio = 0
    if number_of_listings_scrapped_for_number_of_applicants > 0:
        applicants_to_jobs_ratio = number_of_applicants / number_of_listings_scrapped_for_number_of_applicants
    returnData = {}
    returnData["skills"] = skillsDict
    returnData["average-salary"] = averageSalary
    returnData["applicants-to-jobs-ratio"] = applicants_to_jobs_ratio
    
    return returnData

def scrapeInternshalaListingData(profile="", location="", experience=0, type=""):
    jsonData = []
    profile = profile.replace(" ", "-")
    
    def get_html(page):
        url = ""
        if type == "job":
            if(experience == 0):
                url = f"https://internshala.com/fresher-jobs/{profile}-jobs-in-{location}/page-{page}"
            else:
                url = f"https://internshala.com/jobs/{profile}-jobs-in-{location}/experience-{experience}/page-{page}"
        elif type == "internship":
            url = f"https://internshala.com/internships/{profile}-internship-in-{location}/page-{page}"
        resp = httpx.get(url)
        return HTMLParser(resp.text)
    
    webpage = get_html(1)
    number_of_pages = int(webpage.css_first("span#total_pages").text())

    for page_number in range(1, number_of_pages):
        print("page", page_number, "/", number_of_pages)
        webpage = get_html(page_number)
        listingCards = webpage.css_first(f"#internship_list_container_{page_number}")
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

        for url in listingLinks:
            listingData = {
                "title": "",
                "skills": [],
                "url": "",
                "salary": 0,
                "type": type
            }
            listingPage = HTMLParser(httpx.get(url).text)
            print(url)
            return

            # URL #
            listingData["url"] = url
            
            # Title #
            listingData["title"] = listingPage.css_first("#details_container > h1").text().strip()

            # Skills #
            skillsHTML = listingPage.css("span.round_tabs")
            totalListingsVisitedForSkills += 1

            if(len(skillsHTML) == 0):
                print("Listing had no listed skills")
                skillsNotFound += 1
                continue

            listingData["skills"] = list(map(lambda x: x.text().strip().lower(), skillsHTML))
            # Salary #
            if type == "job":
                with open("html.html" , "w+") as f:
                    f.write(listingPage.text())
                    print(listingPage.text())
                
                salaryHTML = listingPage.css_first("span.desktop")
                salaryStr = salaryHTML.text().strip()

                if(salaryStr == "Competitive salary"):
                    continue

                salaryStr = salaryStr[2:]
                endIndexForFirstNumber = len(salaryStr)
                startIndexForSecondNumber = len(salaryStr)
                secondNumber = 0
                divideFactor = 2

                try:
                    endIndexForFirstNumber = salaryStr.index("-")
                    startIndexForSecondNumber = endIndexForFirstNumber + 2
                    secondNumber = int(salaryStr[startIndexForSecondNumber:].strip().replace(",", ""))
                except ValueError as e:
                    divideFactor = 1

                firstNumber = int(salaryStr[0:endIndexForFirstNumber].strip().replace(",", ""))
                listingData["salary"] = (firstNumber + secondNumber) // divideFactor
            elif type == "internship":
                salaryHTML = listingPage.css_first(".stipend")
                salaryStr = salaryHTML.text().strip()

                if(salaryStr == "Competitive salary"):
                    continue

                salaryStr = salaryStr[2:]
                endIndexForFirstNumber = len(salaryStr)
                startIndexForSecondNumber = len(salaryStr)
                secondNumber = 0
                divideFactor = 2

                try:
                    endIndexForFirstNumber = salaryStr.index("-")
                    startIndexForSecondNumber = endIndexForFirstNumber + 2
                    secondNumber = int(salaryStr[startIndexForSecondNumber:].strip().replace(",", ""))
                except ValueError as e:
                    divideFactor = 1

                firstNumber = int(salaryStr[0:endIndexForFirstNumber].strip().replace(",", ""))
                listingData["salary"] = (firstNumber + secondNumber) // divideFactor

            jsonData.append(listingData)

    return jsonData

def scrapeInternshalaJobsAndInternships(profile="", location="", experience=0):
    profile = profile.replace(" ", "-")
    jsonData = []
    jsonData.append(scrapeInternshalaListingData(profile, location, experience, type="job"))
    jsonData.append(scrapeInternshalaListingData(profile, location, experience, type="internship"))
    return jsonData

if __name__ == "__main__":
    # print(scrapeNaukriDotCom(title = "data science analyst", location="", experience=""))
    # print(listings)
    with open("jsonData.json", "w+") as f:
        f.write(str(scrapeNaukriDotCom(title="data science", location="", experience=0)))