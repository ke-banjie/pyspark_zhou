from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'


if __name__ == '__main__':
    conf = SparkConf().setAppName('并行化本地集合').setMaster('local[2]')
    sc = SparkContext(conf=conf)

    init_rdd = sc.parallelize([0,1,2,3,4,5],numSlices=3)
    # 3- 数据处理
    # 查看RDD的分区数有多少个
    print(init_rdd.getNumPartitions())

    # 查看每个分区的具体内容
    print(init_rdd.glom().collect())

    # 4- 数据输出
    # print(init_rdd.collect())

    # 5- 释放资源
    sc.stop()