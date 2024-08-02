# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-03-04 23:12
import librosa
import matplotlib.pyplot as plt
from datasetkits.audio import AudioSegment


def test_read():
    sound_path = "D:/DATAS/UrbanSound8K/UrbanSound8K/audio/fold1/50901-0-1-1.wav"
    # sound_path = "./temp_files/20240411232534_.ogg"
    # audio_seg = AudioSegment.from_file(sound_path)
    y, sr = librosa.core.load(sound_path, sr=16000)
    print(len(y) / sr)
    print(y)
    print(max(y))
    print(min(y))
    plt.figure(0)
    plt.plot(range(len(y)), y, c="black")
    plt.show()


# def test_echarts():


if __name__ == '__main__':
    test_read()
