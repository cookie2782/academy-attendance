"""
초기 설정 도우미 스크립트
"""

import json
import os

def create_sample_excel_info():
    """샘플 엑셀 파일 정보 출력"""
    print("=" * 60)
    print("엑셀 파일 구조 안내")
    print("=" * 60)
    print()
    print("엑셀 파일을 다음과 같이 구성해주세요:")
    print()
    print("┌─────────┬──────────────┬────────┐")
    print("│  A열    │     B열      │  C열   │")
    print("│ (이름)  │  (연락처)    │ (상태) │")
    print("├─────────┼──────────────┼────────┤")
    print("│ 홍길동  │ 010-1234-5678│   0    │")
    print("│ 김영희  │ 010-2345-6789│   1    │")
    print("│ 이철수  │ 010-3456-7890│   0    │")
    print("└─────────┴──────────────┴────────┘")
    print()
    print("• C열 값:")
    print("  - 0: 하원 상태")
    print("  - 1: 등원 상태")
    print()
    print("• 0 → 1로 변경하면: 등원 문자 발송")
    print("• 1 → 0으로 변경하면: 하원 문자 발송")
    print()

def setup_config():
    """config.json 설정"""
    print("=" * 60)
    print("기본 설정 (config.json)")
    print("=" * 60)
    print()
    
    academy_name = input("학원 이름을 입력하세요 [기본: OO학원]: ").strip()
    if not academy_name:
        academy_name = "OO학원"
    
    check_interval = input("엑셀 파일 체크 주기(초) [기본: 5]: ").strip()
    if not check_interval:
        check_interval = 5
    else:
        check_interval = int(check_interval)
    
    config = {
        "academy_name": academy_name,
        "check_interval": check_interval,
        "name_column": "A",
        "phone_column": "B",
        "status_column": "C",
        "start_row": 2
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print()
    print("✓ config.json 파일이 생성되었습니다.")
    print()

def setup_sms_config():
    """sms_config.json 설정"""
    print("=" * 60)
    print("SMS 설정 (sms_config.json)")
    print("=" * 60)
    print()
    print("SMS API 서비스를 선택하세요:")
    print("1. 네이버 클라우드 플랫폼 SENS (권장)")
    print("2. 쿨SMS")
    print("3. 알리고")
    print("4. 나중에 설정 (테스트 모드로 사용)")
    print()
    
    choice = input("선택 [1-4]: ").strip()
    
    config = {
        "provider": "naver",
        "test_mode": True,
        "naver": {
            "service_id": "YOUR_SERVICE_ID",
            "access_key": "YOUR_ACCESS_KEY",
            "secret_key": "YOUR_SECRET_KEY",
            "sender_phone": "01012345678"
        },
        "coolsms": {
            "api_key": "YOUR_API_KEY",
            "api_secret": "YOUR_API_SECRET",
            "sender_phone": "01012345678"
        },
        "aligo": {
            "api_key": "YOUR_API_KEY",
            "user_id": "YOUR_USER_ID",
            "sender_phone": "01012345678"
        }
    }
    
    if choice == "1":
        print()
        print("네이버 클라우드 플랫폼 SENS 설정")
        print("가입: https://www.ncloud.com/")
        print()
        
        service_id = input("Service ID: ").strip()
        access_key = input("Access Key: ").strip()
        secret_key = input("Secret Key: ").strip()
        sender_phone = input("발신번호: ").strip()
        
        config["provider"] = "naver"
        config["naver"]["service_id"] = service_id
        config["naver"]["access_key"] = access_key
        config["naver"]["secret_key"] = secret_key
        config["naver"]["sender_phone"] = sender_phone
        
        test_mode = input("테스트 모드로 시작하시겠습니까? [Y/n]: ").strip().lower()
        config["test_mode"] = test_mode != "n"
        
    elif choice == "2":
        print()
        print("쿨SMS 설정")
        print("가입: https://www.coolsms.co.kr/")
        print()
        
        api_key = input("API Key: ").strip()
        api_secret = input("API Secret: ").strip()
        sender_phone = input("발신번호: ").strip()
        
        config["provider"] = "coolsms"
        config["coolsms"]["api_key"] = api_key
        config["coolsms"]["api_secret"] = api_secret
        config["coolsms"]["sender_phone"] = sender_phone
        
        test_mode = input("테스트 모드로 시작하시겠습니까? [Y/n]: ").strip().lower()
        config["test_mode"] = test_mode != "n"
        
    elif choice == "3":
        print()
        print("알리고 설정")
        print("가입: https://smartsms.aligo.in/")
        print()
        
        api_key = input("API Key: ").strip()
        user_id = input("User ID: ").strip()
        sender_phone = input("발신번호: ").strip()
        
        config["provider"] = "aligo"
        config["aligo"]["api_key"] = api_key
        config["aligo"]["user_id"] = user_id
        config["aligo"]["sender_phone"] = sender_phone
        
        test_mode = input("테스트 모드로 시작하시겠습니까? [Y/n]: ").strip().lower()
        config["test_mode"] = test_mode != "n"
        
    else:
        print()
        print("테스트 모드로 설정됩니다. (실제 문자 전송 안됨)")
        config["test_mode"] = True
    
    with open('sms_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print()
    print("✓ sms_config.json 파일이 생성되었습니다.")
    print()

def main():
    """메인 함수"""
    print()
    print("=" * 60)
    print("학원 등원/하원 자동 알림 시스템 - 초기 설정")
    print("=" * 60)
    print()
    
    # 엑셀 파일 구조 안내
    create_sample_excel_info()
    input("Enter 키를 눌러 계속...")
    print()
    
    # 기본 설정
    setup_config()
    input("Enter 키를 눌러 계속...")
    print()
    
    # SMS 설정
    setup_sms_config()
    
    print()
    print("=" * 60)
    print("설정 완료!")
    print("=" * 60)
    print()
    print("다음 명령으로 프로그램을 실행하세요:")
    print("  python main.py")
    print()
    print("설정을 수정하려면:")
    print("  - config.json: 기본 설정")
    print("  - sms_config.json: SMS 설정")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n설정을 취소했습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")

