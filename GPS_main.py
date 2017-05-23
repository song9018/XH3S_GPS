#! /usr/bin/env python
# -*- coding=utf-8 -*-
import os,glob
import xlrd
import xlsxwriter
from xlutils.copy import copy
import shutil

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


def gps_ori_data(file_path):
    """
    原始GPS数据，提取经纬度信息写入kml文件。
    """
    try:
        file = open(file_path, 'r', encoding='utf-8')
        list = file.readlines()
        list1 = []
        for line in list:
            data = line.split()
            if data != []:
                if data[1] != '0.000000' and data[2] != '0.000000':
                    list1.append(data[1])
                    list1.append(data[2])
                    list1.append('0')
            data = (',').join(list1)
            data = data.replace(',0,', ',0 ')

        return data
    except Exception as e:
        print(e)


def read_data(gps_data, file_kml,path):
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
        file = open(path, 'w', encoding='utf-8')
        file.writelines(list)
    except Exception as e:
        print(e)


def list_data(path1):
    """
    获取所有星值数据，写入列表
    """
    try:

        file = open(path1, 'r', encoding='utf-8')
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
        print(e)


def excel_write(path1,path):
    """
    统计所有的星值数据和占的百分比
    """
    try:
        list1 = list_data(path1)
        j = 0
        k = 0
        ll=xlsxwriter.Workbook( './数据汇总/%s/数据统计_%s.xls' %(path,path))
        ll.close()
        excel = xlrd.open_workbook('./数据汇总/%s/数据统计_%s.xls' %(path,path), 'wb')
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
            wb.save('./数据汇总/%s/数据统计_%s.xls' %(path,path))

    except Exception as e:
        print(e)
    finally:
        wb.save('./数据汇总/%s/数据统计_%s.xls' % (path, path))


def choice_print(file_path,path,path1):
    """
    统计一定范围的星值数据占的百分比
    """
    try:
        list = list_data(path1)
        excel = xlrd.open_workbook(file_path, 'wb')
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
            wb.save('./数据汇总/%s/数据统计_%s.xls' %(path,path))
            j += 1
            print("--- 星数范围在%s占的百分比为%s%% " % (range_input, (round(count / len(list), 5)) * 100))

    except Exception as e:
        print(e)


def time_gps(file_path,path):
    """
    统计定位成功所需要的时间，默认打印经纬度时间为1s一行。
    """
    file = open(file_path, 'r', encoding='utf-8')
    list = file.readlines()
    time = 0
    for line in list:
        data = line.split()
        if data != []:
            if data[1] == '0.000000' and data[2] == '0.000000':
                time += 1
    excel = xlrd.open_workbook( './数据汇总/%s/数据统计_%s.xls' %(path,path), 'wb')
    excel.sheet_by_index(0)
    wb = copy(excel)
    ws = wb.get_sheet(0)
    ws.write(0, 7, "定位时间（s）")
    ws.write(1, 7, time)
    wb.save('./数据汇总/%s/数据统计_%s.xls' %(path,path))


def park_ios(file_path):
    """
    提取原始数据文件的经纬度写入算法程序所需的文件：zsPark_iOS.txt
    """
    file = open(file_path, 'r', encoding='utf-8')
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



def get_data():
    file1 = glob.glob("*.log")
    for i in range(len(file1)):
        file = open(file1[i], 'r', encoding="utf-8")
        k = 0
        list1 = []
        time_list=[]
        list = file.readlines()
        for i in range(len(list)):
            if "YF_GPS" in list[i]:
                k += 1
                list1.append(i)
                time_list.append(list[i].replace(":","_").strip("\n"))
        list1.append(len(list) - 1)
        s = 0

        for j in range(k):
            os.mkdir("./数据汇总/%s" %time_list[j])
        for j in range(k):
            o_fd = open('./数据汇总/%s/%s.txt' % (time_list[j],time_list[j]), 'w', encoding="utf-8")
            for i in range(len(list) - (list1[s]) - 1):
                o_fd.write(list[i + (list1[s])])
                if i + (list1[s]) + 1 == list1[s + 1]:
                    break

            o_fd.close()
            s += 1
            k -= 1
        handle_data(time_list)
        runmain(time_list)

def handle_data(time_list):
    for f in range(len(time_list)):
        file = glob.glob(".\\数据汇总\\%s\\YF_GPS_*.txt" %time_list[f])
        file1 = open(file[0], 'r', encoding="utf-8")
        list = file1.readlines()
        list1 = []
        for k in range(len(list)):
            if len(list[k].split())==11:
                    list1.append(list[k])

        path = file[0].split(".")[1].split("\\")[2]
        file2 = open("./数据汇总/%s/原始数据_%s.txt" % (time_list[f],path), 'w', encoding="utf-8")
        file2.writelines(list1)

