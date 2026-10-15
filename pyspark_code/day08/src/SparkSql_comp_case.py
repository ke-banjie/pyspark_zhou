import os
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    #创建sparksession对象
    spark = SparkSession.builder\
        .appName("SparkSQl综合案例分析")\
        .master("yarn")\
        .getOrCreate()

    #读取数据
    init_data = spark.read\
        .format("csv")\
        .option("sep", ",")\
        .option("header", True)\
        .option("encoding", "UTF-8")\
        .schema("InvoiceNo string, StockCode string, Description string, Quantity integer, InvoiceDate string, UnitPrice double, CustomerId integer, Country string")\
        .load("hdfs://node1:8020/data/E_Commerce_Data.csv")

    print(init_data.count())

    #ETL
    tmp_etl_df = init_data.where("CustomerId != 0 and Description != ''")

    etl_df = tmp_etl_df.withColumn("InvoiceDate", F.from_unixtime(F.unix_timestamp("InvoiceDate", "M/d/yyyy H:mm"), "yyyy-MM-dd HH:mm"))


    #需求一：统计各个国家有多少的客户量
    Cou_custom_num = etl_df.groupBy("Country").agg(
        F.countDistinct("CustomerId").alias("Custom_num")
    ).show()

    #需求二: 销量最高的10个国家
    sale_cou = etl_df.groupBy("Country").agg(
        F.sum("Quantity").alias("Quantity1")
    ).sort("Quantity1",ascending=False).limit(10)

    #需求三: 统计各个国家的总销售额分布情况

    total_sale_cou = sale_cou.join(etl_df,on="Country", how="left")\
        .groupBy("Country") \
        .agg(F.expr("SUM(Quantity1 * UnitPrice)").alias("sale"))\
        .show(20, truncate=False)


    #需求四: 销售最高10个商品
    #需求五: 商品描述的热门关键词TOP300
    #需求六: 统计退货订单数最多的10个国家
    #需求七: 商品的平均单价与销量的关系
    #需求八: 月销售额随时间的变化趋势
    #需求九: 日销售随时间的变化趋势
    #需求十: 各国的购买订单量和退货订单量的关系

    #释放资源
    spark.stop()

