import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

sounds = AudioSegment.from_file(file='./test.mp3',format= 'mp3')

print(f'channel: {sounds.channels}')
print(f'frame rate: {sounds.frame_rate}')
print(f'duration: {sounds.duration_seconds} s')


#チャンネルが2 （ステレオ）の場合は交互にデータが入っているので２つおきに動き出すのです
# 今回は音楽ファイルなので未知数ですがまずは読み込んでみます