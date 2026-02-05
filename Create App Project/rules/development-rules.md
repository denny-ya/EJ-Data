# 📋 개발 진행 규칙 (Development Rules)

> 이 문서는 앱 개발 시 준수해야 할 코딩 규칙과 협업 규칙을 정의합니다.

---

## 1. 코드 작성 규칙

### 1.1 네이밍 컨벤션

| 항목 | 규칙 | 예시 |
|------|------|------|
| **컴포넌트** | PascalCase | `SearchBar.tsx`, `ListItem.tsx` |
| **함수** | camelCase | `handleSearch()`, `formatDate()` |
| **상수** | UPPER_SNAKE_CASE | `API_URL`, `MAX_ITEMS` |
| **타입/인터페이스** | PascalCase | `UserSettings`, `ApiResponse` |
| **파일명 (컴포넌트)** | PascalCase.tsx | `FilterModal.tsx` |
| **파일명 (유틸)** | camelCase.ts | `dateFormat.ts` |
| **폴더명** | camelCase | `components`, `hooks` |

### 1.2 파일 구조 규칙

```
✅ 좋은 예:
- 하나의 컴포넌트 = 하나의 파일
- 관련 스타일은 같은 파일 내 StyleSheet로 정의
- 재사용 컴포넌트는 components/ 폴더에 배치

❌ 나쁜 예:
- 한 파일에 여러 컴포넌트 정의
- 인라인 스타일 남용
- 비즈니스 로직과 UI 혼합
```

### 1.3 코드 포맷팅

- **들여쓰기**: 2 spaces (탭 사용 금지)
- **세미콜론**: 사용
- **따옴표**: 싱글 쿼트 `'` 사용
- **줄 길이**: 최대 100자
- **빈 줄**: 함수 사이 1줄, import 그룹 사이 1줄

### 1.4 주석 규칙

```typescript
// ✅ 함수에 JSDoc 주석 작성
/**
 * 날짜를 YYYY-MM-DD 형식으로 변환
 * @param date - 변환할 날짜
 * @returns 포맷팅된 날짜 문자열
 */
function formatDate(date: Date): string { ... }

// ✅ 복잡한 로직에 설명 주석
// 검색 결과가 없으면 빈 배열 반환
if (!results.length) return [];

// ❌ 불필요한 주석 금지
const count = 0; // count를 0으로 설정 (불필요)
```

---

## 2. Git 커밋 메시지 규칙

### 2.1 커밋 메시지 형식

```
<type>: <subject>

[optional body]
```

### 2.2 Type 종류

| Type | 설명 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | `feat: 검색 기능 구현` |
| `fix` | 버그 수정 | `fix: 검색 결과 없음 오류 수정` |
| `style` | UI/스타일 변경 | `style: 버튼 색상 변경` |
| `refactor` | 코드 리팩토링 | `refactor: API 호출 로직 분리` |
| `docs` | 문서 수정 | `docs: README 업데이트` |
| `chore` | 기타 작업 | `chore: 패키지 업데이트` |
| `test` | 테스트 추가/수정 | `test: 검색 기능 테스트 추가` |

### 2.3 커밋 메시지 규칙

- ✅ 한글 또는 영어로 통일 (혼용 금지)
- ✅ 제목은 50자 이내
- ✅ 제목 끝에 마침표 금지
- ✅ 명령형으로 작성 (추가, 수정, 삭제)

---

## 3. 브랜치 전략

### 3.1 브랜치 구조

```
main (프로덕션)
  └── develop (개발 통합)
        ├── feature/기능명 (기능 개발)
        ├── fix/버그명 (버그 수정)
        └── hotfix/긴급수정 (긴급 수정)
```

### 3.2 브랜치 네이밍

| 브랜치 | 형식 | 예시 |
|--------|------|------|
| 기능 개발 | `feature/기능명` | `feature/search`, `feature/login` |
| 버그 수정 | `fix/버그명` | `fix/search-error` |
| 긴급 수정 | `hotfix/설명` | `hotfix/api-url-fix` |

### 3.3 머지 규칙

1. `feature/*` → `develop`: PR 생성 후 리뷰 완료 시 머지
2. `develop` → `main`: 배포 준비 완료 시 머지
3. `hotfix/*` → `main`: 긴급 시 직접 머지 가능

---

## 4. 코드 리뷰 규칙

### 4.1 PR 생성 시 필수 항목

- [ ] 변경 사항 설명
- [ ] 테스트 완료 여부
- [ ] 스크린샷 (UI 변경 시)

### 4.2 리뷰어 체크리스트

- [ ] 코드가 요구사항을 충족하는가?
- [ ] 네이밍 컨벤션을 준수하는가?
- [ ] 불필요한 코드가 없는가?
- [ ] 에러 처리가 적절한가?

---

## 5. 기술 스택 규칙

| 분류 | 기술 | 비고 |
|------|------|------|
| 프레임워크 | React Native + Expo | 필수 |
| 언어 | TypeScript | 필수 |
| 상태관리 | Zustand | 전역 상태 |
| 스타일링 | StyleSheet | RN 기본 |
| API 통신 | fetch | 기본 사용 |
| 로컬 저장소 | AsyncStorage | 기본 사용 |
