#! /usr/bin/env python
# -*- coding=utf-8 -*-
import math
import random, os


def DistanceToLogLat(distance, number, logLatPtStr):
    """
    将相对于起点的距离转换为经纬度,distance代表到点的距离，angle代表方位角度
    """
    lat_lng = logLatPtStr.split(",")
    lng1 = float(lat_lng[0])  # 经度
    lat1 = float(lat_lng[1])  # 纬度
    LngLat = []
    for i in range(number):
        angle = random.randint(-180, 180)  # 方位角随机设置
        lon = lng1 + (float(distance) * math.sin(angle * math.pi / 180)) / (
            111.31955 * math.cos(lat1 * math.pi / 180))  # 将距离转换成经度
        lat = lat1 + (float(distance) * math.cos(angle * math.pi / 180)) / 111.31955  # 将距离转换成纬度
        lon1 = round(lon, 6)  # 保留六位小数点
        lat1 = round(lat, 6)
        lnglat = str(lon1) + "," + str(lat1)
        LngLat.append(lnglat)
    return LngLat


def jiazao():
    """
    原始GPS数据，提取经纬度信息写入kml文件。
    """
    try:
        file = open(os.path.join(os.getcwd(), 'GPS原始数据.txt'), 'r', encoding='utf-8')
        list = file.readlines()
        list1 = []
        j = 0
        for line in list:
            data = line.split()
            if data[1] != '0.000000' and data[2] != '0.000000':
                data_str = data[1] + "," + data[2]
                list1.append(data_str)  # 获取定位成功后经纬度信息
            else:
                j += 1  # 统计定位定位成功后持续时间，1s为单位

        while True:
            print("请输入离中心点的距离(单位：km)及加噪个数，以空格隔开(0.01 10)：")
            Input = input(str())
            distance = float(Input.split()[0])
            number = int(Input.split()[1])
            i = random.randint(j, len(list1))  # 随机获取定位成功后的某一点的经纬度
            dd = list[i].split()
            log_Lat = dd[1] + "," + dd[2]
            LonLnt = DistanceToLogLat(distance, number, log_Lat)  # 以某一点为圆心，获取特定距离的若干个经纬度信息
            for k in range(number):
                lon = LonLnt[k].split(",")[0]
                lat = LonLnt[k].split(",")[1]
                dd[0] = str(int(dd[0]) + 1)
                dd[1] = lon
                dd[2] = lat
                lat_lng = (" ").join(dd)
                list.insert(i + k + 1, lat_lng + "\n")  # 将获取到的噪声插入到原始经纬度数据
                count = i + k + 1
            file = open(os.path.join(os.getcwd(), '加噪数据.txt'), 'w+', encoding='utf-8')
            for i in range(len(list) - count - 1):
                """
                加噪后对中心点以后的经纬度的时间戳做处理
                """
                change_list = list[count + i + 1].split()
                change_list[0] = str(int(change_list[0]) + 10)
                list0 = (" ").join(change_list)
                list[count + i + 1] = list0

            for i in range(len(list)):
                ss = list[i].strip("\n")
                file.write(str(ss) + "\n")  # 将加入噪声后的经纬度信息写入文件
            file.close()
            print("是否继续添加信号噪声,输入y继续,其他则退出！")
            INPUT = input(str())
            if INPUT.lower() == "y":
                continue
            else:
                break

    except Exception as e:
        print(e)


def runmain():
    jiazao()
    path = os.path.dirname(os.getcwd()) + "\\GPS原始数据.txt"
    path1 = os.path.join(os.getcwd(), "加噪数据.txt")
    print(path, path1)
    os.system("copy %s %s" % (path1, path))


if __name__ == "__main__":
    #runmain()
    s= DistanceToLogLat(1,1,"113.89723055555555,22.95137777777778")
    s1 = DistanceToLogLat(5, 1, "113.89723055555555,22.95137777777778")
    s2 = DistanceToLogLat(10, 1, "113.89723055555555,22.95137777777778")
    s3 = DistanceToLogLat(50, 1, "113.89723055555555,22.95137777777778")
    s4 = DistanceToLogLat(100, 1, "113.89723055555555,22.95137777777778")
    print(s,s1,s2,s3,s4)
#"113.89723055555555,22.95137777777778"