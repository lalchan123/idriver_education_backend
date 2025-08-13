import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import requests
import json


def DateFormatingConvert(timed):
    currenttimestamp = datetime.strptime(
                timed, "%m/%d/%Y").timestamp()
    currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate


def C3Ai():

    API_ENDPOINT = "https://itb-usa.a2hosted.com/account/c3ai-news-data-list/"
    url = "https://ir.c3.ai/news"

    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    c3ainews_tags= s.find_all("article", class_="clearfix")
    c3aiNewsTime=[]
    c3aiNewsTitle=[]
    c3aiNewsURL=[]
    c3aiNewsAllList=[]

    for i in c3ainews_tags:

        c3aitime_tags= i.find_all("div", class_="nir-widget--news--date-time")
        for timed in c3aitime_tags:
            dateTime = DateFormatingConvert(timed.text.strip())
            c3aiNewsTime.append(dateTime)
        c3aiheadline_tags= i.find_all("div", class_="nir-widget--news--headline")  
        for headlined in c3aiheadline_tags:
            c3aiNewsTitle.append(headlined.text.strip())
        for j in c3aiheadline_tags:
            c3aiA_tags= j.find_all("a")
            for link in c3aiA_tags:
                c3aiNewsURL.append("https://ir.c3.ai"+link.get('href'))     

          



    for timeindex in range(len(c3aiNewsTime)):
        for titleindex in range(len(c3aiNewsTitle)):
            for urlindex in range(len(c3aiNewsURL)):

                if timeindex==titleindex and urlindex==timeindex and urlindex==titleindex:
                    c3aiNewsDict = {
                        'time': c3aiNewsTime[timeindex],
                        'presenttimestand': c3aiNewsTime[0],
                        'headline': c3aiNewsTitle[titleindex],
                        'url': c3aiNewsURL[urlindex],
                    }

                    if c3aiNewsDict != "":
                        c3aiNewsAllList.append(c3aiNewsDict)
                        c3aiNewsDict={}

    r = requests.post(url=API_ENDPOINT, json=c3aiNewsAllList)
    print("75", r.text)