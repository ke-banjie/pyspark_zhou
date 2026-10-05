from pyspark import SparkContext, SparkConf
import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    spark = SparkSession.builder \
        .appName('RDD1') \
        .master('local[*]') \
        .getOrCreate()

    sc = spark.sparkContext

    #数据输入
    init_rdd = sc.parallelize(['1 赵云 18','2 李白 20'])

    new_rdd = init_rdd.map(lambda line:line.split())\
        .map(lambda tmp_list:[int(tmp_list[0]), tmp_list[1], int(tmp_list[2])])

    print(new_rdd.collect())

    # #方式一
    # schema_1 = StructType([
    #     StructField("userid", IntegerType(), True),
    #     StructField("name",StringType(), True),
    #     StructField("age",IntegerType(), True)

    # #方式二
    # schema_2 = StructType()\
    # .add("userid", IntegerType(), True)\
    # .add("name", StringType(), True)\
    # .add("age", IntegerType(), True)

    #方式三
    # schema_3 = "user_id int, name string, age int"

    #方式四
    schema_4 = ['userid', 'name', 'age']

    init_df = new_rdd.toDF(schema_4)

    init_df.show()
    init_df.printSchema()

    spark.stop()