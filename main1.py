#! /usr/bin/env python
# -*- coding=utf-8 -*-
import os
import xlrd
import xlsxwriter
from xlutils.copy import copy


def gps_handle_data():
    """
    经过算法程序处理后，提取经纬度信息写入kml文件。
    """
    try:
        file = open(os.path.join(os.getcwd(), 'zsPark_iOS.plt'), 'r', encoding='utf-8')
        list = file.readlines()
        list1 = []
        for line in list:
            if ",," in line:
                data = line.split(",")
                list1.append(data[1])
                list1.append(data[0])
                list1.append('0')
                data = (',').join(list1)
                data = data.replace(',0,', ',0 ')
        return data
    except Exception as e:
        print(e)


def gps_ori_data():
    """
    原始GPS数据，提取经纬度信息写入kml文件。
    """
    try:
        file = open(os.path.join(os.getcwd(), 'GPS原始数据.txt'), 'r', encoding='utf-8')
        list = file.readlines()
        list1 = []
        for line in list:
            data = line.split()
            if data !=[]:
                if data[1] != '0.000000' and data[2] != '0.000000':
                    list1.append(data[1])
                    list1.append(data[2])
                    list1.append('0')
            data = (',').join(list1)
            data = data.replace(',0,', ',0 ')
        return data
    except Exception as e:
        print(e)


def read_data(gps_data, file_kml):
    """
    传入经纬度信息写入kml文件，区分原始数据与算法处理过的数据
    """
    try:
        file = open(os.path.join(os.getcwd(), file_kml), 'r', encoding='utf-8')
        list = file.readlines()
        len_t = len(list) - 1
        for i in range(len_t):
            if '<coordinates>' in list[i]:
                data = list[i].split('<coordinates>')[1].split('</coordinates>\n')
                data = data[0]
                data1 = gps_data
                list[i] = list[i].replace(data, data1)
        file = open(file_kml, 'w', encoding='utf-8')
        file.writelines(list)
    except Exception as e:
        print(e)


def list_data():
    """
    获取所有星值数据，写入列表
    """
    try:
        file = open(os.path.join(os.getcwd(), 'GPS原始数据.txt'), 'r', encoding='utf-8')
        list = file.readlines()
        list1 = []
        for line in list:
            data = line.split()
            if data != []:
                if data[1] != '0.000000' and data[2] != '0.000000':
                    list1.append(data[7])
                    list1.append(data[8])
                    list1.append(data[9])
                    list1.append(data[10])
        list1.sort()
        return list1
    except Exception as e:
        pass


def excel_write():
    """
    统计所有的星值数据和占的百分比
    """
    try:
        list1 = list_data()
        j = 0
        k = 0
        xlsxwriter.Workbook(os.path.join(os.getcwd(), '数据统计.xls'))
        excel = xlrd.open_workbook(os.path.join(os.getcwd(), '数据统计.xls'), 'wb')
        rs = excel.sheet_by_index(0)
        wb = copy(excel)
        ws = wb.get_sheet(0)
        ws.write(0, 0, "星值")
        ws.write(0, 1, "出现次数")
        ws.write(0, 2, "占百分比（%）")
        for l in range(len(list1)):
            for i in range(len(list1)):
                if list1[k] == list1[i]:
                    j += 1
            k = j
            count = list1.count(list1[j - 1])
            ws.write(l + 1, 0, int(list1[j - 1]))
            ws.write(l + 1, 1, count)
            ws.write(l + 1, 2, (round((count / len(list1)), 5)) * 100)
            wb.save(os.path.join(os.getcwd(), '数据统计.xls'))

    except Exception as e:
        pass


