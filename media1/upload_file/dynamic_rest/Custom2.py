import json
import os
import asyncio

# global function
from FunctionFolder.WrapperFunc import *

from media.upload_file.dynamic_rest.CustomTest import *


async def Custom2(user, api_name, paramList):
    
    task1 = asyncio.create_task(CustomTest(user, api_name, paramList))
   
    await task1
    

asyncio.run(Custom2(user='a', api_name='a', paramList='a'))
# asyncio.run(Custom2(user, api_name, paramList))