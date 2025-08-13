import json
import os

# global function
from FunctionFolder.WrapperFunc import *


        
        
def Custom(user, api_name, paramList):
    print("hello")
    
    
    if user == 'hello6' and api_name == 'hello6' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        # return startwith(['Lalchan', 'LalAbc', 'lalmcmm', 'Abc', 'abd'], 'lal')
        # return contains('Lalchan', 'La')
        # return read_csv('investingCalender')
        # return read_json('apple_news_data')
        # return avg(a, b)
        # return avg(a, b)
                
        # root = Node(27)
        # root.insert(14)
        # root.insert(35)
        # root.insert(10)
        # root.insert(19)
        # root.insert(31)
        # root.insert(42)
        # return root.PrintTree()       
        # return root.inorderTraversal(root)       
        # return root.PreorderTraversal(root)       
        # return root.PostorderTraversal(root)       
        # print(root.PreorderTraversal(root)) 
        
        # query =  "SELECT User.email, User.password, User.is_active, User.is_email_verified, User.is_superuser, User_Password_Details.user_email, User_Password_Details.user_otp, User_Password_Details.timestamp FROM User, User_Password_Details WHERE User.email = User_Password_Details.user_email and User.email < 2 ORDER BY email"    

        # query =  "SELECT User.email, User.password FROM User ORDER BY email"    
        # return Execute_sql(query) 
        
        filename = 'lalchan_array_json'
        array_json = [
            {
                'fname': 'lal',
                'lname': 'badsa',
            },
            {
                'fname': 'I',
                'lname': 'J',
            },
            {
                'fname': 'C',
                'lname': 'D',
            }
        ]

        return write_json(filename, array_json)



