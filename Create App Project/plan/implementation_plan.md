# 📱 React Native + Expo 모바일 앱 개발 계획

> **목표**: 현재 Apps Script 웹앱을 React Native + Expo 기반 네이티브 모바일 앱으로 전환
> **예상 소요 시간**: 2~4주 (기능 복잡도에 따라 변동)

---

## 📋 사전 준비 체크리스트

### 1. 필수 소프트웨어 설치

| 소프트웨어 | 용도 | 다운로드 링크 |
|------------|------|---------------|
| **Node.js** (v18 이상) | JavaScript 런타임 | https://nodejs.org/ko |
| **Git** | 버전 관리 | https://git-scm.com/downloads |
| **VS Code** | 코드 에디터 | https://code.visualstudio.com |
| **Android Studio** | 에뮬레이터 & SDK | https://developer.android.com/studio |
| **Expo Go 앱** (안드로이드 폰) | 실시간 테스트 | Google Play Store에서 설치 |

---

### 2. 계정 준비

| 계정 | 용도 | 비용 |
|------|------|------|
| **Expo 계정** | 앱 빌드 서비스 | 무료 (기본) |
| **Google Play 개발자 계정** | Play Store 등록 | $25 (일회성) |
| **Google Cloud Console** | Sheets API 사용 | 무료 (일정 사용량) |

---

## 🛠️ 개발 환경 설정 단계

### Step 1: Node.js 설치 확인
```powershell
# PowerShell에서 실행
node --version   # v18.x.x 이상이어야 함
npm --version    # 9.x.x 이상 권장
```

### Step 2: Expo CLI 설치
```powershell
npm install -g @expo/cli
npx expo --version  # 설치 확인
```

### Step 3: Expo 계정 생성 & 로그인
```powershell
npx expo register  # 계정 생성 (웹에서도 가능: expo.dev)
npx expo login     # 로그인
```

### Step 4: Android Studio 설정

> [!IMPORTANT]
> 에뮬레이터 테스트를 위해 필요합니다. 실제 안드로이드 폰으로만 테스트할 경우 생략 가능.

1. Android Studio 설치
2. SDK Manager에서 설치:
   - Android SDK Platform 33 (또는 최신)
   - Android SDK Build-Tools
   - Android Emulator
3. AVD Manager에서 가상 디바이스 생성

### Step 5: 환경 변수 설정 (Windows)
```powershell
# 시스템 환경 변수에 추가
ANDROID_HOME = C:\Users\{사용자명}\AppData\Local\Android\Sdk

# Path에 추가
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\emulator
```

---

## 📂 프로젝트 구조 설계

```
mobile-app/
├── app/                    # 화면 (Pages) - Expo Router
│   ├── (tabs)/            # 탭 네비게이션
│   │   ├── index.tsx      # 홈/대시보드
│   │   ├── search.tsx     # 검색 화면
│   │   ├── list.tsx       # 리스트 화면
│   │   └── settings.tsx   # 설정
│   └── _layout.tsx        # 네비게이션 설정
│
├── components/            # 재사용 UI 컴포넌트
│   ├── SearchBar.tsx
│   ├── ListItem.tsx
│   └── FilterModal.tsx
│
├── services/              # API 연동 로직
│   ├── googleSheets.ts    # Google Sheets API
│   ├── api.ts             # API 호출 함수
│   └── storage.ts         # 로컬 저장소
│
├── types/                 # 🆕 TypeScript 타입 정의
│   ├── index.ts           # 공통 타입 export
│   ├── api.types.ts       # API 응답 타입
│   └── navigation.types.ts
│
├── utils/                 # 🆕 유틸리티 함수
│   ├── dateFormat.ts      # 날짜 포맷
│   ├── stringUtils.ts     # 문자열 처리
│   └── validation.ts      # 유효성 검사
│
├── store/                 # 🆕 전역 상태 관리
│   ├── useAppStore.ts     # Zustand 스토어
│   └── context/           # React Context (필요시)
│
├── config/                # 🆕 환경 설정
│   ├── api.config.ts      # API URL 설정
│   └── app.config.ts      # 앱 설정 상수
│
├── hooks/                 # 커스텀 훅
│   ├── useSearch.ts
│   └── useApi.ts
│
├── constants/             # 상수 (색상, 스타일)
│   ├── Colors.ts
│   └── Layout.ts
│
├── assets/               # 이미지, 폰트
│   ├── images/
│   └── fonts/
│
├── __tests__/            # 🆕 테스트 코드 (선택)
│
├── .env                  # 🆕 환경 변수 (Git 제외)
├── .env.example          # 🆕 환경 변수 예시
├── app.json              # 앱 설정
├── eas.json              # EAS 빌드 설정
└── package.json          # 의존성
```

### 추가된 폴더 설명

