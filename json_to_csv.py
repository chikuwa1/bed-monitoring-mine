# posture_bed_data.jsonをcsvファイルに変換
import json
import csv

# ファイルの読み込み
with open("posture_bed_data.json", "r") as f: # 姿勢別のデータの読み込み
    posture_bed_data = json.load(f)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()

with open('tag_name.txt', 'r') as f: # タグ名の読み込み
    tag_names = f.read().splitlines()

# 列名の設定
header = ["posture", "tester", "E280116060000204AC6AD0EC", "E280116060000204AC6AD0E6", "E280116060000204AC6AD1FE", "E280116060000204AC6AD1FD", "E280116060000204AC6AC8F0" ,"E280116060000204AC6AD1FC"]

# csvファイルへの書き込み
with open("posture_bed_data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for posture, posture_data in posture_bed_data.items():
        for i, tester in enumerate(tester_names):
            for j in range(len(posture_data[tester]["E280116060000204AC6AD0EC"])):
                data = [posture, i]
                for tag in tag_names:
                    data.append(posture_data[tester][tag][j])
                writer.writerow(data)

