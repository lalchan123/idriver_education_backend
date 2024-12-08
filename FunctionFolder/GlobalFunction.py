import json
import os
import csv
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from pandas_datareader import data as pdr

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.views import *

from courseapp.models import *

import asyncio

from FunctionFolder.UserConfig import *

# global function
from FunctionFolder.WrapperFunc import *


def JsonFileNameYahooFinanceHist():
    fileName = main_media_url+'/media/upload_file/yahoo_finance_hist'
    dir_list = os.listdir(fileName)
    return dir_list  

def JsonFileNameYahooFinanceInfo():
    fileName = main_media_url+'/media/upload_file/yahoo_finance'
    dir_list = os.listdir(fileName)
    return dir_list  
    

def hist_data(periodTime, symbol):
    API_ENDPOINT = main_url+"/account/json-yahoo-hist-api/"
    OpenItem = []
    Item1 = []
    Item2 = []
    Item3 = []
    Item4 = []
    Item5 = []
    Item6 = []
    Item7 = []
    OpenSectionDic = {}
    

    alv = yf.Ticker(symbol)

    alv_daat = alv.history(period=periodTime)
   
    for i, j in alv_daat['Open'].items():
        OpenSectionDic['Date']=i.strftime('%Y-%m-%d')
        OpenSectionDic['Open']=j
        if OpenSectionDic != "":
            OpenItem.append(OpenSectionDic)
            OpenSectionDic={}

    for i, j in alv_daat['High'].items():
        for m in OpenItem:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=j
                if OpenSectionDic != "":
                    Item1.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Low'].items():
        for m in Item1:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=j
                if OpenSectionDic != "":
                    Item2.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Close'].items():
        for m in Item2:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=j
                if OpenSectionDic != "":
                    Item3.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Volume'].items():
        for m in Item3:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=m['Close']
                OpenSectionDic['Volume']=j
                if OpenSectionDic != "":
                    Item4.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Dividends'].items():
        for m in Item4:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=m['Close']
                OpenSectionDic['Volume']=m['Volume']
                OpenSectionDic['Dividends']=j
                if OpenSectionDic != "":
                    Item5.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Stock Splits'].items():
        for m in Item5:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=m['Close']
                OpenSectionDic['Volume']=m['Volume']
                OpenSectionDic['Dividends']=m['Dividends']
                OpenSectionDic['Stock Splits']=j
                if OpenSectionDic != "":
                    Item6.append(OpenSectionDic)
                    OpenSectionDic={}
    data={
        'symbol': symbol,
        'datalist': Item6,
    }
    r = requests.post(url=API_ENDPOINT, json=data)
    print("75", r.text)

        
