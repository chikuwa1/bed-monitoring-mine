# 被験者別に全姿勢（もしくは姿勢0以外の姿勢）の平均RSSI値データをplotする
# 縦軸，横軸はそれぞれのタグのcombination
# 全姿勢データの図はposture_png/all_rssis_png/に保存する
# 姿勢0以外の全姿勢データの図はposture_png/no0_rssis_png/に保存する

import json
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
from itertools import combinations

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


# ファイルの確認
# ディレクトリが存在していたら削除後、再度作成

# 全姿勢
dir_path = 'posture_png/all_rssis_png/'

if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
os.mkdir(dir_path)

# 姿勢0以外の姿勢
dir_path_no0 = 'posture_png/no0_rssis_png/'

if os.path.exists(dir_path_no0):
    shutil.rmtree(dir_path_no0)
os.mkdir(dir_path_no0)


# データの読み込み
df = pd.read_csv("posture_bed_data.csv")
df = pd.get_dummies(df, drop_first=True)

# 全姿勢
df_tester = df.drop(['posture'], axis=1) 

# 姿勢0以外の姿勢
df_no0 = df[df['posture'] != 0]
df_tester_no0 = df_no0.drop(['posture'], axis=1) 



# 2つのタグの組み合わせ
tag_combination = list(combinations(range(len(tag_names)), 2))



for tag_pair in tag_combination:
    x_tag, y_tag = tag_pair
    
    #全姿勢
    for tester in range(len(tester_names)):       
        rssis1 = df_tester[df_tester['tester'] == tester][tag_dict[x_tag]]
        rssis2 = df_tester[df_tester['tester'] == tester][tag_dict[y_tag]]
        plt.scatter(rssis1, rssis2, s=20, c=[cm.Paired(tester)], marker='o', label = "tester" + str(tester))
        plt.xlim(-80.0, -55.0)
        plt.ylim(-80.0, -55.0)
        

    plt.xlabel('Tag {}'.format(x_tag))
    plt.ylabel('Tag {}'.format(y_tag))
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
    plt.tight_layout()
    file_name = 'tag{}_tag{}.png'.format(x_tag, y_tag)
    plt.savefig(os.path.join(dir_path, file_name))
    plt.clf()
    plt.close()

    # 姿勢0以外の姿勢
    for tester in range(len(tester_names)):       
        rssis1 = df_tester_no0[df_tester_no0['tester'] == tester][tag_dict[x_tag]]
        rssis2 = df_tester_no0[df_tester_no0['tester'] == tester][tag_dict[y_tag]]
        plt.scatter(rssis1, rssis2, s=20, c=[cm.Paired(tester)], marker='o', label = "tester" + str(tester))
        plt.xlim(-80.0, -60.0)
        plt.ylim(-80.0, -60.0)
        

    plt.xlabel('Tag {}'.format(x_tag))
    plt.ylabel('Tag {}'.format(y_tag))
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
    plt.tight_layout()
    file_name = 'tag{}_tag{}.png'.format(x_tag, y_tag)
    plt.savefig(os.path.join(dir_path_no0, file_name))
    plt.clf()
    plt.close()