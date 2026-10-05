import pandas as pd

# 读取默认的第一个表单
df = pd.read_excel('data.xlsx')
print(df)

print('')
print('-'*30)

# 读取指定表单的内容（表单名称）
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
print(df)

print('')
print('-'*30)

# 读取多个表单，返回一个字典
dfs = pd.read_excel('data.xlsx', sheet_name=['Sheet1', 'Sheet2'])
print(dfs)

print('')
print('-'*30)

# 自定义列名并跳过前两行
df = pd.read_excel('data.xlsx', header=None, names=['A', 'B', 'C'], skiprows=2)
print(df)