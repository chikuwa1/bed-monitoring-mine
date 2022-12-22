import json
import os
import shutil


with open("standardized_data.json", "r") as json_file:
    standardized_data = json.load(json_file)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

import matplotlib.pyplot as plt

posture_bed_data = {}
posture_num = 7 # 姿勢数

for i in range(posture_num):
    posture_bed_data[str(i)] = {}
    for tester_name in tester_names:
        posture_bed_data[str(i)][tester_name]={}

for tester, tester_data in standardized_data.items():

    for posture, posture_data in tester_data.items():        
        
        posture_bed_data[posture][tester] = posture_data
   

# 姿勢ごとの図をplot

# 名前ごとに処理を行う
for tester, tester_data in standardized_data.items():
  # 姿勢ごとに処理を行う
  for posture, posture_data in tester_data.items():
    # 各タグのデータをプロットする
    dir_path_posture = f'/mnt/c/Users/chiaki/Desktop/posture{str(posture)}/'
    
    if os.path.exists(dir_path_posture):
        shutil.rmtree(dir_path_posture)

    os.mkdir(dir_path_posture)
    
    for tag, rssis in posture_data.items():
      plt.plot(rssis, label=tag)
    plt.legend()
    plt.title(f"{tester}, {posture}")
    plt.show()
