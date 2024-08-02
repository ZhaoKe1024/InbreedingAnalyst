# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-03-04 23:02
import os
import soundfile
import numpy as np
import io
import av
import itertools


class AudioSegment(object):
    """Monaural audio segment abstraction.

    :param samples: Audio samples [num_samples x num_channels].
    :type samples: ndarray.float32
    :param sample_rate: Audio sample rate.
    :type sample_rate: int
    :raises TypeError: If the sample data type is not float or int.
    """

    def __init__(self, samples, sample_rate):
        """Create audio segment from samples.

        Samples are convert float32 internally, with int scaled to [-1, 1].
        """
        self._samples = self._convert_samples_to_float32(samples)
        self._sample_rate = sample_rate
        if self._samples.ndim >= 2:
            self._samples = np.mean(self._samples, 1)

    def gain_db(self, gain):
        """对音频施加分贝增益。

        Note that this is an in-place transformation.

        :param gain: Gain in decibels to apply to samples.
        :type gain: float|1darray
        """
        self._samples *= 10. ** (gain / 20.)

    @classmethod
    def from_file(cls, file):
        """从音频文件创建音频段

        :param file: 文件路径，或者文件对象
        :type file: str, BufferedReader
        :return: 音频片段实例
        :rtype: AudioSegment
        """
        assert os.path.exists(file), f'文件不存在，请检查路径：{file}'
        try:
            samples, sample_rate = soundfile.read(file, dtype='float32')
        except:
            # 支持更多格式数据
            sample_rate = 16000
            samples = decode_audio(file=file, sample_rate=sample_rate)
        return cls(samples, sample_rate)

    def to_wav_file(self, filepath, dtype='float32'):
        """保存音频段到磁盘为wav文件

        :param filepath: WAV文件路径或文件对象，以保存音频段
        :type filepath: str|file
        :param dtype: Subtype for audio file. Options: 'int16', 'int32',
                      'float32', 'float64'. Default is 'float32'.
        :type dtype: str
        :raises TypeError: If dtype is not supported.
        """
        samples = self._convert_samples_from_float32(self._samples, dtype)
        subtype_map = {
            'int16': 'PCM_16',
            'int32': 'PCM_32',
            'float32': 'FLOAT',
            'float64': 'DOUBLE'
        }
        soundfile.write(
            filepath,
            samples,
            self._sample_rate,
            format='WAV',
            subtype=subtype_map[dtype])

    @classmethod
    def from_pcm_bytes(cls, data, channels=1, samp_width=2, sample_rate=16000):
        """从包含无格式PCM音频的字节创建音频

        :param data: 包含音频样本的字节
        :type data: bytes
        :param channels: 音频的通道数
        :type channels: int
        :param samp_width: 音频采样的宽度，如np.int16为2
        :type samp_width: int
        :param sample_rate: 音频样本采样率
        :type sample_rate: int
        :return: 音频部分实例
        :rtype: AudioSegment
        """
        samples = buf_to_float(data, n_bytes=samp_width)
        if channels > 1:
            samples = samples.reshape(-1, channels)
        return cls(samples, sample_rate)

    def _convert_samples_to_float32(self, samples):
        """Convert sample type to float32.

        Audio sample type is usually integer or float-point.
        Integers will be scaled to [-1, 1] in float32.
        """
        float32_samples = samples.astype('float32')
        if samples.dtype in np.sctypes['int']:
            bits = np.iinfo(samples.dtype).bits
            float32_samples *= (1. / 2 ** (bits - 1))
        elif samples.dtype in np.sctypes['float']:
            pass
        else:
            raise TypeError("Unsupported sample type: %s." % samples.dtype)
        return float32_samples

    def _convert_samples_from_float32(self, samples, dtype):
        """Convert sample type from float32 to dtype.

        Audio sample type is usually integer or float-point. For integer
        type, float32 will be rescaled from [-1, 1] to the maximum range
        supported by the integer type.

        This is for writing a audio file.
        """
        dtype = np.dtype(dtype)
        output_samples = samples.copy()
        if dtype in np.sctypes['int']:
            bits = np.iinfo(dtype).bits
            output_samples *= (2 ** (bits - 1) / 1.)
            min_val = np.iinfo(dtype).min
            max_val = np.iinfo(dtype).max
            output_samples[output_samples > max_val] = max_val
            output_samples[output_samples < min_val] = min_val
        elif samples.dtype in np.sctypes['float']:
            min_val = np.finfo(dtype).min
            max_val = np.finfo(dtype).max
            output_samples[output_samples > max_val] = max_val
            output_samples[output_samples < min_val] = min_val
        else:
            raise TypeError("Unsupported sample type: %s." % samples.dtype)
        return output_samples.astype(dtype)

    @property
    def samples(self):
        """返回音频样本

        :return: Audio samples.
        :rtype: ndarray
        """
        return self._samples.copy()

    @property
    def sample_rate(self):
        """返回音频采样率

        :return: Audio sample rate.
        :rtype: int
        """
        return self._sample_rate

    @property
    def duration(self):
        """返回音频持续时间

        :return: Audio duration in seconds.
        :rtype: float
        """
        return self._samples.shape[0] / float(self._sample_rate)

    @property
    def num_samples(self):
        """返回样品数量

        :return: Number of samples.
        :rtype: int
        """
        return self._samples.shape[0]

    @property
    def rms_db(self):
        """返回以分贝为单位的音频均方根能量

        :return: Root mean square energy in decibels.
        :rtype: float
        """
        # square root => multiply by 10 instead of 20 for dBs
        mean_square = np.mean(self._samples ** 2)
        return 10 * np.log10(mean_square)

    def __str__(self):
        """返回该音频的信息"""
        return ("%s: num_samples=%d, sample_rate=%d, duration=%.2fsec, "
                "rms=%.2fdB" % (type(self), self.num_samples, self.sample_rate, self.duration, self.rms_db))


