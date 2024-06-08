import httpx
from selectolax.parser import HTMLParser
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from flask import Response
from dataclasses import dataclass, asdict
import collections
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "AppId" : "109",
    "SystemId" : "Naukri"
}

def scrapeNaukriDotCom(title: str, experience: int, location: str) -> list:
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    
    testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo=1&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
    resp = requests.get(testURL, headers=headers)
    respJson = resp.json()
    listingsCSVStyle = {
                "title": [],
                "companyName": [],
                "skills": [],
                "jobURL": []
            }
    jobDetails = respJson["jobDetails"] 
    for jobDetail in jobDetails:
        try:
            jobDetailTitle = jobDetail["title"]
            jobDetailCompanyName = jobDetail["companyName"]
            jobDetailTagsAndSkills = jobDetail["tagsAndSkills"]
            jobDetailJobURL = jobDetail["jdURL"]
        except KeyError as err:
            continue
        listingsCSVStyle["title"].append(jobDetailTitle)
        listingsCSVStyle["companyName"].append(jobDetailCompanyName)
        listingsCSVStyle["skills"].append(jobDetailTagsAndSkills)
        listingsCSVStyle["jobURL"].append(jobDetailJobURL)
    
    listingsJsonStyle = []

    for i in range(0, len(listingsCSVStyle["title"])):
        temp = {}
        temp["companyName"] = listingsCSVStyle["companyName"][i]
        temp["title"] = listingsCSVStyle["title"][i]
        temp["skills"] = listingsCSVStyle["skills"][i]
        temp["jobURL"] = "https://www.naukri.com" + listingsCSVStyle["jobURL"][i]
        listingsJsonStyle.append(temp)

    # listingsJsonStyle = json.dumps(listingsJsonStyle)
    return listingsJsonStyle
    # listingsCSVStyle = json.dumps(listingsCSVStyle)
    # return listingsCSVStyle
    
def scrapeInternshala(profile: str, location: str) -> list:
    # for now we are only supporting profile and location
    # profile is a mendatory argument
    URL = "https://www.internshala.com/internship/"
    profile = profile.strip().lower().replace(' ', '-') + "-internship/"
    location = location.strip().lower().replace(' ', '-')
    if(location != ''):
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships-in-{location}/part-time-true/"
    else:
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships/part-time-true/"
    
    listingsCSVStyle = {"title": [],
                    "companyName": [],
                    "skills": [],
                    "jobURL": []
                }
    resp = httpx.get(URL, headers=headers)
    soup = BeautifulSoup(resp, 'html.parser')
    numberOfPages = int(soup.find(id="total_pages").text)
    # for i in range(1, numberOfPages+1):
    for i in range(1, 2):
        URL = URL + f"page-{i}/"
        resp = httpx.get(URL, headers=headers)
        print(URL)
        soup = BeautifulSoup(resp, 'html.parser')
        internshipListingCards = soup.find_all(class_="container-fluid individual_internship visibilityTrackerItem")
        for internshipListingCard in internshipListingCards:
            #Getting title and company name
            internshipListingCardTitleAndCompany = internshipListingCard.div.find(class_ = "individual_internship_header").find(class_="company")
            internshipListingCardTitle = internshipListingCardTitleAndCompany.find(class_="heading_4_5 profile")
            internshipListingCardCompanyName = internshipListingCardTitleAndCompany.find(class_="heading_6 company_name")
            
            listingsCSVStyle["title"].append(internshipListingCardTitle.text.strip())
            listingsCSVStyle["companyName"].append(internshipListingCardCompanyName.text.strip())
            
            #Getting skills
            internshipListingCardDetailsPageLink = "https://internshala.com" + internshipListingCard.find(class_="button_container_card").div.a['href']
            detailsPage = httpx.get(internshipListingCardDetailsPageLink, headers=headers)
            detailsPageHTML = BeautifulSoup(detailsPage, "html.parser")
            # in case no skills are found
            try:
                skillsFromDetailsPage = detailsPageHTML.find(class_ = "round_tabs_container").children
                skills = []
                for skill in skillsFromDetailsPage:
                    if(skill.text != "\n"):
                        skills.append(skill.text)
                listingsCSVStyle["skills"].append(skills)
            except AttributeError as err:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                print(URL)
                print(err)
                skillsFromDetailsPage = "No skills found"
                listingsCSVStyle["skills"].append(["No skills listed"])
            listingsCSVStyle["jobURL"].append(internshipListingCardDetailsPageLink)

    listingsJsonStyle = []

    for i in range(0, len(listingsCSVStyle["title"])):
        temp = {}
        temp["companyName"] = listingsCSVStyle["companyName"][i]
        temp["title"] = listingsCSVStyle["title"][i]
        temp["skills"] = listingsCSVStyle["skills"][i]
        temp["jobURL"] = listingsCSVStyle["jobURL"][i]
        listingsJsonStyle.append(temp)

    return listingsJsonStyle

def scrapeInternshalaV2(profile="", location="", experience=0):
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

    sorted_array = [item[0] for item in sorted_items]

    skillsDict = sorted(skillsDict, reverse=False)
    # Returing data
    applicants_ratio_to_jobs_ratio = number_of_applicants / number_of_listings_scrapped_for_number_of_applicants
    returnData = {}
    returnData["skills"] = sorted_array
    returnData["average-salary"] = averageSalary
    returnData["applicants-to-jobs-ratio"] = applicants_ratio_to_jobs_ratio
    with open("output.json", "w+") as f:
        f.write(json.dumps(returnData))
    
    return returnData
    

def scrape(info: dict) -> json:
    internshalaData = scrapeInternshalaV2(profile=info["title"], location=info["location"], experience=info["experience"])
    naukriDotComData = scrapeNaukriDotCom(info["title"], info["experience"], info["location"])
    response = internshalaData + naukriDotComData
    response = json.dumps(response)
    return response

if __name__ == "__main__":
    scrapeInternshalaV2("web-development", "", 0)