| 폴더/파일 | 용도 | 중요도 |
|-----------|------|--------|
| `types/` | TypeScript 타입 정의 (인터페이스, DTO 등) | 🔴 높음 |
| `utils/` | 유틸리티 함수 (날짜 포맷, 문자열 처리 등) | 🟡 높음 |
| `store/` | 전역 상태 관리 (Zustand 사용 권장) | 🟡 중간 |
| `config/` | 환경 설정 파일 (API URL, 환경 변수 관리) | 🟡 중요 |
| `.env` | 환경 변수 관리 (API 키, 엔드포인트) | 🔴 높음 |
| `__tests__/` | 테스트 코드 (Jest, React Testing Library) | 🔵 선택 |

---

## 🔗 Google Sheets API 연동 방법

### 옵션 A: Google Apps Script를 API로 활용 (추천)
현재 Apps Script를 그대로 백엔드로 사용하고, 앱에서 호출

```javascript
// Apps Script에서 doGet/doPost 함수로 API 엔드포인트 제공
function doGet(e) {
  const action = e.parameter.action;
  if (action === 'search') {
    return ContentService.createTextOutput(JSON.stringify(searchData(e.parameter.query)));
  }
}
```

```typescript
// React Native에서 호출
const response = await fetch('YOUR_APPS_SCRIPT_URL?action=search&query=검색어');
const data = await response.json();
```

### 옵션 B: Google Sheets API 직접 연동
- Google Cloud Console에서 API 키 발급
- `@google-cloud/local-auth` 또는 서비스 계정 사용

---

## 📱 APK 빌드 프로세스

### EAS Build 설정 (Expo Application Services)
```powershell
# EAS CLI 설치
npm install -g eas-cli

# 프로젝트에서 EAS 초기화
eas build:configure

# Android APK 빌드 (클라우드)
eas build --platform android --profile preview
```

### 빌드 프로필 설정 (`eas.json`)
```json
{
  "build": {
    "preview": {
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "android": {
        "buildType": "app-bundle"
      }
    }
  }
}
```

---

## 🏪 Google Play Store 등록 절차

### 1. 개발자 계정 등록
1. [Google Play Console](https://play.google.com/console) 접속
2. $25 등록비 결제
3. 개발자 정보 입력

### 2. 앱 등록 준비물

| 항목 | 규격 | 설명 |
|------|------|------|
| **앱 아이콘** | 512x512px PNG | 투명 배경 불가 |
| **기능 그래픽** | 1024x500px | 스토어 상단 배너 |
| **스크린샷** | 최소 2장 | 폰 화면 캡처 |
| **앱 이름** | 최대 30자 | |
| **간단한 설명** | 최대 80자 | |
| **자세한 설명** | 최대 4000자 | |
| **개인정보처리방침 URL** | 필수 | 웹페이지 필요 |

### 3. 콘텐츠 등급 설정
- 설문지 작성 후 자동 등급 부여

### 4. 출시 트랙 선택
- 내부 테스트 → 비공개 테스트 → 프로덕션

> [!TIP]
> **팀 내부용**이라면 "내부 테스트" 트랙으로 등록하면 심사 없이 바로 사용 가능합니다!
> 최대 100명까지 이메일로 초대 가능.

---

## 📅 개발 일정 (예상)

| 단계 | 작업 내용 | 소요 시간 |
|------|----------|----------|
| **Phase 1** | 개발 환경 설정 | 1일 |
| **Phase 2** | 프로젝트 생성 & 기본 구조 | 1일 |
| **Phase 3** | 메인 화면 UI 구현 | 2~3일 |
| **Phase 4** | 검색/필터 기능 구현 | 2~3일 |
| **Phase 5** | Google Sheets API 연동 | 2~3일 |
| **Phase 6** | 상세 화면 & 네비게이션 | 2~3일 |
| **Phase 7** | 테스트 & 버그 수정 | 2~3일 |
| **Phase 8** | APK 빌드 & 배포 | 1~2일 |

---

## ⚡ 다음 액션 아이템

1. [ ] Node.js 설치 확인 또는 설치
2. [ ] Expo CLI 설치
3. [ ] Expo 계정 생성
4. [ ] Android Studio 설치 (선택)
5. [ ] 새 Expo 프로젝트 생성
6. [ ] 현재 Apps Script UI 화면 목록 정리

---

## ❓ 확인 필요 사항

진행 전 아래 사항을 확인해주시면 더 정확한 계획을 세울 수 있습니다:

1. **현재 Apps Script의 주요 화면 개수**는 몇 개인가요?
2. **오프라인 사용**이 필요한가요? (네트워크 없이도 동작)
3. **팀 내부용**으로만 사용할 예정인가요, 아니면 일반 공개할 예정인가요?
4. **푸시 알림** 기능이 필요한가요?
