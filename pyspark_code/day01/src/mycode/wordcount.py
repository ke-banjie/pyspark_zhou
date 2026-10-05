from pyspark import SparkContext, SparkConf
import os

# 绑定Python解释器和Spark安装路径
os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

if __name__ == '__main__':
    # 1- 创建顶级对象 / 创建Spark的运行环境
    """
        setAppName：给PySpark应用程序取名称
        setMaster：设置程序的运行方式。local[*]使用本机所有的CPU来执行程序
    """
    conf = SparkConf().setAppName('WordCount').setMaster('local[*]')
    sc = SparkContext(conf=conf)

    # 2- 数据读取
    # sc.textFile('D:\code\gz19_pyspark\day01\data\content.txt')
    """
        textFile(参数): 读取文件。支持读取HDFS和本地文件
            本地文件的路径写法 file://路径
            HDFS文件的路径写法 hdfs://node1:8020/路径
    """
    init_rdd = sc.textFile('file:///export/data/pyspark_code/day01/data/content.txt')

    # 3- 数据处理
    # 3.1- 文本内容切分flatMap
    # 输出结果： ['hello', 'hello', 'spark', 'hello', 'heima', 'spark']
    flatmap_rdd = init_rdd.flatMap(lambda line: line.split(" "))

    # 3.2- 数据格式转换map：hello -> (hello,1)
    # 输出结果： [('hello', 1), ('hello', 1), ('spark', 1), ('hello', 1), ('heima', 1), ('spark', 1)]
    map_rdd = flatmap_rdd.map(lambda word: (word, 1))

    # 3.3- 分组聚合reduceByKey
    # 输出结果： [('hello', 3), ('spark', 2), ('heima', 1)]
    """
        reduceByKey：先对数据按照key进行分组，将相同key的value组织成一个List；再对value组织成一个List进行聚合操作
        分组：
            [('hello', 1), ('hello', 1), ('spark', 1), ('hello', 1), ('heima', 1), ('spark', 1)]
            分组后的结果
            hello -> [1,1,1]
            spark -> [1,1]
            heima -> [1]

        聚合：以hello为例
            agg：表示中间临时聚合结果；curr：表示当前遍历到的元素

            第一次聚合：agg默认取列表中的第一个元素，curr默认取列表中的第二个元素，因此agg=1,curr=1，聚合结果是2；再将2的值重新赋值给agg
            第二次聚合：agg=2，curr遍历到第3个元素值是1，2+1=3
            由于已经将value组成的列表遍历完成，因此hello最终的次数就是3
    """
    result = map_rdd.reduceByKey(lambda agg, curr: agg + curr)

    # 4- 数据输出
    """
        collect：因为RDD是分布式的数据结构，因此需要将各个地方的数据
    """
    print(result.collect())

    # 5- 释放资源
    sc.stop()