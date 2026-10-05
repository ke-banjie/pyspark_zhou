import pandas as pd

# 创建 DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}
df = pd.DataFrame(data)

# 查看前两行数据
print(df.head(2))

print('-'*30)

# 查看 DataFrame 的基本信息
print(df.info())

print('-'*30)

# 获取描述统计信息
print(df.describe())

print('-'*30)

# 按年龄排序
df_sorted = df.sort_values(by='Age', ascending=False)
print(df_sorted)

print('-'*30)

# 选择指定列
print(df[['Name', 'Age']])

print('-'*30)

# 按索引选择行
print(df.iloc[1:3])  # 选择第二到第三行（按位置）

print('-'*30)

# 按标签选择行
print(df.loc[1:2])  # 选择第二到第三行（按标签）
print('-'*30)

# 计算分组统计（按城市分组，计算平均年龄）
print(df.groupby('City')['Age'].mean())
print('-'*30)

# 处理缺失值（填充缺失值）
df['Age'] = df['Age'].fillna(30)
print('-'*30)

# 导出为 CSV 文件
df.to_csv('output.csv', index=False)