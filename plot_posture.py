import json
import os
import shutil
from itertools import combinations

import matplotlib.pyplot as plt



posture_num = 7 # 姿勢数

with open("standardized_data.json", "r") as json_file:
    standardized_data = json.load(json_file)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

with open('tag_name.txt', 'r') as f: # タグ名の読み込み
    tag_names = f.readlines()

tag_dict = {} # tagの名前を0から順に対応させる
for i, tag_name in enumerate(tag_names):
    tag_dict[i] = tag_name.strip()

posture_bed_data = {}

for i in range(posture_num):
    posture_bed_data[str(i)] = {}
    for tester_name in tester_names:
        posture_bed_data[str(i)][tester_name] = {}

for tester, tester_data in standardized_data.items():
    for posture, posture_data in tester_data.items():        
        posture_bed_data[posture][tester] = posture_data

# 姿勢ごとの図をplot

colors = [] # color map　利用したいYO

# 2つのタグの組み合わせ
tag_combination = list(combinations(range(len(tag_names)), 2))

for posture, posture_data in posture_bed_data.items():

    print("姿勢"+str(posture)+ ":")

    dir_path_posture = f'posture_png/posture{posture}/'
    if os.path.exists(dir_path_posture):
        shutil.rmtree(dir_path_posture)
    os.mkdir(dir_path_posture)
    for tag_pair in tag_combination:
        print("tagペア：" + str(tag_pair))
        x_tag, y_tag = tag_pair
    
        fig, ax = plt.subplots()
        for tester, tester_data in posture_data.items():
            print(tester)
            rssis1 = tester_data[tag_dict[x_tag]]
            rssis2 = tester_data[tag_dict[y_tag]]
            plt.scatter(rssis1, rssis2, s=20, c=tester, marker='D', alpha=0.05, label = tester)
        
        ax.set_xlabel('Tag {}'.format(x_tag))
        ax.set_ylabel('Tag {}'.format(y_tag))
        ax.legend()
        file_name = 'tag{}_tag{}.png'.format(x_tag, y_tag)
        plt.savefig(os.path.join(dir_path_posture, file_name))
        plt.clf() # ないとメモリが完全に解放されない
        plt.close()

