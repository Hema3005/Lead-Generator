import urllib.request
from bs4 import BeautifulSoup
import Get_Address #create module to get address
import json
import csv
import re
import usaddress
import logging



def get_webpage(url : str )-> str:
    try:
        # Getting the webpage, creating a Response object.
        response = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        html = urllib.request.urlopen(response)
        html_bytes = html.read()
        page_html= html_bytes.decode("utf8")
        return page_html
    except:
        return None

def get_webpage_text(html : str )-> str:
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

    company_name_url_list=[]
    for name in a_tag:
        if name.text!="View From The Top Profile":
            company_name_url_list.append([name.text,name.get('href')])
    return company_name_url_list


def get_contact_page_link(html : str )-> list:
    contact_list=[]
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.find_all('a'):
        try:
            link=tag.attrs['href']
        
            name=tag.text
            title=["Contact","Offices","about","contact","support"]
            for item in title:
                if item in name:
                    contact_list.append(link)
        
        except:
            link=tag.get('href')
            name=tag.text
            title=["Contact","Offices","about","contact","support"]
            for item in title:
                if item in name:
                    contact_list.append(link)
        
    contact_list=list(dict.fromkeys(contact_list))
    return contact_list


def get_location(text : str)-> list:
    
    location_list=[]
    #using module Get_Address to get address list
    address_list=Get_Address.get(text)
    #remove repeating address
    location_list=[item for item in address_list if item not in location_list]
    return location_list

def save_to_json(filename : str ,json_dict : dict)-> None:

     with open(filename, "w") as file_obj:
            #write company and address in json
            file_obj.write(json.dumps(json_dict, sort_keys=False, indent=2, separators=(',', ': ')))
            print("\nSuccessfully company address details save into \"company_adderss.json\" \n ")
     

def json_to_csv_file(json_filename  : str ,csv_filename : str)-> None:
    # Opening JSON file and loading the data 
    # into the variable data 
    with open(json_filename) as json_file: 
        data =json.load(json_file)
        
         # writing to csv file  
        with open(csv_filename, 'w') as csvfile: 

            # field names  
            fields = ["Company Name","Addresses"]  
       
            # creating a csv dict writer object  
            writer = csv.DictWriter(csvfile ,fieldnames = fields)  
        
            # writing headers (field names)  
            writer.writeheader()  
            for item in data:
                add=" | ".join(data[item])
                
                row={'Company Name':item,'Addresses':add}
        
               # writing  row  
                writer.writerow(row)
            print("Successfully convert \"comapny_address.json\" into \"company_address.csv\" \n") 


if __name__ == '__main__':
    #Create and configure logger
    logging.basicConfig(filename="Company_details.log",format='%(asctime)s %(message)s',filemode='w')
    #Creating an object
    logger=logging.getLogger()
    #Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    logger.info("List of companies that has no contact details and no address details")

    #starts from here
    url = "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm"
    #getting html content
    html= get_webpage(url)
    print("html content of The Top 100 Companies in the Digital Content Industry: The 2016-2017 EContent 100")
    # print(html)
    print("\n\n")
    #getting company list
    company_list=get_list(html)
    print("list of 100 company with its url: ")
    print("\n\n")
    #print list contain company and their url
    print(company_list)
    print("\n\n")
    print("length of company list : ",len(company_list))
    print("\n\n")
    
    all_contact_list=[]
    #testing for 1st ten companies
    for company in company_list[:10]:
        contact_list=[]
        url=company[1]
        html=get_webpage(url)
        if html==None:
            print("could not get contact page for :"+company[0]+"\n")
            pass
        else:
            #getting contact list of each company 
            contact_page_list=get_contact_page_link(html)
            if len(contact_page_list):
                print("got contact page links for :"+company[0]+"\n")
                for item in contact_page_list:
                    if item.startswith('/'):
                        contact_list.append(company[1]+item)
                    else:
                        contact_list.append(item)
                all_contact_list.append([company[0],contact_list])
            else:
                print("no contact page for "+company[0]+"\n")
                logger.setLevel(logging.DEBUG)
                logger.info("NO CONTACT DETAILS")
                logger.info(company[0])
            
    print("list of  company with its contact url: ")
    print("\n\n")
    #print company  contact list
    print(all_contact_list)
    print("\n\n")
    print("No. of company has contact list : ",len(all_contact_list))
    print("\n\n")
    
    no_address_list=[]
    final_dict={}
    for item in all_contact_list:
        company_name=item[0]
        companyContact_url=item[1][0]
        #getting contact url html 
        page_html=get_webpage(companyContact_url)
        if page_html==None:
            no_address_list.append(company_name)
            pass
        else:
            #getting contact url text
            page_text=get_webpage_text(page_html)
            #getting location_list
            location_list=get_location(page_text)
            if len(location_list):
                final_dict.update({company_name:location_list})
                print("Company name:",company_name)
                print("Addresses:\n",location_list)
                print("\n")
            else:
                no_address_list.append(company_name)

    
    print("\nCompany with address:\n")
    print(final_dict)
    print("\nList to companies not have address:\n ")
    print(no_address_list)
    logger.info("NO ADDRESS DETAILS")
    #company has no adress store in log file
    for name in no_address_list:
        logger.setLevel(logging.DEBUG)
        logger.info(name)
      
    filename="company_address.json"
    save_to_json(filename,final_dict)
    json_to_csv_file(filename,"company_address.csv")
    print("Company may not have contact page and adress details stored in Log file.\nCheck \"Company_details.log\" ")