from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #1- 创建spark顶级对象
    conf = SparkConf().setAppName("housework01").setMaster("yarn")
    sc = SparkContext(conf=conf)

    #2- 读取数据
    init_RDD = sc.textFile("hdfs://node1:8020/data/data.txt")

    #3- 处理数据
    flatmap_RDD = init_RDD.flatMap(lambda line:line.split(' '))
    map_RDD = flatmap_RDD.map(lambda adress:tuple(adress.split('-')))


    #4- 输出数据
    print(map_RDD.collect())
    #5- 释放资源
    sc.stop()