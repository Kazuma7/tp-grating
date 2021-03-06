#ライブラリの読み込み
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

#パラメータの設定
width = 512
height = 512
# -ガウシアンの半径
w0 = 100
# -全エネルギー
power = 1
# -2値の部分
a = 1

#sin波の配列を作る関数
def sin_g(w, h):
    n = 10
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
def bmp_store(img, file_name):
    #nor8 = np.uint8(255*(img/(2*np.pi)))
    nor8 = np.uint8(normalize(img, 0, 255))
    
    pil_img = Image.fromarray(nor8)
    pil_img.show()
    pil_img.save(file_name)

#ガウシアンビームの作成
def gauss_beam(w, h, w0, power):
    w02 = w0*w0
    hw = w /2 
    hh = h / 2
    ilist = np.array([[i for i in range(width)] for j in range(height)], dtype=int)
    jlist = np.array([[j for i in range(width)] for j in range(height)], dtype=int)
    r = np.sqrt((hh - jlist) ** 2 + (hw - ilist) ** 2)
    r2 = r*r
    
    peak_intensity = power * (2/(np.pi*w02))
    g_intensity = peak_intensity * np.exp((-2*r2)/w02)
    array = np.sqrt(g_intensity)
    
    return array,r
    
#g_ampとg_phaseによってできる複素表現
def make_complex(amp, phase, w, h):
    u = np.zeros((w,h), dtype=np.complex128)
    u.real = amp * np.cos(phase)
    u.imag = amp * np.sin(phase)
    
    return u

#高速フーリエ変換を行う
def fft_2d(array, w):
    array_shift = np.fft.fftshift(array)
    array_normalize = np.fft.fft2(array_shift)/w
    fft_array = np.fft.fftshift(array_normalize)
    
    return fft_array

#回折効率を計算する部分
def calc_diffraction_eff(g_int, r_int, rp, w, h):
    #パラメータ
    hh = h/2
    hw = w/2
    mask_d = 3
    g_total = np.sum(g_int)
    
    pos = np.unravel_index(np.argmax(r_int), r_int.shape)
    print("y position = %d" %pos[0])
    print("x position = %d" %pos[1])
    
    # マスク配列の作成
    mask = np.where(rp<= mask_d, 1, 0)
    mask_shift = np.roll(mask, int(hh-pos[0]), axis=0)
    mask_shift = np.roll(mask_shift, int(hw-pos[1]), axis=1)
    r_total = np.sum(r_int * mask_shift)
    
    # 回折効率の計算
    return r_total/g_total

if __name__ == '__main__':
    
    #1 2次元のsin波の２値グレーティングを設計する
    g_phase = sin_g(width,height)
    binary_g = binary_g(g_phase,0,a*np.pi,a*np.pi)
    
    #2 設計したグレーティングを画像として表示して保存
    bmp_store(binary_g, "grating_phase.bmp")
    
    #3 グレーティングに照射するレーザービーム面を設計
    g_amp, r = gauss_beam(width, height, w0, power)
    
    #4 ガウシアンビームを画像として表示して保存
    bmp_store(g_amp, "grating_amp.bmp")
    
    #5 グレーティング通過後の光の波を記述する
    g_wave = make_complex(g_amp, binary_g, width, height)
    after_fft = fft_2d(g_wave, width)
    
    #6 強度分布を求める
    rec_int = np.abs(after_fft)**2
    
    #7 求めた強度分布を画像として保存
    bmp_store(rec_int, "rec_int.bmp")
    
    #8 回折効率を求める
    g_amp_int = np.abs(g_amp)**2
    print(calc_diffraction_eff(g_amp_int,rec_int,r, width, height))