# 被験者毎に姿勢の標準化したRSSI値データをplotする
# 縦軸，横軸はそれぞれのタグのcombination
# tester_png/standardized_png/tester_"被験者名"/に図を保存する

import json
import os
import shutil
from itertools import combinations

import matplotlib.pyplot as plt
import matplotlib.cm as cm

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

tester_bed_data = standardized_data

# 姿勢ごとの図をplot

# 2つのタグの組み合わせ
tag_combination = list(combinations(range(len(tag_names)), 2))

for tester, tester_data in tester_bed_data.items():

    dir_path_tester = f'tester_png/standardized_png/tester_{tester}/'
    
    # ディレクトリが存在していたら削除後、再度作成
    if os.path.exists(dir_path_tester):
        shutil.rmtree(dir_path_tester)
    os.mkdir(dir_path_tester)

    for tag_pair in tag_combination:
        x_tag, y_tag = tag_pair

        for posture, posture_data in tester_data.items():
            try:
                rssis1 = posture_data[tag_dict[x_tag]]
                rssis2 = posture_data[tag_dict[y_tag]]
                plt.scatter(rssis1, rssis2, s=20, c=[cm.Paired(int(posture))], marker='o', label = 'posture' + posture)
                plt.xlim(-4, 4)
                plt.ylim(-4, 4)
                
            except:
                print("エラー箇所 > tester：" + str(tester) + ", tag_pair:" + str(tag_pair) + ", " + str(posture))

        plt.xlabel('Tag {}'.format(x_tag))
        plt.ylabel('Tag {}'.format(y_tag))
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
        plt.tight_layout()
        
        file_name = 'tag{}_tag{}.png'.format(x_tag, y_tag)
        plt.savefig(os.path.join(dir_path_tester, file_name))
        plt.clf() # ないとメモリが完全に解放されない
        plt.close()
