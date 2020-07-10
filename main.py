import requests
 
from bs4 import BeautifulSoup

import spacy

#load the language model instance in spacy
nlp =spacy.load('en_core_web_sm') 

def get_webpage(url : str )-> str:
    # Getting the webpage, creating a Response object.
    response = requests.get(url)
 
# Extracting the source code of the page.
    data = response.text
    return data

def get_webpage_text(html : str )-> str:

# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(page_html, 'lxml')
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
    for name_list in companyName_list:
     try:
        com_name=name_list[0]
        com_url=name_list[1]
        com_html=get_webpage(com_url)
    
        soup = BeautifulSoup(com_html, 'lxml')
        a_tag = soup.findAll('a')
        for name in a_tag:
            if "Contact" or "About" in name.text:
                contact_list.append([com_name,com_url+name.get('href')])
     except:
         print(com_name)

    return contact_list


def get_location(text : str)-> list:
    loc_list=[]
    doc = nlp(data)
#itrate each entity and append in list 
    for ent in doc.ents:
            if "GPE" in ent.label_ :
                data_list.append(ent.text)
#remove repeated name and their entity 
    com_loc_list= [] 
    [com_loc_list.append(x) for x in data_list if x not in res ]

    return com_loc_list


url = "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"

#to get page html
page_html=get_webpage(url)
# to get list conataining company name and contact url
comName_contactUrl_list=get_contact_page_link(page_html)

for company in comName_contactUrl_list:
     
     name=company[0]
     url=company[1]
     text=get_webpage_text(url)
     loction_list=get_location(text)
     print({name:loction_list)






