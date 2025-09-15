# 커뮤니티 서비스

FastAPI와 PostgreSQL, Redis를 활용한 커뮤니티 서비스입니다.

## 주요 특징

### 하이브리드 JWT 인증 시스템
- **Stateless Access Token** (5분) + **Stateful Refresh Token** (30일)
- RT Rotation으로 보안 강화
- HttpOnly 쿠키로 XSS 공격 방지
- 다중 기기 세션 관리 및 개별/전체 로그아웃 지원

### Clean Architecture
- 계층 분리를 통한 유지보수성 향상
- Repository Pattern으로 데이터 접근 추상화
- Dependency Injection으로 테스트 용이성 확보

### 성능 최적화
- Redis 기반 게시글 카운트 캐싱
- 효율적인 페이지네이션 (Offset/Cursor 혼합)
- 인덱스 최적화된 쿼리 설계

## 개발 환경 설정

### 요구사항
- Docker & Docker Compose
- Python 3.10+

### 실행 방법

```bash
# 환경 구성 및 빌드
make build

# 서비스 시작
make up

# 로그 확인
make logs

# 서비스 종료
make down
```

### 개발 환경 접속

```bash
# API 컨테이너 쉘 접속
make shell

# Redis CLI 접속
make shell-redis

# PostgreSQL 접속
make shell-postgres
```

## 관리 명령어

### 게시글 수 동기화
Redis에 누적된 게시글 증감량을 DB에 반영합니다.

```bash
# 수동 실행
make sync-post-count
```

향후 Airflow 또는 Cron Job으로 주기적 실행 예정

## 기술 스택

- **FastAPI** - 현대적인 비동기 웹 프레임워크
- **SQLAlchemy** - ORM 및 데이터베이스 추상화  
- **PostgreSQL** - 메인 데이터베이스
- **Redis** - 게시글 카운트 캐싱
- **JWT + Sessions** - 하이브리드 인증 시스템

## API 문서

서버 실행 후 http://localhost/docs 에서 Swagger UI를 확인할 수 있습니다.

## 프로젝트 문서

### 아키텍처
- [아키텍처 개요](./docs/아키텍처/아키텍처%20개요.md)
- [데이터베이스 설계](./docs/아키텍처/데이터베이스%20설계.md)  
- [API 설계](./docs/아키텍처/API%20설계.md)

### 구현
- [하이브리드 JWT 인증 구현](./docs/구현/하이브리드%20JWT%20인증%20구현.md)
- [페이지네이션 구현](./docs/구현/페이지네이션%20구현.md)
- [Redis 캐싱 전략](./docs/구현/Redis%20캐싱%20전략.md)

## 프로젝트 구조

```
docs/               # 프로젝트 문서
app/
├── main.py         # FastAPI 애플리케이션 엔트리포인트
├── entities/       # SQLAlchemy 모델
├── repositories/   # 데이터 접근 계층  
├── services/       # 비즈니스 로직 계층
├── routers/        # API 라우터
├── schemas/        # Pydantic 스키마
├── infra/          # 인프라 설정
├── lib/            # 공통 유틸리티
├── commands/       # 관리 명령어
└── manage.py       # CLI 도구
```