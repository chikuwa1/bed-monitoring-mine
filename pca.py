import json
from pandas import json_normalize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import os

# jsonファイルの読み込み
with open("posture_bed_data.json", "r") as f: # 姿勢別のデータの読み込み
    posture_data = json.load(f)

