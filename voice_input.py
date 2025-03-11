import pyaudio
import wave
import os
import whisper
import pyautogui
import pyperclip
import numpy as np
import torch
import time

# 加载预训练的 Whisper 模型
model = whisper.load_model("base")
model.eval()

# 定义流式解码函数
def stream_decode(audio_buffer, sample_rate=16000):
    audio_tensor = torch.tensor(audio_buffer).float()
    result = model.transcribe(audio_tensor, fp16=False)
    return result['text']

# 音频缓冲区和其他参数
buffer_size = 32000  # 每个音频块的大小（1秒）
audio_buffer = np.zeros(buffer_size * 10, dtype=np.float32)  # 预留10秒缓冲区
buffer_offset = 0
silence_threshold = 0.5  # 声音门限
# 记录没有声音的时长（单位：秒）
silence_duration = 0
# 没有声音的最大时长，超过这个时长就停止程序
max_silence_duration = 5  

# 麦克风回调函数
def callback(in_data, frame_count, time_info, status):
    global audio_buffer, buffer_offset, silence_duration
    if status:
        print(status, flush=True)
    indata = np.frombuffer(in_data, dtype=np.float32)
    # 计算当前音频块的音量
    volume_norm = np.linalg.norm(indata) * 10
    print(f"Volume: {volume_norm}", flush=True)
    if volume_norm > silence_threshold:
        silence_duration = 0  # 有声音时重置时长
        # 将新音频数据复制到缓冲区
        audio_buffer[buffer_offset:buffer_offset+frame_count] = indata[:frame_count]
        buffer_offset += frame_count

        # 当缓冲区达到或超过设定的大小时进行处理
        if buffer_offset >= buffer_size:
            text = stream_decode(audio_buffer[:buffer_size])
            print(f"Transcription: {text}", flush=True)
            # 将转录结果复制到剪贴板并粘贴
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')

            # 移动缓冲区的数据
            audio_buffer = np.roll(audio_buffer, -buffer_size)
            buffer_offset -= buffer_size
    else:
        silence_duration += frame_count / 16000  # 更新没有声音的时长
        if silence_duration > max_silence_duration:
            raise Exception("长时间无声音，停止程序")  # 超过最大时长时抛出异常
        # 如果检测到的音量低于门限，将缓冲区位置重置
        buffer_offset = 0
    return (in_data, pyaudio.paContinue)

# 启动麦克风流
def start_streaming():
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    stream.start_stream()
    print("Listening...")
    try:
        while stream.is_active():
            pass
    except (Exception, KeyboardInterrupt) as e:
        print(f"Stopping... {str(e)}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    start_streaming()