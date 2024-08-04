import pickle
import pandas as pd
entryLevel = 0
advanceLevel = 0

def dataCleaningKnown(data):
    # with open("data", "rb") as fp:   # Unpickling
        # data = pickle.load(fp)  
    
 
    df = pd.DataFrame(data, columns=["jobTitle","companyName","skills","jobDetailURL","jobDescription","salary","experience","listingType","portal"])
    for i in data:
        if len(i)!= 9:
            print(i)

    def convert_and_return_avg_in_lakhs(value):
    # function that extract value from salary string and return the average in LPA

        try:
            #for range which has both thousands and lacks
            if ',' in value and ('Lac' in value or 'Lacs' in value):
                value = value.replace(',', '') #str
                value=value.split(" ")[0] #str
                value = value.split("-") #arr of str
                temp = 0
                for i in value:
                    i=float(i)
                    if i > 1000:
                        i=i/100000
                    temp += float(i)
                value = temp/2
                return value 
            
            # for range which has only thousands
            elif ',' in value:
                
                value = value.replace(',', '') #str
                value=value.split(" ")[0] #str
                
                if "-" in value: 
                    value = value.split("-") #arr of str
                    temp = 0
                    for i in value:
                        i=float(i)
                        i= i/100000
                        temp += i
                    value = temp/2
                    return value
                else:
                    value = float(value)
                    value = value/100000
                    return value
            # values that has lacs and crores     
            elif 'Cr' in value and ('Lac' in value or 'Lacs' in value):
                value = value.replace(' Lacs', '').replace(' Lac', '').replace(' Cr', "")
                value = value.split(" ")[0]
                value = value.split("-")
                temp = 0
                for i in range(len(value)):
                    value[i]=float(value[i])
                    if i == 1:
                        value[i]=value[i]*100
                    temp += value[i]
                value = temp/2
                return value
            # values that has range in crores
            elif 'Cr' in value:
                value=value.split(" ")[0] #str
                if "-" in value: 
                    value = value.split("-") #arr of str
                    temp = 0
                    for i in value:
                        i=float(i)
                        i=i*100
                        temp += i
                    value = temp/2
                    return value
                else:
                    value = float(value)
                    return value
            # for lacs    
            elif 'Lac' in value or 'Lacs' in value:
                
                value=value.split(" ")[0] #str
                if "-" in value: 
                    value = value.split("-") #arr of str
                    temp = 0
                    for i in value:
                        i=float(i)
                        temp += i
                    value = temp/2
                    return value
                else:
                    value = float(value)
                    return value
            else:
                return None
        except:
            return value
        
    df['Average Salary (Lacs PA)'] = df['salary'].apply(convert_and_return_avg_in_lakhs)


        # it only consiters the numeric and replace rest with None and then it calculates the mean salary or average salary
    average_salary = pd.to_numeric(df["Average Salary (Lacs PA)"], errors='coerce').mean() 


    #extracting skills
    skills={}
    def extracting_skills(value):
        arr = value
        for skill in arr:
            if skill in skills:
                skills[skill]+=1
            else:
                skills[skill]=1

    df["skills"].apply(extracting_skills)
    #sorting the skill dictionary in decresing order to frequency of the skills
    sorted_skills = dict(sorted(skills.items(), key=lambda item: item[1], reverse=True))



    jobTitles={}
    def extracting_jobTitles(value):
        
        if value in jobTitles:
            jobTitles[value]+=1
        else:
            jobTitles[value]=1

    df["jobTitle"].apply(extracting_jobTitles)

    #sorting the skill dictionary in decresing order to frequency of the skills
    sorted_jobTitles = dict(sorted(jobTitles.items(), key=lambda item: item[1], reverse=True))
    

    # print(df["experience"])

    def experience(value):
        global entryLevel, advanceLevel  # Access global variables
        if value[0] == "0":
            entryLevel += 1
        else:
            advanceLevel += 1

    df["experience"].apply(experience)




    total_jobs = len(df.index)
    skill_list = []
    skillValue_list = []
    jobTitle_list = []
    jobTitleValue_list = []

    for key, value in sorted_jobTitles.items():
        jobTitle_list.append(key)
        jobTitleValue_list.append(value)


    for key, value in sorted_skills.items():
        skill_list.append(key)
        skillValue_list.append(value)
    
    #this dict contains 2 key value pair each value is a tuple of all the skill and its corresponding
    skill_value_dict = {"total_jobs":total_jobs,"skills" : tuple(skill_list),"skillValues" : tuple(skillValue_list),"avg_sal":average_salary,"jobTitles":tuple(jobTitle_list),"jobTitleValues":tuple(jobTitleValue_list),"entryLevel": entryLevel, "advanceLevel": advanceLevel}

    with open("knownData", "wb") as fp:   #Pickling
        pickle.dump(skill_value_dict, fp)

    return skill_value_dict


