from pyspark import SparkContext, SparkConf
import os

from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'


if __name__ == '__main__':
    #1-创建spark顶级对象
    spark = SparkSession.builder\
        .appName("点击最多的10个网站域名")\
        .getOrCreate()

    sc = spark.sparkContext

    #2-数据读取
    init_df = sc.textFile('file:///export/data/pyspark_code/day04/data/SogouQ.sample')

    #3-数据处理
    #---ETL
    map_rdd = init_df.map(lambda line:line.split())
    print(map_rdd.count())
    ETL_rdd = map_rdd.filter(lambda line_list:len(line_list)==6)
    print(ETL_rdd.count())


    #释放资源
    sc.stop()
