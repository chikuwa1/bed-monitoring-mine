import pandas as pd
from datetime import datetime


# 姿勢0（Left the bed）のファイルの読み込み

# CSVファイルを読み込んで、時刻・タグ名・RSSI値を取り出す
file_name = "/home/chiaki/bed-monitoring/csv/log1208/zero.csv"
df = pd.read_csv(file_name, header=0)
df = df[["time", "EPC", "RSSI"]]    # time,EPCはString型, RSSIはfloat64型
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


# 被験者名->姿勢->タグ名->[時刻,RSSI]の形になるよう形成


