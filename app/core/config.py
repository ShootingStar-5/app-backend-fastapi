from typing import List, Union
from pydantic import AnyHttpUrl, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 전역 설정을 관리하는 클래스"""
    
    # Core Settings
    PROJECT_NAME: str = "Yakkobak"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    APP_ENV: str = "dev"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # Authentication
    SECRET_KEY: str = "changethis"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Azure Computer Vision (OCR)
    AZURE_OCR_KEY: str | None = None
    AZURE_OCR_ENDPOINT: str | None = None

    # Azure Speech Service (STT)
    AZURE_SPEECH_KEY: str | None = None
    AZURE_SPEECH_REGION: str | None = None
    AZURE_SPEECH_ENDPOINT: str | None = None
    AZURE_TTS_KEY: str | None = None
    AZURE_TTS_ENDPOINT: str | None = None

    # Azure OpenAI (LLM)
    AZURE_OPENAI_KEY: str | None = None
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4o"

    # RAG Settings
    FOOD_SAFETY_API_KEY: str = ""
    FOOD_SAFETY_BASE_URL: str = 'http://openapi.foodsafetykorea.go.kr/api'

    # ElasticSearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ES_HOST: str = 'localhost'
    ES_PORT: int = 9200
    ES_INDEX_NAME: str = 'health_supplements'
    
    # Embeddings
    EMBEDDING_MODEL: str = 'jhgan/ko-sroberta-multitask'
    EMBEDDING_DIM: int = 768
    
    # Search
    DEFAULT_TOP_K: int = 5
    VECTOR_WEIGHT: float = 0.8
    KEYWORD_WEIGHT: float = 0.2
    
    # Data Collection
    API_BATCH_SIZE: int = 1000
    API_REQUEST_DELAY: float = 0.5

    # Google SERP API
    SERP_API_KEY: str = ""
    SERP_API_ENABLED: bool = False
    SERP_MAX_RESULTS: int = 5
    SERP_TIMEOUT: int = 5

    # Google Gemini LLM
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = 'gemini-pro'
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_OUTPUT_TOKENS: int = 500

    # Weights
    RAG_WEIGHT: float = 0.5
    GEMINI_WEIGHT: float = 0.5

    # Output
    MAX_RESPONSE_LENGTH: int = 200

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_TO_ELASTICSEARCH: bool = True
    LOG_ES_INDEX: str = "yakkobak-logs"

    # Docker Settings
    DOCKER_USERNAME: str = ""

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"  # 추가 필드 허용 (Pydantic v2)
    )


# settings 객체를 만들어서 어디서든 import해서 쓸 수 있도록 합니다.
settings = Settings()
