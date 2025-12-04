from pydantic import BaseModel
from typing import Optional


class MedicationDataResponse(BaseModel):
    """약 정보 응답 스키마"""
    medication_name: str
    total_duration_days: int
    daily_frequency: int
    meal_context: str  # "pre_meal" | "post_meal" | "at_bedtime"
    specific_offset_minutes: int
    special_instructions: Optional[str] = None


class OCRResponse(BaseModel):
    """OCR 텍스트 추출 응답"""
    success: bool
    text: str
    lines: list[str]
    message: str


class MedicationExtractionResponse(BaseModel):
    """약 정보 추출 통합 응답 (OCR + LLM)"""
    success: bool
    ocr_text: str
    medication_data: Optional[MedicationDataResponse] = None
    message: str
