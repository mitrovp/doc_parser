from openai import OpenAI

from app.core.constants import GPT_MODEL_VERSION
from app.core.settings import settings
from app.schemas.schemas import Contract


class OpenaiAPIClient:
    def __init__(self):
        self.client = self.get_openai_client()

    @staticmethod
    def get_openai_client() -> OpenAI:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

        return OpenAI(api_key=settings.OPENAI_API_KEY)

    def gpt_request(self, file_data: str) -> Contract:
        response = self.client.responses.parse(
            model=GPT_MODEL_VERSION,
            input=[
                {"role": "system", "content": "You are a helpful assistant that "
                                              "extracts structured data from contracts."},
                {
                    "role": "user",
                    "content": file_data,
                },
            ],
            text_format=Contract,
        )
        result = response.output_parsed
        return result


gpt_client = OpenaiAPIClient()
