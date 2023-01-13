import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
import json
from scipy.linalg import svd
import os  
import shutil
from itertools import combinations
import matplotlib.cm as cm

posture_num = 7 # 姿勢数

with open("posture_bed_data.json", "r") as json_file:
    posture_bed_data = json.load(json_file)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

with open('tag_name.txt', 'r') as f: # タグ名の読み込み
    tag_names = f.read().splitlines()

tag_dict = {} # tagの名前を0から順に対応させる
for i, tag_name in enumerate(tag_names):
    tag_dict[tag_name.strip()] = i


# データを姿勢ごとにまとめる
# each_posture_data={姿勢:[データ数][タグ数]}
each_posture_data = {}

for posture, posture_data in posture_bed_data.items():

    # 全被験者のデータ数の合計
    one_tag = 'E280116060000204AC6AD0EC'
    data_num = 0
    for tester in tester_names:
        data_num += len(posture_data[tester][one_tag])

    data = np.empty((data_num, len(tag_names)))
    for tag in tag_names:
        data_index = 0
        for tester, tester_data in posture_data.items():
            for tag_data_value in tester_data[tag]:
            
                data[data_index,tag_dict[tag]] = tag_data_value
                data_index += 1
                
    each_posture_data[posture] = data

 
# PCA
from sklearn.decomposition import PCA

y=["E280116060000204AC6AD0EC","E280116060000204AC6AD0E6","E280116060000204AC6AD1FE","E280116060000204AC6AD1FD","E280116060000204AC6AC8F0","E280116060000204AC6AD1FC"]
pca = PCA(n_components=2, random_state=0)
reduced_pca = pca.fit_transform(each_posture_data["1"])

# 可視化
Figure = plt.figure(figsize=(24, 7))
ax1 = Figure.add_subplot(1,3,1)
ax1.scatter(reduced_pca[:, 0], reduced_pca[:, 1],
            c=y, cmap='jet', alpha=0.5)

ax1.set_title("PCA")

plt.legend()
file_name = 'PCA.png'.format(x_tag, y_tag)
plt.savefig(os.path.join( f'posture_png/svd_png/posture1/', file_name))
plt.clf() # ないとメモリが完全に解放されない
plt.close()


# A = each_posture_data["1"]
#     # 特異値分解SVDによる次元削除
#     # sは最初の2つが最も大きい特異値

# n, p = A.shape
# U, s, VT = svd(A)
# V_svd = VT.T

# V_2 = np.delete(V_svd, np.s_[2:], 1)

# AV_2 = np.dot(A, V_2)

# AV_2 = list(AV_2)

# dir_path_posture = f'posture_png/svd_png/posture{posture}/'
# if os.path.exists(dir_path_posture):
#     shutil.rmtree(dir_path_posture)
# os.mkdir(dir_path_posture)
# for tag_pair in tag_combination:
#     x_tag, y_tag = tag_pair
#     for i in range(len(AV_2)):    
#         rssis1 = AV_2[i][x_tag]
#         rssis2 = AV_2[i][y_tag]
#         plt.scatter(rssis1, rssis2, s=20, c=[cm.Paired(11)], marker='o')
        
#     plt.xlabel('Tag {}'.format(x_tag))
#     plt.ylabel('Tag {}'.format(y_tag))
#     plt.legend()
#     file_name = 'tag{}_tag{}.png'.format(x_tag, y_tag)
#     plt.savefig(os.path.join(dir_path_posture, file_name))
#     plt.clf() # ないとメモリが完全に解放されない
#     plt.close()




# # t-SNE
# from sklearn.manifold import TSNE

# tsne = TSNE(n_components=2, random_state=0)
# X_reduced_tsne = tsne.fit_transform(X)


# # UMAP
# import umap
# from scipy.sparse.csgraph import connected_components

# umap = umap.UMAP(n_components=2, random_state=0)
# X_reduced_umap = umap.fit_transform(X)

# # 可視化
# Figure = plt.figure(figsize=(24, 7))
# ax1 = Figure.add_subplot(1,3,1)
# ax2 = Figure.add_subplot(1,3,2)
# ax3 = Figure.add_subplot(1,3,3)

# ax1.scatter(X_reduced_pca[:, 0], X_reduced_pca[:, 1],
#             c=y, cmap='jet', alpha=0.5)
# ax2.scatter(X_reduced_tsne[:, 0], X_reduced_tsne[:, 1],
#             c=y, cmap='jet', alpha=0.5)
# ax3.scatter(X_reduced_umap[:, 0], X_reduced_umap[:, 1],
#             c=y, cmap='jet', alpha=0.5)

# ax1.set_title("PCA")
# ax2.set_title("t-SNE")
# ax3.set_title("UMAP")

# plt.show()