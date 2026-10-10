from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #创建spark顶级对象
    conf = SparkConf().setAppName("day02pyspark作业1").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    #读取数据
    init_RDD = sc.textFile("file:///export/data/pyspark_code/day02/data/word.txt")

    #数据处理
    flatmap_RDD =init_RDD.flatMap(lambda line:line.split(' '))

    #过滤hive
    filter_RDD = flatmap_RDD.filter(lambda word:word!='hive')

    map_RDD = filter_RDD.map(lambda word:(word,1))

    result = map_RDD.reduceByKey(lambda agg,curr:agg+curr)


    #数据输出
    print(result.top(5, lambda word:-word[1]))

    #统计有多少个不同的单词
    print(result.count()+1)
    print(result.collect())

    #释放资源
    sc.stop()

