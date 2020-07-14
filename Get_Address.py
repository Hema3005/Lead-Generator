import re

def get(data):
    address_list=[]
    patterns=[r'[0-9|a-zA-Z]*\s[a-z|A-Z|0-9]*\s[A-Z|a-z|0-9]*\s[A-Z|a-z|0-9]*[,]\s[A-Z]{2}[\s][0-9]{5}',r'[0-9|A-Z|a-z ]*\n[A-Z|a-z ]*\n\t\t\t\t\t[A-Z|a-z]*[,]\s[A-Z]{2}\s[0-9]{5}',r'[0-9|A-Z|a-z]*\s[A-Z|a-z|0-9]*\s[A-Z|a-z|0-9]*[, ]\s[A-Z|a-z]*\s[0-9]*\n[A-Z|a-z\s]*[,]\s[A-Z]{2}\s[0-9]{5}',r'^\s[0-9]{3}\s[a-z|A-Z|0-9\s]*[,]\s[0-9|a-z|A-Z]*\s[a-z|A-Z]*\n[A-Z|a-z\s]*[, ]\s[A-Z]{2}\s[0-9]{5}',r'^[0-9a-zA-Z ]*[, ]\s[0-9A-Za-z\s]*[, ]\s[a-zA-z\s]*[0-9a-zA-z]{5}\n\bUnited States|USA\b$',r'^[0-9]{3}[a-z|A-Z\s]*\s[a-z|A-Z]{2}.[A-Z|a-z]*\s[0-9]*[A-z|a-z|0-9]*[,]\s[A-Z]{2}\s[0-9]{5}$']
    for pattern in patterns:
        find = re.findall(pattern,data.strip(), flags = re.MULTILINE)
        for item in find:
            item= re.sub(r'[^\x00-\x7f]',' ', item)
            item= re.sub(r'\n|\t|\r',' ', item)
            if len(item)>4:
                 address_list.append(item)
    address_list=list(dict.fromkeys(address_list))
    return address_list