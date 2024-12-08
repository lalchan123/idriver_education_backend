import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import requests
import json

from FunctionFolder.UserConfig import *


def DateFormatingConvertAPPLE(timed):
    currenttimestamp = datetime.strptime(
                timed, "%B %d, %Y").timestamp()
    currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate


def DateFormatingConvertC3Ai(timed):
    currenttimestamp = datetime.strptime(
                timed, "%m/%d/%Y").timestamp()
    currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate


def DateFormatingConvertReuters(timed):
    currenttimestamp = datetime.strptime(
                timed, "%A, %B %y, %Y").timestamp()
    currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate

def DateFormatingConvertInvestingReuters(timed):
    currenttimestamp = datetime.datetime.strptime(
                timed, "%A, %B %y, %Y").timestamp()
    currenttimedate = datetime.datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate


def APPLE():

    API_ENDPOINT = main_url+"/account/apple-news-data-list/"
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
                dateTime = DateFormatingConvertAPPLE(timed.text)
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
    return r.text



def C3Ai():

    API_ENDPOINT = main_url+"/account/c3ai-news-data-list/"
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
            dateTime = DateFormatingConvertC3Ai(timed.text.strip())
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

    return r.text


def CNBC():

    API_ENDPOINT = main_url+"/account/cnbc-news-data-list/"
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

    return r.text


def Reuters():

    API_ENDPOINT = main_url+"/account/investing-reuters-json-data/"
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

    return r.text


   
def GoogleFinance():

    API_ENDPOINT = main_url+"/account/google-finance-json-data/"
    url = "https://www.google.com/finance/"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    news_tags= s.find_all("div", class_="yY3Lee")
    Title=[]
    URL=[]


    for i in news_tags:

        title= i.find_all("div", class_="Yfwt5")
   
      
        if len(title)!=0:
            for t in title:
                Title.append(t.text)

        url= i.find_all("div", class_="z4rs2b")
        for u in url:
            A_tags= u.find_all("a")
            if len(A_tags)!=0:
                for link in A_tags:
                    URL.append(link.get('href'))                  
    
    
    data = {
        'title': Title,
        'url': URL
    } 

    df = pd.DataFrame(data)
       
    df_json_dict = json.loads(df.to_json())
    r = requests.post(url=API_ENDPOINT, json=df_json_dict)
    print("75", r.text)

    return r.text

    

def GoogleNews():

    API_ENDPOINT = main_url+"/account/google-news-json-data/"
    url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB/sections/CAQiXENCQVNQd29JTDIwdk1EbHpNV1lTQW1WdUdnSlZVeUlQQ0FRYUN3b0pMMjB2TURsNU5IQnRLaG9LR0FvVVRVRlNTMFZVVTE5VFJVTlVTVTlPWDA1QlRVVWdBU2dBKioIAComCAoiIENCQVNFZ29JTDIwdk1EbHpNV1lTQW1WdUdnSlZVeWdBUAFQAQ?hl=en-US&gl=US&ceid=US%3Aen"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    news_tags= s.find_all("c-wiz", class_="XBspb")
    Title=[]
    URL=[]

    for i in news_tags:

        # title= i.find_all("h4", class_="JtKRv")
   
      
        # if len(title)!=0:
        #     for t in title:
        #         Title.append(t.text)

        url= i.find_all("div", class_="IL9Cne")
        for u in url:
            A_tags= u.find_all("a")
            if len(A_tags)!=0:
                for link in A_tags:
                    Title.append(link.text)
                    URL.append("https://news.google.com"+link.get('href'))          
    

    data = {
        'title': Title,
        'url': URL
    } 

    df = pd.DataFrame(data)
    
    df_json_dict = json.loads(df.to_json())
    r = requests.post(url=API_ENDPOINT, json=df_json_dict)
    print("75", r.text)

    return r.text    



def InvestingReuters():

    # API_ENDPOINT = "http://localhost:8000/account/investing-reuters-json-data/"
    API_ENDPOINT = main_url+"/account/investing-reuters-json-data/"
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

    return r.text



def MarketingGainers():

    # API_ENDPOINT = "http://localhost:8000/account/investing-reuters-json-data/"
    API_ENDPOINT = main_url+"/account/marketing-gainer-json-data/"
    url = "https://www.google.com/finance/markets/gainers"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    news_tags= s.find_all("ul", class_="sbnBtf")
    mostActiveTitle=[]
    Gainers=[]
    Losers=[]

    for i in news_tags:

        mostActive= i.find_all("div", class_="COaKTb")
        gainer= i.find_all("div", class_="YMlKec")
        loser= i.find_all("div", class_="JwB6zf")
       
        if len(mostActive)!=0:
            for most in mostActive:
                mostActiveTitle.append(most.text)
        if len(gainer)!=0:
            for g in gainer:
                Gainers.append(g.text)
        if len(loser)!=0:
            for l in loser:
                Losers.append(l.text)
                
            

    data = {
        'symbol': mostActiveTitle,
        'value': Gainers,
        'percent': Losers
    } 

    df = pd.DataFrame(data)
    
   
    df_json_dict = json.loads(df.to_json())
    r = requests.post(url=API_ENDPOINT, json=df_json_dict)
    print("75", r.text)

    return r.text


def MarketingLosers():

    # API_ENDPOINT = "http://localhost:8000/account/investing-reuters-json-data/"
    API_ENDPOINT = main_url+"/account/marketing-loser-json-data/"
    url = "https://www.google.com/finance/markets/losers"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    news_tags= s.find_all("ul", class_="sbnBtf")
    mostActiveTitle=[]
    Gainers=[]
    Losers=[]

    for i in news_tags:

        mostActive= i.find_all("div", class_="COaKTb")
        gainer= i.find_all("div", class_="YMlKec")
        loser= i.find_all("div", class_="JwB6zf")
       
        if len(mostActive)!=0:
            for most in mostActive:
                mostActiveTitle.append(most.text)
        if len(gainer)!=0:
            for g in gainer:
                Gainers.append(g.text)
        if len(loser)!=0:
            for l in loser:
                Losers.append(l.text)
                
            
    data = {
        'symbol': mostActiveTitle,
        'value': Gainers,
        'percent': Losers
    } 

    df = pd.DataFrame(data)
   
    df_json_dict = json.loads(df.to_json())
    r = requests.post(url=API_ENDPOINT, json=df_json_dict)
    print("75", r.text)

    return  r.text



def MarketingMostActive():

    # API_ENDPOINT = "http://localhost:8000/account/investing-reuters-json-data/"
    API_ENDPOINT = main_url+"/account/marketing-most-active-json-data/"
    url = "https://www.google.com/finance/markets/most-active"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "lxml")
    news_tags= s.find_all("ul", class_="sbnBtf")
    mostActiveTitle=[]
    Gainers=[]
    Losers=[]

    for i in news_tags:

        mostActive= i.find_all("div", class_="COaKTb")
        gainer= i.find_all("div", class_="YMlKec")
        loser= i.find_all("div", class_="JwB6zf")
       
        if len(mostActive)!=0:
            for most in mostActive:
                mostActiveTitle.append(most.text)
        if len(gainer)!=0:
            for g in gainer:
                Gainers.append(g.text)
        if len(loser)!=0:
            for l in loser:
                Losers.append(l.text)
                
            

    data = {
        'symbol': mostActiveTitle,
        'value': Gainers,
        'percent': Losers
    } 

    df = pd.DataFrame(data)
    
   
    df_json_dict = json.loads(df.to_json())
    r = requests.post(url=API_ENDPOINT, json=df_json_dict)
    print("75", r.text)

    return r.text