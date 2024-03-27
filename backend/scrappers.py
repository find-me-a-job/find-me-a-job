import httpx
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


def scrapeNaukriDotCom(title="", experience=0, location = ""):
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    
    testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo=1&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "AppId" : "109",
        "SystemId" : "Naukri"
    }
    resp = requests.get(testURL, headers=headers)
    with open("foo2.json", 'w') as f:
        json.dump(resp.json(), f)
    respJson = resp.json()

    listings = {"title": [],
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
        listings["title"].append(jobDetailTitle)
        listings["companyName"].append(jobDetailCompanyName)
        listings["skills"].append(jobDetailTagsAndSkills)
        listings["jobURL"].append(jobDetailJobURL)
    df = pd.DataFrame(listings)
    print(df)

    


scrapeNaukriDotCom("web develoment", 0, "vadodara")






def scrapeInternshala(profile, location):
    # for now we are only supporting profile and location
    # profile is a mendatory argument
    URL = "https://internshala.com/internships/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    profile = profile.strip().lower().replace(' ', '-') + "-internship/"
    location = location.strip().lower().replace(' ', '-')
    if(location != ''):
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships-in-{location}/part-time-true/"
    else:
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships/part-time-true/"
    
    listings = {"title": [],
                "companyName": [],
                "skills": [],
                }
    resp = httpx.get(URL, headers=headers)
    soup = BeautifulSoup(resp, 'html.parser')
    numberOfPages = int(soup.find(id="total_pages").text)
    print(numberOfPages)
    for i in range(1, numberOfPages+1):
        URL = URL + f"page-{i}/"
        resp = httpx.get(URL, headers=headers)
        print(URL)


        soup = BeautifulSoup(resp, 'html.parser')
        try:
            internshipListingCards = soup.find_all(class_="container-fluid individual_internship visibilityTrackerItem")
            for internshipListingCard in internshipListingCards:
                #Getting title and company name
                internshipListingCardTitleAndCompany = internshipListingCard.div.find(class_ = "individual_internship_header").find(class_="company")
                internshipListingCardTitle = internshipListingCardTitleAndCompany.find(class_="heading_4_5 profile")
                internshipListingCardCompanyName = internshipListingCardTitleAndCompany.find(class_="heading_6 company_name")
                
                listings["title"].append(internshipListingCardTitle.text.strip())
                listings["companyName"].append(internshipListingCardCompanyName.text.strip())
                
                #Getting skills
                internshipListingCardDetailsPageLink = "https://internshala.com" + internshipListingCard.find(class_="button_container_card").div.a['href']
                detailsPage = httpx.get(internshipListingCardDetailsPageLink, headers=headers)
                detailsPageHTML = BeautifulSoup(detailsPage, "html.parser")
                skillsFromDetailsPage = detailsPageHTML.find(class_ = "round_tabs_container").children
                skills = []
                for skill in skillsFromDetailsPage:
                    if(skill.text != "\n"):
                        skills.append(skill.text)
                listings["skills"].append(skills)
        except AttributeError as err:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(URL)
            print(err)
    df = pd.DataFrame(listings)
    print(df)

    
scrapeInternshala("web development", "vadodara")