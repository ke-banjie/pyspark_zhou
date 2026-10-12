from pyspark import SparkContext, SparkConf
import os

from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #1- 创建sparkSQL顶级对象
    spark = SparkSession.builder\
        .appName("读txt文件")\
        .master('local[*]')\
        .getOrCreate()

    #读取txt文件
    init_dataframe = spark.read\
        .schema("myvalue string")\
        .text(paths="file:///export/data/pyspark_code/day05/data/stu.txt")

    init_dataframe.show()
    init_dataframe.printSchema()

    #释放资源
    spark.stop()