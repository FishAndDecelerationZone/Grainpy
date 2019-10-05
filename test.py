

import re

from Grainpy.extractor import Base
from Grainpy.draw import *
from Grainpy.analysis import *

def combine_test():
    """
    测试base
    :return:
    """
    base1 = Base('127.0.0.2', 'root', '2333333', 'barn', 3306)
    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)

    barns1_times = base1.get_tables_name()
    new_table = base1.new_barn(barns1_times)
    base1.combine(barns1_times, new_table, base2)


def draw_test():
    """
    测试绘制时间序列温度散点图
    :return:
    """
    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    barn_name = '上河湾分库_1号罩棚'
    barn_name, time, temperature = base2.point_times_temperate(barn_name, 1, 1, 1)
    draw1(barn_name, time, temperature)


def person_test():
    """
    测试o氏距离和pearson相关度
    :return:
    """
    p = [1,34,56,24,56,4,5,6,4,575,467,568,41,89]
    q = [1,34,56,24,56,4,5,6,4,575,467,568,41,89]
    r = pearson(p,q)

    v1 = [[2,4,5], [3,4,5], [7,3,2]]
    v2 = [[2,4,5], [3,4,5], [7,3,2]]
    r2 = euclidean(v1, v2)
    print(r2)

    print(r)


def  relevance(barn, point):
    """
    分析该点和周围各点的相关性
    :param barn: 粮仓数据 四维列表   行列层+测量温度的时间序列
    :param point: 点坐标 （r, c, l)
    :return:
    """
    r, c, l = point[0]-1, point[1]-1, point[2]-1    # r,c,l 为粮仓坐标而非索引

    barn = np.array(barn, dtype=np.float)
    (rmax,  cmax, lmax, count) = barn.shape

    if r < rmax:  #r+1
        p_r1 = pearson(barn[r][c][l], barn[r+1][c][l])
        e_r1 = euclidean(barn[r][c][l], barn[r+1][c][l])
        print("r+1  点皮尔逊相关系数矩阵：\n", p_r1)
        print("r+1  点欧式距离：", e_r1, '\n')

    if r > 0:       #r-1
        p_r2 = pearson(barn[r][c][l], barn[r-1][c][l])
        e_r2 = euclidean(barn[r][c][l], barn[r-1][c][l])
        print("r-1  点皮尔逊相关系数矩阵：\n", p_r2)
        print("r-1  点欧式距离：", e_r2, '\n')

    if l < lmax:  #l+1
        p_l1 = pearson(barn[r][c][l], barn[r][c][l+1])
        e_l1 = euclidean(barn[r][c][l],  barn[r][c][l+1])
        print("l+1  点皮尔逊相关系数矩阵：\n", p_l1)
        print("l+1  点欧式距离：", e_l1, '\n')

    if l > 0:       #l-1
        p_l2 = pearson(barn[r][c][l], barn[r ][c][l- 1])
        e_l2 = euclidean(barn[r][c][l], barn[r ][c][l- 1])
        print("l-1  点皮尔逊相关系数矩阵：\n", p_l2)
        print("l-1  点欧式距离：", e_l2, '\n')

    if c < lmax:  #c+1
        p_c1 = pearson(barn[r][c][l], barn[r][c+1][l])
        e_c1 = euclidean(barn[r][c][l], barn[r][c+1][l])
        print("c+1  点皮尔逊相关系数矩阵：\n", p_c1)
        print("c+1  点欧式距离：", e_c1, '\n')

    if c > 0:       #c-1
        p_c2 = pearson(barn[r][c][l], barn[r ][c-1][l])
        e_c2 = euclidean(barn[r][c][l], barn[r ][c-1][l])
        print("c-1  点皮尔逊相关系数矩阵：\n", p_c2)
        print("c-1  点欧式距离：", e_c2, '\n')


def barn_times_relate():
    """
    测量点于周围点相关性分析
    :return:
    """
    barn_name = '上河湾分库_2号库'
    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    barn = base2.barn_times_temperate(barn_name)
    #print(barn)
    point = (2, 3, 2)
    print(point)
    relevance(barn, point)


def barn_slices_test():
    """
    三维粮仓切片测试  (barn[层， 列， 行]
    行为列索引取值， 列是行索引取值， 层为层索引取值
    :return:
    """
    time = "2019_01_31_10_08_33"
    barn_name = '上河湾分库_1号罩棚'
    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    barn = base2.barn_temperate(barn_name, time=time)
    print(type(barn))
    print(barn)
    print("第一层14x6： \n", barn[0, :, :])
    print("第一行3x6： \n", barn[:, 0, :])
    print("第一列3x14： \n", barn[:, :, 0])


def barn_slices_test2():
    """
    三维粮仓切片测试  (barn[列， 行， 层]
    行为列索引取值， 列是行索引取值， 层为层索引取值
    :return:
    """
    time = "2019_01_31_10_08_33"
    barn_name = '上河湾分库_1号罩棚'
    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    barn = base2.barn_temperate2(barn_name, time=time)
    print(type(barn))
    print(barn)
    print("第一行 行x层： \n", barn[0, :, :])
    print("第一列 列x层： \n", barn[:, 0, :])
    print("第一层 列x行： \n", barn[:, :, 0])


