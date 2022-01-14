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

    if order == 1 or order == 2:
        data.sort(key=sortKey, reverse=(order == 2))

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
