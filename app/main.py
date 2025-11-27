# app/main.py

from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    애플리케이션 팩토리 함수.
    - FastAPI 인스턴스를 만들고
    - 라우터를 등록하고
    - 필요한 초기화 작업을 여기서 수행합니다.
    """
    app = FastAPI(
        title="Medicine Management Backend",
        description="의약품 관리 앱 FastAPI 백엔드 서버 (OCR/STT)",
        version="0.2.0",
    )

    # TODO: API 라우터 등록
    # app.include_router(ocr_router.router, prefix="/api/v1")
    # app.include_router(stt_router.router, prefix="/api/v1")

    return app


app = create_app()
