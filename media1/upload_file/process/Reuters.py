import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import requests
import json


def DateFormatingConvert(timed):
    currenttimestamp = datetime.strptime(
                timed, "%A, %B %y, %Y").timestamp()
    currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate
    

def Reuters():

    API_ENDPOINT = "https://itb-usa.a2hosted.com/account/investing-reuters-json-data/"
    url = "https://www.reuters.com/"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    news_tags= s.find_all("div", class_="content-layout__item__SC_GG")
    NewsTime=[]
    NewsTitle=[]
    NewsURL=[]
                

    for i in news_tags:
        mediaStoryCard= i.find_all("div", {'data-testid': 'MediaStoryCard'})
        if len(mediaStoryCard)!=0:
            for m in mediaStoryCard:
                mediaHeading= m.find_all("h3", {'data-testid': 'Heading'})
                amediaHeading= m.find_all("a", {'data-testid': 'Heading'})
                for heading in mediaHeading:
                    NewsTitle.append(heading.text)
                    A_tags= heading.find_all("a")
                    for link in A_tags:
                        NewsURL.append("https://www.reuters.com"+link.get('href')) 

                for heading in amediaHeading:
                    NewsTitle.append(heading.text)
                    NewsURL.append("https://www.reuters.com"+heading.get('href'))  


                mediaTime= m.find_all("time", {'data-testid': 'Label'})
                for time in mediaTime:
                    NewsTime.append(time.text)  


        textStoryCard= i.find_all("div", {'data-testid': 'TextStoryCard'})
        if len(textStoryCard)!=0:
            for m in textStoryCard:
                amediaHeading= m.find_all("a", {'data-testid': 'Heading'})
                

                for heading in amediaHeading:
                    NewsTitle.append(heading.text)
                    NewsURL.append("https://www.reuters.com"+heading.get('href'))  


                mediaTime= m.find_all("time", {'data-testid': 'Label'})
                for time in mediaTime:
                    NewsTime.append(time.text)        

        
    
    data = {
        'time': NewsTime,
        'NewsTitle': NewsTitle,
        'url': NewsURL
    } 

    df = pd.DataFrame(data)
    

   
    df_json_dict = json.loads(df.to_json())
    r = requests.post(url=API_ENDPOINT, json=df_json_dict)
    print("75", r.text)