def dataCleaningUnknown(data):
    # with open("data", "rb") as fp:   # Unpickling
        # data = pickle.load(fp)  
    
 
    df = pd.DataFrame(data, columns=["field","jobTitle","skills","salary","experience","listingType","portal"])
    
    field_freq_dict = df['field'].value_counts().to_dict()

    def convert_and_return_avg_in_lakhs(value):
    # function that extract value from salary string and return the average in LPA

        try:
            #for range which has both thousands and lacks
            if ',' in value and ('Lac' in value or 'Lacs' in value):
                value = value.replace(',', '') #str
                value=value.split(" ")[0] #str
                value = value.split("-") #arr of str
                temp = 0
                for i in value:
                    i=float(i)
                    if i > 1000:
                        i=i/100000
                    temp += float(i)
                value = temp/2
                return value 
            
            # for range which has only thousands
            elif ',' in value:
                
                value = value.replace(',', '') #str
                value=value.split(" ")[0] #str
                
                if "-" in value: 
                    value = value.split("-") #arr of str
                    temp = 0
                    for i in value:
                        i=float(i)
                        i= i/100000
                        temp += i
                    value = temp/2
                    return value
                else:
                    value = float(value)
                    value = value/100000
                    return value
            # values that has lacs and crores     
            elif 'Cr' in value and ('Lac' in value or 'Lacs' in value):
                value = value.replace(' Lacs', '').replace(' Lac', '').replace(' Cr', "")
                value = value.split(" ")[0]
                value = value.split("-")
                temp = 0
                for i in range(len(value)):
                    value[i]=float(value[i])
                    if i == 1:
                        value[i]=value[i]*100
                    temp += value[i]
                value = temp/2
                return value
            # values that has range in crores
            elif 'Cr' in value:
                value=value.split(" ")[0] #str
                if "-" in value: 
                    value = value.split("-") #arr of str
                    temp = 0
                    for i in value:
                        i=float(i)
                        i=i*100
                        temp += i
                    value = temp/2
                    return value
                else:
                    value = float(value)
                    return value
            # for lacs    
            elif 'Lac' in value or 'Lacs' in value:
                
                value=value.split(" ")[0] #str
                if "-" in value: 
                    value = value.split("-") #arr of str
                    temp = 0
                    for i in value:
                        i=float(i)
                        temp += i
                    value = temp/2
                    return value
                else:
                    value = float(value)
                    return value
            else:
                return None
        except:
            return value
        
    # Apply the function to the 'salary' column
    df['Average Salary (Lacs PA)'] = df['salary'].apply(convert_and_return_avg_in_lakhs)

    # Group by 'field' and calculate the mean of 'Average Salary (Lacs PA)'
    average_salary_dict = df.groupby('field')['Average Salary (Lacs PA)'].apply(lambda x: pd.to_numeric(x, errors='coerce').mean()).to_dict()
    
# 
# -________________________skill___________________________
    # Initialize an empty dictionary to store the top 5 skills for each field
    top_skills_dict = {}

    # Loop through each unique field
    for field in df['field'].unique():
        # Filter the data for the current field
        field_data = df[df['field'] == field]
        
        # Initialize an empty dictionary to store the skill frequencies
        skill_freq = {}
        
        # Loop through each row in the filtered data
        for skills in field_data['skills']:
            # Loop through each skill in the row
            for skill in skills:
                # Increment the frequency of the skill
                if skill in skill_freq:
                    skill_freq[skill] += 1
                else:
                    skill_freq[skill] = 1
    
        # Get the top 5 skill names
        top_5_skills = [skill for skill, freq in sorted(skill_freq.items(), key=lambda item: item[1], reverse=True)[:5]]
        
        # Store the top 5 skills in the dictionary
        top_skills_dict[field] = top_5_skills
#   -________________________skill___________________________
    # print(top_skills_dict)
    # return

#   -________________________No of Listings___________________________

    listing_count_dict = df.groupby('field').size().to_dict()
    # print(listing_count_dict)
    # return
#   -________________________No of Listings___________________________






    def experience(value, entryLevel, advanceLevel):
        if value[0] == "0":
            entryLevel[0] += 1
        else:
            advanceLevel[0] += 1

    field_experience_counts = {}

    for field in df['field'].unique():
        entryLevel = [0]
        advanceLevel = [0]
        
        field_data = df[df['field'] == field]
        
        field_data['experience'].apply(lambda x: experience(x, entryLevel, advanceLevel))
        
        field_experience_counts[field] = {
            'entryLevel': entryLevel[0],
            'experienced': advanceLevel[0]
        }

    # print(field_experience_counts)
    # return

    
    #this dict contains 2 key value pair each value is a tuple of all the skill and its corresponding
    returnData = {"total_jobs_comparision":listing_count_dict,"AvgSalary" : average_salary_dict,"experience_counts":field_experience_counts,"topFiveSkills" : top_skills_dict,}
    
    with open("unknownData", "wb") as fp:   #Pickling
        pickle.dump(returnData, fp)
    
    return returnData

