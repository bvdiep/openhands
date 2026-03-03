import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
print("Đang thử đọc Micro...")
try:
    for i in range(10):
        data = stream.read(1024)
        print(f"Lần {i}: Nhận được {len(data)} bytes")
except Exception as e:
    print(f"Lỗi Micro: {e}")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()