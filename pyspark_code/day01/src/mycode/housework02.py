from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #1- 创建spark顶级对象
    conf = SparkConf().setAppName("day02_spark作业2").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    #2- 读取数据
    init_RDD = sc.textFile("file:///export/data/pyspark_code/day02/data/users.txt")

    #3- 数据处理
    map_RDD = init_RDD.map(lambda line:list(line.split(',')))

    filter_RDD = map_RDD.filter(lambda list:list[1]!='' and list[2]!='')

    tuple_RDD = filter_RDD.map(lambda list:(list[2],1))

    reduceBykey_RDD =tuple_RDD.reduceByKey(lambda agg,curr:agg+curr)

    result = reduceBykey_RDD.sortBy(lambda tup:tup[1],ascending=False)


    #4- 数据输出

    print(result.collect())
    #5- 释放资源
    sc.stop()
