from pyspark import SparkConf, SparkContext
import os
import jieba
# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'


def etl(init_rdd):
    """
        为什么这里不能使用flatMap?
        因为要对每行的字段个数是否有6个进行判断，所以要将每行的内容都分别切分得到一个新的列表
    """
    # flatmap_rdd = init_rdd.flatMap(lambda line: line.split())
    map_rdd = init_rdd.map(lambda line: line.split())
    # 脏数据过滤：过滤掉字段个数不等于6的
    filter_rdd = map_rdd.filter(lambda line_list: len(line_list) == 6)

    return filter_rdd


if __name__ == '__main__':
    # 1- 创建顶级对象
    conf = SparkConf().setAppName('sogou').setMaster('local[*]')
    sc = SparkContext(conf=conf)

    # 2- 数据输入
    init_rdd = sc.textFile('file:////export/data/pyspark_code/day04/data/SogouQ.sample')

    # 3- 数据处理
    # 3.1- ETL
    print(init_rdd.count())
    filter_rdd = etl(init_rdd)
    print(filter_rdd.take(10))
    print(filter_rdd.count())
    # 5- 释放资源
    sc.stop()