from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'


def Count_pv_uv():
    #统计网站总访问量PV
    pv = map_rdd.count()

    #统计网站独立访客数
    uv = map_rdd.map(lambda list: list[0]).distinct().count()

    print(f"网站的总访问量pv为:{pv}次,独立访客数为:{uv}人 ")


def Url_method():
    # 统计请求的URI路径的TOP10
    url_rdd = map_rdd.map(lambda list: (list[6], 1))
    result = url_rdd.reduceByKey(lambda agg, cur: agg + cur)
    url_list = result.top(10, lambda tup: tup[1])
    print(url_list)


if __name__ == '__main__':
    # 1- 创建spark顶级对象
    conf = SparkConf().setAppName('day03点击流日志分析案例').setMaster("yarn")
    sc = SparkContext(conf=conf)

    # 2- 读取数据
    file_rdd = sc.textFile("hdfs://node1:8020/data/access.log")

    # 3- 数据处理
    #去除首尾空格与去除空行
    file_tmp_rdd = file_rdd.map(lambda line:line.strip(''))

    map_rdd = file_tmp_rdd.map(lambda list:list.split(' ')).filter(lambda list:len(list) >= 12)

    #统计网站总PV和UV
    Count_pv_uv()

    Url_method()