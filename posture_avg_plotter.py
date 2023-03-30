# 姿勢毎に被験者の平均化したRSSI値データをplotする
# 縦軸，横軸はそれぞれのタグのcombination

import json
import os
import shutil
from itertools import combinations

import matplotlib.pyplot as plt
import matplotlib.cm as cm

posture_num = 7 # 姿勢数


# ファイルの読み込み
with open("avg_bed_data.json", "r") as json_file:
    average_data = json.load(json_file)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

with open('tag_name.txt', 'r') as f: # タグ名の読み込み
    tag_names = f.readlines()


# tag名を0から順に対応させる
tag_dict = {}
for i, tag_name in enumerate(tag_names):
    tag_dict[i] = tag_name.strip()


# average_dataを{"姿勢番号":{ "被験者名" : {"tag" : [毎秒の平均RSSI値] }}}の形として格納
posture_bed_data = {}

for i in range(posture_num):
    posture_bed_data[str(i)] = {}
    for tester_name in tester_names:
        posture_bed_data[str(i)][tester_name] = {}

for tester, tester_data in average_data.items():
    for posture, posture_data in tester_data.items():        
        posture_bed_data[posture][tester] = posture_data

# jsonファイルへ保存
with open("posture_bed_data.json", "w") as json_file:
    json.dump(posture_bed_data, json_file)



# 姿勢ごとの図をplot
tester_index = {tester: i for i, tester in enumerate(tester_names)}

# 2つのタグの組み合わせ
tag_combination = list(combinations(range(len(tag_names)), 2))

for posture, posture_data in posture_bed_data.items():

    dir_path_posture = f'posture_png/average_png/posture{posture}/'

    # ディレクトリが存在していたら削除後、再度作成
    if os.path.exists(dir_path_posture):
        shutil.rmtree(dir_path_posture)
    os.mkdir(dir_path_posture)

    for tag_pair in tag_combination:
        x_tag, y_tag = tag_pair
        tester_num = 0
        for tester, tester_data in posture_data.items():
            try:
                rssis1 = tester_data[tag_dict[x_tag]]
                rssis2 = tester_data[tag_dict[y_tag]]
                plt.scatter(rssis1, rssis2, s=20, c=[cm.Paired(tester_num)], marker='o', label = "tester" + str(tester_num))
                plt.xlim(-80.0, -55.0)
                plt.ylim(-80.0, -55.0)
                
                tester_num += 1
            except:
                print("エラー箇所 > 姿勢：" + str(posture) + ", tag_pair:" + str(tag_pair) + ", " + str(tester))

        plt.xlabel('Tag {}'.format(x_tag))
        plt.ylabel('Tag {}'.format(y_tag))
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
        plt.tight_layout()

        file_name = 'tag{}_tag{}.png'.format(x_tag, y_tag)
        plt.savefig(os.path.join(dir_path_posture, file_name))
        plt.clf() # ないとメモリが完全に解放されない
        plt.close()

