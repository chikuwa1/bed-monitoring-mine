# PCAを用いて次元削減し,被験者ごとに姿勢別に色分けして図を出力する
# PCAの図の保存先:tester_png/pca_png/
# PCAの寄与率・固有ベクトル:tester_pca_contribution_rate.txt

import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD

posture_num = 7 # 姿勢数
tester_num = 11 # 被験者数

# ファイルの確認
# ディレクトリが存在していたら削除後、再度作成
dir_path_PCA = 'tester_png/pca_png'

if os.path.exists(dir_path_PCA):
    shutil.rmtree(dir_path_PCA)
os.mkdir(dir_path_PCA)

p_file = open('tester_pca_contribution_rate.txt', 'w')

# データの読み込み
df = pd.read_csv("posture_bed_data.csv") # 値や表の形は大丈夫
df = pd.get_dummies(df, drop_first=True)


# 図の出力
for tester in range(tester_num):
    df_tester = df[df['tester'] == tester]
    df_rssis = df_tester.drop(['posture', 'tester'], axis=1) # 各姿勢の全員分のrssiデータをタグごとにまとめたもの（各姿勢，各被験者名の情報なし）
    
    # 標準化
    sc = StandardScaler()
    df_std = sc.fit_transform(df_rssis)

    # PCA
    pca = PCA(n_components=2)
    df_pca = pd.DataFrame(pca.fit_transform(df_std)) # 第一主成分0と第二主成分1がわかる
    
    df_pca['posture'] = df[df['tester'] == tester]['posture'].reset_index(drop=True)
    
    for posture in range(posture_num):
        x_pca = df_pca[df_pca['posture'] == posture][0]
        y_pca = df_pca[df_pca['posture'] == posture][1]
        plt.scatter(x_pca, y_pca, s=20, c=[cm.Paired(posture)], marker='o', label = 'posture' + str(posture))
        plt.xlim(-4.0, 6.0)
        plt.ylim(-4.0, 6.0)
    
    plt.xlabel('0') # 第一主成分
    plt.ylabel('1') # 第二主成分
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
    plt.tight_layout()
    file_name = 'tester{}_sc_PCA.png'.format(tester)
    plt.savefig(os.path.join(dir_path_PCA, file_name))
    plt.clf()
    plt.close()

    #寄与率・固有ベクトルをテキストファイルに書き込む
    # 寄与率
    explained_variance_ratio_df = pd.DataFrame(pca.explained_variance_ratio_)
    p_file.write("========== tester"+ str(tester) + " ==========\n")
    p_file.write("<第一主成分0，第二主成分1の寄与率>\n")
    p_file.write(str(explained_variance_ratio_df)+ "\n")
    p_file.write('\n')

    # 各タグの固有ベクトル
    loadings_df = pd.DataFrame(pca.components_.T, index=df_rssis.columns)
    p_file.write("<第一主成分0，第二主成分1に対する各タグの固有ベクトル>\n")
    p_file.write(str(loadings_df)+ "\n")
    p_file.write('\n')

p_file.close()