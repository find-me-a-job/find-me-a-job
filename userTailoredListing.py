import pandas as pd
import json
import pickle



def listingSortedBySkills(data):

    with open('user_info.json', 'r') as file:
        user_data_json = json.load(file)

    users_skills = user_data_json["skill_stack"]

    df = pd.DataFrame(data, columns=["jobTitle","companyName","skills","jobDetailURL","jobDescription","salary","experience","listingType","portal"])
    
    def no_missing_skills(value):
        
        users_skill_set = set(users_skills)
        skills_from_df_set  = set(value)

        CommonElements = users_skill_set & skills_from_df_set

        noOfCommonElements = len(CommonElements)

        noOfMissingSkills = len(value) - noOfCommonElements

        return noOfMissingSkills
    
    def list_common_skills(value):

        users_skill_set = set(users_skills)
        skills_from_df_set  = set(value)

        CommonElements = users_skill_set & skills_from_df_set

        CommonSkills = list(CommonElements)

        return CommonSkills
    
    def list_missing_skills(value):
        common_skills = []
        for i in value:
            if i in users_skills:
                continue
            else:
                common_skills.append(i)

        return common_skills
    
    df['noOfMissingSkills'] = df['skills'].apply(no_missing_skills)
    
    df['CommonSkills'] = df['skills'].apply(list_common_skills)

    df['MissingSkills'] = df['skills'].apply(list_missing_skills)


    df = df.sort_values('noOfMissingSkills')

    listings = []


    for index, row in df.iterrows():
        listing_dict = {}
        skill_diff = []
        listing_dict["job_title"] = row["jobTitle"]
        listing_dict["company_name"] = row["companyName"]
        listing_dict["url"] = row["jobDetailURL"]

        for i in row['CommonSkills']:
            temp={}
            temp["skill"] = i
            temp["acquired"] = True
            skill_diff.append(temp)
        
        for i in row['MissingSkills']:
            temp={}
            temp["skill"] = i
            temp["acquired"] = False
            skill_diff.append(temp)
        
        listing_dict["skill_diff"] = skill_diff
        listings.append(listing_dict)
    
    with open("knownListings", "wb") as fp:   #Pickling
        pickle.dump(listings, fp)
    
    return listings



