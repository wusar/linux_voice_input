import pyaudio
import wave
import os
import whisper
import pyautogui
import pyperclip
import time

def record_audio(filename="recording.wav", duration=10):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* 开始录音")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* 录音结束")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename="recording.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]

def type_chinese_text_into_input(text):
    # time.sleep(1)  # 等待 1 秒，确保焦点在输入框上
    pyperclip.copy(text)  # 将文本复制到剪贴板
    pyautogui.hotkey('ctrl', 'v')  # 模拟粘贴操作

if __name__ == "__main__":
    record_audio()
    transcription = transcribe_audio()
    type_chinese_text_into_input(transcription)
    print("转录结果已输入到输入框:", transcription)