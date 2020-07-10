import requests
 
from bs4 import BeautifulSoup

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

url = "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"

#to get page html
page_html=get_webpage(url)

#to get page text
page_text=get_webpage_text(page_html)


# to get list containing companies and url
companyName_list=get_list(page_html)
# # Extracting URLs from the attribute href in the <a> tags.
print(companyName_list)
