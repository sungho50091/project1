# 📚 Study Planner App - AI 수행평가 피드백 앱

중·고등학생을 위한 일정 관리 및 AI 기반 수행평가 피드백 애플리케이션

## 🎯 프로젝트 개요

- **주요 기능**: 캘린더 기반 일정 관리, 우선도 설정, AI 수행평가 분석
- **개발 언어**: Python 3.11+
- **UI 프레임워크**: Flet (Flutter 철학 구현)
- **데이터 저장**: SQLite + JSON (하이브리드)
- **외부 API**: OpenAI API

## ✨ 핵심 기능

- ✅ 일정 입력, 수정, 삭제, 캘린더 조회
- ✅ 알람 기능 (OS 레벨 notification)
- ✅ 일정 우선도 설정 및 필터링
- ✅ 공부 계획 작성
- ✅ 계정 관리
- ✅ AI 수행평가 분석 및 개선점 추천

## 📁 프로젝트 구조

```
study_planner_app/
├── app/                    # 메인 애플리케이션
├── core/                   # 비즈니스 로직
├── database/               # 데이터베이스 관리
├── models/                 # 데이터 모델
├── services/               # 외부 서비스 통합
├── utils/                  # 공용 유틸리티
├── data/                   # 로컬 데이터 저장
├── tests/                  # 테스트 코드
├── config/                 # 설정 파일
├── requirements.txt        # 의존성
└── README.md              # 이 파일
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# Python 3.11+ 필수
python --version

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp config/.env.example config/.env
# .env 파일에 OpenAI API Key 입력
```

### 3. 애플리케이션 실행

```bash
python app/main.py
```

## 🛠️ 기술 스택

| 카테고리 | 기술 |
|---------|------|
| UI | Flet (Python) |
| Database | SQLite3 + SQLAlchemy (ORM) |
| API | OpenAI GPT-4 |
| Scheduling | APScheduler |
| Testing | pytest |
| Code Quality | black, pylint |

## 📋 개발 로드맵

### Phase 1: 기초 (1-2주)
- [ ] SQLite 스키마 설계 및 테이블 생성
- [ ] Flet 기본 UI (홈 화면, 네비게이션)
- [ ] Schedule, User 모델 정의

### Phase 2: 핵심 기능 (2-3주)
- [ ] 일정 CRUD (생성, 수정, 삭제, 조회)
- [ ] 캘린더 뷰 구현
- [ ] 우선도 필터링 및 정렬
- [ ] 알람 기능 (OS 레벨 notification)

### Phase 3: AI 통합 (2-3주)
- [ ] OpenAI API 연결
- [ ] 수행평가 텍스트 분석 프롬프트
- [ ] 피드백 JSON 저장
- [ ] 피드백 결과 UI 표시

### Phase 4: 폴리싱 (1주)
- [ ] 오류 처리 및 로깅
- [ ] 단위 테스트 작성
- [ ] 사용자 피드백 반영
- [ ] 배포 (APK 또는 실행파일)

## 📝 커밋 컨벤션

```
feat: 새로운 기능
fix: 버그 수정
refactor: 코드 리팩토링
docs: 문서 작성
test: 테스트 추가
chore: 기타 변경
```

## 👨‍💻 개발 가이드라인

1. **MVC 패턴**: UI와 비즈니스 로직 철저히 분리
2. **단일 책임 원칙**: 각 모듈은 하나의 책임만 수행
3. **테스트 우선**: 기능 구현 후 반드시 테스트 작성
4. **타입 힌트**: 모든 함수에 타입 힌트 사용

## 📧 문의

질문이나 피드백은 Issues에서 등록해주세요.

---

**Made with ❤️ for High School Students**
