# 数値計算やデータフレーム操作に関するライブラリをインポートする
import numpy as np
import pandas as pd
# URL によるリソースへのアクセスを提供するライブラリをインポートする。
import urllib.request 
# 図やグラフを図示するためのライブラリをインポートする。
import matplotlib.pyplot as plt
# %matplotlib inline
import sklearn #機械学習のライブラリ
from sklearn.decomposition import PCA #主成分分析器

url = "https://raw.githubusercontent.com/maskot1977/ipython_notebook/master/toydata/wine.txt"
urllib.request.urlretrieve(url, 'wine.txt') 

# データの書き込み
df = pd.read_csv("wine.txt", sep="\t", index_col=0)

print(df)

# # 標準化（一列目はclassなので，一列目以外をいじり，第一列目で色分けすることでデータを観測）
# dfs = df.iloc[:, 1:].apply(lambda x: (x-x.mean())/x.std(), axis=0)

# # 主成分分析の実行
# pca = PCA()
# pca.fit(dfs)

# # データを主成分空間に写像
# feature = pca.transform(dfs)

# # 主成分得点
# print(str(pd.DataFrame(feature, columns=["PC{}".format(x + 1) for x in range(len(dfs.columns))])))


