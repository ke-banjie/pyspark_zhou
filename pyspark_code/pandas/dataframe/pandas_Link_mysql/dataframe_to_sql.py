# import pandas as pd
# from sqlalchemy import create_engine
#
# engine = create_engine("mysql+pymysql://root:123456@localhost:3306/db1?charset=utf8mb4")
#
# # 准备示例数据
# df = pd.DataFrame({
#     "name": ["张三", "李四", "王五"],
#     "department": ["IT", "HR", "IT"],
#     "salary": [12000, 8000, 15000]
# })
#
# # 将 DataFrame 写入 employees 表，如果已存在则替换
# df.to_sql(
#     "employees",
#     con=engine,
#     if_exists="replace",  # 覆盖原有数据
#     index=False           # 不将 DataFrame 的行索引写入数据库（通常不需要）
# )
#
# # 向已有表追加新数据（注意：列名和数据类型必须匹配）
# new_employees = pd.DataFrame({
#     "name": ["赵六"],
#     "department": ["Finance"],
#     "salary": [11000]
# })
# new_employees.to_sql("employees", con=engine, if_exists="append", index=False)
#
# # 验证写入结果
# result = pd.read_sql("SELECT * FROM employees", con=engine)
# print(result)


import pandas as pd
from sqlalchemy import create_engine

# ✅ 关键修改：在连接字符串中添加 ?charset=utf8mb4
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/db1?charset=utf8mb4")

# 准备示例数据
df = pd.DataFrame({
    "name": ["张三", "李四", "王五"],
    "department": ["IT", "HR", "IT"],
    "salary": [12000, 8000, 15000]
})

# 将 DataFrame 写入 employees 表，如果已存在则替换
df.to_sql(
    "employees",
    con=engine,
    if_exists="replace",
    index=False
)

# 向已有表追加新数据
new_employees = pd.DataFrame({
    "name": ["赵六"],
    "department": ["Finance"],
    "salary": [11000]
})
new_employees.to_sql("employees", con=engine, if_exists="append", index=False)

# 验证写入结果
result = pd.read_sql("SELECT * FROM employees", con=engine)
print(result)