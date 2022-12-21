import json
import os
import shutil


with open("standardized_data.json", "r") as json_file:
    standardized_data = json.load(json_file)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

import matplotlib.pyplot as plt

posture_data = {}
posture_num = 7 # 姿勢数


for tester, tester_data in standardized_data.items():

  for posture, posture_data in tester_data.items():
        if posture not in posture_data:
            posture_data[posture] = {}
        posture_data[posture][tester] = {}

        

#     for tester in tester_names:
#         if i in standardized_data[tester]:
#             posture_data[i][tester].append(standardized_data[tester][i])

# print("姿勢ごと：")
print(posture_data[1])
# print("被験者ごと：")
# print(standardized_data[1]["furushima"]["E280116060000204AC6AD1FE"])

# # 名前ごとに処理を行う
# for tester, tester_data in standardized_data.items():
#   # 姿勢ごとに処理を行う
#   for posture, posture_data in tester_data.items():
#     # 各タグのデータをプロットする
#     dir_path_posture = f'/mnt/c/Users/chiaki/Desktop/posture{str(posture)}/'
    
#     if os.path.exists(dir_path_posture):
#         shutil.rmtree(dir_path_posture)

#     os.mkdir(dir_path_posture)
    
#     for tag, rssis in posture_data.items():
#       plt.plot(rssis, label=tag)
#     plt.legend()
#     plt.title(f"{tester}, {posture}")
#     plt.show()
