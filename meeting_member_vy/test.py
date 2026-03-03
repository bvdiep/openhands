#!/usr/bin/env python3
"""
Test script cho Meeting Member Vy
Kiểm tra các chức năng cơ bản
"""

import os
import sys
import asyncio
from main import MeetingMemberVy

def test_basic_functionality():
    """Test các chức năng cơ bản"""
    print("🧪 Test chức năng cơ bản...")
    
    # Test khởi tạo
    app = MeetingMemberVy()
    print(f"✅ Khởi tạo thành công - Simulation mode: {app.simulation_mode}")
    
    # Test phát hiện tên
    test_cases = [
        ("Hạ Vy, bạn có ý kiến gì?", True),
        ("Vy ơi, giúp tôi với", True),
        ("Chào mọi người", False),
        ("Hôm nay thời tiết đẹp", False),
        ("Anh Vy đã đến chưa?", True),  # Có thể false positive
    ]
    
    print("\n🔍 Test phát hiện tên:")
    for text, expected in test_cases:
        result = app.detect_name_mention(text)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{text}' -> {result} (expected: {expected})")
    
    return app

async def test_simulation():
    """Test chế độ simulation"""
    print("\n🎭 Test chế độ simulation...")
    
    app = MeetingMemberVy()
    
    # Chạy simulation trong thời gian ngắn
    print("Chạy simulation trong 10 giây...")
    
    try:
        # Tạo task với timeout
        simulation_task = asyncio.create_task(app.start_simulation())
        await asyncio.wait_for(simulation_task, timeout=10.0)
    except asyncio.TimeoutError:
        print("✅ Simulation hoạt động bình thường (timeout như mong đợi)")
        app.is_listening = False
    except Exception as e:
        print(f"❌ Lỗi simulation: {e}")

def test_audio_processor():
    """Test audio processor"""
    print("\n🎵 Test audio processor...")
    
    try:
        from audio_processor import AudioProcessor, PYAUDIO_AVAILABLE
        
        processor = AudioProcessor()
        print(f"✅ AudioProcessor khởi tạo thành công")
        print(f"   PyAudio available: {PYAUDIO_AVAILABLE}")
        
        if PYAUDIO_AVAILABLE:
            devices = processor.list_audio_devices()
            print(f"   Tìm thấy {len(devices)} audio input devices")
            for device in devices[:3]:  # Chỉ hiển thị 3 device đầu
                print(f"     - {device['name']} ({device['channels']} channels)")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi AudioProcessor: {e}")
        return False

def test_environment():
    """Test môi trường"""
    print("\n🌍 Test môi trường...")
    
    # Check files
    files_to_check = ['.env', '.env.example', 'main.py', 'audio_processor.py', 'requirements.txt']
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file} tồn tại")
        else:
            print(f"❌ {file} không tồn tại")
    
    # Check environment variables
    api_key = os.getenv('GEMINI_API_KEY')
    log_level = os.getenv('LOG_LEVEL', 'info')
    
    print(f"✅ LOG_LEVEL: {log_level}")
    if api_key and api_key != 'your_gemini_api_key_here':
        print("✅ GEMINI_API_KEY đã được cấu hình")
    else:
        print("⚠️  GEMINI_API_KEY chưa được cấu hình (sẽ chạy simulation)")

async def main():
    """Hàm main test"""
    print("🧪 Meeting Member Vy - Test Suite")
    print("=" * 50)
    
    # Test environment
    test_environment()
    
    # Test basic functionality
    app = test_basic_functionality()
    
    # Test audio processor
    test_audio_processor()
    
    # Test simulation
    await test_simulation()
    
    print("\n" + "=" * 50)
    print("✅ Hoàn thành test suite!")
    print("\n💡 Để chạy ứng dụng thực tế:")
    print("   python main.py")

if __name__ == "__main__":
    asyncio.run(main())