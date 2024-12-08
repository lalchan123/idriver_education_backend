import json, os
from datetime import datetime, date, timedelta
from itertools import chain, combinations
import pandas as pd
import numpy as np
from time import gmtime, strftime
import uuid
import random
import time
import math
from FunctionFolder.UserConfig import *

def JsonConvertData(df):
    try:
        DataItem = []
        KeyItem = []
        sections={}
        for key, value in df.iteritems():
            KeyItem.append(key)

        for index, row in df.iterrows():

            for i in range(len(KeyItem)):
                sections[KeyItem[i]]= row[KeyItem[i]]
            if sections != "":
                DataItem.append(sections)
                sections={}

        return DataItem
    
    except Exception as err:
        print("err", err)


def XYAxisFuncLeft(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, points):
    x_output_value = 0
    x_sum_value = 0.0
    x_diff_value_actual=0
    x_starting_point = starting_point
    x_starting_point_value = 0
    x_starting_point_loop = starting_point
    x_starting_value=starting_value
    x_starting_value1=starting_value
    x_output_value1=0
    
    y_output_value = 0
    y_sum_value = 0.0
    y_diff_value_actual=0
    y_starting_point = starting_point
    y_starting_point_value = 0
    y_starting_point_loop = starting_point
    y_starting_value=starting_value
    y_starting_value1=starting_value
    y_output_value1=0

    DataList = []
    DataListOutput = []
    Section = {}
  

    if starting_point > points:
        if day == 1:
            x_starting_value=x_starting_value
        elif day == 2:
            x_starting_value=daygap

        x_diff_value= (points - x_starting_point_loop)
        x_diff_value_actual+=x_diff_value
        x_starting_point=points
        Section['starting_point']=points
        x_dif_point = math.ceil((x_starting_point_loop - points)/5)
        x_output_value = x_starting_value
        for x_k in range(x_dif_point):
            if x_k+1 > 9:
                x_output_value += 5
            else:
                x_key = f'x{x_k+1}'
                x_output_value += rule_data_x[x_key]
                       

        # x_output_value= x_starting_value+x_output_value
        x_starting_value1=x_output_value
        x_sum_value=x_diff_value_actual-x_output_value 
        x_starting_point_value-=x_diff_value  

        Section['starting_point_value']=x_starting_point_value
        Section['starting_value']=x_starting_value
        Section['output_value']=round(x_output_value, 2)  
        Section['sum_value']=round(x_sum_value, 2) 
        Section['Side']="Left" 
        Section['Day']=day 
        if len(Section) !=0:
            DataList.append(Section)  
            Section={}  
            x_output_value=x_starting_value1
            DataListOutput.append(x_starting_point)

        # if day == 2:
        #     # x_starting_value=x_starting_value+daygap
        #     x_starting_value=daygap
        #     x_diff_value= (points - x_starting_point_loop)
        #     x_diff_value_actual+=x_diff_value
        #     x_starting_point=points
        #     Section['starting_point']=points
        #     x_dif_point = math.ceil((x_starting_point_loop - points)/5)
        #     for x_k in range(x_dif_point):
        #         if x_k+1 > 9:
        #             x_output_value += 5
        #         else:
        #             x_key = f'x{x_k+1}'
        #             x_output_value += rule_data_x[x_key]
                       

        #     x_output_value= x_starting_value+x_output_value
        #     x_starting_value1=x_output_value
        #     x_sum_value=x_diff_value_actual-x_output_value 
        #     x_starting_point_value-=x_diff_value  

        #     Section['starting_point_value']=x_starting_point_value
        #     Section['starting_value']=x_starting_value
        #     Section['output_value']=round(x_output_value, 2)  
        #     Section['sum_value']=round(x_sum_value, 2) 
        #     Section['Side']="Left" 
        #     Section['Day']=day 
        #     if len(Section) !=0:
        #         DataList.append(Section)  
        #         Section={}  
        #         x_output_value=x_starting_value1
        #         DataListOutput.append(x_starting_point)
            
    else:
        if day == 1:
            y_starting_value=y_starting_value
        elif day == 2: 
            y_starting_value=daygap   
           
        y_diff_value= (points - y_starting_point_loop)
        y_diff_value_actual+=y_diff_value
        y_starting_point=points
        Section['starting_point']=points
        y_dif_point = math.ceil((points - y_starting_point_loop)/5)
        y_output_value = y_starting_value
        for y_k in range(y_dif_point):
            if y_k+1 > 9:
                y_output_value -= 5
            else:
                y_key = f'y{y_k+1}'
                y_output_value -= rule_data_y[y_key]

            # y_output_value= y_starting_value-y_output_value
        y_starting_value1=y_output_value
        y_sum_value=y_diff_value_actual-y_output_value 
        y_starting_point_value+=y_diff_value 

        Section['starting_point_value']=y_starting_point_value
        Section['starting_value']=y_starting_value
        if y_output_value <=-1:
            Section['output_value']=0 
        else:     
            Section['output_value']=round(y_output_value, 2)

        # Section['output_value']=round(y_output_value, 2)

        Section['sum_value']=round(y_sum_value, 2) 
        Section['Side']="Left" 
        Section['Day']=day 
        if len(Section) !=0:
            DataList.append(Section)  
            Section={}  
            y_output_value=y_starting_value1
            DataListOutput.append(y_starting_point) 

        # if day == 2:
        #     y_starting_value=daygap
        #     y_diff_value= (points - y_starting_point_loop)
        #     y_diff_value_actual+=y_diff_value
        #     y_starting_point=points
        #     Section['starting_point']=points
        #     y_dif_point = math.ceil((points - y_starting_point_loop)/5)
        #     for y_k in range(y_dif_point):
        #         if y_k+1 > 9:
        #             y_output_value -= 5
        #         else:
        #             y_key = f'y{y_k+1}'
        #             y_output_value += rule_data_y[y_key]

        #     y_output_value= y_starting_value-y_output_value
        #     y_starting_value1=y_output_value
        #     y_sum_value=y_diff_value_actual-y_output_value 
        #     y_starting_point_value+=y_diff_value 

        #     Section['starting_point_value']=y_starting_point_value
        #     Section['starting_value']=y_starting_value
        #     if y_output_value <=-1:
        #         Section['output_value']=0 
        #     else:     
        #         Section['output_value']=round(y_output_value, 2)

        #     Section['sum_value']=round(y_sum_value, 2) 
        #     Section['Side']="Left" 
        #     Section['Day']=day 
        #     if len(Section) !=0:
        #         DataList.append(Section)  
        #         Section={}  
        #         y_output_value=y_starting_value1
        #         DataListOutput.append(y_starting_point) 
            

    return DataList, DataListOutput

