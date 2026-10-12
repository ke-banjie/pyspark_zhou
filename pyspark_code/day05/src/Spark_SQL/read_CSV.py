import os

from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #创建sparkSQL顶级对象
    spark = SparkSession.builder\
        .appName("读CSV文件")\
        .master("local[*]")\
        .getOrCreate()

    #使用CSV方式读文件
    # init_dataframe = spark.read.csv(
    #     path="file:///export/data/pyspark_code/day05/data/stu.txt",
    #     schema="id int, name string, address string, sex string, age int",
    #     sep=' ',
    #     encoding='UTF-8',
    #     header=True
    # )

    #复杂API
    init_dataframe = spark.read.format('csv')\
        .option('encoding', 'UTF-8')\
        .option('sep', ' ')\
        .option('header', "True")\
        .schema('id int, name string, address string, sex string, age int')\
        .load('file:///export/data/pyspark_code/day05/data/stu.txt')
    #输出数据
    init_dataframe.show()
    init_dataframe.printSchema()

    #释放资源
    spark.stop()