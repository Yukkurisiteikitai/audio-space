# #! /usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

sounds = AudioSegment.from_file(file='./test.wav',format= 'wav')

print(f'channel: {sounds.channels}')
print(f'frame rate: {sounds.frame_rate}')
print(f'duration: {sounds.duration_seconds} s')


# #チャンネルが2 （ステレオ）の場合は交互にデータが入っているので２つおきに動き出すのです
# # 今回は音楽ファイルなので未知数ですがまずは読み込んでみます

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter


# 1. 音声データの読み込み
def load_audio(file_path):
    """
    Load the audio file and return the sample rate and data.
    """
    sample_rate, data = wavfile.read(file_path)
    return sample_rate, data

# 2. エアコン音のフィルタリング (バンドパスフィルタ)
def bandpass_filter(data, lowcut, highcut, sample_rate, order=5):
    """
    Apply a bandpass filter to isolate specific frequency ranges.
    """
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    filtered_data = lfilter(b, a, data)
    return filtered_data

# 3. 特徴的な音を制御するためのフィルタリング (拡張可能)
def flexible_filter(data, freq_ranges, sample_rate, order=5):
    """
    Apply multiple bandpass filters for different frequency ranges.
    """
    combined_filtered = np.zeros_like(data, dtype=float)
    for lowcut, highcut in freq_ranges:
        combined_filtered += bandpass_filter(data, lowcut, highcut, sample_rate, order)
    return combined_filtered

# 4. 音声原点の検出 (最大音量位置)
def detect_origin(filtered_data):
    """
    Detect the index of the highest amplitude in the filtered audio.
    """
    max_idx = np.argmax(np.abs(filtered_data))
    return max_idx

# 5. 音量差から距離を予測
def estimate_distance(base_volume, measured_volume, reference_distance=1):
    """
    Estimate distance using the inverse square law and logarithmic attenuation.
    """
    return reference_distance * 10 ** ((base_volume - measured_volume) / 20)

# 6. 音源の位置を算出 (複数マイク対応)
def localize_sound(microphone_positions, delays, speed_of_sound=343):
    """
    Localize sound using time differences of arrival (TDOA) between microphones.
    """
    # Placeholder for advanced localization algorithm.
    # This could involve multilateration or optimization techniques.
    return microphone_positions[0]  # Simplified for one microphone

# メイン処理
if __name__ == "__main__":
    # 入力ファイルのパス
    file_path = "./test.wav"
    
    # 1. 音声データを読み込む
    sample_rate, data = load_audio(file_path)
    
    # 2. エアコン音をフィルタリング
    filtered_data = bandpass_filter(data, 50, 150, sample_rate)
    
    # 3. 特徴的な音（必要に応じて複数周波数帯）をフィルタリング
    freq_ranges = [(50, 150), (1000, 2000)]  # 例: エアコン音と他の特徴音
    controlled_data = flexible_filter(data, freq_ranges, sample_rate)
    
    # 4. 音声原点を検出
    origin_idx = detect_origin(filtered_data)
    print(f"音源の推定位置 (サンプルインデックス): {origin_idx}")

    # 5. 音量差から距離を推定
    base_volume = np.max(np.abs(filtered_data))  # 仮定: 基準音量
    measured_volume = np.abs(filtered_data[origin_idx])  # 検出された音量
    estimated_distance = estimate_distance(base_volume, measured_volume)
    print(f"推定距離: {estimated_distance:.2f} m")

    # 6. 音源位置を計算 (シンプルなローカライゼーション)
    microphone_positions = [(0, 0), (1, 0), (0, 1)]  # マイクの位置
    delays = [0.0, 0.01, 0.02]  # 到達時間差 (仮定)
    sound_position = localize_sound(microphone_positions, delays)
    print(f"音源の推定位置 (座標): {sound_position}")

#ま