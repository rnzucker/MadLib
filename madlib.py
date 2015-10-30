"""Practicing some basic web scraping

I am using the O'Reilly book, "Web Scraping with Python" by Ryan Mitchell.
It's a very readable book for a technical book.

This will just be basic demonstrations. No deep scraping of a website(s)
as I don't want to get in trouble.
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys, logging, requests

__author__ = 'rnzucker'

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def id_spoof():
    """Simple browser agent spoofing
    """
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    # Check to
    url = "https://www.whatismybrowser.com/developers/what-http-headers-is-my-browser-sending"
    req = session.get(url, headers=headers)

    bsObj = BeautifulSoup(req.text, "html.parser")
    print(bsObj.find("table",{"class":"table-striped"}).get_text)

def main():
    # id_spoof()
    # try:
    #     html = urlopen("http://www.pythonscraping.com/pages/page1.html")
    # except HTTPError as e:
    #     print(e)
    #     return
    # if html is None:
    #     print("URL is not found")
    #     return
    r = requests.get("http://www.pythonscraping.com/pages/page1.html")
    # bsObj = BeautifulSoup(html.read(), "html.parser")
    print(r.text)
    bsObj = BeautifulSoup(r.text, "html.parser")
    # print(bsObj.h1)
    print(bsObj.body)



main()
