import pandas as pd

# 原始數據
data = {
    "Age": [44, 27, 30, 38, 35],
    "Salary": [75000, 73000, 54000, 70000, 66000]
}

# 建立 DataFrame
df = pd.DataFrame(data)

# 計算正規化值
df["NormC1"] = df["Age"] / df["Age"].sum()
df["NormC2"] = df["Salary"] / df["Salary"].sum()

# 計算 NormC1 / NormC2
df["NormC1/NormC2"] = df["NormC1"] / df["NormC2"]

# 顯示結果
print(df)
