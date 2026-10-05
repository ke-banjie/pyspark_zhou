import pandas as pd

# 创建 DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
})

# 将 DataFrame 转换为 JSON 文件，指定 orient='records'
df.to_json('data.json', orient='records', lines=True)

# 输出生成的文件内容：
# [
#   {"Name":"Alice","Age":25,"City":"New York"},
#   {"Name":"Bob","Age":30,"City":"Los Angeles"},
#   {"Name":"Charlie","Age":35,"City":"Chicago"}
# ]