import pandas as pd
import json

# 准备测试 JSON 数据
data_records = '''
[
    {"name": "张三", "age": 25, "city": "北京"},
    {"name": "李四", "age": 30, "city": "上海"},
    {"name": "王五", "age": 28, "city": "广州"}
]
'''

# 方式1：JSON 数组（每行一个对象）-> DataFrame
df = pd.read_json(data_records, orient="records")
print("orient='records':")
print(df)
print()

# 方式2：JSON 对象（键值对）-> Series
data_dict = '{"name": "张三", "age": 25, "city": "北京"}'
s = pd.read_json(data_dict, typ="series")
print("读取为 Series:")
print(s)