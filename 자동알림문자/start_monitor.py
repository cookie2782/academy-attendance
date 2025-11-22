# -*- coding: utf-8 -*-
"""
학원 등원/하원 자동 알림 시스템
자동 시작 버전 (Enter 키 입력 없이 바로 시작)
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
os.chdir(current_dir)

from attendance_monitor import AttendanceMonitor

def main():
    """메인 실행 함수"""
    
    # 엑셀 파일 확인
    excel_file = "202511_자동알림.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"오류: 엑셀 파일을 찾을 수 없습니다: {excel_file}")
        print("엑셀 파일을 현재 디렉토리에 배치해주세요.")
        return
    
    print("=" * 60)
    print("학원 등원/하원 자동 알림 시스템")
    print("=" * 60)
    print()
    print("설정 안내:")
    print("1. config.json 파일에서 학원명, 체크 주기 등을 설정할 수 있습니다.")
    print("2. sms_config.json 파일에서 SMS API 설정을 할 수 있습니다.")
    print("   - 현재 테스트 모드로 실행됩니다 (실제 문자 전송 안됨)")
    print("   - 실제 사용 시 test_mode를 false로 변경하세요.")
    print()
    print("엑셀 파일 구조:")
    print("  - A열: 이름")
    print("  - B열: 연락처")
    print("  - C열: 등원/하원 상태 (0=하원, 1=등원)")
    print()
    print("프로그램을 종료하려면 Ctrl+C를 누르세요.")
    print()
    print("모니터링을 시작합니다...")
    print()
    
    # 모니터 시작
    monitor = AttendanceMonitor(excel_file)
    monitor.start_monitoring()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

