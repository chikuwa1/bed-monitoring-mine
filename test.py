import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn #機械学習のライブラリ
from sklearn.decomposition import PCA #主成分分析器

with open('tag_name.txt', 'r') as f: # タグ名の読み込み
    tag_names = f.read().splitlines()


df = pd.read_csv("posture_bed_data.csv")
df_p = df[df['posture'] == 1]
# print(df_p)
dfs = df_p.iloc[:, 2:].apply(lambda x: (x-x.mean())/x.std(), axis=0)
# print(dfs)
for tag in tag_names:
    if dfs[tag].isnull().all(): 
        dfs_t = dfs.drop(tag, axis=1)
# print(str(dfs_t))

for tag in tag_names:
    if dfs[tag].isnull().all(): 
        dfs_t = dfs.drop(tag, axis=1)

print(str(dfs_t))
# #主成分分析の実行
# pca = PCA()
# pca.fit(dfs)
# # データを主成分空間に写像
# feature = pca.transform(dfs)
