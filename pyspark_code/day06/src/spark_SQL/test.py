from pyspark import SparkContext, SparkConf
import os
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #创建SparkSession对象
    spark = SparkSession.builder\
        .appName("电影分析案例")\
        .master("yarn")\
        .getOrCreate()

    #读取数据
    init_df = spark.read.csv(
        path="hdfs://node1:8020/data/u.data",
        schema="userid int, movieid int, score int, duration string",
        sep="\t",
        encoding="UTF-8",
        header=True
    )

    #过滤掉空值和重复数据
    etl_df = init_df.dropDuplicates().dropna()

    etl_df.createTempView("t1")
    # 1 - 统计每部电影的平均分
    # 2 - 过滤出平均分 > 3分的高分电影
    sql_t2 = spark.sql("""
           select
               movieid,
               round(avg(score),2) as avg_score
           from t1
           group by movieid
           having avg_score>3
       """)
    sql_t2.createTempView("t2")
    sql_t2.show()

    # 3 - 从高分电影中筛选出打分次数最多的用户
    sql_t3 = spark.sql("""
           select
               t1.userid,
               count(1) as cnt
           from t2 left join t1 
           on t2.movieid = t1.movieid
           group by t1.userid
           order by cnt desc
           limit 1
       """)
    sql_t3.createTempView("t3")
    sql_t3.show()

    # 4 - 统计该用户，所有的打分记录中的总平均值是多少
    spark.sql("""
           select
               round(avg(score),2) as user_avg_score
           from t1
           where userid=(select userid from t3)
       """).show()

    # DSL
    # 1 - 统计每部电影的平均分
    # 2 - 过滤出平均分 > 3分的高分电影
    """
        DSL中没有having，由于having也是进行数据的过滤，因此实际调用的是where
    """
    dsl_t2 = etl_df.groupBy("movieid").agg(
        F.round(F.avg("score"), 2).alias("avg_score")
    ).where("avg_score>3")
    dsl_t2.show()

    # 3 - 从高分电影中筛选出打分次数最多的用户
    # 如果on的字段名称完全一致，可以这样写on
    # dsl_t2.join(etl_df,on="movieid",how="left")
    # 如果on的字段名称不一致，可以这样写on
    dsl_t3 = dsl_t2.join(etl_df, on=dsl_t2.movieid == etl_df.movieid, how="left") \
        .groupBy("userid") \
        .agg(F.count("userid").alias("cnt")) \
        .orderBy("cnt", ascending=False) \
        .limit(1)
    dsl_t3.show()

    # 4 - 统计该用户，所有的打分记录中的总平均值是多少
    # 注意：where中如果传递Column对象，等于的时候需要写两个=
    etl_df.where(etl_df.userid == dsl_t3.first().userid).agg(
        F.round(F.avg("score"), 2).alias("user_avg_score")
    ).show()