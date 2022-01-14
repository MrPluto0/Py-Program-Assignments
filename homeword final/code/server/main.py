from numpy.lib.shape_base import column_stack
from sanic import Sanic
from sanic import response
from sanic.views import HTTPMethodView
from shapely import geometry

import re
import os
import json
import struct
import numpy as np

app = Sanic("GPW-App")

SIZE = 30
COUNT = 360
RANGE = 10800

# 0.00833333 * SIZE
CELL = 0.25


class Factory():
    def __init__(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.srcPath = self.dir + "./data/gpw_v4_population_count_rev11_2020_30_sec_{}.asc"
        self.dstPath = self.dir + "./data/gpw.bin"

    def preProcess(self):
        if not os.path.exists(self.dstPath):
            for i in range(1, 9):
                self.merge(i)

    # ascii to binary
    def merge(self, num):
        dst = open(self.dstPath, "ab")
        src = open(self.srcPath.format(num), 'r')
        data = [0] * COUNT
        row = 0
        for line in src:
            print(f"row:{row}")

            if row >= 6:
                lineArr = re.split("\s+", line)
                col = 0
                for i in range(0, RANGE):
                    tmp = float(lineArr[i])
                    if tmp != -9999:
                        data[int(col/SIZE)] += tmp
                    col += 1

                if (row-6) % SIZE == (SIZE-1):
                    for val in data:
                        tmp = struct.pack('f', val)
                        dst.write(tmp)
                    data = [0] * COUNT
            row += 1
        src.close()

    def point2line(self, x1, y1, x2, y2):
        return [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

    def calcPopulation(self, lonLats):
        polygon = geometry.Polygon(lonLats)
        lonMin, latMin, lonMax, latMax = polygon.bounds
        cellArea = geometry.Polygon(self.point2line(0, 0, CELL, CELL)).area
        popuTotal = 0
        grids = []

        for lon in np.arange(lonMin, lonMax, CELL):
            for lat in np.arange(latMin, latMax, CELL):
                cellLon1 = lon - lon % CELL
                cellLon2 = cellLon1 + CELL
                cellLat1 = lat - lat % CELL
                cellLat2 = cellLat1 + CELL
                cellPolygon = geometry.Polygon(
                    self.point2line(cellLon1, cellLat1, cellLon2, cellLat2))
                area = cellPolygon.intersection(polygon).area
                if area > 0.0:
                    p = self.getPopulationFromFile(cellLon1, cellLat1)
                    popuTotal += (area/cellArea) * p
                    grids.append({
                        "lon": cellLon1+CELL/2,
                        "lat": cellLat1+CELL/2,
                        "population": p
                    })
                else:
                    grids.append({
                        "lon": cellLon1+CELL/2,
                        "lat": cellLat1+CELL/2,
                        "population": 0
                    })
        return {
            "population": popuTotal,
            "grids": grids
        }

    def getPopulationFromFile(self, lon, lat):
        # no for block 90*90
        no = int((lon+180)/90) % 4
        if lat < 0.0:
            no += 4

        i = (lon % 90)/CELL
        j = (lat % 90)/CELL
        offset = no * COUNT*COUNT + j * COUNT + i
        return self.getData(np.int64(offset))

    def getData(self, offset):
        # offset < 360*360*8
        # fileSize = 360*360*8*4 Byte
        dst = open(self.dstPath, "rb")
        dst.seek(4*offset)
        data = struct.unpack('f', dst.read(4))[0]
        return data


class GPW(HTTPMethodView):
    async def get(self, request):
        return response.text("GET on GPW.")

    async def post(self, request):
        population = []

        geo = request.json["geometry"]
        if geo["type"] == 'Polygon':
            fac = Factory()
            for coordinate in geo["coordinates"]:
                p = fac.calcPopulation(coordinate)
                population.append(p)

        return response.json(population)


app.add_route(GPW.as_view(), "/gpw")


@ app.get("/")
async def index(request):
    return response.text("Hello, Welcome to GPW Search !!!")

if __name__ == "__main__":
    # fac = Factory()
    # p = fac.calcPopulation(fac.point2line(115.07, 39.07, 117.0833, 41.01))
    # print(p)
    app.run(host="127.0.0.1", port=8000, auto_reload=True, debug=True)
