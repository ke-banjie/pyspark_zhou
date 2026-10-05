from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #2、创建spark顶级对象/创建spark运行环境
    conf = SparkConf().setAppName('housework_02').setMaster('local[*]')
    sc = SparkContext(conf = conf)

    #2、数据读取
    init_RDD = sc.textFile('hdfs://node1:8020/data/data.txt')

    #3、数据处理
    flatmap_RDD = init_RDD.flatMap(lambda line:line.split(' '))


    #方式一、split切分得到姓名地址列表，再使用数据类型转换成元组
    # map_RDD = flatmap_RDD.map(lambda info:tuple(info.split('-')))

    #方式二、使用split函数切分得到的列表元素创建新的元组
    map_RDD = flatmap_RDD.map(lambda info:(info.split('-')[0],info.split('-')[1]))

    #4、数据输出,将数据保存到HDFS
    map_RDD.saveAsTextFile('hdfs://node1:8020/housework/day01/housework_02')
    print(map_RDD.collect())


    #5、资源释放
    sc.stop()