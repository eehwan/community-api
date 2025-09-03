# 게시판 서비스

FastAPI와 PostgreSQL, Redis를 활용한 게시판 서비스입니다.

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

# Cron 설정 (10분마다)
*/10 * * * * cd /path/to/project && make sync-post-count
```

## API 문서

서버 실행 후 http://localhost/docs 에서 Swagger UI를 확인할 수 있습니다.

## 프로젝트 문서

### 아키텍처
- [아키텍처 개요](./docs/아키텍처/아키텍처%20개요.md)
- [데이터베이스 설계](./docs/아키텍처/데이터베이스%20설계.md)  
- [API 설계](./docs/아키텍처/API%20설계.md)

### 구현
- [Redis 캐싱 전략](./docs/구현/Redis%20캐싱%20전략.md)
- [페이지네이션 구현](./docs/구현/페이지네이션%20구현.md)

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