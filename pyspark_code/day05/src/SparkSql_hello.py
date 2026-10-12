from pyspark import SparkContext, SparkConf
import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    spark = SparkSession.builder\
        .appName("SparkSQl_hello")\
        .master('local[*]')\
        .getOrCreate()

    sc = spark.sparkContext

    #数据输入
    init_rdd = sc.parallelize(["1 赵云 18","2 李白 20"])

    #数据处理
    map_rdd= init_rdd.map(lambda line:line.split())

    info_rdd = map_rdd.map(lambda list:[int(list[0]), list[1], int(list[2])])

    print(info_rdd.collect())

    #定义Schema
    Schema = StructType()\
    .add("user_id", IntegerType(), True)\
    .add("name", StringType(), True)\
    .add("age", IntegerType(), True)
    # 定义Schema方式二
    # schema_2 = StructType([
    #     StructField("userid", IntegerType(), True),
    #     StructField("name", StringType(), True),
    #     StructField("age", IntegerType(), True)
    # ])

    # 定义Schema方式三
    # schema_3 = 'userid:int,name:string,age:int'

    # 了解
    # schema_3 = 'userid int,name string,age int'

    # 定义Schema方式四
    # schema_4 = ['userid', 'name', 'age']

    # init_df = spark.createDataFrame(new_rdd,schema_4)

    #RDD转DataFrame
    info_DataFrame = info_rdd.toDF(Schema)

    # init_df = spark.createDataFrame(new_rdd,schema_4)

    #输出
    info_DataFrame.show()
    info_DataFrame.printSchema()

    #释放资源
    spark.stop()