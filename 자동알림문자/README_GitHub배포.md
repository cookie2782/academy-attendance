# GitHub로 웹 호스팅하기 🚀

GitHub 계정으로 간편하게 웹 호스팅!

## 🎯 개요

- **방법**: GitHub + Render
- **시간**: 20분
- **비용**: 무료
- **장점**: `git push`만 하면 자동 배포!

## 📋 준비물

- ✅ GitHub 계정
- ✅ Git 설치
- ✅ 현재 프로젝트

## 🚀 빠른 시작

### 1️⃣ GitHub에 업로드 (10분)

```bash
# 1. Git 초기화
git init

# 2. 사용자 정보 설정
git config user.name "Your Name"
git config user.email "your@email.com"

# 3. GitHub 저장소 연결
git remote add origin https://github.com/yourusername/academy-attendance.git

# 4. 업로드
git add .
git commit -m "초기 버전"
git branch -M main
git push -u origin main
```

### 2️⃣ Render 배포 (10분)

1. https://render.com 접속
2. "Sign in with GitHub" 클릭
3. "New +" → "Web Service"
4. 저장소 선택: `academy-attendance`
5. 설정:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
   - **Plan**: Free

6. 환경 변수 추가:
   ```
   ACADEMY_NAME = OO학원
   NAME_COLUMN = A
   PHONE_COLUMN = B
   STATUS_COLUMN = C
   PAYMENT_COLUMN = D
   START_ROW = 2
   
   SMS_PROVIDER = coolsms
   SMS_API_KEY = your_api_key
   SMS_API_SECRET = your_api_secret
   SMS_SENDER = 01012345678
   ```

7. "Create Web Service" 클릭

### 3️⃣ 완료! 🎉

URL: `https://academy-attendance.onrender.com`

## 🔄 이후 업데이트

코드 수정 후:

```bash
git add .
git commit -m "수정 내용"
git push
```

→ Render가 자동으로 재배포! (3-5분)

## ⚠️ 주의사항

### 엑셀 파일 저장 문제

Render는 임시 파일 시스템 사용:
- ❌ 엑셀 파일 변경사항 재시작 시 초기화
- ✅ 해결: Google Sheets 연동 권장

### 슬립 모드 (무료 플랜)

- 15분 비활성 시 슬립
- 다음 접속 시 30초 소요
- 해결: $7/월 유료 플랜

## 📚 상세 가이드

- `GitHub_웹호스팅_가이드.txt` - 완전 가이드
- `GitHub_빠른시작.txt` - 20분 완성
- `배포체크리스트.txt` - 체크리스트

## 💡 장점

✅ **자동 배포**: git push → 자동 업데이트  
✅ **무료 호스팅**: 소규모 학원 충분  
✅ **HTTPS 기본**: 보안 연결  
✅ **GitHub 백업**: 모든 코드 자동 백업  
✅ **협업 가능**: 여러 명이 함께 개발  

## 🔒 보안

민감한 정보는 GitHub에 올라가지 않음:
- `.gitignore`에 자동 제외
- `sms_config.json` ❌
- `config.json` ❌
- `*.xlsx` ❌

대신 환경 변수로 관리! ✅

## 📊 비용

### 무료 플랜
- 호스팅: $0
- 제한: 슬립 모드, 파일 저장 X

### 유료 플랜 ($7/월)
- always-on
- 빠른 속도
- 안정적

## 🎯 추천 대상

GitHub 배포 추천:
- ✅ 개발자/IT 친화적
- ✅ 자주 업데이트
- ✅ 여러 명이 관리
- ✅ 코드 버전 관리 필요

PythonAnywhere 추천:
- ✅ 비개발자
- ✅ 엑셀 파일 저장 필요
- ✅ 간단한 사용

## 📞 도움말

- [Render 공식 문서](https://render.com/docs)
- [GitHub 가이드](https://docs.github.com/)
- 상세 가이드: `GitHub_웹호스팅_가이드.txt`

## 🔄 다음 단계

1. ✅ GitHub 업로드
2. ✅ Render 배포
3. ⬜ Google Sheets 연동 (권장)
4. ⬜ 커스텀 도메인 (선택)
5. ⬜ 보안 강화 (선택)

---

**완료!** 이제 인터넷 어디서든 접속 가능합니다! 🎉

