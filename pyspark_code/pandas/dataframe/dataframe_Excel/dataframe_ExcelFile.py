import pandas as pd

# 使用 ExcelFile 加载 Excel 文件
excel_file = pd.ExcelFile('data.xlsx')

# 查看所有表单的名称
print(excel_file.sheet_names)

# 读取指定的表单
df = excel_file.parse('Sheet1')
print(df)

# 关闭文件
excel_file.close()
