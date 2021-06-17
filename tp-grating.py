#ライブラリの読み込み
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

#パラメータの設定
width = 512
height = 512

a = 1.0

#sin波の配列を作る関数
def sin_g(w, h):
    n = 5
    x = np.linspace(0, 2*np.pi*n, w)
    nor_vec = np.ones((h))
    x_outer = np.outer(nor_vec,x)
    y = (a*np.pi) * np.sin(x_outer) + (a*np.pi)
    
    #sin波をplotしたいとき
    #plot_y = (a*np.pi) * np.sin(x) + (a*np.pi)
    # plt.plot(x,plot_y)
    # plt.show()
    
    return y

#与えられた配列を２値表現に変更する
def binary_g(array, b_min, b_max, b_split):
    #２値に分別
    y_binary = np.where(array <= b_split, b_min, b_max)
    
    #画像を表示
    # plt.plot(y_binary)
    # plt.show()
    
    return y_binary

#目的の最大値と最小値の配列に変換してくれる関数
def normalize(array,  to_min, to_max):
    array_min = np.min(array)
    array_max = np.max(array)
    to_array = (array - array_min) / (array_max - array_min) * (to_max - to_min) + to_min
    return to_array
    
#画像として保存
def bmp_store(img):
    #nor8 = np.uint8(255*(img/(2*np.pi)))
    nor8 = normalize(img, 0, 255)
    
    pil_img = Image.fromarray(nor8)
    pil_img.show()
    pil_img.save("grating_phase.bmp")

if __name__ == '__main__':
    
    #1. 2次元のグレーティングを設計する
    g_phase = sin_g(width,height)
    
    #2.2値表現に変更する
    binary_g = binary_g(g_phase,0,a*np.pi,a*np.pi)
    
    #2. 設計したグレーティングを画像として表示して保存
    bmp_store(binary_g)
    
    #3. グレーティングに照射するレーザービーム面を設計
    
    
    #4 レーザービームを画像として表示して保存
    
    #5 グレーティング通過後の光の波を記述する
    
    #6 強度分布を求める
    
    #7 求めた強度分布を画像として保存
    
    #8 回折効率を求める