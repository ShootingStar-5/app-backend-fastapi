from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from app.core.config import settings
from io import BytesIO
import time


class OCRService:
    """Azure Computer Vision Read API를 사용한 OCR 서비스"""

    def __init__(self):
        if not settings.AZURE_OCR_KEY or not settings.AZURE_OCR_ENDPOINT:
            raise ValueError(
                "AZURE_OCR_KEY and AZURE_OCR_ENDPOINT must be set in .env file"
            )
        
        self.client = ComputerVisionClient(
            settings.AZURE_OCR_ENDPOINT,
            CognitiveServicesCredentials(settings.AZURE_OCR_KEY)
        )

    def extract_text_from_image(self, image_bytes: bytes) -> dict:
        """
        이미지에서 텍스트를 추출합니다.
        
        Args:
            image_bytes: 이미지 파일의 바이트 데이터
            
        Returns:
            dict: {
                "success": bool,
                "text": str,  # 추출된 전체 텍스트
                "lines": List[str],  # 줄 단위 텍스트 리스트
                "message": str
            }
        """
        try:
            # BytesIO로 변환
            image_stream = BytesIO(image_bytes)
            
            # Read API 호출 (비동기 방식)
            read_response = self.client.read_in_stream(image_stream, raw=True)
            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]

            # 결과 대기 (보통 1초 이내 완료)
            while True:
                read_result = self.client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(0.5)

            # 텍스트 추출
            all_text = []
            lines = []
            
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        lines.append(line.text)
                        all_text.append(line.text)

            full_text = "\n".join(all_text)

            if not full_text.strip():
                return {
                    "success": False,
                    "text": "",
                    "lines": [],
                    "message": "이미지에서 텍스트를 찾을 수 없습니다."
                }

            return {
                "success": True,
                "text": full_text,
                "lines": lines,
                "message": "텍스트 추출 성공"
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "lines": [],
                "message": f"OCR 처리 오류: {str(e)}"
            }