def XYAxisFuncRight(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, points):
    x_output_value = 0
    x_sum_value = 0.0
    x_diff_value_actual=0
    x_starting_point = starting_point
    x_starting_point_value = 0
    x_starting_point_loop = starting_point
    x_starting_value=starting_value
    x_starting_value1=starting_value
    x_output_value1=0
    
    y_output_value = 0
    y_sum_value = 0.0
    y_diff_value_actual=0
    y_starting_point = starting_point
    y_starting_point_value = 0
    y_starting_point_loop = starting_point
    y_starting_value=starting_value
    y_starting_value1=starting_value
    y_output_value1=0

    DataList = []
    DataListOutput = []
    Section = {}
  

    if starting_point < points:
        if day == 1:
            x_starting_value=x_starting_value
        elif day == 2:
            x_starting_value=daygap

        x_diff_value= (points - x_starting_point_loop)
        x_diff_value_actual+=x_diff_value
        x_starting_point=points
        Section['starting_point']=points
        x_dif_point = math.ceil((points - x_starting_point_loop)/5)
        x_output_value = x_starting_value
        for x_k in range(x_dif_point):
            if x_k+1 > 9:
                x_output_value += 5
            else:
                x_key = f'x{x_k+1}'
                x_output_value += rule_data_x[x_key]
                       

        # x_output_value= x_starting_value+x_output_value
        x_starting_value1=x_output_value
        x_sum_value=x_diff_value_actual-x_output_value 
        x_starting_point_value+=x_diff_value  

        Section['starting_point_value']=x_starting_point_value
        Section['starting_value']=x_starting_value
        Section['output_value']=round(x_output_value, 2)  
        Section['sum_value']=round(x_sum_value, 2) 
        Section['Side']="Right" 
        Section['Day']=day 
        if len(Section) !=0:
            DataList.append(Section)  
            Section={}  
            x_output_value=x_starting_value1
            DataListOutput.append(x_starting_point)

        # if day == 2:
        #     x_starting_value= daygap
        #     x_diff_value= (points - x_starting_point_loop)
        #     x_diff_value_actual+=x_diff_value
        #     x_starting_point=points
        #     # Section['starting_point']=points
        #     x_dif_point = math.ceil((points - x_starting_point_loop)/5)
        #     for x_k in range(x_dif_point):
        #         if x_k+1 > 9:
        #             x_output_value += 5
        #         else:
        #             x_key = f'x{x_k+1}'
        #             x_output_value += rule_data_x[x_key]
                       

        #     x_output_value= x_starting_value+x_output_value
        #     x_starting_value1=x_output_value
        #     x_sum_value=x_diff_value_actual-x_output_value 
        #     x_starting_point_value+=x_diff_value  

        #     Section['starting_point_value']=x_starting_point_value
        #     Section['starting_value']=x_starting_value
        #     Section['output_value']=round(x_output_value, 2)  
        #     Section['sum_value']=round(x_sum_value, 2) 
        #     Section['Side']="Left" 
        #     Section['Day']=day 
        #     if len(Section) !=0:
        #         DataList.append(Section)  
        #         Section={}  
        #         x_output_value=x_starting_value1
        #         DataListOutput.append(x_starting_point)
            
    else:
        if day == 1:
            y_starting_value=y_starting_value
        elif day == 2: 
            y_starting_value=daygap  
            
        y_diff_value= (points - y_starting_point_loop)
        y_diff_value_actual+=y_diff_value
        y_starting_point=points
        Section['starting_point']=points
        y_dif_point = math.ceil((y_starting_point_loop - points)/5)
        y_output_value = y_starting_value
        for y_k in range(y_dif_point):
            if y_k+1 > 9:
                y_output_value -= 5
            else:
                y_key = f'y{y_k+1}'
                y_output_value -= rule_data_y[y_key]


        # y_output_value= y_starting_value-y_output_value
        y_starting_value1=y_output_value
        y_sum_value=y_diff_value_actual-y_output_value 
        y_starting_point_value-=y_diff_value 

        Section['starting_point_value']=y_starting_point_value
        Section['starting_value']=y_starting_value
        if y_output_value <=-1:
            Section['output_value']=0 
        else:     
            Section['output_value']=round(y_output_value, 2)

        Section['sum_value']=round(y_sum_value, 2) 
        Section['Side']="Right" 
        Section['Day']=day 
        if len(Section) !=0:
            DataList.append(Section)  
            Section={}  
            y_output_value=y_starting_value1
            DataListOutput.append(y_starting_point) 
        
        # if day == 2:
        #     y_starting_value= daygap
        #     y_diff_value= (points - y_starting_point_loop)
        #     y_diff_value_actual+=y_diff_value
        #     y_starting_point=points
        #     Section['starting_point']=points
        #     y_dif_point = math.ceil((y_starting_point_loop - points)/5)
        #     for y_k in range(y_dif_point):
        #         if y_k+1 > 9:
        #             y_output_value -= 5
        #         else:
        #             y_key = f'y{y_k+1}'
        #             y_output_value += rule_data_y[y_key]

        #     y_output_value= y_starting_value-y_output_value
        #     y_starting_value1=y_output_value
        #     y_sum_value=y_diff_value_actual-y_output_value 
        #     y_starting_point_value-=y_diff_value 

        #     Section['starting_point_value']=y_starting_point_value
        #     Section['starting_value']=y_starting_value
        #     if y_output_value <=-1:
        #         Section['output_value']=0 
        #     else:     
        #         Section['output_value']=round(y_output_value, 2)

        #     Section['sum_value']=round(y_sum_value, 2) 
        #     Section['Side']="Right" 
        #     Section['Day']=day 
        #     if len(Section) !=0:
        #         DataList.append(Section)  
        #         Section={}  
        #         y_output_value=y_starting_value1
        #         DataListOutput.append(y_starting_point) 
            

    return DataList, DataListOutput 

