# 各タグ，各時刻でrssi値を平均化する
# 各タグ,各時刻のデータ数もカウントする

# avg_bed_data{"被験者名":{ 姿勢番号 : {"tag" : [毎秒の平均RSSI] }}} -> 平均RSSIのリストはindexを秒数とした


import json

posture_num = 7 # 姿勢数
non_data_rssi = -105.0 # tagが無反応だった場合に格納するrssi値


# ファイルの読み込み
with open("bed_data.json", "r") as json_file: # 被験者別、姿勢別でタグ名,時刻,RSSIが格納されたデータ
    bed_data = json.load(json_file)

with open('tester_name.txt') as f: # 被験者名の読み込み
    tester_names = f.read().splitlines()
 
with open('tag_name.txt') as f: # タグ名の読み込み
    tag_names = f.read().splitlines()


tag_count_data = {}  # 各タグ，各時刻のデータ取得数を格納
avg_bed_data = {}  # 各タグ，各時刻の平均RSSI値を格納


for tester in tester_names:
    tag_count_data[tester] = {}
    avg_bed_data[tester] = {}

    for i in range(posture_num):

        avg_data = {} # 被験者ごと、姿勢ごとに各タグの毎秒の平均RSSIを格納
        count_one_tag = {} #被験者ごと、姿勢ごとに各タグでカウントされたデータ数を格納


        # データが取得された秒数の最大値を求める（全タグの中での最大値）
        max_second = 0
        for tag in tag_names:
            if tag in bed_data[tester][str(i)] and bed_data[tester][str(i)][tag][-1][0]:
                if max_second < bed_data[tester][str(i)][tag][-1][0]:
                    max_second = bed_data[tester][str(i)][tag][-1][0]
                else:
                    break

        # タグごとに平均RSSIを求める            
        for tag in tag_names:
            if tag not in avg_data:
                avg_data[tag] = []
            if tag not in count_one_tag:
                count_one_tag[tag] = []

            idx = 0  # bed_data内の[(time,RSSI)]のindex
            second = 0  # 前のRSSI値データが観測された秒数
            count = 0  # 毎秒のデータ数カウンター
            sum = 0.0  # 毎秒のrssi値の合計値


             # bed_dataにtagが存在するとき
            if tag in bed_data[tester][str(i)]:

                while second <= max_second:

                    # あるタグにおいては、あるsecondでのデータが存在しない場合があるためidxの大きさでも分岐
                    if idx < len(bed_data[tester][str(i)][tag]) :

                        # secondと秒数が等しい場合
                        if bed_data[tester][str(i)][tag][idx][0] == second:
                            count += 1
                            sum += bed_data[tester][str(i)][tag][idx][1]
                            idx += 1

                        # socondと秒数が異なる場合
                        else: 
                            count_one_tag[tag].append(count)
                            second += 1

                            # カウントしたデータ数が0だった場合、non_data_rssiを格納
                            if count == 0: 
                                avg_data[tag].append(non_data_rssi)
                            
                            # 0でなかったら平均値を求める
                            else:
                                avg_data[tag].append(sum/count)
                                count = 0
                                sum = 0.0

                    
                    # あるidxにデータが存在していなかった場合、前までのデータ結果は格納、その後の平均RSSIはnon_data_rssiを格納
                    else:
                        count_one_tag[tag].append(count)
                        second += 1

                        if count == 0:
                            avg_data[tag].append(non_data_rssi)
                        else:
                            avg_data[tag].append(sum/count)
                            count = 0
                            sum = 0.0

                # もしデータ数がカウントされていたらその結果を格納
                if count != 0:
                    count_one_tag[tag].append(count)
                    avg_data[tag].append(sum/count)
            

            # あるタグのデータが1つも存在しなかったら、全てのRSSIデータにnon_data_rssiを格納、カウントは0
            else: 
                while second <= max_second:
                    count_one_tag[tag].append(count)
                    avg_data[tag].append(non_data_rssi)
                    second += 1


            # 求めた結果を格納
            tag_count_data[tester][str(i)] = count_one_tag
            avg_bed_data[tester][str(i)] = avg_data


# jsonファイルに保存
with open("avg_bed_data.json", "w") as json_file:
    json.dump(avg_bed_data, json_file)

with open("tag_sec_count_data.json", "w") as json_file:
    json.dump(tag_count_data, json_file)
