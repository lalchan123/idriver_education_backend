import pandas as pd
from bs4 import BeautifulSoup
import datetime
from datetime import date, datetime, timedelta
import requests
import json

def CNBC():

    API_ENDPOINT = "https://itb-usa.a2hosted.com/account/cnbc-news-data-list/"
    url = "https://www.cnbc.com/world/?region=world"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    cnbclatestnews_tags= s.find_all("li", class_="LatestNews-item")
    cnbclatestNewsTime=[]
    cnbclatestNewsTitle=[]
    cnbclatestNewsURL=[]
    cnbclatestNewsAllList=[]

    for i in cnbclatestnews_tags:
        cnbctime_tags= i.find_all("time", class_="LatestNews-timestamp")
        for timed in cnbctime_tags:
            cnbclatestNewsTime.append(timed.text)

        cnbcheadline_tags= i.find_all("a", class_="LatestNews-headline")
        for headlined in cnbcheadline_tags:
            cnbclatestNewsTitle.append(headlined.text.strip())
        for link in cnbcheadline_tags:
            cnbclatestNewsURL.append(link.get('href'))     


    for timeindex in range(len(cnbclatestNewsTime)):
        for titleindex in range(len(cnbclatestNewsTitle)):
            for urlindex in range(len(cnbclatestNewsURL)):

                if timeindex==titleindex and urlindex==timeindex and urlindex==titleindex:
                    cnbclatestNewsDict = {
                        'time': cnbclatestNewsTime[timeindex],
                        'presenttimestand': cnbclatestNewsTime[0],
                        'headline': cnbclatestNewsTitle[titleindex],
                        'url': cnbclatestNewsURL[urlindex],
                    }

                    if cnbclatestNewsDict != "":
                        cnbclatestNewsAllList.append(cnbclatestNewsDict)
                        cnbclatestNewsDict={}


    r = requests.post(url=API_ENDPOINT, json=cnbclatestNewsAllList)
    print("75", r.text)



   


    