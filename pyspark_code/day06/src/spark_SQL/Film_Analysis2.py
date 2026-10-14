import os

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

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
        schema="userid int, filmid int, score int, duration string",
        sep="\t",
        encoding="UTF-8",
        header=True
    )

    #过滤掉空值和重复数据
    ETL_df = init_df.dropDuplicates().dropna()


    #需求四：查询高分电影中(电影平均分大于3)打分次数最多的用户, 并且求出此人所有的打分记录中, 打的平均分是多少
    """
    1、统计每部电影的平均打分
    2、过滤出电影平均分大于3的电影
    3、从高分电影中筛选出打分次数最多的用户
    4、统计该用户所有打分记录的平均分
    """
    ETL_df.createTempView("T1")
    #SQL写法
    #1、统计每部电影的平均打分
    Film1 = spark.sql(
        """
        select 
            filmid, 
            round(avg(score),2) as avg_score
        from T1
        group by filmid
        having avg_score > 3
        """
    )

    Film1.createTempView("F1")

    #3、从高分电影中筛选出打分次数最多的用户
    Film2 = spark.sql(
        """
        select userid, count(filmid) cnt
        from T1
        where filmid in (select filmid from F1)
        group by userid
        order by count(filmid) DESC 
        limit 1
        """
    )

    Film2.createTempView("F2")

    #4、统计该用户所有打分记录的平均分
    result_user_avg_score = spark.sql(
        """
        select userid, round(avg(score), 2) user_avg_score
        from T1
        where userid in (select userid from F2)
        group by userid
        """
    ).show()

    #DSL写法
    # 1、统计每部电影的平均打分
    FilmDSL1 = ETL_df.groupBy("filmid").agg(
        F.round(F.avg("score"), 2).alias("film_avg_score")
    ).where("film_avg_score > 3")

    # 3、从高分电影中筛选出打分次数最多的用户
    FilmDSL2 = FilmDSL1.join(ETL_df, on=FilmDSL1.filmid == ETL_df.filmid, how="left").\
        groupBy("userid").\
        agg(
            F.count("userid").alias("cnt")
        ).\
        sort("cnt", ascending=False).limit(1)

    #4、统计该用户所有打分记录的平均分
    result_dsl = ETL_df.join(FilmDSL2, on="userid", how="right")\
        .groupBy("userid").agg(
        F.round(F.avg("score"), 2).alias("user_avg_score")
    )


    result_dsl.show()
    #释放资源
    spark.stop()