from pyspark.sql import SparkSession
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'
if __name__ == '__main__':
    # 1- 创建SparkSession对象
    spark = SparkSession.builder\
             .appName('text方式读取外部文件')\
             .master('local[*]')\
             .getOrCreate()

    # 2- 数据输入
    # init_df = spark.read\
    #            .schema("id string,name string,address string,sex string,age string")\
    #            .text(paths='file:///export/data/gz19_pyspark/day05/data/stu.txt')

    """
        text方式读取总结
            1- text方式会将文件的所有内容当成一个字段进行处理
            2- 会产生一个默认的字段，叫做value，字段类型是string
            3- 如果想自定义schema信息，只能改value的字段名称
    """
    init_df1 = spark.read \
        .text(paths='file:///export/data/pyspark_code/day05/data/stu.txt')

    init_df2 = spark.read \
        .schema("myvalue string") \
        .text(paths='file:///export/data/pyspark_code/day05/data/stu.txt')

    # 3- 数据输出
    init_df1.show()
    init_df1.printSchema()

    print("-"*30)

    init_df2.show()
    init_df2.printSchema()

    # 4- 释放资源
    spark.stop()