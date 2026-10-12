from pyspark import SparkContext, SparkConf
import os

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #创建SparkSQL顶级对象
    spark = SparkSession.builder\
        .appName("电影案例分析")\
        .master("yarn")\
        .getOrCreate()

    #读取数据
    init_df = spark.read.csv(
        path="hdfs://node1:8020/data/u.data",
        schema="user_id int, film_id int, score int, duration string",
        sep="\t",
        encoding="UTF-8"
    )

    #ETL
    ETL_df = init_df.dropDuplicates().dropna()

    ETL_df.createTempView("film")

    #需求一：查询用户平均打分
    #--SQL写法
    userAvg_df1 = spark.sql("""
    select 
    user_id, 
    round(avg(score) ,2) as user_avg_score,
    min(score) as user_min_score,
    max(score) as user_max_score
    from film
    group by user_id
    """)

    userAvg_df1.show()
    userAvg_df1.printSchema()

    #DSL写法
    userAvg_df2 = init_df.groupBy("user_id").agg(
        F.round(F.avg("score"), 2).alias("user_avg_score"),
        F.min("score").alias("user_min_score"),
        F.max("score").alias("user_max_score")
    )

    userAvg_df2.show()
    userAvg_df2.printSchema()

    #需求二：查询每部电影的平均分
    """
    需求分析：查询每部电影的平均分需要对每部电影进行分组，然后求平均分
    """
    requirement2_1 = spark.sql("""
        select 
        film_id,
        round(avg(score), 2) as film_avg
        from film
        group by film_id
    """)
    requirement2_1.show()
    requirement2_1.printSchema()

    #DSL写法
    requirement2_2 = init_df.groupBy("film_id").agg(
        F.round(F.avg("score"),2).alias("film_avg")
    )

    requirement2_2.show()

    # 需求三：查询大于平均分的电影的数量
    """
    1、查询每部电影的平均分
    2、查询所有电影总的平均分
    3、过滤出大于总的平均分的电影
    """
    #数据输出


    #释放资源
    spark.stop()
