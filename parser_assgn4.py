from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

client = MongoClient(host="localhost", port=27017)
db = client.Assignment4_CS4250
pages = db.pages

db = client.Assignment4_CS4250
faculty_members = db.faculty_members


def get_html():
    return pages.find_one({"url": "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"}, {"_id": 0, "url": 0})

def parse_doc():
    faculty_members.drop()
    html = get_html()
    # print(html['html'])
    bs = BeautifulSoup(html['html'], 'html.parser')
    names = []
    faculty_info = {}
    [names.append(name.get_text().replace("\n", " ").strip()) for name in bs.find('section').find_all('h2')]
    for strong in bs.find_all('strong'):
        strong_value = strong.get_text().replace("\n", " ").replace(":", " ").strip()
        if strong_value not in faculty_info:
            faculty_info[strong_value] = []
        if strong_value == 'Web' or strong_value == "Email":
            strong_next_sibling = strong.next_sibling.next_sibling.get_text().replace("\n", " ").strip()
            faculty_info[strong_value].append(strong_next_sibling)        
        else:    
            strong_next_sibling = strong.next_sibling.get_text().replace("\n", " ").strip()
            faculty_info[strong_value].append(strong_next_sibling)

    i = 0
    
    while i < len(names):
        name = names[i]
        title = faculty_info['Title'][i]
        office = faculty_info['Office'][i]
        phone = faculty_info['Phone'][i]
        email = faculty_info['Email'][i]
        web = faculty_info['Web'][i]
        faculty_members.insert_one({"name": name, "title": title, "office": office, "phone": phone, "email": email, "web": web})
        i+=1
    
    
parse_doc()


