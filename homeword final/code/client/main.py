import requests
import mpl_toolkits.axisartist as axisartist
import matplotlib.pyplot as plt
import matplotlib.colors as pcolors
import matplotlib.cm as pcm
from shapely import geometry
import numpy as np

plt.rcParams['font.sans-serif'] = ['Kaiti']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False


url = "http://127.0.0.1:8000/gpw"

Default = [
    [115, 40.2],
    [116, 41],
    [117, 40.2],
    [116.5, 39],
    [115.5, 39]
]

cs = ["#CFECFC", "#B8CAFF",
      "#8FABFF", "#295FFF",
      "#0029A3", "#00185E"]


def post(polygon=Default):
    data = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [polygon]
        },
        "properties": {
            "name": "Dinagat Islands"
        }
    }

    response = requests.post(url, json=data)
    result = response.json()[0]
    result["coordinates"] = data["geometry"]["coordinates"][0]
    # print(result)
    return result


def createCanvas():
    # 创建画布
    fig = plt.figure()
    # 使用axisartist.Subplot方法创建一个绘图区对象ax
    ax = axisartist.Subplot(fig, 111)
    # 将绘图区对象添加到画布中
    fig.add_axes(ax)
    # 通过set_axisline_style方法设置绘图区的底部及左侧坐标轴样式
    # "-|>"代表实心箭头："->"代表空心箭头
    ax.axis["bottom"].set_axisline_style("->", size=1.5)
    ax.axis["left"].set_axisline_style("->", size=1.5)
    # 通过set_visible方法设置绘图区的顶部及右侧坐标轴隐藏
    ax.axis["top"].set_visible(False)
    ax.axis["right"].set_visible(False)


def colorMap(population):
    if population < 1:
        return cs[0]
    elif population <= 5:
        return cs[1]
    elif population <= 25:
        return cs[2]
    elif population <= 250:
        return cs[3]
    elif population <= 1000:
        return cs[4]
    else:
        return cs[5]


def draw(data):
    createCanvas()

    plt.title("网状区域人口分布点图")
    plt.xlabel("经度（-90~90°）")
    plt.ylabel("维度（-180~180°）")

    polygon = geometry.Polygon(data["coordinates"])
    x1, y1 = polygon.exterior.xy
    plt.fill(x1, y1, "#ffffe0")

    lons, lats, pops, colors = [], [], [], []
    for grid in data["grids"]:
        lons.append(grid["lon"])
        lats.append(grid["lat"])
        pops.append(grid["population"])
        colors.append(colorMap(grid["population"]))
    x2 = np.array(lons)
    y2 = np.array(lats)
    sc = plt.scatter(x2, y2, c=pops, cmap="summer")

    plt.colorbar(sc, label="人口数")

    plt.savefig('./img.png')
    plt.show()


if __name__ == "__main__":
    polygon = []
    print("请按顺时针（逆时针）输入凸多边形的点的经纬度(x,y)：")
    print("每行按逗号分隔两个数值，输入空则结束")
    while True:
        str = input("输入坐标x,y:")
        xy = str.split(",")
        if len(xy) == 2:
            polygon.append([float(xy[0]), float(xy[1])])
        else:
            break
    if len(polygon) == 0:
        polygon = Default
    res = post(polygon)
    print(f'总人数为：{res["population"]}')
    draw(res)
