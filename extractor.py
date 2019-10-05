
import re
import pymysql
import pandas
import numpy as np


class Base:
    """
    数据库操作类
    """

    def __init__(self, MYSQL_HOST, MYSQL_USER, PASSWORD, DATABASE_NAME, MYSQL_PORT):
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.password = PASSWORD
        self.db = DATABASE_NAME
        self.port = MYSQL_PORT

        self.GetConnect()



    def GetConnect(self):
        """
        连接数据库
        :return:
        """
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db= self.db)
            self.cursor = self.conn.cursor()
        except Exception as err:
            self.conn = None
            self.cursor = None
            print("数据库连接失败!" , err)



    def Close(self):
        """
        关闭数据库连接
        :return:
        """

        if self.conn:
            try:
                if(type(self.cursor) == 'object'):
                    self.cursor.close()
                if type(self.conn) == 'object':
                    self.conn.close()
            except Exception as err:
                raise("数据库关闭失败，", err)



    def Insertmany(self, table_name,data):
        """
        批量插入数据
        :param data:
        :return:
        """
        print(data)
        sql = "insert into `{}`(`barn_id`, `barn_name`, `time`, `row`, `layer`, `column`, `temperature`) VALUES (%s, %s, %s, %s, %s, %s, %s);".format(pymysql.escape_string(table_name))
        try:
            self.cursor.executemany(sql, data)
            self.conn.commit()
            print("入库成功！")
        except Exception as err:
            #有异常，回滚事务
            self.conn.rollback()


    def combine(self, tables, new_table_names, base):
        """
        mysql 多表合并
        :param tables:  需要合并的tables名称列表
        :param base: 新表存储位置
        :param table_name: 合并表命
        :return:
        """
        newdb_name = base.db

        for new_table_name  in new_table_names:
            #创建总表
            self.creat_table(newdb_name, new_table_name)
            for table in tables:
                if new_table_name in table:
                    #插入表
                    self.insert_to_new_table(newdb_name, new_table_name, table)


    def get_tables_name(self):
        """
        获取所有仓库名
        :return:
        """
        sql = "show tables"

        self.cursor.execute(sql)
        tables = self.cursor.fetchall()

        tables_name = []
        for table in tables:
            tables_name.append(table[0])

        return tables_name


    def new_barn(self, barn_times):
        """
        正则表达式提取仓库名
        :param barn_times:[[上河湾分库_2号库_2019_04_03_09_18_34]...]
        :return:
        """

        p = '(.*?)_\d{4}'

        barns = []
        for table_name in barn_times:
            #print(table_name)
            barns.append( re.match(p, table_name).group(1))

        print("仓库：",set(barns))
        return set(barns)



    def creat_table(self, db, table_name):
        """
        创建一个数据表
        :param db:数据库名
        :param table_name:
        :return:
        """

        try:
            creat = '''
                    CREATE TABLE {}.`{}` (
                      `barn_id` varchar(254) CHARACTER SET UTF8MB3 COLLATE utf8_unicode_ci NOT NULL,
                      `barn_name` varchar(254) CHARACTER SET UTF8MB3 COLLATE utf8_unicode_ci NOT NULL,
                      `time` varchar(255) CHARACTER SET UTF8MB3 COLLATE utf8_unicode_ci NOT NULL,
                      `row` int(225) NOT NULL,
                      `layer` int(225) NOT NULL,
                      `column` int(225) DEFAULT NULL,
                      `temperature` double(225,2) DEFAULT NULL
                    )
                    '''.format(db, table_name)

            sql = 'DROP TABLE IF EXISTS {}.`{}` '.format(db, table_name)
            self.cursor.execute(sql)  # 之前创建则删除
            self.cursor.execute(creat)
            # 提交对表的修改
            self.conn.commit()
        except Exception as err:
            self.conn.roollback()
            print(err.args)


    def insert_to_new_table(self, db, new_table, table):
        """
        插入数据到新表格中
        :param db: 插入的数据库
        :param new_table: 新表名
        :param table: 表名
        :return:
        """
        try:
            sql = 'INSERT INTO {}.`{}` SELECT * FROM `{}` '.format(db, new_table, table)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print("插入失败", err.args)
            self.conn.rollback()

    def get_times(self,barn_name):
        """
        某仓的测量时间序列
        :param barn_name:
        :return:
        """
        try:
            sql = "select  distinct `time` from `{}`".format(barn_name)
            formlist = pandas.read_sql(sql, con=self.conn)
            formlist.sort_values('time', inplace = True)        #按日期排序
            time = formlist['time'].values

            return time

        except Exception as err:
            print(barn_name, "点搜索失败", err.args)


    def point_times_temperate(self, barn_name, row, column, layer):
        """
        获取某点的温度（时间序列）
        :return:
        """
        try:
            sql = "select  `time`, `temperature` from `{}` where `row` = {} and `layer`= {} and `column`= {}".format(barn_name, row, layer, column)
            formlist = pandas.read_sql(sql, con=self.conn)
            formlist.sort_values('time', inplace = True)        #按日期排序
            #print(formlist)
            time = formlist['time'].values
            temperature = formlist['temperature'].values
            return barn_name, time, temperature

        except Exception as err:
            print(barn_name, '\t', row, '\t',column, '\t',layer,"点搜索失败", err.args)


    def point_temperate(self, barn_name, time, row, column, layer):
        """
        获取测量点某个时间的温度
        :return:
        """
        try:
            sql = "select  `temperature` from `{}` where `row` = {} and `layer`= {} and `column`= {} and  `time`='{}'".format(barn_name, row, layer, column, time)
            formlist = pandas.read_sql(sql, con=self.conn)
            #print(formlist)

            temperature = formlist['temperature'].values
            return temperature

        except Exception as err:
            print(barn_name, '\t', row, '\t',column, '\t',layer,"点搜索失败", err.args)


    def barn_times_temperate(self, barn_name):
        """
        生成粮仓 温度时间序列
        索引顺序（行，列，层）  用于单点索引
        :param barn_name:
        :return:
        print("第一层14x6： \n", barn[0, :, :])
        print("第一行3x6： \n", barn[:, 0, :])
        print("第一列3x14： \n", barn[:, :, 0])
        """
        sql = 'select `row`, `column`, `layer` from {}'.format(barn_name)
        formlist = pandas.read_sql(sql, con= self.conn)
        #print(formlist)
        r_max, c_max, l_max = np.max(formlist)
        print("粮仓结构:\t", r_max,"行\t", c_max,"列\t", l_max, "层")
        barn = []
        for row in range(1, r_max+1):
            columns = []
            for column in range(1, c_max +1):
                layers = []
                for layer in range(1, l_max+1):
                    barn_name, time, temperature = self.point_times_temperate(barn_name, row, column, layer)
                    layers.append(list(temperature))

                columns.append(layers)
            barn.append(columns)

        barn = np.array(barn)
        return barn


    def barn_times_temperate2(self, barn_name):
        """
        生成粮仓 温度时间序列
        索引顺序（列，行，层） 用于测量面切片索引
        :param barn_name:
        :return:
        print("第一行 行x层： \n", barn[0, :, :])
        print("第一列 列x层： \n", barn[:, 0, :])
        print("第一层 列x行： \n", barn[:, :, 0])
        """
        sql = 'select `row`, `column`, `layer` from {}'.format(barn_name)
        formlist = pandas.read_sql(sql, con= self.conn)
        #print(formlist)
        r_max, c_max, l_max = np.max(formlist)
        print("粮仓结构:\t", r_max,"行\t", c_max,"列\t", l_max, "层")
        barn = []
        for column in range(1, c_max+1):
            rows = []
            for row in range(1, r_max +1):
                layers = []
                for layer in range(1, l_max+1):
                    barn_name, time, temperature = self.point_times_temperate(barn_name, row, column, layer)
                    layers.append(list(temperature))

                rows.append(layers)
            barn.append(rows)

        barn = np.array(barn)
        return barn

    def barn_temperate(self, barn_name, time):
        """
        生成粮仓某一测量时刻  四维数据
        索引顺序(行，列， 层)  用于单点温度索引
        :param barn_name:
        :return:
        print("第一层14x6： \n", barn[0, :, :])
        print("第一行3x6： \n", barn[:, 0, :])
        print("第一列3x14： \n", barn[:, :, 0])
        """
        sql = "select `row`, `column`, `layer` from {} where `time`='{}'".format(barn_name, time)
        formlist = pandas.read_sql(sql, con= self.conn)
        #print(formlist)
        r_max, c_max, l_max = np.max(formlist)
        print("粮仓结构:\t", l_max,"行\t", c_max,"列\t", r_max, "层")
        barn = []
        for layer in range(1, l_max+1):
            columns = []
            for column in range(1, c_max +1):
                rows = []
                for row in range(1, r_max+1):
                    temperature = self.point_temperate(barn_name=barn_name, time=time, row=row, column=column, layer=layer)
                    #print("索引：",row, column, layer, "温度：", temperature)
                    rows.append(temperature[0])

                columns.append(rows)
            barn.append(columns)

        barn = np.array(barn)
        return barn



    def barn_temperate2(self, barn_name, time):
        """
        生成粮仓某一测量时刻  四维数据
        索引顺序(列，行，层) 用于二维切片索引
        :param barn_name:
        :return:
        print("第一行 行x层： \n", barn[0, :, :])
        print("第一列 列x层： \n", barn[:, 0, :])
        print("第一层 列x行： \n", barn[:, :, 0])
        """
        sql = "select `row`, `column`, `layer` from {} where `time`='{}'".format(barn_name, time)
        formlist = pandas.read_sql(sql, con= self.conn)
        #print(formlist)
        r_max, c_max, l_max = np.max(formlist)
        print("粮仓结构:\t", r_max,"行\t", c_max,"列\t", l_max, "层")
        barn = []
        for column in range(1, c_max+1):
            rows = []
            for row in range(1, r_max +1):
                layers = []
                for layer in range(1, l_max+1):
                    temperature = self.point_temperate(barn_name=barn_name, time=time, row=row, column=column, layer=layer)
                   # print("索引：",row, column, layer, "温度：", temperature)
                    layers.append(temperature[0])

                rows.append(layers)
            barn.append(rows)

        barn = np.array(barn)
        return barn

    def num(self,table_name):
        """
        获取一个仓库内的行，层，列数
        :return:
        """
        sql = "select `row`,`column`,`layer` from `{}`".format(table_name)  # sql语句提取一个仓库内的所有行
        formlist = pandas.read_sql(sql, con = self.conn)
        # 把行层列里面的数据提取出来，存到三个空列表里
        r_max, c_max, l_max = np.max(formlist)
        return r_max, c_max, l_max


    def barn_times_layer(self, barn_name, layer):
        """
        某层粮温时间序列
        :param layer:
        :return: temp_layer  时间 x 行x列
        """
        barn = self.barn_times_temperate2(barn_name=barn_name)      #(列，行，层）
        temp_layer = barn[:, :, layer-1]

        return temp_layer.T



if __name__ == '__main__':
    a = Base('127.0.0.2', 'root', '2333333', 'barn3', 3306)
    barn_name = '上河湾分库_1号罩棚'
    layer =  1
    #barn = a.num(barn_name)
    #print(barn)

    layera_tiems = a.barn_times_layer(barn_name=barn_name, layer=layer)  #某层粮温时间序列test
    print(type(layera_tiems))
    print(np.shape(layera_tiems))
    print(layera_tiems)
