#!/usr/bin/env python3
"""
Demo script cho Meeting Member Vy
Hiển thị các log level khác nhau
"""

import os
import subprocess
import sys
import time

def run_demo(log_level, duration=10):
    """Chạy demo với log level cụ thể"""
    print(f"\n🎯 Demo với LOG_LEVEL={log_level} trong {duration} giây...")
    print("-" * 50)
    
    # Set environment variable
    env = os.environ.copy()
    env['LOG_LEVEL'] = log_level
    
    try:
        # Chạy main.py với timeout
        process = subprocess.Popen(
            [sys.executable, 'main.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        start_time = time.time()
        while time.time() - start_time < duration:
            output = process.stdout.readline()
            if output:
                print(output.strip())
            elif process.poll() is not None:
                break
            time.sleep(0.1)
        
        # Terminate process
        process.terminate()
        process.wait(timeout=2)
        
    except Exception as e:
        print(f"❌ Lỗi chạy demo: {e}")

def main():
    """Demo các log level"""
    print("🎭 Meeting Member Vy - Demo Log Levels")
    print("=" * 60)
    
    # Kiểm tra virtual environment
    if not os.path.exists('.venv'):
        print("❌ Virtual environment không tồn tại. Chạy: python -m venv .venv")
        return
    
    # Demo các log level
    log_levels = [
        ('production', 'Chỉ hiển thị khi Vy được gọi'),
        ('info', 'Hiển thị transcript chính và phản hồi'),
        ('debug', 'Hiển thị tất cả chi tiết')
    ]
    
    for level, description in log_levels:
        print(f"\n📋 {level.upper()}: {description}")
        run_demo(level, duration=8)
        
        if level != log_levels[-1][0]:  # Không pause ở lần cuối
            input("\n⏸️  Nhấn Enter để tiếp tục demo log level tiếp theo...")
    
    print("\n" + "=" * 60)
    print("✅ Hoàn thành demo!")
    print("\n💡 Để chạy với log level cụ thể:")
    print("   LOG_LEVEL=production python main.py")
    print("   LOG_LEVEL=info python main.py")
    print("   LOG_LEVEL=debug python main.py")

if __name__ == "__main__":
    main()