from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    """
    1、创建spark顶级对象/创建spark运行环境
    2、数据读取
    3、数据处理
    4、数据输出
    5、释放资源
    """

#1、创建spark顶级对象/创建spark运行环境
conf = SparkConf().setAppName('wordcount').setMaster('local[*]')
sc = SparkContext(conf=conf)

#2、数据读取
init_RDD = sc.textFile('file:///export/data/pyspark_code/day01/data/content.txt')

#3、数据处理
flatMap_RDD = init_RDD.flatMap(lambda line:line.split(' '))

map_RDD = flatMap_RDD.map(lambda word:(word,1))

result = map_RDD.reduceByKey(lambda agg,cuur:agg+cuur)


#4、数据输出
print(result.collect())

#5、释放资源
sc.stop()

