import pandas as pd
from datetime import datetime
import json

posture_num = 7 # 姿勢数

# csvからデータの抽出
# bed_data{"被験者名":{ 姿勢番号 : {"tag" : [(time,RSSI)] }}}
columns = ['time', 'EPC', 'RSSI']

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

# 姿勢0の際のファイル読み込み
file_name = "/home/chiaki/bed-monitoring/csv/log1208/zero.csv"
df_0 = pd.read_csv(file_name, usecols=columns)  # time,EPCはString型, RSSIはfloat64型

# データを保存する辞書    
bed_data = {}
count_data = {} # 各姿勢の1秒間のデータ取得数（タグ関係なし）
for tester_name in tester_names:
    bed_data[tester_name] = {}
    count_data[tester_name] = {}
    for i in range(posture_num):
        if i == 0:
            df = df_0
        else:        
            # CSVファイルを読み込み
            file_name = f"csv/log1208/{tester_name}_{i}.csv"
            df = pd.read_csv(file_name, usecols=columns)

        # 最小のtime
        min_time = df["time"].min()
        min_time = datetime.strptime(min_time, "%H:%M:%S.%f")
        min_time = int(min_time.timestamp())

        second = 0 # 秒数リセット
        count_data_second = 0

        # 辞書を作成
        data = {}
        count = []
        for index, row in df.iterrows():
            tag = row['EPC']
            # datetimeオブジェクトに変換
            time = datetime.strptime(row['time'], '%H:%M:%S.%f')
            # 秒数に変換
            time = time.timestamp()
            #小数点以下を切り捨て
            time = int(time)
           # 秒数を0～に変更し格納
            time = time- min_time

            if time != second:
                count.append(count_data_second)
                count_data_second = 0
                second = time
            
            count_data_second += 1

            rssi = row['RSSI']
            if tag not in data: # もしtagに対するデータが一つもなかったら空
                data[tag] = []
            data[tag].append((time, rssi))
        
        count.append(count_data_second)
        count_data[tester_name][i] = tuple(count)

        bed_data[tester_name][i] = data

with open("bed_data.json", "w") as json_file:
    json.dump(bed_data, json_file)



# print(len(bed_data["furushima"][1]["E280116060000204AC6AD1FE"][0]))
# print(count_data["furushima"][1])
