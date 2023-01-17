import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm

from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD

posture_num = 7 # 姿勢数
tester_num = 11 # 被験者数

# ファイルの確認
# PCA
dir_path_PCA = 'posture_png/pca_png/'

if os.path.exists(dir_path_PCA):
    shutil.rmtree(dir_path_PCA)
os.mkdir(dir_path_PCA)

# SVD
dir_path_SVD = 'posture_png/svd_png/'
if os.path.exists(dir_path_SVD):
    shutil.rmtree(dir_path_SVD)
os.mkdir(dir_path_SVD)

df = pd.read_csv("posture_bed_data.csv") # 値や表の形は大丈夫
df = pd.get_dummies(df, drop_first=True)

for posture in range(posture_num):
    df_posture = df[df['posture'] == posture]
    df_rssis = df_posture.drop(['posture', 'tester'], axis=1)

    # PCA
    pca = PCA(n_components=2)
    df_pca = pd.DataFrame(pca.fit_transform(df_rssis)) # 第一主成分0と第二主成分1がわかる
    df_pca['tester'] = df[df['posture'] == posture]['tester'].reset_index(drop=True)
     #うまくできてそう->姿勢6で検証:df_pca各被験者のデータ数はlabel追加前のデータ数と一致を確認
    
    for tester in range(tester_num):
        x_pca = df_pca[df_pca['tester'] == tester][0]
        y_pca = df_pca[df_pca['tester'] == tester][1]
        plt.scatter(x_pca, y_pca, s=20, c=[cm.Paired(tester)], marker='o', label = 'tester' + str(tester))
    
    plt.xlabel('0')
    plt.ylabel('1')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
    plt.tight_layout()
    # plt.title('posture{}_PCA'.format(posture))
    file_name = 'posture{}_PCA.png'.format(posture)
    plt.savefig(os.path.join(dir_path_PCA, file_name))
    plt.clf()
    plt.close()


    # SVD
    svd = TruncatedSVD(n_components=2)
    df_svd = pd.DataFrame(svd.fit_transform(df_rssis))
    df_svd['tester'] = df[df['posture'] == posture]['tester'].reset_index(drop=True)
    
    for tester in range(tester_num):
        x_svd = df_svd[df_svd['tester'] == tester][0]
        y_svd = df_svd[df_svd['tester'] == tester][1]
        plt.scatter(x_svd, y_svd, s=20, c=[cm.Paired(tester)], marker='o', label = 'tester' + str(tester))
    
    plt.xlabel('0')
    plt.ylabel('1')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
    plt.tight_layout()
    # plt.title('posture{}_SVD'.format(posture))
    file_name = 'posture{}_SVD.png'.format(posture)
    plt.savefig(os.path.join(dir_path_SVD, file_name))
    plt.clf()
    plt.close()