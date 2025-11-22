# -*- coding: utf-8 -*-
"""
현재 PC의 IP 주소를 확인하고 QR 코드를 생성하는 유틸리티
"""

import socket
import qrcode
import os
from PIL import Image

def get_local_ip():
    """현재 PC의 로컬 IP 주소 가져오기"""
    try:
        # 더미 연결을 만들어서 IP 확인
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generate_qr_code(url, filename='qr_code.png'):
    """QR 코드 생성"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return True
    except ImportError:
        print("⚠️  QR 코드 생성을 위해 qrcode 라이브러리가 필요합니다.")
        print("   설치: pip install qrcode[pil]")
        return False
    except Exception as e:
        print(f"QR 코드 생성 오류: {e}")
        return False

def main():
    print()
    print("=" * 60)
    print("학원 웹 앱 - IP 주소 및 QR 코드 생성")
    print("=" * 60)
    print()
    
    # IP 주소 확인
    local_ip = get_local_ip()
    port = 5000
    url = f"http://{local_ip}:{port}"
    
    print("📍 현재 PC의 IP 주소:")
    print(f"   {local_ip}")
    print()
    
    print("🌐 웹 앱 접속 주소:")
    print()
    print(f"   PC에서:      http://localhost:{port}")
    print(f"   모바일에서:   {url}")
    print()
    
    # QR 코드 생성
    print("🔲 QR 코드 생성 중...")
    if generate_qr_code(url, 'webapp_qr.png'):
        print(f"   ✓ QR 코드가 생성되었습니다: webapp_qr.png")
        print()
        print("   이 QR 코드를 프린트해서 학원에 부착하세요!")
        print("   스마트폰으로 스캔하면 바로 접속됩니다.")
        
        # QR 코드 열기
        try:
            if os.name == 'nt':  # Windows
                os.startfile('webapp_qr.png')
            elif os.name == 'posix':  # Mac/Linux
                os.system('open webapp_qr.png')
        except:
            pass
    else:
        print("   QR 코드 생성을 건너뜁니다.")
    
    print()
    print("=" * 60)
    print()
    print("💡 사용 방법:")
    print()
    print("1. [웹앱실행.bat] 실행")
    print(f"2. 모바일 브라우저에서 {url} 접속")
    print("3. 또는 QR 코드 스캔")
    print()
    print("=" * 60)
    print()
    
    input("Enter 키를 누르면 종료합니다...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"오류 발생: {e}")
        input("Enter 키를 누르면 종료합니다...")