def decode_audio(file, sample_rate: int = 16000):
    """读取音频，主要用于兜底读取，支持各种数据格式

    Args:
      file: Path to the input file or a file-like object.
      sample_rate: Resample the audio to this sample rate.

    Returns:
      A float32 Numpy array.
    """
    resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=sample_rate)

    raw_buffer = io.BytesIO()
    dtype = None

    with av.open(file, metadata_errors="ignore") as container:
        frames = container.decode(audio=0)
        frames = _ignore_invalid_frames(frames)
        frames = _group_frames(frames, 500000)
        frames = _resample_frames(frames, resampler)

        for frame in frames:
            array = frame.to_ndarray()
            dtype = array.dtype
            raw_buffer.write(array)

    audio = np.frombuffer(raw_buffer.getbuffer(), dtype=dtype)

    # Convert s16 back to f32.
    return audio.astype(np.float32) / 32768.0


def buf_to_float(x, n_bytes=2, dtype=np.float32):
    """Convert an integer buffer to floating point values.
    This is primarily useful when loading integer-valued wav data
    into numpy arrays.

    Parameters
    ----------
    x : np.ndarray [dtype=int]
        The integer-valued data buffer

    n_bytes : int [1, 2, 4]
        The number of bytes per sample in ``x``

    dtype : numeric type
        The target output type (default: 32-bit float)

    Returns
    -------
    x_float : np.ndarray [dtype=float]
        The input data buffer cast to floating point
    """

    # Invert the scale of the data
    scale = 1.0 / float(1 << ((8 * n_bytes) - 1))

    # Construct the format string
    fmt = "<i{:d}".format(n_bytes)

    # Rescale and format the data buffer
    return scale * np.frombuffer(x, fmt).astype(dtype)


def _ignore_invalid_frames(frames):
    iterator = iter(frames)

    while True:
        try:
            yield next(iterator)
        except StopIteration:
            break
        except av.error.InvalidDataError:
            continue


def _group_frames(frames, num_samples=None):
    fifo = av.audio.fifo.AudioFifo()

    for frame in frames:
        frame.pts = None  # Ignore timestamp check.
        fifo.write(frame)

        if num_samples is not None and fifo._samples >= num_samples:
            yield fifo.read()

    if fifo._samples > 0:
        yield fifo.read()


def _resample_frames(frames, resampler):
    # Add None to flush the resampler.
    for frame in itertools.chain(frames, [None]):
        yield from resampler.resample(frame)
