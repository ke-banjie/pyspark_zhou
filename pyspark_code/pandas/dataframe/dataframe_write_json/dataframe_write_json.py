import pandas as pd

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "年龄": [25, 30, 28],
    "城市": ["北京", "上海", "广州"]
})

# 写入不同 orient 的 JSON
df.to_json("output_records.json", orient="records", force_ascii=False, indent=2)
df.to_json("output_index.json", orient="index", force_ascii=False, indent=2)
df.to_json("output_columns.json", orient="columns", force_ascii=False, indent=2)

# JSON Lines 格式
df.to_json("output.jsonl", orient="records", lines=True, force_ascii=False)
