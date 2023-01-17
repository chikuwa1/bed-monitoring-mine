import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import os

# jsonファイルの読み込み
with open("posture_bed_data.json", "r") as f: # 姿勢別のデータの読み込み
    posture_data = json.load(f)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

with open('tag_name.txt', 'r') as f: # タグ名の読み込み
    tag_names = f.read().splitlines()

# データの抽出
for posture_num, testers in posture_data.items():
    rssi_data = []
    for tag_name in tag_names:
        temp_data = []
        for tester_name, tags in testers.items():
            temp_data.append(tags[tag_name])
        rssi_data.append(np.concatenate(temp_data, axis=0))    
    rssi_data = np.array(rssi_data)
    rssi_data = rssi_data.T

    # 主成分分析(PCA)
    print(rssi_data)
    print("*****************")
    pca = PCA(n_components=2)
    print(pca)
    print("*****************")
    pca_result = pca.fit_transform(rssi_data)

    print(pca_result)
    print("//////////////////")
    
    # 図の作成
    
    # dir_path = f'posture_png/pca_png/'

    # fig, ax = plt.subplots()
    # for i, tester_name in enumerate(tester_names):
    #     ax.scatter(pca_result[i, 0], pca_result[i, 1], label=tester_name)
    # ax.legend()
    # plt.title("Posture Number : " + posture_num)
    # file_name = 'posture{}_pca.png'.format(posture_num)
    # plt.savefig(os.path.join(dir_path, file_name))
    # plt.clf() # ないとメモリが完全に解放されない
    # plt.close()