def LeftXYAxisFunc(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, value_range_list2):
    x_output_value = 0
    x_sum_value = 0.0
    x_diff_value_actual=0
    x_starting_point = starting_point
    x_starting_point_value = 0
    x_starting_point_loop = starting_point
    x_starting_value=starting_value
    x_starting_value1=starting_value
    x_output_value1=0
    
    y_output_value = 0
    y_sum_value = 0.0
    y_diff_value_actual=0
    y_starting_point = starting_point
    y_starting_point_value = 0
    y_starting_point_loop = starting_point
    y_starting_value=starting_value
    y_starting_value1=starting_value
    y_output_value1=0

    DataList1 = []
    DataListOutput1 = []
    Section = {}
  

    if starting_point > value_range_list2[1]:
        for x_diff_value in reversed(range(value_range_list2[1], x_starting_point_loop, 5)):
            Data_Value_List, Data_Value_Output = XYAxisFuncLeft(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, x_diff_value)
            DataList1.append(Data_Value_List[0])
            DataListOutput1.append(Data_Value_Output[0])

        
     
    if starting_point < value_range_list2[0]:
        for y_diff_value in range(y_starting_point_loop, value_range_list2[0]+5, 5):
            Data_Value_List, Data_Value_Output = XYAxisFuncLeft(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, y_diff_value)
            DataList1.append(Data_Value_List[0])
            DataListOutput1.append(Data_Value_Output[0])
     
    return DataList1, DataListOutput1

