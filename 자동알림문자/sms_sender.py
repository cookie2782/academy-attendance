"""
SMS 및 카카오톡 메시지 전송 모듈

지원하는 서비스:
1. SMS
   - 네이버 클라우드 플랫폼 (SENS)
   - 쿨SMS
   - 알리고

2. 카카오톡 알림톡/친구톡
   - 알리고 카카오톡
   - 네이버 클라우드 플랫폼 카카오톡
   - 카카오 비즈니스 API
"""

import requests
import json
import os
import hashlib
import hmac
import base64
import time

# SMS API 설정 파일
SMS_CONFIG_FILE = 'sms_config.json'

def load_sms_config():
    """SMS 설정 로드 (환경 변수 우선)"""
    # 환경 변수에서 먼저 읽기 (Render, Railway 등 호스팅 서비스용)
    if os.getenv('SMS_PROVIDER'):
        return {
            "provider": os.getenv('SMS_PROVIDER', 'naver'),
            "message_type": os.getenv('SMS_MESSAGE_TYPE', 'sms'),
            "test_mode": os.getenv('SMS_TEST_MODE', 'False').lower() == 'true',
            "naver": {
                "service_id": os.getenv('SMS_NAVER_SERVICE_ID', ''),
                "access_key": os.getenv('SMS_NAVER_ACCESS_KEY', ''),
                "secret_key": os.getenv('SMS_NAVER_SECRET_KEY', ''),
                "sender_phone": os.getenv('SMS_SENDER', '')
            },
            "coolsms": {
                "api_key": os.getenv('SMS_API_KEY', ''),
                "api_secret": os.getenv('SMS_API_SECRET', ''),
                "sender_phone": os.getenv('SMS_SENDER', '')
            },
            "aligo": {
                "api_key": os.getenv('SMS_ALIGO_API_KEY', ''),
                "user_id": os.getenv('SMS_ALIGO_USER_ID', ''),
                "sender_phone": os.getenv('SMS_SENDER', '')
            }
        }
    
    # 로컬 환경에서는 sms_config.json 사용
    if os.path.exists(SMS_CONFIG_FILE):
        with open(SMS_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 기본 설정 파일 생성
        default_config = {
            "provider": "naver",  # naver, coolsms, aligo, kakao_aligo, kakao_naver, kakao_business
            "test_mode": True,  # 테스트 모드 (실제 전송 안함)
            "message_type": "sms",  # sms 또는 kakao
            
            # 네이버 클라우드 플랫폼 SENS 설정
            "naver": {
                "service_id": "YOUR_SERVICE_ID",
                "access_key": "YOUR_ACCESS_KEY",
                "secret_key": "YOUR_SECRET_KEY",
                "sender_phone": "01012345678"
            },
            
            # 쿨SMS 설정
            "coolsms": {
                "api_key": "YOUR_API_KEY",
                "api_secret": "YOUR_API_SECRET",
                "sender_phone": "01012345678"
            },
            
            # 알리고 설정
            "aligo": {
                "api_key": "YOUR_API_KEY",
                "user_id": "YOUR_USER_ID",
                "sender_phone": "01012345678"
            },
            
            # 알리고 카카오톡 설정
            "kakao_aligo": {
                "api_key": "YOUR_API_KEY",
                "user_id": "YOUR_USER_ID",
                "sender_key": "YOUR_SENDER_KEY",
                "template_code": "YOUR_TEMPLATE_CODE"
            },
            
            # 네이버 클라우드 카카오톡 알림톡 설정
            "kakao_naver": {
                "service_id": "YOUR_SERVICE_ID",
                "access_key": "YOUR_ACCESS_KEY",
                "secret_key": "YOUR_SECRET_KEY",
                "plus_friend_id": "YOUR_PLUS_FRIEND_ID",
                "template_code": "YOUR_TEMPLATE_CODE"
            },
            
            # 카카오 비즈니스 API 설정
            "kakao_business": {
                "rest_api_key": "YOUR_REST_API_KEY",
                "sender_key": "YOUR_SENDER_KEY",
                "template_code": "YOUR_TEMPLATE_CODE"
            }
        }
        
        with open(SMS_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        return default_config

def send_sms_naver(phone, message, config):
    """네이버 클라우드 플랫폼 SENS를 통한 SMS 전송"""
    service_id = config['naver']['service_id']
    access_key = config['naver']['access_key']
    secret_key = config['naver']['secret_key']
    sender_phone = config['naver']['sender_phone']
    
    # API 요청 URL
    url = f"https://sens.apigw.ntruss.com/sms/v2/services/{service_id}/messages"
    
    # 타임스탬프
    timestamp = str(int(time.time() * 1000))
    
    # 시그니처 생성
    method = "POST"
    uri = f"/sms/v2/services/{service_id}/messages"
    message_bytes = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message_bytes = bytes(message_bytes, 'UTF-8')
    secret_key_bytes = bytes(secret_key, 'UTF-8')
    
    signing_key = base64.b64encode(hmac.new(secret_key_bytes, message_bytes, digestmod=hashlib.sha256).digest())
    
    # 헤더
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signing_key
    }
    
    # 요청 본문
    body = {
        "type": "SMS",
        "contentType": "COMM",
        "countryCode": "82",
        "from": sender_phone,
        "content": message,
        "messages": [
            {
                "to": phone
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 202:
            return True
        else:
            print(f"네이버 SMS 전송 실패: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"네이버 SMS 전송 오류: {e}")
        return False

def send_sms_coolsms(phone, message, config):
    """쿨SMS를 통한 SMS 전송"""
    # 쿨SMS SDK 사용 시
    # pip install coolsms-python 필요
    
    try:
        from sdk.api.message import Message
        from sdk.exceptions import CoolsmsException
        
        api_key = config['coolsms']['api_key']
        api_secret = config['coolsms']['api_secret']
        sender_phone = config['coolsms']['sender_phone']
        
        params = {
            'type': 'sms',
            'to': phone,
            'from': sender_phone,
            'text': message
        }
        
        cool = Message(api_key, api_secret)
        response = cool.send(params)
        
        return True
    except ImportError:
        print("쿨SMS SDK가 설치되지 않았습니다. pip install coolsms-python")
        return False
    except Exception as e:
        print(f"쿨SMS 전송 오류: {e}")
        return False

def send_sms_aligo(phone, message, config):
    """알리고를 통한 SMS 전송"""
    api_key = config['aligo']['api_key']
    user_id = config['aligo']['user_id']
    sender_phone = config['aligo']['sender_phone']
    
    url = "https://apis.aligo.in/send/"
    
    data = {
        'key': api_key,
        'user_id': user_id,
        'sender': sender_phone,
        'receiver': phone,
        'msg': message,
        'msg_type': 'SMS',
        'title': '학원 알림'
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get('result_code') == '1':
            return True
        else:
            print(f"알리고 SMS 전송 실패: {result}")
            return False
    except Exception as e:
        print(f"알리고 SMS 전송 오류: {e}")
        return False

def send_kakao_aligo(phone, message, student_name, config):
    """알리고 카카오톡 알림톡 전송"""
    api_key = config['kakao_aligo']['api_key']
    user_id = config['kakao_aligo']['user_id']
    sender_key = config['kakao_aligo']['sender_key']
    template_code = config['kakao_aligo']['template_code']
    
    url = "https://kakaoapi.aligo.in/akv10/alimtalk/send/"
    
    data = {
        'apikey': api_key,
        'userid': user_id,
        'senderkey': sender_key,
        'tpl_code': template_code,
        'sender': '카카오톡',
        'receiver_1': phone,
        'subject_1': '학원 알림',
        'message_1': message,
        'failover': 'Y',  # 실패 시 SMS로 대체
        'fsubject_1': '학원 알림',
        'fmessage_1': message
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get('code') == '0':
            return True
        else:
            print(f"알리고 카카오톡 전송 실패: {result}")
            return False
    except Exception as e:
        print(f"알리고 카카오톡 전송 오류: {e}")
        return False

def send_kakao_naver(phone, message, student_name, config):
    """네이버 클라우드 플랫폼 카카오톡 알림톡 전송"""
    service_id = config['kakao_naver']['service_id']
    access_key = config['kakao_naver']['access_key']
    secret_key = config['kakao_naver']['secret_key']
    plus_friend_id = config['kakao_naver']['plus_friend_id']
    template_code = config['kakao_naver']['template_code']
    
    # API 요청 URL
    url = f"https://sens.apigw.ntruss.com/alimtalk/v2/services/{service_id}/messages"
    
    # 타임스탬프
    timestamp = str(int(time.time() * 1000))
    
    # 시그니처 생성
    method = "POST"
    uri = f"/alimtalk/v2/services/{service_id}/messages"
    message_bytes = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message_bytes = bytes(message_bytes, 'UTF-8')
    secret_key_bytes = bytes(secret_key, 'UTF-8')
    
    signing_key = base64.b64encode(hmac.new(secret_key_bytes, message_bytes, digestmod=hashlib.sha256).digest())
    
    # 헤더
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signing_key
    }
    
    # 요청 본문
    body = {
        "plusFriendId": plus_friend_id,
        "templateCode": template_code,
        "messages": [
            {
                "to": phone,
                "content": message
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 202:
            return True
        else:
            print(f"네이버 카카오톡 전송 실패: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"네이버 카카오톡 전송 오류: {e}")
        return False

def send_kakao_business(phone, message, student_name, config):
    """카카오 비즈니스 API 카카오톡 알림톡 전송"""
    rest_api_key = config['kakao_business']['rest_api_key']
    sender_key = config['kakao_business']['sender_key']
    template_code = config['kakao_business']['template_code']
    
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    
    headers = {
        'Authorization': f'Bearer {rest_api_key}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # 템플릿 객체 생성
    template_object = {
        "object_type": "text",
        "text": message,
        "link": {
            "web_url": "https://example.com",
            "mobile_web_url": "https://example.com"
        }
    }
    
    data = {
        'template_object': json.dumps(template_object)
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        
        if result.get('result_code') == 0:
            return True
        else:
            print(f"카카오 비즈니스 API 전송 실패: {result}")
            return False
    except Exception as e:
        print(f"카카오 비즈니스 API 전송 오류: {e}")
        return False

def send_sms(phone, message, student_name=""):
    """
    SMS 또는 카카오톡 메시지 전송 메인 함수
    
    Args:
        phone: 수신자 전화번호
        message: 전송할 메시지
        student_name: 학생 이름 (카카오톡 템플릿용)
        
    Returns:
        bool: 전송 성공 여부
    """
    config = load_sms_config()
    
    # 메시지 타입 확인
    message_type = config.get('message_type', 'sms')
    
    # 테스트 모드인 경우 실제 전송하지 않음
    if config.get('test_mode', True):
        type_text = "카카오톡" if message_type == "kakao" else "SMS"
        print(f"  [테스트 모드] {type_text} 전송 시뮬레이션")
        print(f"  수신: {phone}")
        print(f"  내용: {message}")
        return True
    
    # 전화번호 포맷팅 (하이픈 제거)
    phone = phone.replace('-', '').replace(' ', '')
    
    # 선택된 프로바이더로 전송
    provider = config.get('provider', 'naver')
    
    # 카카오톡 전송
    if message_type == 'kakao':
        if provider == 'kakao_aligo' or provider == 'aligo':
            return send_kakao_aligo(phone, message, student_name, config)
        elif provider == 'kakao_naver' or provider == 'naver':
            return send_kakao_naver(phone, message, student_name, config)
        elif provider == 'kakao_business':
            return send_kakao_business(phone, message, student_name, config)
        else:
            print(f"알 수 없는 카카오톡 프로바이더: {provider}")
            return False
    
    # SMS 전송
    else:
        if provider == 'naver':
            return send_sms_naver(phone, message, config)
        elif provider == 'coolsms':
            return send_sms_coolsms(phone, message, config)
        elif provider == 'aligo':
            return send_sms_aligo(phone, message, config)
        else:
            print(f"알 수 없는 SMS 프로바이더: {provider}")
            return False

# 테스트
if __name__ == "__main__":
    test_phone = "01012345678"
    test_message = '"홍길동"님이 "OO학원"에 등원하였습니다.'
    
    print("SMS 전송 테스트")
    print(f"수신: {test_phone}")
    print(f"내용: {test_message}")
    print()
    
    result = send_sms(test_phone, test_message)
    
    if result:
        print("✓ SMS 전송 성공")
    else:
        print("✗ SMS 전송 실패")

