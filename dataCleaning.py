import pickle
import pandas as pd

def dataCleaning(data):
    # with open("data", "rb") as fp:   # Unpickling
        # data = pickle.load(fp)  
    
    df = pd.DataFrame(data, columns=["jobTitle","companyName","skills","jobDetailURL","jobDescription","salary","listingType","portal"])


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
    total_jobs = len(df.index)
    #sorting the skill dictionary in decresing order to frequency of the skills
    sorted_skills = dict(sorted(skills.items(), key=lambda item: item[1], reverse=True))
    
    skill_list = []
    value_list = []

    for key, value in sorted_skills.items():
        skill_list.append(key)
        value_list.append(value)
    
    #this dict contains 2 key value pair each value is a tuple of all the skill and its corresponding
    skill_value_dict = {"total_jobs":total_jobs,"skills" : tuple(skill_list),"values" : tuple(value_list)}

    return skill_value_dict

