# 平均したrssi値を用いて標準化する(avg_bed_data.json利用)

# standardized_data{"被験者名":{ "姿勢番号" : {"tag" : [毎秒の平均RSSI値を標準化した値] }}}
# standardized_dataをstandardized_data.jsonへ保存



import json
from sklearn import preprocessing
import numpy as np

# ファイルの読み込み
with open("avg_bed_data.json", "r") as json_file:
    average_data = json.load(json_file)

standardized_data = {} # 各タグ，各時刻の標準化したRSSI値を格納

# 平均データから、被験者ごとのデータを取り出す
for tester, tester_data in average_data.items():
  standardized_data[tester] = {}
  
  # 姿勢ごとのデータを取り出す
  for posture, posture_data in tester_data.items():
    standardized_data[tester][posture] = {}
    
    # タグごとのデータを取り出す
    for tag, rssis in posture_data.items():
      np_rssis = np.array(rssis).reshape(-1, 1)
      # StandardScaler クラスを使用して、データを標準化する
      sc = preprocessing.StandardScaler()
      sc.fit(np_rssis)
      standardized_rssis = sc.transform(np_rssis)
      standardized_data[tester][posture][tag] = list(standardized_rssis.reshape(-1))

# jsonファイルに保存
with open("standardized_data.json", "w") as json_file:
    json.dump(standardized_data, json_file)