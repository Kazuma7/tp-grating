#ライブラリの読み込み
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

#パラメータの設定
width = 512
height = 512

a = 1.0
n = 50

def binary_g(array):
    #周期回数と振幅「デフォルトより優先される」
    n = 5
    a = 1.0
    
    x = np.linspace(0, 2*np.pi*n, width)
    y = (a*np.pi) * np.sin(x) + (a*np.pi)
    y_binary = np.where(y <= a*np.pi, 0, a*np.pi)
    
    plt.plot(y_binary)
    plt.show()
    
    return y_binary

if __name__ == '__main__':
    
    #1. 2次元のグレーティングを設計する
    g_phase = np.zeros((width, height), dtype = float)
    binary_g = binary_g(g_phase)
    
    #2. 設計したグレーティングを画像として表示して保存
    
    #3. グレーティングに照射するレーザービーム面を設計
    
    #4 レーザービームを画像として表示して保存
    
    #5 グレーティング通過後の光の波を記述する
    
    #6 強度分布を求める
    
    #7 求めた強度分布を画像として保存
    
    #8 回折効率を求める