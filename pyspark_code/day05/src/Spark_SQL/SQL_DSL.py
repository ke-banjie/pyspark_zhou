from pyspark import SparkContext, SparkConf
import os
import pyspark.sql.functions as F

from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #创建sparkSQL顶级对象
    spark = SparkSession.builder\
        .appName("SQL和DSL实现单词统计")\
        .master('local[*]')\
        .getOrCreate()

    #读取文件
    init_dataframe = spark.read\
        .text(paths="file:///export/data/pyspark_code/day05/data/word.txt")\

    init_dataframe.createTempView('content')
    # 3- 数据处理
    # 3.1- SQL方式实现
    sql_result_df = spark.sql("""
        select 
            word,
            count(1) as cnt
        from (
            select
                explode(split(value,' ')) as word
            from content
        ) as tmp
        group by word
    """)
    # 3.2 DSL方式实现
    dsl_result_df = init_dataframe.select(
        F.explode(F.split('value',' ')).alias('word')
    ).groupBy('word').agg(
        F.count('word').alias('cnt')
    )


    sql_result_df.show()
    dsl_result_df.show()


    #释放资源
    spark.stop()