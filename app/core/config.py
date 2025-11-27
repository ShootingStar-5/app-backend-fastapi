# app/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    애플리케이션 전역 설정을 관리하는 클래스입니다.
    환경 변수(.env)를 기반으로 값을 불러옵니다.
    """

    APP_ENV: str = "dev"

    # Azure Computer Vision (OCR) 설정
    AZURE_OCR_KEY: str | None = None
    AZURE_OCR_ENDPOINT: str | None = None

    # Azure Speech Service (STT) 설정
    AZURE_TTS_KEY: str | None = None
    AZURE_TTS_ENDPOINT: str | None = None

    class Config:
        # 프로젝트 루트에 있는 .env 파일을 자동으로 읽게 합니다.
        env_file = ".env"
        env_file_encoding = "utf-8"


# settings 객체를 만들어서 어디서든 import해서 쓸 수 있도록 합니다.
settings = Settings()
