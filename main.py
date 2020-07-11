import requests
 
from bs4 import BeautifulSoup

import spacy
import json
import csv

#load the language model instance in spacy
nlp =spacy.load('en_core_web_sm') 

def get_webpage(url : str )-> str:
    # Getting the webpage, creating a Response object.
    response = requests.get(url)
 
# Extracting the source code of the page.
    data = response.text
    
    return data

def get_webpage_text(html : str )-> str:
    response = requests.get(url)
 
# Extracting the source code of the page.
    html = response.text
# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(html, 'lxml')
    #Finding the text
    page_text = soup.text
    
    return page_text

def get_list(page_html)->list:
    # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(page_html, 'lxml')
 
# # Extracting all the <a> tags into a list.
    a_tag = soup.findAll('a', {'class': '100link'})

    company_list=[]
    for name in a_tag:
        if name.text!="View From The Top Profile":
         company_list.append([name.text,name.get('href')])

 
    return company_list


def get_contact_page_link(html : str )-> list:

    # to get list containing companies and url
    companyName_list=get_list(page_html)
    contact_list=[]
    
    for name_list in companyName_list[:1]:
       try:
        com_name=name_list[0]
        com_url=name_list[1]
        com_html=get_webpage(com_url)
    
        soup = BeautifulSoup(com_html, 'lxml')
        a_tag = soup.findAll('a')
        for name in a_tag:
            if  "About" and "Contact" in name.text:
                
                contact_list.append([com_name,com_url+name.get('href')])
       except:
         print(com_name)

    return contact_list


def get_location(text : str)-> list:
    loc_list=[]
    doc = nlp(text)
#itrate each entity and append in list 
    for ent in doc.ents:
            if "GPE" in ent.label_ :
                loc_list.append(ent.text)
#remove repeated name 
    com_loc_list= [] 
    [com_loc_list.append(x) for x in loc_list if x not in com_loc_list ]

    return com_loc_list

def save_to_json(filename : str ,json_dict : dict)-> None:

     with open(filename, "w") as f:
#write all the entites data in json
            f.write(json.dumps(json_dict, sort_keys=False, indent=2, separators=(',', ': ')))
     

def json_to_csv_file(json_filename  : str ,csv_filename : str)-> None:
            # Opening JSON file and loading the data 
# into the variable data 
    with open(json_filename) as json_file: 
        data =json.load(json_file)
        temp=[]
        for i in data:
            temp.append({"company name":i,"location":data[i]})

        # field names  
        fields = ["company name","location"]  
        # writing to csv file  
        with open(csv_filename, 'w') as csvfile: 
            # creating a csv dict writer object  
            writer = csv.DictWriter(csvfile, fieldnames = fields)  
        
            # writing headers (field names)  
            writer.writeheader()  
        
            # writing data rows  
            writer.writerows(temp) 


if __name__ == "__main__":
    
    url = "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"

    html= get_webpage(url)

    company_list=get_list(html)

    print(company_list)

    print("company name and url extracted!!!")


#to get page html
    page_html=get_webpage(url)
# to get list conataining company name and contact url
    comName_contactUrl_list=get_contact_page_link(page_html)

    print(" Getting  companyname and contact url list ")
    print(comName_contactUrl_list)
    print("\n")

    filename="ref.json"
    com_dict={}
    for company in comName_contactUrl_list:
        name=company[0]
        url=company[1]
        text=get_webpage_text(url)
    #  print(text)
        loction_list=get_location(text)
     
        com_dict[name]=loction_list
        # com_dict.update({"Comapny name":name,"location:"loction_list})
        print("\n")
    print(com_dict)
    save_to_json(filename,com_dict)
    print("\nsave to json file successfully\n")
    json_to_csv_file(filename,"ref.csv")
    print("Json to csv convert sucessfullly\n")






