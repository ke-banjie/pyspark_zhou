# from pyspark import SparkContext, SparkConf
# import os
#
# # 绑定Python解释器和Spark安装路径
# os.environ['SPARK_HOME'] = '/export/server/spark'
# os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
# os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'
#
# if __name__ == '__main__':
#     #1- 创建spark顶级对象
#     conf = SparkConf().setAppName("点击流日志分析案例").setMaster('yarn')
#     sc = SparkContext(conf=conf)
#
#     #2- 读取数据
#     init_rdd = sc.textFile("hdfs://node1:8020/data/access.log")
#
#     #3- 数据处理
#     #   1.切分数据
#     map_rdd = init_rdd.map(lambda line:line.split(' '))
#     filter_rdd =map_rdd.filter(lambda list:len(list) >= 4)
#     map_rdd1 = filter_rdd.map(lambda list:[list[0],(list[3] + list[4])[1:12]])
#     map_rdd2 =map_rdd1.map(lambda list:tuple(list))
#     map_rdd3 = map_rdd2.map(lambda list:(list, 1))
#     reduceBykey_rdd = map_rdd3.reduceByKey(lambda agg,cur:agg+cur)
#     result = reduceBykey_rdd.sortBy(lambda tup:tup[1],ascending=False)
#
#     # map_rdd1.groupBy()
#     # lines = map_rdd.collect()
#     # for list in lines:
#     #     print(list)
#
#     #4- 输出数据
#     print(result.collect())
#
#     #5- 释放资源
#     sc.stop()

from pyspark import SparkConf, SparkContext
import os
import regex

os.environ['SPARK_HOME'] = '/export/server/spark'
os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/root/anaconda3/bin/python3'

def pu_uv_cnt():
    # 网站访问量就是map_rdd的行数
    pv = map_rdd.count()

    # 访问人数相当于ip地址去重后的结果
    uv = map_rdd.map(lambda list: list[0]).distinct().count()

    print(f"网站的总访问量pv为:{pv}次,独立访客数为:{uv}人")


def uri_top10():
    # 统计请求的URL路径的TOP10,(过滤url为'/'的值)
    url_rdd = map_rdd.map(lambda line: (line[6], 1))

    # 分组聚合
    result_rdd = url_rdd.reduceByKey(lambda agg,curr: agg + curr)

    # 取TOP10
    result_list = result_rdd.top(10, lambda tup: tup[1])

    print(result_list)


if __name__ == '__main__':
    # 创建SparkContext对象
    conf = SparkConf().setAppName("click_log").setMaster("yarn")
    sc = SparkContext(conf=conf)

    # 读取文件
    file_rdd = sc.textFile("hdfs://node1:8020/data/access.log")

    print(file_rdd.take(10))
    # 去除空行
    file_emp_rdd = file_rdd.filter(lambda line: line.strip() != "")
    print(file_emp_rdd.take(10))

    """
       按照空格进行切分，筛选出字段个数大于或等于12个的行
       ['101.226.68.137', '-', '-', '[18/Sep/2013:20:08:54', '+0000]', '"HEAD', '/', 'HTTP/1.1"', '200', '20', '"-"', '"DNSPod-Monitor/1.0"']"""""""
    """
    map_rdd = file_emp_rdd.map(lambda line: line.split())\
        .filter(lambda list: len(list) >= 12)

    print(map_rdd.take(10))

    # 需求一：统计网站的总pv(访问量) 和 uv(独立访客数)
    pu_uv_cnt()

    # 需求二：统计请求的URI路径的TOP10
    uri_top10()
