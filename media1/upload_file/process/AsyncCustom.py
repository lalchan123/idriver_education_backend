import asyncio

import json
import os

from AsyncTest import * 
        

async def Custom():

    task1 = asyncio.create_task(Test())
    # task2 = asyncio.create_task(read_json('asynclal'))
    # task1 = asyncio.create_task(write_json('asynclal', ['badsa', 'abc']))
    # task2 = asyncio.create_task(read_json('asynclal'))

    await task1
    # await task2
    
asyncio.run(Custom())