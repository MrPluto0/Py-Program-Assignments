# Python程序设计#3作业

## 作业题目

基于 aiohttp（https://docs.aiohttp.org/en/stable/）实现一个服务查询客户端，能够访问#2作业提供的服务。数据获取后进行格式转换：

* JSON结果转换为TEXT格式（字段之间使用空格间隔、记录之间使用换行符间隔）
* XML结果转换为TEXT格式（需求同上）。
* CSV格式转换为TEXT格式（需求同上）。

要求客户端可以通过以上3种格式访问数据服务。

## 作业内容

程序源代码嵌入下方的code block中。

```python
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
```

## 代码说明

### 参数说明
|params|info|value|
|----|----|----|
|type|请求数据类型|默认值json，可选值xml/csv/json|
|start|开始时间|默认值1980，要求数字类型|
|end|结束时间|默认值2020，要求数据|
|order|顺序|默认0，可选0/1，0为升序|

### 结构说明
1. 通过type来格式化客户端要请求的URL
```py
URL = "http://127.0.0.1:8000/data/{}"
```
2. 将URL的Query参数通过params字典传递：
```py
params = {
    'start': start if start !='' else "1980", 
    'end': end if end !='' else "2020", 
    'order': order if order !='' else "0"
}
session.get(URL.format(type),params=params) 
```
3. 分别根据type来对三种数据类型进行转换，转换的函数同样设置为async（纤程），可以在处理数据的时候其它纤程仍然继续运行。
   其中xml格式的数据可通过正则表达式匹配其中的数据。
```py
pattern1 = re.compile(r"<item.*/>")
pattern2 = re.compile(r'.+Year="(\d+)" No_Smoothing="(.+)" Lowess="(.+)"')
```