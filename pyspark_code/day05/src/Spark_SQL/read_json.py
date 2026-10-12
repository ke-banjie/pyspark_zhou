from pyspark.sql import SparkSession
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'
if __name__ == '__main__':
    # 1- 创建SparkSession
    spark = SparkSession.builder.appName('json方式').master('local[*]').getOrCreate()

    # 2- 数据输入
    """
        json格式读取总结
            1- 如果json串中没有对应的字段，那么以null值填充
            2- 如果json中的key名称与schema中的字段名称没有对应上，那么以null值填充
            3- 如果不指定schema，那么会自动的解析json串内容，key解析为字段名，value解析字段值
    """
    # init_df = spark.read.json(
    #     path="file:///export/data/gz19_pyspark/day05/data/json.txt",
    #     schema="id int,name string,age int,address string",
    #     encoding="UTF-8"
    # )

    # init_df = spark.read.json(
    #     path="file:///export/data/gz19_pyspark/day05/data/json.txt",
    #     schema="id111 int,name string,age int,address string",
    #     encoding="UTF-8"
    # )

    init_df = spark.read.json(
        path="file:///export/data/pyspark_code/day05/data/json.txt",
        encoding="UTF-8"
    )

    # 3- 数据输出
    init_df.show()
    init_df.printSchema()

    # 4- 释放资源
    spark.stop()