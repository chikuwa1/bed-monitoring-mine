import pandas as pd
from datetime import datetime


# 姿勢0（Left the bed）のファイルの読み込み
# CSVファイルを読み込んで、時刻・タグ名・RSSI値を取り出す
file_name = "/home/chiaki/bed-monitoring/csv/log1208/zero.csv"
columns = ['time', 'EPC', 'RSSI']
df = pd.read_csv(file_name, usecols=columns)  # time,EPCはString型, RSSIはfloat64型
df = df.rename(columns={'EPC': 'tag'})

# min_timeは最小の時刻
min_time = df["time"].min()
min_time = datetime.strptime(min_time, "%H:%M:%S.%f")
min_time = int(min_time.timestamp())

df["time"] = df["time"].copy()


# 時刻を0～秒数で換算
for i, time in enumerate(df["time"]):

    # datetimeオブジェクトに変換
    time = datetime.strptime(time, "%H:%M:%S.%f")

    # 秒数に変換
    time = time.timestamp()

    #小数点以下を切り捨て
    time = int(time)

    # 秒数を0～に変更し格納
    time = time - min_time
    df.loc[i, "time"] = time #df["time"]はint型になる


# EPCごとにtimeとRSSIをまとめる
tag_grouped = df.groupby('tag')[['time', 'RSSI']]


# tag_groupedのデータ内容を確認するためのコード
tag_groups = tag_grouped.groups
for group_name, row_indices in tag_groups.items():
    group_data = df.loc[row_indices]
    print(f"Group name: {group_name}")
    print(group_data)






# bed_data{"name":{ 姿勢番号 : {"tag" : {"time":[], "RSSI":[] }}}}の構造にしたい時
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
            data[tag] = {'time': [], 'RSSI': []}
            data[tag]['time'].append(time)
            data[tag]['RSSI'].append(rssi)
        
        bed_data[name][i] = data