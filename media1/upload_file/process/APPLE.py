import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import requests
import json



def DateFormatingConvert(timed):
    currenttimestamp = datetime.strptime(
                timed, "%B %d, %Y").timestamp()
    currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate


def APPLE():

    API_ENDPOINT = "https://itb-usa.a2hosted.com/account/apple-news-data-list/"
    url = "https://www.apple.com/newsroom/"

    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    applenews_tags= s.find_all("li", class_="tile-item")
    appleNewsTime=[]
    appleNewsTitle=[]
    appleNewsURL=[]
    appleNewsAllList=[]

    for i in applenews_tags:


        appletile_tags= i.find_all("a", class_="tile")
    
        for j in appletile_tags:
            appleheadline_tags= j.find_all("div", class_="tile__headline")
            for headlined in appleheadline_tags:
                appleNewsTitle.append(headlined.text.strip())

            appletime_tags= j.find_all("div", class_="tile__timestamp")
            for timed in appletime_tags:
                dateTime = DateFormatingConvert(timed.text)
                appleNewsTime.append(dateTime)


        for link in appletile_tags:
            appleNewsURL.append("https://www.apple.com/"+link.get('href'))




    for timeindex in range(len(appleNewsTime)):
        for titleindex in range(len(appleNewsTitle)):
            for urlindex in range(len(appleNewsURL)):

                if timeindex==titleindex and urlindex==timeindex and urlindex==titleindex:
                    appleNewsDict = {
                        'time': appleNewsTime[timeindex],
                        'presenttimestand': appleNewsTime[0],
                        'headline': appleNewsTitle[titleindex],
                        'url': appleNewsURL[urlindex],
                    }

                    if appleNewsDict != "":
                        appleNewsAllList.append(appleNewsDict)
                        appleNewsDict={}

    r = requests.post(url=API_ENDPOINT, json=appleNewsAllList)
    print("75", r.text)



