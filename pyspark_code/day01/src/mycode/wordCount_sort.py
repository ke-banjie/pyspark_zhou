from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    # 1、创建Spark顶级对象
    conf = SparkConf().setAppName('词频统计').setMaster('local[*]')
    sc = SparkContext(conf=conf)

    # 2、数据读取
    init_RDD = sc.textFile('file:///export/data/pyspark_code/day01/data/content.txt')
    # 3、处理数据
    # 3_1 文本内容切分flatMap
    flatMap_RDD = init_RDD.flatMap(lambda line:line.split(' '))
    # 3_2 数据格式转换map
    map_RDD = flatMap_RDD.map(lambda word:(word,1))
    # 3_3 分组聚合reduceBykey
    reducebykey_RDD = map_RDD.reduceByKey(lambda agg,curr:agg+curr)


    """
    排序方式
    1、sortByKey:默认升序排序，返回值是一个新的RDD
    2、
    """
    #1- sortByKey

    # result = reducebykey_RDD.map(lambda word.txt:(word.txt[1],word.txt[0]))\
    #     .sortByKey(ascending=False)\
    #     .map(lambda word.txt:(word.txt[1],word.txt[0]))\
    #     .collect()

    #2- sortBY
    # result = reducebykey_RDD.sortBy(lambda info:info[1], ascending=False).collect()

    # 3- top
    result = reducebykey_RDD.top(3,lambda info:info[1])

    # 4、输出数据
    print(result)
    # 5、释放资源
    sc.stop()
