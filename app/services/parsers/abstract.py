from fastapi import UploadFile

from app.core.logger import LogMixin
from app.schemas.schemas import Contract
from app.services.clients.gpt_client import gpt_client


class BaseParser(LogMixin):
    def __init__(self):
        self.gpt_client = gpt_client

    async def parse(self, file: UploadFile) -> str:
        """
        Abstract method to parse a file and extract text content.
        :param file:
        :return:
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_contract_data(self, file_data: str) -> Contract:
        return self.gpt_client.gpt_request(file_data)
