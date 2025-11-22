# 학원 등원/하원 자동 알림 시스템

엑셀 파일의 등원/하원 상태 변화를 실시간으로 모니터링하여 자동으로 SMS 알림을 발송하는 시스템입니다.

## 📋 주요 기능

- 엑셀 파일 실시간 모니터링
- 등원/하원 상태 자동 감지 (0↔1 변화)
- 학부모 연락처로 자동 SMS 발송
- 여러 SMS API 지원 (네이버, 쿨SMS, 알리고)
- 테스트 모드 지원

## 🚀 설치 방법

### 1. Python 설치
Python 3.7 이상이 필요합니다.
https://www.python.org/downloads/

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 📁 엑셀 파일 구조

엑셀 파일은 다음과 같은 형식이어야 합니다:

| A열 (이름) | B열 (연락처) | C열 (상태) |
|-----------|-------------|-----------|
| 홍길동     | 010-1234-5678 | 0 |
| 김영희     | 010-2345-6789 | 1 |
| 이철수     | 010-3456-7890 | 0 |

- **A열**: 학생 이름
- **B열**: 학부모 연락처
- **C열**: 등원/하원 상태
  - `0`: 하원 상태
  - `1`: 등원 상태

## ⚙️ 설정 방법

### 1. config.json (기본 설정)

프로그램을 처음 실행하면 자동으로 생성됩니다.

```json
{
  "academy_name": "OO학원",
  "check_interval": 5,
  "name_column": "A",
  "phone_column": "B",
  "status_column": "C",
  "start_row": 2
}
```

- `academy_name`: 학원 이름
- `check_interval`: 엑셀 파일 체크 주기 (초)
- `name_column`: 이름이 있는 열
- `phone_column`: 연락처가 있는 열
- `status_column`: 상태가 있는 열
- `start_row`: 데이터 시작 행 (보통 2행부터)

### 2. sms_config.json (SMS API 설정)

프로그램을 처음 실행하면 자동으로 생성됩니다.

```json
{
  "provider": "naver",
  "test_mode": true,
  "naver": {
    "service_id": "YOUR_SERVICE_ID",
    "access_key": "YOUR_ACCESS_KEY",
    "secret_key": "YOUR_SECRET_KEY",
    "sender_phone": "01012345678"
  }
}
```

#### 테스트 모드
- `test_mode: true`: 실제 문자를 보내지 않고 콘솔에만 출력
- `test_mode: false`: 실제 문자 전송

#### SMS API 선택

**1. 네이버 클라우드 플랫폼 SENS** (권장)
```json
{
  "provider": "naver",
  "test_mode": false,
  "naver": {
    "service_id": "ncp:sms:kr:xxxxx",
    "access_key": "your_access_key",
    "secret_key": "your_secret_key",
    "sender_phone": "01012345678"
  }
}
```
- 가입: https://www.ncloud.com/
- 서비스: SENS (Simple & Easy Notification Service)
- 비용: 건당 약 10~15원

**2. 쿨SMS**
```json
{
  "provider": "coolsms",
  "test_mode": false,
  "coolsms": {
    "api_key": "your_api_key",
    "api_secret": "your_api_secret",
    "sender_phone": "01012345678"
  }
}
```
- 가입: https://www.coolsms.co.kr/
- 추가 패키지 필요: `pip install coolsms-python`

**3. 알리고**
```json
{
  "provider": "aligo",
  "test_mode": false,
  "aligo": {
    "api_key": "your_api_key",
    "user_id": "your_user_id",
    "sender_phone": "01012345678"
  }
}
```
- 가입: https://smartsms.aligo.in/

## 🎯 사용 방법

### 1. 기본 실행
```bash
python main.py
```

### 2. 동작 방식

1. 프로그램이 엑셀 파일을 주기적으로 모니터링합니다.
2. C열의 상태 값이 변경되면:
   - `0 → 1`: "등원" 문자 발송
   - `1 → 0`: "하원" 문자 발송
3. B열의 연락처로 자동 SMS 발송

### 3. 문자 내용 예시

**등원 시:**
```
"홍길동"님이 "OO학원"에 등원하였습니다.
```

**하원 시:**
```
"홍길동"님이 "OO학원"에서 하원하였습니다.
```

## 📝 사용 팁

1. **테스트 먼저 하기**
   - 처음에는 `test_mode: true`로 설정하여 테스트
   - 정상 동작 확인 후 `test_mode: false`로 변경

2. **엑셀 파일 수정 시**
   - 엑셀을 저장하면 프로그램이 자동으로 변경사항 감지
   - 프로그램을 종료할 필요 없음

3. **체크 주기 조정**
   - 빠른 반응이 필요하면: `check_interval: 3`
   - 시스템 부하 줄이려면: `check_interval: 10`

4. **발신 번호 등록**
   - SMS API 사용 시 발신 번호를 사전 등록해야 합니다.
   - 각 SMS 서비스 웹사이트에서 발신번호 등록 필요

## 🔧 문제 해결

### Q1: "엑셀 파일을 찾을 수 없습니다" 오류
- 엑셀 파일이 프로그램과 같은 폴더에 있는지 확인
- 파일명이 정확한지 확인

### Q2: SMS가 전송되지 않음
- `sms_config.json`의 `test_mode`가 `false`인지 확인
- API 키가 올바르게 설정되었는지 확인
- 발신번호가 등록되어 있는지 확인

### Q3: 상태 변화가 감지되지 않음
- 엑셀 파일을 저장했는지 확인
- C열의 값이 0 또는 1인지 확인 (문자가 아닌 숫자)
- `config.json`의 열 설정이 맞는지 확인

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전 (3.7 이상)
2. 필요한 패키지가 모두 설치되었는지
3. 설정 파일이 올바른지
4. 엑셀 파일 구조가 맞는지

## 📄 라이선스

이 프로젝트는 개인 및 상업적 용도로 자유롭게 사용할 수 있습니다.

## 🎓 업데이트 예정

- [ ] GUI 인터페이스 추가
- [ ] 알림 로그 저장 기능
- [ ] 다중 엑셀 파일 지원
- [ ] 이메일 알림 추가

