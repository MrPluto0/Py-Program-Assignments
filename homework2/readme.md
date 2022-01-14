# Python程序设计#2作业

## 作业题目

数据文件（test.txt）是一个全球温度年度异常历史数据。基于Sanic实现一个查询服务，服务包括：

* 按起始和结束年份查询历史数据，查询结果支持多种格式：JSON、XML、CSV（用逗号作为间隔符）。
* 按温度高低进行排序，支持升序和降序两种排序方式。

## 作业内容

程序源代码嵌入下方的code block中。

```python
import os
import re
from sanic import Sanic
from sanic.response import text, json, redirect, stream

# 当前文件目录绝对路径
dir = os.path.dirname(os.path.abspath(__file__))

app = Sanic("MyHelloWorldApp")

# 若不传入绝对路径，则默认为sanic包下的路径
app.update_config(dir + '/src/config.py')


def getRequestInfo(request):
    start, end, order = "1880", "2020", 0
    if ("start" in request.args):
        start = request.args["start"][0]

    if ("end" in request.args):
        end = request.args["end"][0]

    if ("order" in request.args):
        order = int(request.args["order"][0])

    data = [
        item for item in request.ctx.data
        if item["Year"] >= start and item["Year"] <= end
    ]

    def sortKey(item):
        # 字符串->数字
        return float(item["No_Smoothing"])

    data.sort(key=sortKey, reverse=(order == 1))

    return data


async def writeInfo(response, formatStr, data):
    await response.write(formatStr.format("Year", "No_Smoothing", "Lowess"))
    for item in data:
        await response.write(
            formatStr.format(item["Year"], item["No_Smoothing"],
                             item["Lowess"]))


@app.middleware("request")
async def getData(request):
    context = []
    with open(dir + '/../test.txt', mode="r", encoding="gb2312") as f:
        for line in f.readlines():
            if "#" not in line:
                temp = re.split('\s+', line)
                context.append({
                    "Year": temp[0],
                    "No_Smoothing": temp[1],
                    "Lowess": temp[2]
                })
    request.ctx.data = context


@app.route("/")
async def jumpHome(request):
    return text("Hello World")


@app.route("/data")
async def redir(request):
    return redirect(app.url_for("json"))


@app.get("/data/json", name="json")
async def parseJson(request):
    data = getRequestInfo(request)
    return json(data)


@app.get("/data/xml", name="xml")
async def parseXml(request):
    data = getRequestInfo(request)

    # 流传输
    async def writeXmlInfo(response):
        formatStr = "<item Year=\"{}\" No_Smoothing=\"{}\" Lowess=\"{}\" />\n"
        await writeInfo(response, formatStr, data)

    return stream(writeXmlInfo)


@app.get("/data/csv")
async def parseCsv(request):
    data = getRequestInfo(request)

    # 流传输
    async def writeXmlInfo(response):
        formatStr = "{},{},{}\n"
        await writeInfo(response, formatStr, data)

    return stream(writeXmlInfo)


# 1. 直接运行py文件
# 2. 命令行 sanic main.app
# auto_reload 热更新
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, auto_reload=True)

```

## 代码说明

### 路由结构
- **\\** 根路由：Hello World
- **\data** 数据路由：重定向到\data\json页面
- **\data\json** Json格式数据
- **\data\xml** Xml格式数据
- **\data\csv** Csv格式数据

### 查询参数
- start 开始年份
- end 结束年份
- order 按温度排序，0为顺序，1为逆序
  
```
Default:
start = 1980
end = 2020
order = 0
```

### 相关代码架构
1. 本项目中中增加了中间层$middleWare$,用来在响应前获取并加载`test.txt`中的数据，数据格式默认为字典(JSON)。
2. 本项目在读取文件时
   - 采用`os`模块的文件函数，来获取`main.py`的绝对路径，可适用于任意电脑与文件夹。
   - 采用`re`模块来分割字符串，借助正则表达式来按照空格分割字符串。本项目中为`'\s+'`表示匹配一个或多个空格。
3. 本项目在向响应体中写入内容时，采用流`Stream`的方式写，不需要将所有内容全部加载到字符串中写入响应，节省了缓存。针对大数据量时，流的方式非常合适。