def rm_file():
    if os.path.exists('数据汇总'):
        shutil.rmtree('数据汇总')
        os.mkdir('数据汇总')
    else:
        os.mkdir('数据汇总')

def run_exe():
    os.system(os.path.join(os.getcwd(), "main.exe zsPark_iOS"))
def run_exe_rx(file):
    os.system(os.path.join(os.getcwd(), "main_rx.exe %s" %file))


def runmain(time_list):
    file=[]
    for f in range(len(time_list)):
        file1 = glob.glob(".\\数据汇总\\%s\\原始数据_YF_GPS_*.txt" % time_list[f])
        file.append(file1[0])
    while True:
        print("""请输入你需要执行的功能选项：
        1、原始数据>原始轨迹kml
        2、原始数据>星值百分比分布、TTFF时间
        3、原始+百分比+绕旋程序
        4、原始+百分比+樊笼程序
        5、原始+百分比+绕旋程序+樊笼程序
            按q退出执行！！！
        """)
        int_input = str(input())
        if int_input == '1':

            for i in range(len(file)):
                path = file[i].split("原始数据_")[1].split(".")[0]
                gps_data = gps_ori_data(file[i])
                read_data(gps_data, "gps_ori_data.kml","./数据汇总/%s/gps_ori_data_%s.kml" %(path,path))
            print("执行完毕。\n")

        elif int_input == '4':
            for i in range(len(file)):
                path = file[i].split("原始数据_")[1].split(".")[0]
                excel_write(file[i], path)
                # choice_print(file[i],path,file[i])
                time_gps(file[i], path)

                gps_data1 = gps_ori_data(file[i])
                read_data(gps_data1, "gps_ori_data.kml", "./数据汇总/%s/gps_ori_data_%s.kml" % (path, path))

                park_ios(file[i])
                run_exe()
                gps_data = gps_handle_data()
                read_data(gps_data, "gps_handle_data.kml", "./数据汇总/%s/gps_handle_data_%s.kml" % (path, path))
            print("执行完毕。\n")

        elif int_input == '3':
            for i in range(len(file)):
                path = file[i].split("原始数据_")[1].split(".")[0]
                excel_write(file[i], path)
                # choice_print(file[i],path,file[i])
                time_gps(file[i], path)
                gps_data1 = gps_ori_data(file[i])
                read_data(gps_data1, "gps_ori_data.kml", "./数据汇总/%s/gps_ori_data_%s.kml" % (path, path))

                file11= open(file[i])
                list=file11.readlines()
                file12=open("zsPark_iOS.txt","w",encoding="utf-8")
                file12.writelines(list)
                file12.close()
                run_exe_rx("zsPark_iOS.txt")
                gps_data = gps_ori_data("journey_filted.txt")
                read_data(gps_data, "gps_handle_rx_data.kml", "./数据汇总/%s/gps_handle_rx_data_%s.kml" % (path, path))
            print("执行完毕。\n")

        elif int_input == '2':
            for i in range(len(file)):
                path = file[i].split("原始数据_")[1].split(".")[0]
                excel_write(file[i],path)
                #choice_print(file[i],path,file[i])
                time_gps(file[i],path)
            print("---数据处理完毕！---\n")

        elif int_input == '5':
            for i in range(len(file)):
                path = file[i].split("原始数据_")[1].split(".")[0]

                excel_write(file[i], path)
                # choice_print(file[i],path,file[i])
                time_gps(file[i], path)

                gps_data = gps_ori_data(file[i])
                read_data(gps_data, "gps_ori_data.kml", "./数据汇总/%s/gps_ori_data_%s.kml" % (path, path))

                park_ios(file[i])
                run_exe()
                gps_data = gps_handle_data()
                read_data(gps_data, "gps_handle_data.kml", "./数据汇总/%s/gps_handle_data_%s.kml" % (path, path))
                excel_write(file[i], path)
                choice_print(file[i], path, file[i])
                time_gps(file[i], path)

                file111 = open(file[i])
                list = file111.readlines()
                file121 = open("zsPark_iOS.txt", "w", encoding="utf-8")
                file121.writelines(list)
                file121.close()
                run_exe_rx("zsPark_iOS.txt")
                gps_data = gps_ori_data("journey_filted.txt")
                read_data(gps_data, "gps_handle_rx_data.kml", "./数据汇总/%s/gps_handle_rx_data_%s.kml" % (path, path))
                print(path)
            print("---数据处理完毕！---\n")
        elif int_input.lower() == 'q':
            break
        else:
            print("---输入选项有误，请重新输入---\n")
            continue


if __name__ == "__main__":
    rm_file()
    get_data()


