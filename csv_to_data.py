# csvファイルからEPC（タグ名）,time（時刻）,RSSI（電波強度）の３つのデータを抽出し、jsonファイルに保存
# 各被験者，各姿勢ごとの1秒ごとのデータ取得数をカウントする
# bed_data.jsonに被験者ごと,姿勢ごとのEPC（タグ名）,time（時刻）,RSSI（電波強度）を保存
# count_dataには被験者ごと,姿勢ごとの毎秒のデータ数を格納(タグの区別なし)

import pandas as pd
from datetime import datetime
import json

posture_num = 7 # 姿勢数

# bed_data{"被験者名":{ 姿勢番号 : {"tag" : [(time,RSSI)] }}}
columns = ['time', 'EPC', 'RSSI']

# 被験者名をファイルから読み込む
with open('tester_name.txt') as f:
    tester_names = f.read().splitlines()

# 姿勢0のデータファイルを読み込む
file_name = "csv/log1208/zero.csv"
df_0 = pd.read_csv(file_name, usecols=columns)  # time,EPCはString型, RSSIはfloat64型
  
bed_data = {} # データを保存する辞書
count_data = {} # 各姿勢の1秒間のデータ取得数（タグ関係なし）を格納

for tester_name in tester_names: # 被験者の数くり返す
    bed_data[tester_name] = {}
    count_data[tester_name] = {}
    
    for i in range(posture_num): # 姿勢の数くりかえす
        # 姿勢0の場合
        if i == 0:
            df = df_0
        
        # 姿勢0以外の場合
        else:        
            # CSVファイルを読み込む
            file_name = f"csv/log1208/{tester_name}_{i}.csv"
            df = pd.read_csv(file_name, usecols=columns)

        # 時刻の最小値を0秒とし、秒数でデータを管理する

        min_time = df["time"].min() # 時刻の最小値
        # min_timeの時刻形式を秒数に変換（小数点以下の秒数は切り捨て）
        min_time = datetime.strptime(min_time, "%H:%M:%S.%f")
        min_time = int(min_time.timestamp())


        # 被験者ごと、姿勢ごとにデータ整理

        # 辞書、リストを作成
        data = {}
        count = []

        second = 0 # 1つ前のデータの秒数を管理
        count_data_second = 0 # 1秒間に取得するデータ数をカウント


        # タグ名,時刻,RSSIのデータを取得
        for index, row in df.iterrows():

            # タグ名取得
            tag = row['EPC']

            # 時刻取得後、秒数変換(小数点以下の秒数は切り捨て)
            time = datetime.strptime(row['time'], '%H:%M:%S.%f')
            time = time.timestamp()
            time = int(time)
            # 秒数を0～に変更し格納
            time = time - min_time

            # 前のデータと秒数が異なる場合はデータカウント数を格納
            if time != second:
                count.append(count_data_second)
                count_data_second = 0
                second = time
            
            count_data_second += 1

            # RSSI取得
            rssi = row['RSSI']
            if tag not in data: # もしtagに対するデータが一つもなかったら空
                data[tag] = []
            data[tag].append((time, rssi))

        count.append(count_data_second)


        # 被験者ごと、姿勢ごとのデータとして保存
        count_data[tester_name][i] = tuple(count)
        bed_data[tester_name][i] = data

# タグ名,時刻,RSSIのデータのみjsonファイルで保存
with open("bed_data.json", "w") as json_file:
    json.dump(bed_data, json_file)

