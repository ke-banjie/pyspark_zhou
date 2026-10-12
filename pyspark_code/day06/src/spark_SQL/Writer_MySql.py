import os

from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #创建SparkSQL顶级对象
    spark = SparkSession.builder\
        .appName('写数据到MySQL')\
        .master('yarn')\
        .getOrCreate()

    #读数据
    init_df = spark.read.csv(
        path="hdfs://node1:8020/data/clear_data.csv",
        schema="id int, name string, age int, address string",
        encoding='UTF-8',
        header=True,
        sep=','
    )

    init_df.show()
    init_df.printSchema()

    #写数据到mysql
    init_df.write.jdbc(
        url="jdbc:mysql://node1:3306/day06?useUnicode=true&characterEncoding=utf-8",
        table="day06_stu",
        mode="overwrite",
        properties={'user': 'root', 'password': '123456'}
    )

    #释放资源
    spark.stop()
