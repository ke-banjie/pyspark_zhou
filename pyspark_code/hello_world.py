from pyspark.sql import SparkSession

# 创建 SparkSession
spark = SparkSession.builder \
    .appName("HelloWorld") \
    .master("local[*]") \
    .getOrCreate()

# 创建一个简单的 DataFrame
data = [("Hello", "World!")]
df = spark.createDataFrame(data, ["col1", "col2"])

# 显示结果
df.show()

# 打印一条消息
print("Hello, World! PySpark is running successfully!")

# 关闭 SparkSession
spark.stop()
