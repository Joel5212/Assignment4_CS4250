from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re

client = MongoClient(host="localhost", port=27017)
db = client.Assignment4_CS4250
pages = db.pages

def crawlerThread():
    pages.drop()
    frontier = ['https://www.cpp.edu/sci/computer-science/']
    counter = 0
    base_urls = {}
    while len(frontier) > 0:
        url = frontier.pop(0)
        try:
            html = urlopen(url)
            bs = BeautifulSoup(html, 'html.parser')
        except Exception:
            pass
        storePage(url, bs)
        if targetPage(bs):
            frontier.clear()
            print("FOUND WEBPAGE, Attempts: " + str(counter))
            break
        else:
            counter+=1 
            regex = re.compile('.*\.(html|shtml)$|[^.]*$')
            a_tags = bs.find_all("a", href = regex)
            for a_tag in a_tags:
                url_tag = a_tag['href']

                if (re.match("^https://www.cpp.edu", url_tag) == None):
                    url_tag = "https://www.cpp.edu" + url_tag

                if urlAlreadyExists(url_tag) == False:
                    frontier.append(url_tag)

def urlAlreadyExists(url):
    return pages.find_one({"url": url}) != None

def storePage(url, bs):
    pages.insert_one({"url": url, "html": bs.prettify()})

def targetPage(bs):
    return bs.find('h1', string ="Permanent Faculty") != None

crawlerThread()



