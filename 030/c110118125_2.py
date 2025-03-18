import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from matplotlib.colors import ListedColormap

# 1. 讀取數據
data = pd.read_csv('knn-dataset.csv')

# 2. 數據預處理
X = data[['Height', 'Weight']]  # 特徵
y = data['Label'].map({'M': 0, 'F': 1})  # 將標籤轉換為數值

# 3. 分割數據
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. KNN 分類與可視化
k_values = [1, 3, 5, 7]  # 不同的 k 值

# 創建一個網格來繪製決策邊界
def plot_decision_boundary(X, y, model, title):
    h = 0.02  # 網格步長
    x_min, x_max = X.iloc[:, 0].min() - 1, X.iloc[:, 0].max() + 1
    y_min, y_max = X.iloc[:, 1].min() - 1, X.iloc[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.8, cmap=ListedColormap(['#FFAAAA', '#AAAAFF']))
    plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, edgecolors='k', marker='o', cmap=ListedColormap(['#FF0000', '#0000FF']))
    plt.title(title)
    plt.xlabel('Height')
    plt.ylabel('Weight')
    plt.show()

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    
    # 將 X_test 轉換為 DataFrame 以避免警告
    X_test_df = pd.DataFrame(X_test, columns=X_train.columns)
    y_pred = knn.predict(X_test_df)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f'k = {k}, Accuracy = {accuracy:.2f}')
    
    # 繪製決策邊界
    plot_decision_boundary(X_train, y_train, knn, f'KNN Decision Boundary (k={k})')