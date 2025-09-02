import io

from fastapi import UploadFile

from app.schemas.schemas import Contract
from app.services.clients.whisperer_client import whisperer_client
from app.services.parsers.abstract import BaseParser


class PdfParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.whisperer_client = whisperer_client

    async def parse(self, files: list[UploadFile]) -> list[Contract]:
        result = []
        for file in files:
            file_bytes = await file.read()
            raw_data = self.read_file_data(io.BytesIO(file_bytes))
            contract = self.gpt_client.gpt_request(raw_data)
            result.append(contract)
        return result

    def read_file_data(self, file: io.BytesIO) -> str:
        extracted_text = self.whisperer_client.read_file_data(file)
        return extracted_text


pdf_parser = PdfParser()
