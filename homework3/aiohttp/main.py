import asyncio
import aiohttp
import json,re

URL = "http://127.0.0.1:8000/data/{}"

async def main():
    # help info
    print("Data type: json/xml/csv")
    print("Date Range: 1980 ~ 2020")
    print("Sort Order: 0 for increase, 1 for decrease")
    
    type = input("Please Input the data type you want (Defalut:json): ")
    start = input("Please Input the start date (default:1980):")
    end = input("Please Input the end date (default:2020):")
    order = input("Please Input the order (default:0):")
    
    # params
    type = type if type !="" else "json"
    params = {
        'start': start if start !='' else "1980", 
        'end': end if end !='' else "2020", 
        'order': order if order !='' else "0"
    }

    # validator
    if not params["start"].isdigit() or not params["end"].isdigit() \
        or not params["order"].isdigit() or type not in ["json","xml","csv"]:
        raise Exception("The params Error.")
    
    # main process
    async with aiohttp.ClientSession() as session:
        async with session.get(URL.format(type),params=params) as resp:
            print(resp.url)
            data = await resp.text()

            # parse the text of json/csv/xml
            async def parseText(type='json'):
                text = "Year,No_Smoothing,Lowess\n"
                if type == 'json':
                    jdata = json.loads(data)
                    for j in jdata:
                        text += f'{j["Year"]},{j["No_Smoothing"]},{j["Lowess"]}\n'
                elif type == 'xml':
                    pattern1 = re.compile(r"<item.*/>")
                    pattern2 = re.compile(r'.+Year="(\d+)" No_Smoothing="(.+)" Lowess="(.+)"')
                    lis =  pattern1.findall(data)
                    for item in lis:
                        res = pattern2.match(item)
                        if res:
                            text += f'{res.group(1)},{res.group(2)},{res.group(3)}\n'
                elif type == 'csv':
                    text = data
                    
                return text

            print(await parseText(type))
            
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())