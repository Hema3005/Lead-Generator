import re
import usaddress
import urllib.request
from bs4 import BeautifulSoup
def get(data):
    address_list=[]
    patterns=[
    r"[0-9]{1,4} .+\n.+, [A-Z]{2} [0-9]{5}",
r"[0-9]{1,4} .+,.+ [0-9]{5}",
r"[0-9]{1,4} .+\n.+\n.+, [A-Z]{2} [0-9]{5}",
r"[0-9]{1,4} .+\n.+, [A-Z]{2} .+\nCanada\b",
r"[0-9]{1,4} .+, [A-Z]{2} [0-9]{5}",
r"[0-9]{1,4} .+\n.+ [A-Z]{2} [0-9]{5}",
r"Wells .+\n.+\n.+\n.+\nUnited Kingdom",
r"One Apple .+\n\s*[A-Z|a-z]*, [A-Z]{2} [0-9]{5}" ,
r"[0-9]{4}.+, [A-Z]{2} [0-9]{5} ",
r"[0-9]{1,4} .+\n.+, [A-Z]{2} [0-9]{5}",
r"[0-9]{1,4}.+, India [0-9]{6}",
r"Level [0-9]{1,4}.+, [A-Z]{3} [0-9]{4} Australia",
r"[0-9]{1,4} .+[A-Z 0-9]{5}",
r"[0-9]{1,4} .+,\s[A-Z|0-9]{5}\s[A-Z|0-9]{3}",
r"[0-9]{1,4} .+\n.+\n\n.+, [A-Z]{2}\n.+ [0-9]{5}",
r"[0-9]{1,4} .+\n\s*.+\n\s*.+, [A-Z]{2}\s*[A-Z 0-9]{7}",
r"[A-Z a-z,]* [A-Z]{2}\n{3}[0-9]{1,5}",
r"[0-9].+,\s[0-9].+\n.+\n.+,\s[a-z A-Z -]*[0-9]{6}\n.Maharashtra"

]



   
    for pattern in patterns:
        find = re.findall(pattern,data.strip(), flags = re.MULTILINE)
        if find:
            print("Searching...........")
            for item in find:
                item= re.sub(r'[^\x00-\x7f]',' ', item)
                item= re.sub(r'\n|\t|\r',' ', item)
                if len(item)>4:
                   address_list.append(item)
                   
        else:
            print("Searching...........")
    address_list=list(dict.fromkeys(address_list))
    print("got the address")
    return address_list

    
# def get_state(address_list):
#     state_list=[]
#     for item in address_list:
#         item_parse=usaddress.parse(item)
#         for index in item_parse:
#             if index[1]=="StateName":
#                 state_list.append(index[0])
#     return state_list

# def get_companyAddress_list(company,address_list):
#     companyAdress_list=[]
#     for address in address_list:
#         companyAdress_list.append( company+","+address )
#     return companyAdress_list
        