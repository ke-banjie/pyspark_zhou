import os

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #建立SparkSession对象
    spark = SparkSession.builder \
        .appName("电影分析案例") \
        .master("yarn") \
        .getOrCreate()

    # 读取数据
    init_df = spark.read.csv(
        path="hdfs://node1:8020/data/u.data",
        schema="userid int, filmid int, score int, duration string",
        sep="\t",
        encoding="UTF-8",
        header=True
    )

    # 过滤掉空值和重复数据
    ETL_df = init_df.dropDuplicates().dropna()

    #需求五：查询每个用户的平均打分，最低打分、最高打分
    """
    需求分析：对用户ID分组聚合，统计平均分、最低打分、最高打分
    """
    ETL_df.createTempView("T1")

    #SQL写法
    user_record = spark.sql(
        """
        select 
            userid,
            round(avg(score), 2) avg_score,
            min(score),
            max(score)
        from T1
        group by userid
        """
    )
    user_record.show()

    #DSL写法
    user_recordDSL = ETL_df.groupBy("userid").agg(
        F.round(F.avg("score"), 2).alias("avg_score_dsl"),
        F.min("score").alias("min_score"),
        F.max("score").alias("max_score")
    ).show()

    #需求六
    """
    1、统计评分超过100次的电影
    2、计算这些电影的平均分
    3、降序排序limit 10得到TOP10
    """

    #SQL写法
    xuqiu6_cnt = spark.sql(
        """
        select 
            filmid, 
            count(score) cnt
        from T1
        group by filmid
        having cnt > 100
        """
    )

    xuqiu6_cnt.createTempView("T2")

    xuqiu6_avg = spark.sql(
        """
        select 
            T2.filmid,
            round(avg("score"), 2) avg_score
        from T2 left join T1 on T2.filmid = T1.filmid
        group by T2.filmid
        order by avg_score desc 
        limit 100
        """
    ).show()

    #DSL写法
    XuQiu6_cnt = ETL_df.groupBy("filmid").agg(
        F.round(F.count("score"), 2).alias("cnt_d")
    ).where("cnt_d > 100")

    XuQiu6_avg_score = XuQiu6_cnt.join(ETL_df, on="filmid", how="left")\
        .groupBy("filmid").avg(
            F.round(F.avg("score"), 2).alias("avg_score")
    ).sort("avg_score").limit(100).show()

    #释放资源
    spark.stop()