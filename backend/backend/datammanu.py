def convert_to_lacs(value):
    """Helper function to convert various salary components to lacs."""
    try:
        if ',' in value and ('Lac' in value or 'Lacs' in value):
            value = value.replace(',', '') #str
            value=value.strip(" ")[0] #str
            value = value.strip("-") #arr of str
            temp = 0
            for i in value:
                i=float(i)
                if i > 1000:
                    i=i/100
                temp += float(i)
            value = temp/2
            return value  # 1 Lakh = 100 Thousand
        elif ',' in value:
            value = value.replace(',', '') #str
            value=value.strip(" ")[0] #str
            if "-" in value: 
                value = value.strip("-") #arr of str
                temp = 0
                for i in value:
                    i=float(i)
                    if i > 1000:
                        i=i/100
                    temp += i
                value = temp/2
            else:
                value = float(value)
            
        elif 'Cr' in value and ('Lac' in value or 'Lacs' in value):
            value = value.replace(' Lac', '').replace(' Lacs', '').replace(' Cr', "")
            value = value.strip(" ")[0]
            value = value.strip("-")
            temp = 0
            for i in range(value):
                value[i]=float(value[i])
                if i == 1:
                    value[i]=value[i]*100
                temp += value[i]
            value = temp/2
            return value
        
        elif 'Cr' in value:
            value=value.strip(" ")[0] #str
            if "-" in value: 
                value = value.strip("-") #arr of str
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
            
        elif 'Lac' in value or 'Lacs' in value:
            value=value.strip(" ")[0] #str
            if "-" in value: 
                value = value.strip("-") #arr of str
                temp = 0
                for i in value:
                    i=float(i)
                    temp += i
                value = temp/2
            return value
            else:
                value = float(value)
                return value
    except:
            return