def barn_times_slices_test():
    """
    时间序列粮仓温度切片测试    barn[列， 行， 层]
    行为列索引取值， 列是行索引取值， 层为层索引取值
    :return:
    """
    time = "2019_01_31_10_08_33"
    barn_name = '上河湾分库_1号罩棚'
    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    barn = base2.barn_times_temperate2(barn_name)
    print(type(barn), np.shape(barn))
    print(barn)
    print("第一行 行x层： \n", barn[0, :, :])
    print("第一列 列x层： \n", barn[:, 0, :])
    print("第一层 列x行： \n", barn[:, :, 0])



def layer_times_mean_chart(layers):
    """
    层均温时间序列走势图
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)      #时间序列
    lengend = []
    for layer in range(layers) :
        lengend.append('第{}层'.format(layer+1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.mean(layer_tem)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}均温走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()



def layer_times_max_chart(layers):
    """
    层最大温度时间序列走势图
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列
    lengend = []
    for layer in range(layers):
        lengend.append('第{}层'.format(layer + 1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.max(layer_tem)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}最高温度走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()


def layer_times_min_chart(layers=3):
    """
    层最小温度时间序列走势图
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列
    lengend = []
    for layer in range(layers):
        lengend.append('第{}层'.format(layer + 1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.min(layer_tem)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}最低温走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()

def layer_times_ptp_chart(layers):
    """
    层最高最低温度差值走势图
    :param layers:
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列
    lengend = []
    for layer in range(layers):
        lengend.append('第{}层'.format(layer + 1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.ptp(layer_tem)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}最高最低温度差值走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()


def layer_times_std_chart(layers):
    """
    层标准差走势图
    :param layers:
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列
    lengend = []
    for layer in range(layers):
        lengend.append('第{}层'.format(layer + 1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.std(layer_tem)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}层间标准差走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()


def layer_times_median_chart(layers):
    """
    层标准差走势图
    :param layers:
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列
    lengend = []
    for layer in range(layers):
        lengend.append('第{}层'.format(layer + 1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.median(layer_tem)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}层间中位数数走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()



def layer_times_75_chart(layers):
    """
    层标准差走势图
    :param layers:
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列
    lengend = []
    for layer in range(layers):
        lengend.append('第{}层'.format(layer + 1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.percentile(layer_tem, 75)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}75%百分位数走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()



def layer_times_25_chart(layers):
    """
    层标准差走势图
    :param layers:
    :return:
    """
    plt.figure(figsize=(15, 10))
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列
    lengend = []
    for layer in range(layers):
        lengend.append('第{}层'.format(layer + 1))
        layer_times = base2.barn_times_layer(barn_name, layer=layer)
        # print(np.shape(layer_times))
        means = []
        for time in range(0, len(times)):
            layer_tem = layer_times[time, :, :]
            mean = np.percentile(layer_tem, 25)
            # print(time,"均值：", mean)
            means.append(mean)
        print(means)

        plt.plot(range(len(means)), means, linestyle='--', marker='v')

    # 绘制
    # title = "{}{}层均温走势图".format(barn_name, layer)
    # point_line_chart(title=title, times=times, temperature=means)
    plt.legend(lengend)
    plt.xlabel('时间')
    plt.ylabel('温度')
    plt.xticks(range(len(times)), times, rotation=45)
    title = "{}25%百分位数走势图".format(barn_name)
    plt.title(title)
    plt.savefig('G:/Python/Laboratory/Grainpy/chart/{}.png'.format(title))
    plt.show()



def barn_std():
    """
    整仓某一测量时间标准差
    :return:
    """
    time = "2019_01_31_10_08_33"
    barn_name = '上河湾分库_1号罩棚'
    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    barn = base2.barn_temperate2(barn_name, time=time)
    print("{}{}整仓标准差:".format(barn_name, time),np.std(barn))



    #假设半仓
    barn[:,:, 0:1] = barn[:,:, 1:2]
    a = np.random.rand(14, 6)
    barn[:,:,2] = a

    print("{}{}1/3空仓标准差".format(barn_name, time),np.std(barn))



def layer_relate( layer1, layer2):
    """
    两层均温相关度分析
    :return:
    """
    barn_name = '上河湾分库_1号罩棚'

    base2 = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    times = base2.get_times(barn_name)  # 时间序列

    layer1_times= base2.barn_times_layer(barn_name, layer=layer1)
    layer2_times = base2.barn_times_layer(barn_name, layer=layer2)
    means1 = []
    means2 = []
    for time in range(0, len(times)):
        layer1_tem = layer1_times[time, :, :]
        mean1 = np.mean(layer1_tem)
        means1.append(mean1)

        layer2_tem = layer2_times[time, :, :]
        mean2 = np.mean(layer2_tem)
        means2.append(mean2)

    pear = pearson(means1, means2)
    eucl = euclidean(means1, means2)

    print("\n{}{}层与{}层pearson相关系数:\n ".format(barn_name, layer1,  layer2),  pear)
    print("\n{}{}层与{}层euclidean系数: ".format(barn_name, layer1, layer2), eucl)




if __name__ == '__main__':
    #ss()
    #combine_test()
    #draw_test()
    #person_test()

    #barn_slices_test2()
   # barn_times_slices_test()

    # layer_times_75_chart(3)
    # layer_times_25_chart(3)
    # layer_times_ptp_chart(3)
    # layer_times_median_chart(3)
    # layer_times_std_chart(3)
    # layer_times_mean_chart(3)
    # layer_times_max_chart(3)
    # layer_times_min_chart(3)

    #barn_std()

    layer_relate(1,3)


