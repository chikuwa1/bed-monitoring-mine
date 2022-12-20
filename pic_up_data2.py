import numpy as np
import csv
from datetime import datetime

posture_num = 7 # 姿勢数

# csvからデータの抽出
# bed_data{"被験者名":{ 姿勢番号 : {"tag" : [(time,RSSI)] }}}

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

with open('tag_name.txt') as f: # タグ名の読み込み
    tag_names = f.read().splitlines()

# データを保存する辞書    
bed_data = {}
count_data = {} # 各姿勢の1秒間のデータ取得数（タグ関係なし）
for tester_name in tester_names:
    bed_data[tester_name] = {}
    count_data[tester_name] = {}
    for i in range(posture_num):
        # CSVファイルを読み込み
        file_name = f"csv/log1208/{tester_name}_{i}.csv"
        with open(file_name, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # 最小のtime
            min_time = float('inf')
            for row in reader:
                # datetimeオブジェクトに変換
                time = datetime.strptime(row['time'], '%H:%M:%S.%f')
                # 秒数に変換
                time = time.timestamp()
                # 小数点以下を切り捨て
                time = int(time)
                min_time = min(min_time, time)

            # 辞書を作成
            data = {}
            count = [0] * posture_num
            f.seek(0)
            reader = csv.DictReader(f)
            for row in reader:
                tag = row['EPC']
                # datetimeオブジェクトに変換
                time = datetime.strptime(row['time'], '%H:%M:%S.%f')
                # 秒数に変



# こっから続きを書いてくれないAI



# タグごとに平均値を計算する関数
def calc_avg(data):
    n = len(data)
    avg = np.empty(n)
    for i in range(n):
        if data[i][0] == 0:
            avg[i] = -110.0
        else:
            avg[i] = data[i][1] / data[i][0]
    return avg

tag_count_data = {}  # 各タグ，各時刻のデータ取得数
avg_bed_data = {}  # 各タグ，各時刻の平均値

for tester in tester_names:
    tag_count_data[tester] = {}
    avg_bed_data[tester] = {}
    for i in range(posture_num):
        data = bed_data[tester][i]
        n = max(len(data[tag]) for tag in tag_names)
        count = np.zeros((len(tag_names), n))
        sum = np.zeros((len(tag_names), n))
        for j, tag in enumerate(tag_names):
            for t, rssi in data[tag]:
                count[j][t] += 1
                sum[j][t] += rssi
        tag_count_data[tester][i] = count
        avg_bed_data[tester][i] = np.apply_along_axis(calc_avg, 0, np.stack((count, sum), axis=2))

