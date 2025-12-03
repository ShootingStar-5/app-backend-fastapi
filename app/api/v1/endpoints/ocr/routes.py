from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ocr.service import OCRService
from app.services.ocr.llm_service import MedicationLLMService
from app.schemas.medication_schema import (
    OCRResponse,
    MedicationExtractionResponse,
    MedicationDataResponse
)

router = APIRouter()

# 서비스 인스턴스 생성
ocr_service = OCRService()
llm_service = MedicationLLMService()


@router.post("/extract-text", response_model=OCRResponse)
async def extract_text_from_image(file: UploadFile = File(...)):
    """
    이미지에서 텍스트만 추출 (OCR only)
    
    - **file**: 약봉투 이미지 파일 (JPEG, PNG 등)
    """
    try:
        # 파일 읽기
        image_bytes = await file.read()
        
        # OCR 처리
        result = ocr_service.extract_text_from_image(image_bytes)
        
        return OCRResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR 처리 중 오류 발생: {str(e)}")


@router.post("/extract-medication", response_model=MedicationExtractionResponse)
async def extract_medication_from_image(file: UploadFile = File(...)):
    """
    약봉투 이미지에서 약 정보 추출 (OCR + LLM 통합 파이프라인)
    
    - **file**: 약봉투 이미지 파일 (JPEG, PNG 등)
    
    Returns:
        - ocr_text: 추출된 텍스트
        - medication_data: 구조화된 약 정보 (JSON)
    """
    try:
        # 1. OCR로 텍스트 추출
        image_bytes = await file.read()
        ocr_result = ocr_service.extract_text_from_image(image_bytes)
        
        if not ocr_result["success"]:
            return MedicationExtractionResponse(
                success=False,
                ocr_text="",
                medication_data=None,
                message=ocr_result["message"]
            )
        
        ocr_text = ocr_result["text"]
        
        # 2. LLM으로 약 정보 파싱
        llm_result = llm_service.extract_medication_info(ocr_text)
        
        if not llm_result["success"]:
            return MedicationExtractionResponse(
                success=False,
                ocr_text=ocr_text,
                medication_data=None,
                message=f"LLM 파싱 실패: {llm_result['message']}"
            )
        
        # 3. 응답 생성
        medication_data = MedicationDataResponse(**llm_result["data"])
        
        return MedicationExtractionResponse(
            success=True,
            ocr_text=ocr_text,
            medication_data=medication_data,
            message="약 정보 추출 성공"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"약 정보 추출 중 오류 발생: {str(e)}"
        )