def choice_print():
    """
    统计一定范围的星值数据占的百分比
    """
    try:
        list = list_data()
        excel = xlrd.open_workbook(os.path.join(os.getcwd(), '数据统计.xls'), 'wb')
        rs = excel.sheet_by_index(0)
        wb = copy(excel)
        ws = wb.get_sheet(0)
        ws.write(0, 4, "星值范围")
        ws.write(0, 5, "占百分比（%）")
        j = 1

        file = open(os.path.join(os.getcwd(), "范围输入.txt"), 'r', encoding='utf-8')
        f = file.readline()
        li = f.split()
        for range_input in li:
            first = range_input.split("-")[0]
            last = range_input.split("-")[1]
            count = 0
            for i in range(len(list)):
                if int(list[i]) >= int(first) and int(list[i]) <= int(last):
                    count += 1
            ws.write(j, 4, range_input)
            ws.write(j, 5, (round(count / len(list), 5)) * 100)
            wb.save(os.path.join(os.getcwd(), '数据统计.xls'))
            j += 1
            print("--- 星数范围在%s占的百分比为%s%% " % (range_input, (round(count / len(list), 5)) * 100))

    except Exception as e:
        print(e)


def time_gps():
    """
    统计定位成功所需要的时间，默认打印经纬度时间为1s一行。
    """
    file = open(os.path.join(os.getcwd(), 'GPS原始数据.txt'), 'r', encoding='utf-8')
    list = file.readlines()
    time = 0
    for line in list:
        data = line.split()
        if data != []:
            if data[1] == '0.000000' and data[2] == '0.000000':
                time += 1
    excel = xlrd.open_workbook(os.path.join(os.getcwd(), '数据统计.xls'), 'wb')
    excel.sheet_by_index(0)
    wb = copy(excel)
    ws = wb.get_sheet(0)
    ws.write(0, 7, "定位时间（s）")
    ws.write(1, 7, time)
    wb.save(os.path.join(os.getcwd(), '数据统计.xls'))


def park_ios():
    """
    提取原始数据文件的经纬度写入算法程序所需的文件：zsPark_iOS.txt
    """
    file = open(os.path.join(os.getcwd(), 'GPS原始数据.txt'), 'r', encoding='utf-8')
    list = file.readlines()
    list1 = []
    for line in list:
        data0 = line.split()
        if data0 != []:
            if data0[1] != '0.000000' and data0[2] != '0.000000':
                data = line.split()[:6]
                data1 = (" ").join(data)
                list1.append(data1)
    file1 = open(os.path.join(os.getcwd(), "zsPark_iOS.txt"), 'w', encoding='utf-8')
    file1.write("# %s\n" % str(len(list1)))
    file1.write("# time lon lat ele hdop vdop\n")
    for i in range(len(list1)):
        file1.write(list1[i] + "\n")


def run_exe():
    os.system(os.path.join(os.getcwd(),"main.exe zsPark_iOS"))


def runmain():
    while True:
        print("""请输入你需要执行的功能选项：
        1、原始数据>原始轨迹kml
        2、原始数据>算法处理后的轨迹kml
        3、原始数据>星值百分比分布、TTFF时间
        4、执行以上3个全部功能。
            按q退出执行！！！
        """)
        int_input = str(input())
        if int_input == '1':
            gps_data = gps_ori_data()
            read_data(gps_data, "gps_ori_data.kml")
            print("执行完毕。\n")

        elif int_input == '2':
            park_ios()
            run_exe()
            gps_data = gps_handle_data()
            read_data(gps_data, "gps_handle_data.kml")
            print("执行完毕。\n")

        elif int_input == '3':
            excel_write()
            choice_print()
            time_gps()
            print("---数据处理完毕！---\n")

        elif int_input == '4':
            gps_data = gps_ori_data()
            read_data(gps_data, "gps_ori_data.kml")

            park_ios()
            run_exe()
            gps_data = gps_handle_data()
            read_data(gps_data, "gps_handle_data.kml")

            excel_write()
            choice_print()
            time_gps()
            print("---数据处理完毕！---\n")
        elif int_input.lower() == 'q':
            break
        else:
            print("---输入选项有误，请重新输入---\n")
            continue


if __name__ == "__main__":
    runmain()
