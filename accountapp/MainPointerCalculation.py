

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
from accountapp.PointerValueCalculation import *



def generate_unique_random_number():
    # Get the current time in seconds since the Epoch
    current_time = int(time.time() * 1000)  # Multiply by 1000 to include milliseconds
    
    # Generate a random number
    random_number = random.randint(0, 99999)
    
    # Combine the current time with the random number to ensure uniqueness
    unique_random_number = int(f"{current_time}{random_number}")
    
    return unique_random_number




def combination(stuff):
    DataList=[]
    for i, combo in enumerate((combinations(stuff, 3)), 1):
        DataList.append(combo)
    return DataList   

def UniqueCombination(day1, day12, day2):
    Datalist=[]
    for m in day1:
        for k in day12:
            for j in day2:
                Datalist.append((m, k, j))
    return Datalist

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





 




def write_json(fileName, XDataList1, XDataList2, YDataList1, YDataList2):
    with open(fileName, 'r+') as file:
            file_data = json.load(file)
            file_data.update({
                "day1":{'x':XDataList1, 'y':YDataList1},
                "day2":{'x':XDataList2, 'y':YDataList1},
            })
            file.seek(0)
            json.dump(file_data, file, indent=4)

def write_json1(fileName, setup_value):
    with open(fileName, 'r+') as file:
            file_data = json.load(file)
            file_data.update({
                "setup_value": setup_value
            })
            file.seek(0)
            json.dump(file_data, file, indent=4)



def CombinationValue(value0, value1, value2, XDataList1, YDataList1, XDataList2, YDataList2, XDataList3, YDataList3):
    dfList=[]
    new_row={}

    x_data_day1 = [x for x in XDataList1 if x['starting_point'] == value0]
    y_data_day1 = [x for x in YDataList1 if x['starting_point'] == value0]

    data1=0
    data12=0
    data2=0

    if len(x_data_day1)!=0:
        data1=x_data_day1[0]['output_value']
    if len(y_data_day1)!=0:
        data1=y_data_day1[0]['output_value']

    x_data_day12 = [x for x in XDataList2 if x['starting_point'] == value1]
    y_data_day12 = [x for x in YDataList2 if x['starting_point'] == value1]
        
    if len(x_data_day12)!=0:
        data12=x_data_day12[0]['output_value']
    if len(y_data_day12)!=0:
        data12=y_data_day12[0]['output_value']

       
    x_data_day2 = [x for x in XDataList3 if x['starting_point'] == value2]
    y_data_day2 = [x for x in YDataList3 if x['starting_point'] == value2]
               
               
    if len(x_data_day2)!=0:
        data2=x_data_day2[0]['output_value']
    if len(y_data_day2)!=0:
        data2=y_data_day2[0]['output_value']


    new_row={
        "data1":data1, 
        "data12":data12, 
        "data2":data2
    }
    if len(new_row)!=0:
        dfList.append(new_row)
        new_row={}
    return dfList


def ExcelFileWrite(file_name, df):
    df_data = pd.read_excel(file_name)
    df_data = pd.concat([df_data, df], ignore_index=True)
    df_data.to_excel(file_name, index=False)


def PointerValueRangeFunc(inital_starting_point, starting_point, starting_value, rule_data, rule_data_x, rule_data_y, ValueList, daygap, value_range_list2):
    DataListTLeft=[]    
    DataListTRight=[]    

    for dt in ValueList:    
        if dt['v_point'] == "Left":
            DataListLeft, DataListOutputLeft = XYAxisFuncLeft(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, points=dt['points'])
            DataListTLeft+=DataListLeft

        if dt['v_point'] == "Right":
            DataListRight, DataListOutputRight = XYAxisFuncRight(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, points=dt['points'])
            DataListTRight+=DataListRight


    
    file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
    summary_df = pd.read_excel(file_name1)
    d1lp1, d1rp1, d2lp2, d3lp3, Left_Day, Left_Point, Right_Day, Right_Point, pv0, pv1, pv2, pv3, Left_pv, Right_pv = summary_df['d1lp1'].iloc[0], summary_df['d1rp1'].iloc[0], summary_df['d2lp2'].iloc[0], summary_df['d3lp3'].iloc[0], summary_df['Left_Day'].iloc[0], summary_df['Left_Point'].iloc[0], summary_df['Right_Day'].iloc[0], summary_df['Right_Point'].iloc[0], summary_df['pv0'].iloc[0], summary_df['pv1'].iloc[0], summary_df['pv2'].iloc[0],  summary_df['pv3'].iloc[0], summary_df['Left_pv'].iloc[0], summary_df['Right_pv'].iloc[0]      


    TotalDataItem = DataListTLeft+DataListTRight

    Data1 = [x for x in TotalDataItem if x['starting_point'] == d1lp1 and  x['Side'] == 'Left' and  x['Day'] == 1]
    Data2 = [x for x in TotalDataItem if x['starting_point'] == d1rp1 and  x['Side'] == 'Left' and  x['Day'] == 1]
    Data3 = [x for x in TotalDataItem if x['starting_point'] == d2lp2 and  x['Side'] == 'Left' and  x['Day'] == 1]
    Data4 = [x for x in TotalDataItem if x['starting_point'] == d3lp3 and  x['Side'] == 'Left' and  x['Day'] == 2]
    Data5 = [x for x in TotalDataItem if x['starting_point'] == Left_Point and  x['Side'] == 'Left' and  x['Day'] == Left_Day]
    Data6 = [x for x in TotalDataItem if x['starting_point'] == Right_Point and  x['Side'] == 'Right' and  x['Day'] == Right_Day]
    Data7 = DuplicateRemove(Data1)+DuplicateRemove(Data2)+DuplicateRemove(Data3)+DuplicateRemove(Data4)+DuplicateRemove(Data5)+DuplicateRemove(Data6)
    return Data7


