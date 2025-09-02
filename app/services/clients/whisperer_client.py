import time

from unstract.llmwhisperer import LLMWhispererClientV2

from app.core.constants import LLM_WHISPERER_URL
from app.core.settings import settings


class WhispererApiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = self.get_client()

    def read_file_data(self, file) -> str:
        raw_result = self.client.whisper(stream=file)
        result = None

        while True:
            status = self.client.whisper_status(whisper_hash=raw_result["whisper_hash"])
            if status["status"] == "processed":
                result = self.client.whisper_retrieve(whisper_hash=raw_result["whisper_hash"])
                break
            time.sleep(2)

        extracted_text = result["extraction"]["result_text"] if result else ""

        return extracted_text

    def get_client(self):
        return LLMWhispererClientV2(
            base_url=LLM_WHISPERER_URL,
            api_key=self.api_key,
        )


whisperer_client = WhispererApiClient(api_key=settings.WHISPERER_API_KEY)
