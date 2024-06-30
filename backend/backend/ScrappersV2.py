import httpx
from selectolax.parser import HTMLParser
import json
import pickle

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
    sumOfSalaries = 0
    numberOfSalariesCalculated = 0

    for page in range(1,noOfPages+1):
        print(page)
        URL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={page}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
        
        
        try:
            httpxResponse = httpx.get(URL, headers=headers, timeout=0.001)
        except httpx.TimeoutException as e:
            print('gottem')


        # httpxResponse = httpx.get(URL, headers=headers)
        jsonResponse = httpxResponse.json()
        jobDetails = jsonResponse["jobDetails"]

        for jobDetail in jobDetails:
            tempListing = {}
            try:
                
                # tempListing['jobTitle'] = jobDetail["title"]
                # tempListing["skills"] = jobDetail["tagsAndSkills"].lower().split(",")
                # tempListing["jobDetailURL"] = jobDetail["jdURL"]
                # tempListing["salary"] = jobDetail["placeholders"][1]["label"]
                # tempListing["type"] = "job"

                jobTitle = jobDetail["title"]
                skills = jobDetail["tagsAndSkills"].lower().split(",")
                jobDetailURL = jobDetail["jdURL"]
                jobDetailURL = "https://www.naukri.com"+jobDetailURL
                salary = jobDetail["placeholders"][1]["label"]
                listingType = "job"

                tempList = [jobTitle,skills,jobDetailURL,salary,listingType]

                listings.append(tempList)
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

            except KeyError as err:
                continue
        # if(numberOfSalariesCalculated == 0):
        #     returnData["average-salary"] = 0
        # else:
        #     returnData["average-salary"] = sumOfSalaries / numberOfSalariesCalculated
    
    return listings

# tempListing['jobTitle'] = jobDetail["title"]
# tempListing["skills"] = jobDetail["tagsAndSkills"].lower().split(",")
# tempListing["jobDetailURL"] = jobDetail["jdURL"]
# tempListing["salary"] = jobDetail["placeholders"][1]["label"]
# tempListing["type"] = "job"



# def scrapeInternshala(profile="", location="", experience=0):
#     profile = profile.replace(" ", "-")
#     def get_html(page):
#         if(experience == 0):
#             # Fresher
#             url = f"https://internshala.com/fresher-jobs/{profile}-jobs-in-{location}/page-{page}"
            
#         else:
#             url = f"https://internshala.com/fresher-jobs/{profile}-jobs-in-{location}/experience-{experience}/page-{page}"
#         resp = httpx.get(url, headers=normalHeaders)
#         return HTMLParser(resp.text)
#     webpage = get_html(1)
#     number_of_pages = int(webpage.css_first("span#total_pages").text())
#     salaryList = []
#     averageSalary = 0
#     skills = []
#     skillsDict = {}
#     applicants = []
#     number_of_applicants = 0
#     number_of_listings_scrapped_for_number_of_applicants = 0
#     for page_number in range(1, number_of_pages):
#         # # This if block is here for debugging. It would take a really long time to scrape so many pages so i limit it to only 1 page here.
#         # if page_number > 1:
#         #     break
#         print("page", page_number, "/", number_of_pages)
#         webpage = get_html(page_number);
#         salaries = webpage.css("span.desktop")
#         # return
#         listingCards = webpage.css_first(f"#internship_list_container_{page_number}")
#         if(listingCards is None):
#             print("listing container was not found in the html so early returning!")
#             str = webpage.html
#             return
#         else:
#             listingCards = listingCards.iter()
#         listingLinks = []
#         for listingCard in listingCards:
#             try:
#                 listingLinks.append("https://internshala.com" + listingCard.attributes['data-href'] + '/')
#             except KeyError:
#                 print(KeyError, "data-href attribute was not found in listing div")
#                 continue
#         totalListingsVisitedForSkills = 0
#         skillsNotFound = 0
#         # Scrapping Skills #
#         for url in listingLinks:
#             listingPage = HTMLParser(httpx.get(url, headers=normalHeaders).text)
#             # skillsExtractedRaw = listingPage.css("span.round_tabs")
#             skillsRawHTML = listingPage.css("span.round_tabs")
#             totalListingsVisitedForSkills += 1
#             if(len(skillsRawHTML) == 0):
#                 print("LENGTH OF SKILLS_RAW_HTML WAS 0 - No skills div found.")
#                 skillsNotFound += 1
#                 continue
#             skills_for_current_listing = list(map(lambda x: x.text().strip().lower(), skillsRawHTML))
#             skills.append(skills_for_current_listing)

#             # Applicants
#             try:
#                 number_of_applicants_in_current_listing = listingPage.css_first(".applications_message").text()[:-11].strip()
#                 if(number_of_applicants_in_current_listing == "1000+"):
#                     number_of_applicants_in_current_listing = 1000
#                 number_of_applicants += int(number_of_applicants_in_current_listing)
#                 number_of_listings_scrapped_for_number_of_applicants += 1
#             except Exception as e:
#                 print("something went wrong while scrapping number of applicants")
#                 print(e)
#                 print("-->", number_of_applicants_in_current_listing)
#             # Skills new format
#             for skill in skills_for_current_listing:
#                 incrementValueOfKey(skillsDict, skill)
#         print("totalListingsVisitedForSkills :", totalListingsVisitedForSkills, " / ", "skillsNotFound :", skillsNotFound)
#         for i in salaries:
#             if(i.text().strip() == "Competitive salary"):
#                 continue
#             salaryRange = i.text().strip()[2:]
#             endIndexForFirstNumber = len(salaryRange)
#             startIndexForSecondNumber = len(salaryRange)
#             secondNumber = 0
#             divideFactor = 2
#             try:
#                 endIndexForFirstNumber = salaryRange.index("-")
#                 startIndexForSecondNumber = endIndexForFirstNumber + 2
#                 secondNumber = int(salaryRange[startIndexForSecondNumber:].strip().replace(",", ""))
#             except ValueError as e:
#                 divideFactor = 1
#             firstNumber = int(salaryRange[0:endIndexForFirstNumber].strip().replace(",", ""))
#             averageSalary = (firstNumber + secondNumber) // divideFactor
#             salaryList.append(averageSalary)
#     sumOfSalaries = 0
#     for i in salaryList:
#         sumOfSalaries += i
#     if(len(salaryList) > 0):
#         averageSalary = sumOfSalaries/len(salaryList)
#     else:
#         print("why is salaryList's length 0????")
#         print(salaryList)
    
#     print(skillsDict)


#     sorted_items = sorted(skillsDict.items(), key=lambda x: x[1], reverse=True)

#     skillsSortedByFrequency = [item[0] for item in sorted_items]

#     applicants_to_jobs_ratio = 0
#     if number_of_listings_scrapped_for_number_of_applicants > 0:
#         applicants_to_jobs_ratio = number_of_applicants / number_of_listings_scrapped_for_number_of_applicants
#     returnData = {}
#     returnData["skills"] = skillsDict
#     returnData["average-salary"] = averageSalary
#     returnData["applicants-to-jobs-ratio"] = applicants_to_jobs_ratio
    
#     return returnData





if __name__ == "__main__":
    data = scrapeNaukriDotCom(title = "data science analyst", location="", experience="")
    
    with open("data", "wb") as fp:   #Pickling
        pickle.dump(data, fp)
    # print(listings)
    # scrapeInternshala(profile="data science", location="", experience=0)