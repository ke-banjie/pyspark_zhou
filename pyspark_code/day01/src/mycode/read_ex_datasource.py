from pyspark import SparkConf, SparkContext
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'
if __name__ == '__main__':
    # 1- 创建顶级对象
    conf = SparkConf().setAppName('读取外部文件').setMaster('local[1]')
    sc = SparkContext(conf=conf)

    # 2- 数据输入
    """
        textFile中的minPartitions设置的是最小分区数，也就是最终实际的分区数>=minPartitions
    """
    # init_rdd = sc.textFile('file:///export/data/gz19_pyspark/day03/data/content.txt',minPartitions=3)
    # init_rdd = sc.textFile('file:///export/data/gz19_pyspark/day03/data/content.txt',minPartitions=5)
    init_rdd = sc.textFile('file:///export/data/pyspark_code/day03/data/content.txt',minPartitions=6)

    # 3- 数据处理
    # 查看分区数
    print(init_rdd.getNumPartitions())

    # 查看每个分区的具体内容
    print(init_rdd.glom().collect())

    # 4- 释放资源
    sc.stop()