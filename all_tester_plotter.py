# 全被験者データを用いて姿勢別に出力（2つのタグを選択し2次元へ）
# 縦軸，横軸はそれぞれのタグのcombination
# tester_png/all_tester_png/に図を保存する

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
dir_path = 'tester_png/all_tester_png/'

if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
os.mkdir(dir_path)

# データの読み込み
df = pd.read_csv("posture_bed_data.csv")
df = pd.get_dummies(df, drop_first=True)
df_posture = df.drop(['tester'], axis=1) 


# 2つのタグの組み合わせ
tag_combination = list(combinations(range(len(tag_names)), 2))

for tag_pair in tag_combination:
    x_tag, y_tag = tag_pair
    
    for posture in range(posture_num):       
        rssis1 = df_posture[df_posture['posture'] == posture][tag_dict[x_tag]]
        rssis2 = df_posture[df_posture['posture'] == posture][tag_dict[y_tag]]
        plt.scatter(rssis1, rssis2, s=20, c=[cm.Paired(posture)], marker='o', label = "posture" + str(posture))
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
