import pandas as pd

# JSON Lines 格式数据
jsonl_data = '''{"name": "张三", "age": 25}
{"name": "李四", "age": 30}
{"name": "王五", "age": 28}
{"name": "赵六", "age": 35}
'''

# 写入 JSON Lines 文件
with open("data.jsonl", "w", encoding="utf-8") as f:
    f.write(jsonl_data)

# 读取 JSON Lines（每行是一个 JSON 对象）
df = pd.read_json("data.jsonl", lines=True)
print(df)