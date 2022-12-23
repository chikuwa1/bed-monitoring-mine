# 試す用のpyファイル

import json
from sklearn import preprocessing
import numpy as np

list_m = [1,2,3,4,5,6,7,8,9,10]

np_list = np.array(list_m).reshape(-1, 1)
# StandardScaler クラスを使用して、データを標準化する
sc = preprocessing.StandardScaler()
sc.fit(np_list)
standardized_list = sc.transform(np_list)
list_v = list(standardized_list.reshape(-1))

print(list_v)






# # import pandas as pd
# # from datetime import datetime
# import json

# posture_num = 7 # 姿勢数

# with open("bed_data.json", "r") as json_file:
#     bed_data = json.load(json_file)

# # print(bed_data["furushima"]["1"]["E280116060000204AC6AD1FE"][0])    

# with open('tester_name.txt') as f: # 被験者名の読み込み
#     tester_names = f.read().splitlines()
 
# with open('tag_name.txt') as f: # タグ名の読み込み
#     tag_names = f.read().splitlines()


# # 各タグ，各時刻のデータ数とrssi平均値の取得

# tag_count_data = {}  # 各タグ，各時刻のデータ取得数
# avg_bed_data = {}  # 各タグ，各時刻の平均値


# # for tester in tester_names:
# tester = "furushima"
# tag_count_data[tester] = {}
# avg_bed_data[tester] = {}
# # for i in range(posture_num):
# i = 1 # 姿勢1
    
# count = 0  # 毎秒のデータ数カウンター
# sum = 0.0  # 毎秒のrssi値の合計値
# avg_data = {}
# count_one_tag = {}
# max_second = 0  # maxの秒数
# for tag in tag_names:
#     if tag in bed_data[tester][str(i)] and bed_data[tester][str(i)][tag][-1][0]:
#         if max_second < bed_data[tester][str(i)][tag][-1][0]:
#             max_second = bed_data[tester][str(i)][tag][-1][0]
#         else:
#             break
#     # print(tester, i, tag, max_second)
# # for tag in tag_names:
# tag = "E280116060000204AC6AD1FD"
# if tag not in avg_data:
#     avg_data[tag] = []
# if tag not in count_one_tag:
#     count_one_tag[tag] = []

# if tag in bed_data[tester][str(i)]:
#     # print(tester + "の姿勢" + str(i) + "のタグ" + tag + "はデータが存在します")
#     second = 0  # 秒数
#     idx = 0  # データのindex
#     while second <= max_second:
#         if idx < len(bed_data[tester][str(i)][tag]) :
            
#             if bed_data[tester][str(i)][tag][idx][0] == second:
#                 print(str(second) + "sec 合計：" + str(sum) + " 加える値：" + str(bed_data[tester][str(i)][tag][idx][1]))
#                 count += 1
#                 sum += bed_data[tester][str(i)][tag][idx][1]
#                 idx += 1
#             else: 
#                 count_one_tag[tag].append(count)
#                 second += 1
#                 if count == 0:
#                     print(str(second - 1) + "秒のデータなし！泣")   
#                     avg_data[tag].append(-110.0)
#                     print("平均値：（最低）"+ str(avg_data[tag][second-1]))
#                 else:
#                     avg_data[tag].append(sum/count)
#                     print(str(second - 1) + "秒の平均は")
#                     print("合計：" + str(sum) + " 数：" +  str(count))
#                     print("平均値：" + str(avg_data[tag][second-1]))
#                     count = 0
#                     sum = 0.0
                
#         else:
#             count_one_tag[tag].append(count)
#             second += 1
#             if count == 0:
#                 avg_data[tag].append(-110.0)
#             else:
#                 avg_data[tag].append(sum/count)
#                 print(str(second - 1) + "秒の平均は")
#                 print("合計：" + str(sum) + " 数：" +  str(count))
#                 print("平均値：" + str(avg_data[tag][second-1]))
#                 count = 0
#                 sum = 0.0

#     if count != 0:
#         count_one_tag[tag].append(count)
#         avg_data[tag].append(sum/count)
#         print(str(second - 1) + "秒の平均は")
#         print("合計：" + str(sum) + " 数：" +  str(count))
#         print("平均値：" + str(avg_data[tag][second-1]))
#         count = 0
#         sum = 0.0

# # else: print(tester + "の姿勢" + str(i) + "のタグ" + tag + "はデータが存在しません")
# tag_count_data[tester][str(i)] = count_one_tag
# avg_bed_data[tester][str(i)] = avg_data

# # print(bed_data["furushima"]["1"]["E280116060000204AC6AD1FD"])