"""
Audio processing module cho Meeting Member Vy
Xử lý audio input từ microphone và file
"""

import logging
import threading
import time
from typing import Optional, Callable
from pydub import AudioSegment
import io

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logging.warning("PyAudio không có sẵn. Chỉ hỗ trợ xử lý file audio.")

class AudioProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_recording = False
        self.audio_callback = None
        
        # Audio settings
        self.sample_rate = 16000
        self.channels = 1
        self.chunk_size = 1024
        self.format = None
        
        if PYAUDIO_AVAILABLE:
            self.pyaudio = pyaudio.PyAudio()
            self.format = pyaudio.paInt16
        else:
            self.pyaudio = None
            
    def __del__(self):
        """Cleanup"""
        if self.pyaudio:
            self.pyaudio.terminate()
            
    def set_audio_callback(self, callback: Callable[[bytes], None]):
        """Đặt callback để xử lý audio chunks"""
        self.audio_callback = callback
        
    def process_audio_file(self, file_path: str) -> Optional[AudioSegment]:
        """Xử lý file audio thành định dạng PCM 16-bit 16kHz"""
        try:
            self.logger.info(f"🎵 Đang xử lý file audio: {file_path}")
            
            # Load audio file
            audio = AudioSegment.from_file(file_path)
            
            # Chuyển đổi về định dạng yêu cầu
            audio = audio.set_frame_rate(self.sample_rate)
            audio = audio.set_sample_width(2)  # 16-bit
            audio = audio.set_channels(self.channels)  # Mono
            
            self.logger.info(f"✅ Xử lý thành công: {len(audio)}ms, {audio.frame_rate}Hz, {audio.channels} channel(s)")
            return audio
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi xử lý file audio: {e}")
            return None
            
    def get_audio_chunks(self, audio: AudioSegment, chunk_duration_ms: int = 1000):
        """Chia audio thành các chunks"""
        for i in range(0, len(audio), chunk_duration_ms):
            chunk = audio[i:i + chunk_duration_ms]
            yield chunk.raw_data
            
    def start_microphone_recording(self):
        """Bắt đầu thu âm từ microphone"""
        if not PYAUDIO_AVAILABLE:
            self.logger.error("❌ PyAudio không có sẵn. Không thể thu âm từ microphone.")
            return False
            
        try:
            self.logger.info("🎤 Bắt đầu thu âm từ microphone...")
            
            stream = self.pyaudio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            self.is_recording = True
            
            def record_audio():
                while self.is_recording:
                    try:
                        data = stream.read(self.chunk_size, exception_on_overflow=False)
                        if self.audio_callback:
                            self.audio_callback(data)
                    except Exception as e:
                        self.logger.error(f"❌ Lỗi thu âm: {e}")
                        break
                        
                stream.stop_stream()
                stream.close()
                self.logger.info("🛑 Dừng thu âm")
                
            # Chạy recording trong thread riêng
            record_thread = threading.Thread(target=record_audio)
            record_thread.daemon = True
            record_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi khởi tạo microphone: {e}")
            return False
            
    def stop_recording(self):
        """Dừng thu âm"""
        self.is_recording = False
        
    def stream_audio_file(self, file_path: str, chunk_duration_ms: int = 1000):
        """Stream audio file theo chunks"""
        audio = self.process_audio_file(file_path)
        if not audio:
            return
            
        self.logger.info(f"🎵 Bắt đầu stream audio file...")
        
        for chunk_data in self.get_audio_chunks(audio, chunk_duration_ms):
            if self.audio_callback:
                self.audio_callback(chunk_data)
            time.sleep(chunk_duration_ms / 1000.0)  # Giả lập thời gian thực
            
        self.logger.info("✅ Hoàn thành stream audio file")
        
    def list_audio_devices(self):
        """Liệt kê các thiết bị audio có sẵn"""
        if not PYAUDIO_AVAILABLE:
            self.logger.warning("PyAudio không có sẵn")
            return []
            
        devices = []
        for i in range(self.pyaudio.get_device_count()):
            info = self.pyaudio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:  # Chỉ lấy input devices
                devices.append({
                    'index': i,
                    'name': info['name'],
                    'channels': info['maxInputChannels'],
                    'sample_rate': info['defaultSampleRate']
                })
                
        return devices
        
    def test_microphone(self, duration_seconds: int = 3):
        """Test microphone trong thời gian ngắn"""
        if not PYAUDIO_AVAILABLE:
            self.logger.error("❌ PyAudio không có sẵn")
            return False
            
        try:
            self.logger.info(f"🎤 Test microphone trong {duration_seconds} giây...")
            
            stream = self.pyaudio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            frames = []
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration_seconds)):
                data = stream.read(self.chunk_size)
                frames.append(data)
                
            stream.stop_stream()
            stream.close()
            
            # Tạo AudioSegment từ recorded data
            audio_data = b''.join(frames)
            audio = AudioSegment(
                audio_data,
                frame_rate=self.sample_rate,
                sample_width=2,
                channels=self.channels
            )
            
            # Kiểm tra volume
            volume = audio.dBFS
            self.logger.info(f"✅ Test thành công. Volume: {volume:.1f} dBFS")
            
            return volume > -50  # Threshold để xác định có âm thanh
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi test microphone: {e}")
            return False