def DuplicateRemove(Data):
    DataList = []
    for m in range(len(Data)):
        # print("m", m)
        if m == 0:
            DataList.append(Data[m])
        else:
            for k in DataList:
                if k['starting_point'] == Data[m]['starting_point'] and  k['Side'] == Data[m]['Side'] and k['Day'] == Data[m]['Day']:
                    pass
                else:
                    DataList.append(Data[m])   
    return DataList


def PVFunction(Data):
    try:
        data1 = Data[0]['output_value']
        return data1
    except:
        return 0    

def MainPointerCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, SumList, daygap):
    try:
        print("1411 starting_value", starting_value)
        file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
        summary_df = pd.read_excel(file_name1)
        d1lp1, d1rp1, d2lp2, d3lp3, Left_Day, Left_Point, Right_Day, Right_Point, pv0, pv1, pv2, pv3, Left_pv, Right_pv = summary_df['d1lp1'].iloc[0], summary_df['d1rp1'].iloc[0], summary_df['d2lp2'].iloc[0], summary_df['d3lp3'].iloc[0], summary_df['Left_Day'].iloc[0], summary_df['Left_Point'].iloc[0], summary_df['Right_Day'].iloc[0], summary_df['Right_Point'].iloc[0], summary_df['pv0'].iloc[0], summary_df['pv1'].iloc[0], summary_df['pv2'].iloc[0],  summary_df['pv3'].iloc[0], summary_df['Left_pv'].iloc[0], summary_df['Right_pv'].iloc[0]      
        print("d1lp1 d1rp1 d2lp2 d3lp3 Left_Day Left_Point Right_Day Right_Point", d1lp1, d1rp1, d2lp2, d3lp3, Left_Day, Left_Point, Right_Day, Right_Point)
        original_actual_value = round((pv0+pv1+pv2+pv3+Left_pv+Right_pv), 2)
        # uniqueCombination= [(d1_point0, d1_point1, d2_point2, Left_Point, Right_Point)]
        ValueList = []
        if d1lp1 != 0:
            ValueList.append({
                'points': d1lp1,
                'v_day': 1,
                'v_point': "Left",
            })

        if d1rp1 != 0:
            ValueList.append({
                'points': d1rp1,
                'v_day': 1,
                'v_point': "Left",
            })
        if d2lp2 != 0:
            ValueList.append({
                'points': d2lp2,
                'v_day': 1,
                'v_point': "Left",
            })
        if d3lp3 != 0:
            ValueList.append({
                'points': d3lp3,
                'v_day': 2,
                'v_point': "Left",
            })
        if Left_Point != 0:
            ValueList.append({
                'points': Left_Point,
                'v_day': Left_Day,
                'v_point': "Left",
            })

        if Right_Point != 0:
            ValueList.append({
                'points': Right_Point,
                'v_day': Right_Day,
                'v_point': "Right",
            })

        DataListTLeft=[]    
        DataListTRight=[]    
    

        
        print("ValueList", ValueList)
        for dt in ValueList:
        
            if dt['v_point'] == "Left":
                DataListLeft, DataListOutputLeft = XYAxisFuncLeft(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, points=dt['points'])
                DataListTLeft+=DataListLeft

            if dt['v_point'] == "Right":
                DataListRight, DataListOutputRight = XYAxisFuncRight(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, points=dt['points'])
                DataListTRight+=DataListRight
            

    

        SList=[]
        Section={}

        Section['starting_point']=starting_point
        Section['starting_value']=starting_value
        Section['daygap']=daygap
        Section['value_range_0']=value_range_list2[0]
        Section['value_range_1']=value_range_list2[1]
        Section['created_time']=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        Section['d1lp1']=d1lp1
        Section['d1rp1']=d1rp1
        Section['d2lp2']=d2lp2
        Section['d3lp3']=d3lp3
        Section['point_id']=str(Section['d1lp1'])+str(Section['d1rp1'])+str(Section['d2lp2'])+str(Section['d3lp3'])+str(generate_unique_random_number())


        print("DataListTLeft", DataListTLeft)
        TotalDataItem = DataListTLeft+DataListTRight
        Data1 = [x for x in TotalDataItem if x['starting_point'] == d1lp1 and  x['Side'] == 'Left' and  x['Day'] == 1]
        Data2 = [x for x in TotalDataItem if x['starting_point'] == d1rp1 and  x['Side'] == 'Left' and  x['Day'] == 1]
        Data3 = [x for x in TotalDataItem if x['starting_point'] == d2lp2 and  x['Side'] == 'Left' and  x['Day'] == 1]
        Data4 = [x for x in TotalDataItem if x['starting_point'] == d3lp3 and  x['Side'] == 'Left' and  x['Day'] == 2]
        # Data3 = [x for x in TotalDataItem if x['starting_point'] == d2_point2 and  x['Side'] == 'Left']
        Data5 = [x for x in TotalDataItem if x['starting_point'] == Left_Point and  x['Side'] == 'Left' and  x['Day'] == Left_Day]
        Data6 = [x for x in TotalDataItem if x['starting_point'] == Right_Point and  x['Side'] == 'Right' and  x['Day'] == Right_Day]
        # print("1505 Data2", Data1, Data2, Data3, Data4, Data5, Data6)

        
        Section['pv0']= PVFunction(Data1)
        Section['pv1']= PVFunction(Data2)
        Section['pv2']= PVFunction(Data3)
        Section['pv3']= PVFunction(Data4)
        Section['actual_value']=  round(Section['pv0']+Section['pv1']+Section['pv2']+Section['pv3']+PVFunction(Data5)+PVFunction(Data6), 2)
        Actual_Value_Calculation = Section['actual_value']

    
        DataList2 = PointerValueRangeFunc(starting_point, value_range_list2[0], starting_value, rule_data, rule_data_x, rule_data_y, ValueList, daygap, value_range_list2)
        DataList3 = PointerValueRangeFunc(starting_point, value_range_list2[1], starting_value, rule_data, rule_data_x, rule_data_y, ValueList, daygap, value_range_list2)
        
        # print("DataList2", DataList2)
        # print("DataList3", DataList3)
    
        LeftSumMax=0
        RightSumMax=0
        for h in DataList2:
            if h['Side'] == 'Left':
                LeftSumMax+=h['output_value']
            if h['Side'] == 'Right':
                RightSumMax+=h['output_value']

        print("1516 LeftSumMax", LeftSumMax, RightSumMax, original_actual_value)        
        Section['maxv']=round(((LeftSumMax+RightSumMax)-original_actual_value), 2)

        # Section['maxv']=round((sum_value2-Section['actual_value']), 2)
        # Section['minv']=round((sum_value3-Section['actual_value']), 2)

        LeftSumMin=0
        RightSumMin=0
        for h in DataList3:
            if h['Side'] == 'Left':
                LeftSumMin+=h['output_value']
            if h['Side'] == 'Right':
                RightSumMin+=h['output_value']
                
        Section['minv']=round(((LeftSumMin+RightSumMin)-original_actual_value), 2)
        # Section['maxv_value']=round((Section['maxv']-(value_range_list2[0]-starting_point)), 2)
        # Section['minv_value']=round((Section['minv']-(value_range_list2[1]-starting_point)), 2)

        # if Section['maxv'] > 0:
        #     Section['maxv_net']=round((Section['maxv']-(value_range_list2[0]-starting_point)), 2)
        # else:
        #     Section['maxv_net']=round(((value_range_list2[0]-starting_point)+abs(Section['maxv'])), 2)


        Section['maxv_net']=round((Section['maxv']+(value_range_list2[0]-starting_point)), 2)



        # if Section['minv'] > 0:
        #     Section['minv_net']=round(((starting_point-value_range_list2[1])-Section['minv']), 2)
        # else:
        #     Section['minv_net']=round((Section['minv']+(starting_point-value_range_list2[1])), 2)

        Section['minv_net']=round((Section['minv']-(starting_point-value_range_list2[1])), 2)



        Section['remarks']="sum_max_value"
        Section['first_run']="No"
        Section['pv_max']= round(-(LeftSumMax+RightSumMax), 2)
        Section['pv_min']= round(-(LeftSumMin+RightSumMin), 2)
        Section['RangeSum']=round(abs(Section['maxv_net']) + abs(Section['minv_net']), 2)

        file_name1 = main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
        output_df = pd.read_excel(file_name1)
        exist_data = output_df['first_run'].iloc[0]
        i_starting_point=0
        if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
            Section['ActualP'] = round((((output_df['actual_value'].iloc[0]-Section['actual_value'])/output_df['actual_value'].iloc[0])*100), 2)
            i_starting_point = output_df['starting_point']

        Section['MaxP'] = round(((Section['maxv_net']/Section['RangeSum'])*100), 2)
        Section['MinP'] = round(((Section['minv_net']/Section['RangeSum'])*100), 2)
        Section['Left_Day'] = Left_Day
        Section['Left_Point'] = Left_Point
        Section['Left_pv'] = PVFunction(Data4)
        Section['Right_Day'] = Right_Day
        Section['Right_Point'] = Right_Point
        Section['Right_pv'] = PVFunction(Data5)

        SList.append(Section)

        df = pd.DataFrame(SList)

        ExcelFileWrite(main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx', df)
        
        SList1=[]
        Section1={}
        extra_value=0
        for i in range(1, 21, 1):
            extra_value+=5

            DataList21 = PointerValueRangeFunc(starting_point, starting_point+extra_value, starting_value, rule_data, rule_data_x, rule_data_y, ValueList, daygap, value_range_list2)
            DataList31 = PointerValueRangeFunc(starting_point, starting_point-extra_value, starting_value, rule_data, rule_data_x, rule_data_y, ValueList, daygap, value_range_list2)
            
        

            Section1['created_time']=strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Section1['starting_point']=starting_point
            Section1['starting_point_first']=starting_point+extra_value
            Section1['starting_point_second']=starting_point-extra_value
            Section1['actual_value']=Actual_Value_Calculation
            Section1["pv0"]=pv0
            Section1["pv1"]=pv1
            Section1["pv2"]=pv2
            Section1["pv3"]=pv3
            Section1["Left_pv"] = Left_pv
            Section1["Right_pv"] = Right_pv

            LeftSumMax1=0
            RightSumMax1=0
            for h in DataList21:
                if h['Side'] == 'Left':
                    LeftSumMax1+=h['output_value']
                if h['Side'] == 'Right':
                    RightSumMax1+=h['output_value']
                    
            Section1['maxv']=round(((LeftSumMax1+RightSumMax1)-original_actual_value), 2)

            LeftSumMin1=0
            RightSumMin1=0
            for h in DataList31:
                if h['Side'] == 'Left':
                    LeftSumMin1+=h['output_value']
                if h['Side'] == 'Right':
                    RightSumMin1+=h['output_value']
                    
            Section1['minv']=round(((LeftSumMin1+RightSumMin1)-original_actual_value), 2)
            
            # if Section1['maxv'] > 0:
            #     Section1['maxv_value']=round((Section1['maxv']-((starting_point+extra_value)-starting_point)), 2)
            # else:
            #     Section1['maxv_value']=round((((starting_point+extra_value)-starting_point)+abs(Section1['maxv'])), 2)
            Section1['maxv_net']=round((Section1['maxv']+((starting_point+extra_value)-starting_point)), 2)


            # if Section1['minv'] > 0:
            #     Section1['minv_value']=round(((starting_point-(starting_point-extra_value))-Section1['minv']), 2)
            # else:
            #     Section1['minv_value']=round((Section1['minv']+(starting_point-(starting_point-extra_value))), 2)

            Section1['minv_net']=round((Section1['minv']-(starting_point-(starting_point-extra_value))), 2)



            Section1['RangeSum']=round(abs(Section1['maxv_net']) + abs(Section1['minv_net']), 2)
            
            # Deviation Calculation Max
            ld1=0
            ld2=0
            ld3=0
            ld4=0
            ld5=0
            rd1=0

            if d1lp1 > 0:
                ld1 = Section1['starting_point_first']-d1lp1
            if d1rp1 > 0:
                ld2 = Section1['starting_point_first']-d1rp1
            if d2lp2 > 0:    
                ld3 = Section1['starting_point_first']-d2lp2
            if d3lp3 > 0:    
                ld4 = Section1['starting_point_first']-d3lp3
            if Left_Point > 0:    
                ld5 = Section1['starting_point_first']-Left_Point
            if Right_Point > 0:    
                rd1 = Section1['starting_point_first']-Right_Point
            MaxDivSum = 0

            if ld1 > 0:
                MaxDivSum+=ld1
            if ld2 > 0:
                MaxDivSum+=ld2
            if ld3 > 0:
                MaxDivSum+=ld3
            if ld4 > 0:
                MaxDivSum+=ld4
            if ld5 > 0:
                MaxDivSum+=ld5
            if rd1 < 0:
                MaxDivSum+=abs(rd1)


            # print("MaxDivSum", MaxDivSum)

            # Deviation Calculation Min
            ld1min=0
            ld2min=0
            ld3min=0
            ld4min=0
            ld5min=0
            rd1min=0

            if d1lp1 > 0:
                ld1min = Section1['starting_point_second']-d1lp1
            if d1rp1 > 0:    
                ld2min = Section1['starting_point_second']-d1rp1
            if d2lp2 > 0:    
                ld3min = Section1['starting_point_second']-d2lp2
            if d3lp3 > 0:    
                ld4min = Section1['starting_point_second']-d3lp3
            if Left_Point > 0:    
                ld5min = Section1['starting_point_second']-Left_Point
            if Right_Point > 0:    
                rd1min = Section1['starting_point_second']-Right_Point
            MinDivSum = 0

            if ld1min > 0:
                MinDivSum+=ld1min
            if ld2min > 0:
                MinDivSum+=ld2min
            if ld3min > 0:
                MinDivSum+=ld3min
            if ld4min > 0:
                MinDivSum+=ld4min
            if ld5min > 0:
                MinDivSum+=ld5min
            if rd1min < 0:
                MinDivSum+=abs(rd1min)


            print("MinDivSum", MinDivSum)


            Section1['MaxDeviation']=round(MaxDivSum, 2)
            Section1['MinDeviation']=round(MinDivSum, 2)
            # Section1['MaxPL']=round(((MaxDivSum+Section1['maxv'])+(Section1['starting_point_first']-i_starting_point)), 2)
            # Section1['MinPL']=round(((MinDivSum+Section1['minv'])+(i_starting_point - Section1['starting_point_second'])), 2)
            Section1['MaxPL']=round(MaxDivSum+Section1['maxv'], 2)
            Section1['MinPL']=round(MinDivSum+Section1['minv'], 2)


            file_name1 = main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
            output_df = pd.read_excel(file_name1)
            exist_data = output_df['first_run'].iloc[0]
            if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                Section1['ActualP'] = round((((output_df['actual_value'].iloc[0]-Actual_Value_Calculation)/output_df['actual_value'].iloc[0])*100), 2)

            Section1['MaxP'] = round(((Section1['maxv_net']/Section1['RangeSum'])*100), 2)
            Section1['MinP'] = round(((Section1['minv_net']/Section1['RangeSum'])*100), 2)
            
            print("Section1['MaxP']", Section1['MaxP'])
        
            SList1.append(Section1)
            df1 = pd.DataFrame(SList1)
            ExcelFileWrite(main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx', df1)
            Section1={}
            SList1=[]

            print("1732")


        main_df = pd.read_excel(main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx')

        file_name2 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
        summary_df2 = pd.read_excel(file_name2)
    
        file_name3 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
        summary_df3 = pd.read_excel(file_name3)

        print("1743")
    

        df_res1 = pd.DataFrame()
        df_res2 = pd.DataFrame()

        df_res1['points'] =  summary_df3['starting_point_first']
        df_res1['values_max'] =  summary_df3['maxv']

        df_res2['points'] =  summary_df3['starting_point_second']
        df_res2['values_min'] =  summary_df3['minv']

        df_data = pd.concat([df_res1, df_res2], ignore_index=True)
        df_data['values_max'] = df_data['values_max'].fillna(0)
        df_data['values_min'] = df_data['values_min'].fillna(0)

        print("1759")

        ExcelFileWrite(main_media_url+'/media/upload_file/investing/xlsx/point_value.xlsx', df_data)


        print("1765")




        day1=[]
        for p in range(value_range_list2[1], value_range_list2[0]+5, 5):
            day1.append(p)

        print("1773", day1)
        

        return JsonConvertData(main_df), JsonConvertData(summary_df2), JsonConvertData(summary_df3), day1
        # return True

        # return 0
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        

    