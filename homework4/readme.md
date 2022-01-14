# Python程序设计#4作业

## 作业题目

基于#3作业获取的数据（No_Smoothing，非平滑数据），计算出LOWESS（局部加权回归，fraction取前后各5年的数据）结果，该结果可以与test.txt文件中的Lowess字段进行比较。

## 作业内容

程序源代码嵌入下方的code block中。

```python
import asyncio
import aiohttp
import json
import re
import statsmodels.api as sm

URL = "http://127.0.0.1:8000/data/{}"


async def main():
    # help info
    print("Data type: json/xml/csv")
    print("Date Range: 1880 ~ 2020")
    print("Sort Order: 0 for increase, 1 for decrease")

    type = input("Please Input the data type you want (Defalut:json): ")
    start = input("Please Input the start date (default:1880):")
    end = input("Please Input the end date (default:2020):")
    order = input("Please Input the order (default:0):")

    # params
    type = type if type != "" else "json"
    params = {
        'start': start if start != '' else "1880",
        'end': end if end != '' else "2020",
        'order': order if order != '' else "0"
    }

    # validator
    if not params["start"].isdigit() or not params["end"].isdigit() \
            or not params["order"].isdigit() or type not in ["json", "xml", "csv"]:
        raise Exception("The params Error.")

    # main process
    async with aiohttp.ClientSession() as session:
        async with session.get(URL.format(type), params=params) as resp:
            print(resp.url)
            data = await resp.text()

            # parse the text of json/csv/xml
            async def parseText(type='json'):
                text = "Year,No_Smoothing,Lowess\n"
                if type == 'json':
                    jdata = json.loads(data)
                    for j in jdata:
                        text += f'{j["Year"]},{j["No_Smoothing"]}\n'
                elif type == 'xml':
                    pattern1 = re.compile(r"<item.*/>")
                    pattern2 = re.compile(
                        r'.+Year="(\d+)" No_Smoothing="(.+)" Lowess="(.+)"')
                    lis = pattern1.findall(data)
                    for item in lis:
                        res = pattern2.match(item)
                        if res:
                            text += f'{res.group(1)},{res.group(2)}\n'
                elif type == 'csv':
                    text = data

                # lowess 局部加权回归
                years, No_Smoothing = [], []
                for line in text.split('\n'):
                    if line != '':
                        item = line.split(",")
                        years.append(item[0])
                        No_Smoothing.append(item[1])
                years.remove("Year")
                No_Smoothing.remove("No_Smoothing")

                yest = sm.nonparametric.lowess(
                    No_Smoothing, years, frac=10/len(years))
                lowess = list(list(zip(*yest))[1])

                text = "Year,No_Smoothing,Lowess\n"
                for i in range(0, len(years)):
                    text += f"{years[i]},{No_Smoothing[i]},{format(lowess[i], '.2f')}\n"
                
                return text

            print(await parseText(type))
            # await parseText(type)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## 代码说明

本项目在实验三的基础上进行加工，根据获取的数据中的年份和No_Smoothing，计算温度平滑处理后的数据。

在结果计算完毕后，与原Lowess数据进行对比，结果近似，因此计算结果符合要求。

### 主要代码段

```py
yest = sm.nonparametric.lowess(
    No_Smoothing, years, frac=10/len(years))
lowess = list(list(zip(*yest))[1])
```
### Lowess
本实验主要用到了statsmodels中的lowess函数，来根据x值对y值进行平滑处理。其中要求lowess的计算依据当前年份的前后5年，共10年。

根据lowess函数说明，计算时局部数据为离该点最近的$frac*dataLen$个点，因此frac参数的取值就应该为 $10/dataLength$。