def RightXYAxisFunc(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, value_range_list2):
    x_output_value = 0
    x_sum_value = 0.0
    x_diff_value_actual=0
    x_starting_point = starting_point
    x_starting_point_value = 0
    x_starting_point_loop = starting_point
    x_starting_value=starting_value
    x_starting_value1=starting_value
    x_output_value1=0
    
    y_output_value = 0
    y_sum_value = 0.0
    y_diff_value_actual=0
    y_starting_point = starting_point
    y_starting_point_value = 0
    y_starting_point_loop = starting_point
    y_starting_value=starting_value
    y_starting_value1=starting_value
    y_output_value1=0

    DataList1 = []
    DataListOutput1 = []
    Section = {}
  


    if starting_point > value_range_list2[1]:
        # big to small
        for x_diff_value in reversed(range(value_range_list2[1], x_starting_point_loop, 5)):
            Data_Value_List, Data_Value_Output = XYAxisFuncRight(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, x_diff_value)
            DataList1.append(Data_Value_List[0])
            DataListOutput1.append(Data_Value_Output[0])

        
     
    if starting_point < value_range_list2[0]:
        # small to big
        for y_diff_value in range(y_starting_point_loop, value_range_list2[0]+5, 5):
            Data_Value_List, Data_Value_Output = XYAxisFuncRight(day, starting_point, starting_value, rule_data_x, rule_data_y, daygap, y_diff_value)
            DataList1.append(Data_Value_List[0])
            DataListOutput1.append(Data_Value_Output[0])
     
    return DataList1, DataListOutput1