def CurrentPriceHistoricalData(symbol):
    if type(symbol) is str:
        fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json'
        ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance_hist/{symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json')
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            object_data = {}
           
        
            object_data['Symbol']=symbol
            object_data['Date']=array_data[len(array_data)-1]['Date']
            object_data['Close']=array_data[len(array_data)-1]['Close']
            return object_data
    if type(symbol) is list:
        Data = []
        object_data = {}
        for m in symbol:
            fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{m}.json'
            ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance_hist/{m}.json', api_url=main_url+f'/media/upload_file/yahoo_finance_hist/{m}.json')
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                array_data = data['data']
                
            
                object_data['Symbol']=m
                object_data['Date']=array_data[len(array_data)-1]['Date']
                object_data['Close']=array_data[len(array_data)-1]['Close']
                
                if len(object_data) != 0:
                    Data.append(object_data)
                    object_data = {}
        return Data   
        
        
def YahooFinanceHistData(symbol, startDate, endDate):
    API_ENDPOINT = main_url+"/account/json-yahoo-hist-api1/"
    yf.pdr_override() # <== that's all it takes :-)

    OpenItem = []
    Item1 = []
    Item2 = []
    Item3 = []
    Item4 = []
    Item5 = []
    Item6 = []
    Item7 = []
    OpenSectionDic = {}

    # download dataframe
    alv_daat = pdr.get_data_yahoo(symbol, start=startDate, end=endDate)

    for i, j in alv_daat['Open'].items():
        OpenSectionDic['Date']=i.strftime('%Y-%m-%d')
        OpenSectionDic['Open']=j
        if OpenSectionDic != "":
            OpenItem.append(OpenSectionDic)
            OpenSectionDic={}

    for i, j in alv_daat['High'].items():
        for m in OpenItem:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=j
                if OpenSectionDic != "":
                    Item1.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Low'].items():
        for m in Item1:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=j
                if OpenSectionDic != "":
                    Item2.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Close'].items():
        for m in Item2:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=j
                if OpenSectionDic != "":
                    Item3.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Adj Close'].items():
        for m in Item3:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=m['Close']
                OpenSectionDic['Adj Close']=j
                if OpenSectionDic != "":
                    Item4.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Volume'].items():
        for m in Item4:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=m['Close']
                OpenSectionDic['Adj Close']=m['Adj Close']
                OpenSectionDic['Volume']=j
                if OpenSectionDic != "":
                    Item5.append(OpenSectionDic)
                    OpenSectionDic={}



    data={
        'symbol': symbol,
        'datalist': Item5,
    }
    r = requests.post(url=API_ENDPOINT, json=data)
    print("75",  r.text)



def YahooFinanceHist(symbol):
    now_utc = datetime.utcnow()
    currenttimedate = datetime.strftime(now_utc, '%Y-%m-%d')
    try:
        yfinance_file_check = requests.get(url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json')
        array_data = yfinance_file_check.json()['data']

        startDate=array_data[len(array_data)-1]['Date']
        YahooFinanceHistData(symbol, startDate, currenttimedate)
    except:
        yfinance_configure = requests.get(url=main_url+'/media/upload_file/investing/json/yahoo_finance_configure.json')
        startDate = yfinance_configure.json()['data'][0]['BeginDate']  
        YahooFinanceHistData(symbol, startDate, currenttimedate) 
        
        
        
        
def Daily_diff(symbol):
    fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance_hist/{symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json')
    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        Data = []
        object_data = {}
        
        for m in array_data:
            object_data['Date'] = m['Date']
            object_data['diff']=  round(m['High']-m['Low'], 2)  

            if len(object_data) != 0:
                Data.append(object_data)
                object_data = {}
           
        return Data   
        
        
def avg(a, b):
    av = (a+b)/2
    return av

def sum(a, b):
    s = a+b
    return s


def read_csv(filename):
    fileName = main_media_url+f'/media/upload_file/investing/csv/{filename}.csv'
    if os.path.isfile(fileName):
        f = open(fileName)
        # data = json.load(f)
        csvreader = csv.DictReader(f)

        return csvreader

def read_json(filename):
    fileName = main_media_url+f'/media/upload_file/investing/json/{filename}.json'
    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        return array_data
        
        
def write_json(filename, array_json):
    fileName = main_media_url+f'/media/upload_file/investing/json/{filename}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/{filename}.json', api_url=main_url+f'/media/upload_file/investing/json/{filename}.json')
    if os.path.isfile(fileName):
    
        def write_json(new_data, filename=fileName):
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data["data"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        
        for ajson in array_json:
            write_json(ajson)
        return "Write Json Added Successfully" 
   
    else:
        f = open(fileName, 'wb')
        jsonformat = {
            "data": []
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)

        def write_json(new_data, filename=fileName):
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data["data"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        
        for ajson in array_json:
            write_json(ajson)
        return "Write Json Added Successfully" 
        
        
        
async def read_json1(filename):
    fileName = main_media_url+f'/media/upload_file/investing/json/{filename}.json'
    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        print("array_data", array_data)
        return array_data
        
        
async def write_json1(filename, array_json):
    fileName = main_media_url+f'/media/upload_file/investing/json/{filename}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/{filename}.json', api_url=main_url+f'/media/upload_file/investing/json/{filename}.json')
    if os.path.isfile(fileName):
    
        def write_json(new_data, filename=fileName):
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data["data"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        
        for ajson in array_json:
            write_json(ajson)
        return "Write Json Added Successfully" 
   
    else:
        f = open(fileName, 'wb')
        jsonformat = {
            "data": []
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)

        def write_json(new_data, filename=fileName):
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data["data"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        
        for ajson in array_json:
            write_json(ajson)
        return "Write Json Added Successfully" 
        


def contains(string, value):
    if string.find(value) != -1:
        return True
    else:
        return False
    
def startwith(list, value):
    item = [idx for idx in list if idx[0].lower() == value.lower() or idx[0:2].lower() == value.lower() or idx[0:3].lower() == value.lower()]  
    return item
        
        


# Node Tree start
class Node:
   def __init__(self, data):
      self.left = None
      self.right = None
      self.data = data
# Insert Node
   def insert(self, data):
      if self.data:
         if data < self.data:
            if self.left is None:
               self.left = Node(data)
            else:
               self.left.insert(data)
         elif data > self.data:
            if self.right is None:
               self.right = Node(data)
            else:
               self.right.insert(data)
         else:
            self.data = data
# Print the Tree
   def PrintTree(self):
      if self.left:
         self.left.PrintTree()
      print(self.data),
      if self.right:
         self.right.PrintTree()

# Inorder traversal
# Left -> Root -> Right
   def inorderTraversal(self, root):
      res = []
      if root:
         res = self.inorderTraversal(root.left)
         res.append(root.data)
         res = res + self.inorderTraversal(root.right)
      return res    
        
# Preorder traversal
# Root -> Left ->Right
   def PreorderTraversal(self, root):
      res = []
      if root:
         res.append(root.data)
         res = res + self.PreorderTraversal(root.left)
         res = res + self.PreorderTraversal(root.right)
      return res
   

# Postorder traversal
# Left ->Right -> Root
   def PostorderTraversal(self, root):
        res = []
        if root:
            res = self.PostorderTraversal(root.left)
            res = res + self.PostorderTraversal(root.right)
            res.append(root.data)
        return res


# Node Tree end
        
        
        
# Queue Start   


class Queue:

	# __init__ function
	def __init__(self, capacity):
		self.front = self.size = 0
		self.rear = capacity - 1
		self.Q = [None]*capacity
		self.capacity = capacity

	# Queue is full when size becomes
	# equal to the capacity
	def isFull(self):
		return self.size == self.capacity

	# Queue is empty when size is 0
	def isEmpty(self):
		return self.size == 0

	# Function to add an item to the queue.
	# It changes rear and size
	def EnQueue(self, item):
		if self.isFull():
			print("Full")
			return
		self.rear = (self.rear + 1) % (self.capacity)
		self.Q[self.rear] = item
		self.size = self.size + 1
		print("% s enqueued to queue" % str(item))

	# Function to remove an item from queue.
	# It changes front and size
	def DeQueue(self):
		if self.isEmpty():
			print("Empty")
			return

		print("% s dequeued from queue" % str(self.Q[self.front]))
		self.front = (self.front + 1) % (self.capacity)
		self.size = self.size - 1

	# Function to get front of queue
	def que_front(self):
		if self.isEmpty():
			print("Queue is empty")

		print("Front item is", self.Q[self.front])

	# Function to get rear of queue
	def que_rear(self):
		if self.isEmpty():
			print("Queue is empty")
		print("Rear item is", self.Q[self.rear])






# Queue End   
          

# Stack Start  




class StackNode: 

	# Constructor to initialize a node 
	def __init__(self, data): 
		self.data = data 
		self.next = None


class Stack: 

	# Constructor to initialize the root of linked list 
	def __init__(self): 
		self.root = None

	def isEmpty(self): 
		return True if self.root is None else False

	def push(self, data): 
		newNode = StackNode(data) 
		newNode.next = self.root 
		self.root = newNode 
		print ("% d pushed to stack" % (data)) 

	def pop(self): 
		if (self.isEmpty()): 
			return float("-inf") 
		temp = self.root 
		self.root = self.root.next
		popped = temp.data 
		return popped 

	def peek(self): 
		if self.isEmpty(): 
			return float("-inf") 
		return self.root.data 




# Stack End                 
        


# General Log Function
def GeneralLogFunction(Process_Name,  Time, error):
    try:
        process_data = [{
            "Process_Name": Process_Name,
            "Time": Time,
            "error": error,
        }]

        GeneralLogJsonWrite(process_data)
    except Exception as error:
        print("error", error)    
       

def GeneralLogJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/general_log.json'
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/general_log.json'

        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']


            for i in DataList:
                y = {
                    "Process_Name": i['Process_Name'],
                    "Time": i['Time'],
                    "error": i['error'],
                }

                write_json(y, fileName)
                try:
                    f = open(fileName)
                    data1 = json.load(f)
                except Exception as error:
                    with open(fileName, 'w') as file:
                        file.write(json.dumps(data, indent=4))

    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))