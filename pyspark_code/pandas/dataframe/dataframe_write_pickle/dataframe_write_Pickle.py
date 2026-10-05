import pandas as pd
import pickle

# 创建复杂结构的 DataFrame
df = pd.DataFrame({
    "A": range(10),
    "B": range(10, 20),
    "C": ["foo", "bar"] * 5
})

# 写入 Pickle 文件
df.to_pickle("data.pkl")

# 读取 Pickle 文件
df_loaded = pd.read_pickle("data.pkl")
print(df_loaded)

# 压缩写入（gzip 压缩，文件更小）
df.to_pickle("data.pkl.gz", compression="gzip")
df_loaded = pd.read_pickle("data.pkl.gz", compression="gzip")

import os
print(os.listdir('.'))  # 查看当前目录下的所有文件
print(f"普通pkl大小: {os.path.getsize('data.pkl')} bytes")
print(f"压缩pkl大小: {os.path.getsize('data.pkl.gz')} bytes")