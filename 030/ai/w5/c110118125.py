import pandas as pd

data = {
    "Age": [44, 27, 30, 38, 35],
    "Salary": [75000, 73000, 54000, 70000, 66000]
}

df = pd.DataFrame(data)

df["NormC1"] = df["Age"] / df["Age"].sum()
df["NormC2"] = df["Salary"] / df["Salary"].sum()

df["NormC1/NormC2"] = df["NormC1"] / df["NormC2"]
print(df)
