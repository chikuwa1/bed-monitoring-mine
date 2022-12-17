import pandas as pd
from datetime import datetime

# csvからデータの抽出
# bed_data{"被験者名":{ 姿勢番号 : {"tag" : [(time,RSSI)] }}}
columns = ['time', 'EPC', 'RSSI']

with open('tester_name.txt') as f:
    names = f.read().splitlines()

# 姿勢0の際のファイル読み込み
file_name = "/home/chiaki/bed-monitoring/csv/log1208/zero.csv"
df_0 = pd.read_csv(file_name, usecols=columns)  # time,EPCはString型, RSSIはfloat64型

# データを保存する辞書    
bed_data = {}

for name in names:
    bed_data[name] = {}

    for i in range(7):
        if i == 0:
            df = df_0
        else:        
            # CSVファイルを読み込み
            file_name = f"csv/log1208/{name}_{i}.csv"
            df = pd.read_csv(file_name, usecols=columns)

        # 最小のtime
        min_time = df["time"].min()
        min_time = datetime.strptime(min_time, "%H:%M:%S.%f")
        min_time = int(min_time.timestamp())
        
        # 辞書を作成
        data = {}
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

            rssi = row['RSSI']
            if tag not in data: # もしtagに対するデータが一つもなかったら空
                data[tag] = []
            data[tag].append((time, rssi))

        bed_data[name][i] = data

print(bed_data["furushima"][1]["E280116060000204AC6AD1FE"])



# 各タグ，各時刻の平均値求める

avg_bed_data = {}


