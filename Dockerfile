# FastAPI 애플리케이션용 Dockerfile
# Multi-stage build with pre-downloaded models for faster startup

# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /build

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 🚀 모델 미리 다운로드 (재시작 시간 단축)
RUN python -c "from sentence_transformers import SentenceTransformer; \
    print('Downloading model...'); \
    model = SentenceTransformer('jhgan/ko-sroberta-multitask'); \
    print('Model downloaded successfully!')"

# Stage 2: Runtime
FROM python:3.12-slim

# 작업 디렉토리를 프로젝트 루트로 설정
WORKDIR /workspace

# 시스템 의존성 (런타임만)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Builder에서 설치한 패키지 복사
COPY --from=builder /root/.local /root/.local

# 🚀 Builder에서 다운로드한 모델 캐시 복사
COPY --from=builder /root/.cache /root/.cache

ENV PATH=/root/.local/bin:$PATH

# Python이 .pyc 파일을 생성하지 않도록 설정
ENV PYTHONDONTWRITEBYTECODE=1

# Python 출력을 버퍼링하지 않도록 설정
ENV PYTHONUNBUFFERED=1

# PYTHONPATH 설정 - app 디렉토리를 Python 모듈 경로에 추가
ENV PYTHONPATH=/workspace

# 애플리케이션 코드 복사
COPY . .

# 로그 디렉토리 생성
RUN mkdir -p logs

# 포트 노출
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# 실행 명령 - app.main:app 형식으로 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
