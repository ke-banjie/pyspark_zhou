import os

from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    # 1- 创建SparkSQL顶级对象
    spark = SparkSession.builder\
        .appName("写文件")\
        .master("local[*]")\
        .getOrCreate()

    # 2- 读文件
    init_df = spark.read.csv(
        path="file:///export/data/pyspark_code/day06/data/clear_data.csv",
        sep=',',
        encoding='utf-8',
        header=True
    )

    #删除缺失值
    mid_df = init_df.dropna(thresh=2,subset=['age', 'address'])

    # 3- 数据处理
    result_df = mid_df.where("name = '张三'")

    result_df.show()

    # 4- 写操作
    result_df.write.csv(
        path="hdfs://node1:8020/input",
        mode='append',
        sep=',',
        header=True
    )

    # 5- 释放资源
    spark.stop()

