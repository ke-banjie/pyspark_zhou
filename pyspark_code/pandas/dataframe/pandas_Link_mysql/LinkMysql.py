import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/db1")

with engine.connect() as conn:
    print("连接成功")

# 带条件的查询
df = pd.read_sql("SELECT * FROM employees WHERE department = 'IT'", con=engine)

print(df)
print('_'*30)

# 多表关联查询
sql = """
    SELECT e.name, e.salary, d.department_name
    FROM employees e
    JOIN departments d ON e.dept_id = d.id
    WHERE e.salary < 20000
    ORDER BY e.salary DESC
"""
df = pd.read_sql(sql, con=engine)
print(df.head(10))