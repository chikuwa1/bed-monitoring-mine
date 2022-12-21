import json

posture_num = 7 # 姿勢数

non_data_rssi = -105.0 # tagが無反応だった場合のrssi値

with open("bed_data.json", "r") as json_file:
    bed_data = json.load(json_file)


with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()
 
with open('tag_name.txt') as f: # タグ名の読み込み
    tag_names = f.read().splitlines()


# 各タグ，各時刻のデータ数とrssi平均値の取得

tag_count_data = {}  # 各タグ，各時刻のデータ取得数
avg_bed_data = {}  # 各タグ，各時刻の平均値


for tester in tester_names:
    tag_count_data[tester] = {}
    avg_bed_data[tester] = {}

    for i in range(posture_num):

        avg_data = {}
        count_one_tag = {}

        max_second = 0  # maxの秒数
        for tag in tag_names:
            if tag in bed_data[tester][str(i)] and bed_data[tester][str(i)][tag][-1][0]:
                if max_second < bed_data[tester][str(i)][tag][-1][0]:
                    max_second = bed_data[tester][str(i)][tag][-1][0]
                else:
                    break

        for tag in tag_names:
            if tag not in avg_data:
                avg_data[tag] = []
            if tag not in count_one_tag:
                count_one_tag[tag] = []

            idx = 0  # データのindex
            second = 0  # 秒数
            count = 0  # 毎秒のデータ数カウンター
            sum = 0.0  # 毎秒のrssi値の合計値

            if tag in bed_data[tester][str(i)]:

                while second <= max_second:
                    if idx < len(bed_data[tester][str(i)][tag]) :

                        if bed_data[tester][str(i)][tag][idx][0] == second:
                            count += 1
                            sum += bed_data[tester][str(i)][tag][idx][1]
                            idx += 1
                        else: 
                            count_one_tag[tag].append(count)
                            second += 1
                            if count == 0: 
                                avg_data[tag].append(non_data_rssi)
                            else:
                                avg_data[tag].append(sum/count)
                                count = 0
                                sum = 0.0

                    else:
                        count_one_tag[tag].append(count)
                        second += 1
                        if count == 0:
                            avg_data[tag].append(non_data_rssi)
                        else:
                            avg_data[tag].append(sum/count)
                            count = 0
                            sum = 0.0

                if count != 0:
                    count_one_tag[tag].append(count)
                    avg_data[tag].append(sum/count)
            
            else: 
                while second <= max_second:
                    count_one_tag[tag].append(count)
                    avg_data[tag].append(non_data_rssi)
                    second += 1

            tag_count_data[tester][str(i)] = count_one_tag
            avg_bed_data[tester][str(i)] = avg_data

with open("avg_bed_data.json", "w") as json_file:
    json.dump(avg_bed_data, json_file)

with open("tag_sec_count_data.json", "w") as json_file:
    json.dump(tag_count_data, json_file)
