# Python 程序设计#5 作业

## 作业题目

基于#3 作业、#4 作业获取的 No_Smoothing、Lowess 数据项，在同一个图上分别绘制出折线图（No_Smoothing）和平滑线图（Lowess）。绘制结果对照参考图片（test.png）。

## 作业内容

程序源代码嵌入下方的 code block 中。

```python
import asyncio
import aiohttp
import json
import re
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


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
                    if line != '' and "Year" not in line:
                        item = line.split(",")
                        years.append(item[0])
                        No_Smoothing.append(float(item[1]))

                yest = sm.nonparametric.lowess(
                    No_Smoothing, years, frac=10/len(years))
                lowess = list(list(zip(*yest))[1])

                draw(years,No_Smoothing,lowess)

                text = "Year,No_Smoothing,Lowess\n"
                for i in range(0, len(years)):
                    text += f"{years[i]},{No_Smoothing[i]},{format(lowess[i], '.2f')}\n"

                return text

            def draw(years,no_smoothing,lowess):
                x = np.array(years)
                y1 = np.array(no_smoothing)
                y2 = np.array(lowess)

                plt.title("Temperature with Years")
                plt.xlabel("YEAR")
                plt.ylabel("Temperature Anomaly(C)")

                x_major_locator = MultipleLocator(20)
                y_major_locator = MultipleLocator(0.5)
                ax = plt.gca()
                ax.xaxis.set_major_locator(x_major_locator)
                ax.yaxis.set_major_locator(y_major_locator)

                plt.plot(x,y1,marker="o",mec="#CBCBCB",mfc="w",color="#CBCBCB")
                plt.plot(x,y2,color="g")
				
                plt.savefig('test2.png')
                plt.show();

            print(await parseText(type))
            # await parseText(type)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## 代码说明

本程序在实验 4 的基本上继续进行封装，增加了对图形的绘制

### Numpy

绘制图形所需要的数组数据需要通过`Numpy`模块来转换

```py
x = np.array(years)
y1 = np.array(no_smoothing)
y2 = np.array(lowess)
```

### Matplotlib

绘制图形主要用到了`Matplotlib`图形库中的`pyplot`模块来绘制图像。

绘制包括两部分，一部分为以`No_Smoothing`作为 y 轴，另一部分以`Lowess`平滑后的数据作为 y 轴。

绘制时调整图形的颜色，x 与 y 轴的标签与刻度。

其中刻度问题需要借助`MultipleLocator`，来设置刻度。

```py
x_major_locator = MultipleLocator(20)
y_major_locator = MultipleLocator(0.5)
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.yaxis.set_major_locator(y_major_locator)
```

若要导出图片，可在`show`之前`savefig`即可。
