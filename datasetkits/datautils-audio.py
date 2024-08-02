# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2023-09-01 10:36
import os
import librosa


# 查询文件夹下各种类型文件的个数
def print_all_type():
    # 采样率都是 22050
    wav_path = "E:/DATAS/COUGHVID-public_dataset_v3/coughvid_20211012/"
    cnt = 0
    appendx = dict()
    for f in os.listdir(wav_path):
        if f.split('.')[1] not in appendx:
            appendx[f.split('.')[1]] = 1
        else:
            appendx[f.split('.')[1]] += 1
    print(appendx)
# print_all_type()
# {'json': 34434, 'webm': 29348, 'wav': 3309, 'ogg': 1777, 'csv': 1}


def show_sr(audio_path):
    # audio_path = 'E:/DATAS/COUGHVID-public_dataset_v3/coughvid_20211012/00bfe21c-ab71-4e5a-a941-4f83f5de5c82.wav'
    x, sr = librosa.load(audio_path)  # [sr=44100]   # 22kHz default
    print(type(x), type(sr))
    print(x.shape, sr)


def make_data_txt():
    # 采样率都是 22050
    wav_path = "E:/DATAS/COUGHVID-public_dataset_v3/coughvid_20211012/"
    cnt = 0
    for f in os.listdir(wav_path):
        if "wav" in f:
            show_sr(os.path.join(wav_path, f))
            cnt += 1
    print(cnt)


# 不需要转换，直接多种类型读取吧，写个Adapter
def webm_to_wav(webm_path, wav_path, sampling_rate, channel):
    """
    webm 转 wav
    :param webm_path: 输入 webm 路劲
    :param wav_path: 输出 wav 路径
    :param sampling_rate: 采样率
    :param channel: 通道数
    :return: wav文件
    """
    # 如果存在wav_path文件，先删除。
    if os.path.exists(wav_path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(wav_path)
    # 终端命令
    command = "ffmpeg -loglevel quiet -i {} -ac {} -ar {} {}".format(webm_path, channel, sampling_rate, wav_path)
    print('命令是：',command)
    # 执行终端命令
    os.system(command)


# 也不需要了，直接多种类型读取吧，写个Adapter
def webm2wav_dirlist():
    wav_path = "E:/DATAS/COUGHVID-public_dataset_v3"  # /coughvid_20211012/"
    sampling_rate = 22050
    channel = 1
    for f in os.listdir(wav_path):
        if "webm" in f:
            webm_to_wav(os.path.join(wav_path, f),
                       os.path.join(wav_path, f.split('.')[0]+".wav"),
                       sampling_rate, channel)
    print("---- end ----")
# webm2wav_dirlist()


if __name__ == '__main__':
    show_sr()
    # webm_path = "record_audio.webm"
    # wav_path = "record_audio.wav"
    # sampling_rate = 16000
    # channel = 1
    # webm_to_wav(webm_path, wav_path, sampling_rate, channel)
