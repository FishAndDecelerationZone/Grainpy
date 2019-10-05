
import pymysql
import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


def draw1(title,time,temperature):
    """
    绘制柱状图

    :param title:
    :param time:
    :param temperature:
    :return:
    """
    #绘制画布大小s
    plt.figure(figsize=(8, 6))
    #绘制散点图
    plt.plot(range(len(temperature)),temperature, marker='o')
    #x轴标签
    plt.xlabel('时间')
    #y轴标签
    plt.ylabel('温度')
    #y轴刻度范围
    #plt.ylim((-30, 30))
    #x轴的刻度
    plt.xticks(range(len(time)), time, rotation=45)
    #图形标题
    plt.title(title)
    #保存图形
    #plt.savefig('D:/python/czpython/save_temperature.png')
    #展示
    plt.show()


def point_line_chart(title, temperature, times):
    """
    绘制点线图
    :param title:
    :param temp:
    :param times:
    :return:
    """
    plt.figure(figsize=(8,7))
    plt.plot(range(len(temperature)), temperature, color='r', linestyle='--', marker='v')
    plt.xlabel('时间')
    # y轴标签
    plt.ylabel('温度')
    # y轴刻度范围
    # plt.ylim((-30, 30))
    # x轴的刻度
    plt.xticks(range(len(times)), times, rotation=45)
    # 图形标题
    plt.title(title)
    # 保存图形
    # plt.savefig('D:/python/czpython/save_temperature.png')
    # 展示
    plt.show()