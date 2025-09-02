from typing import List
from fastapi import UploadFile

from app.core.logger import LogMixin
from app.schemas.schemas import Domains, DataOutput
from app.services.parsers.csv_parser import csv_parser
from app.services.parsers.doc_parser import doc_parser
from app.services.parsers.image_parser import image_parser
from app.services.parsers.pdf_parser import pdf_parser

FILE_TYPE_TO_PARSER_MAP = {
    "pdf": pdf_parser,
    "image": image_parser,
    "doc": doc_parser,
    "table": csv_parser,
}


class DocumentDataExtractor(LogMixin):
    async def get_data_from_files(self, files: List[UploadFile]) -> DataOutput:
        """Extract data from a list of uploaded files and return structured data."""

        contracts = []
        domains = None
        try:
            sorted_files = self.sort_files(files)

            for key, file_list in sorted_files.items():
                if not file_list:
                    continue

                parser = FILE_TYPE_TO_PARSER_MAP.get(key)
                self.log(f"Using parser for {key}: {parser}")

                files_data = await parser.parse(file_list) if parser else None

                if key == "table" and files_data:
                    domains = Domains(**files_data)
                else:
                    contracts.extend(files_data or [])

        except Exception as e:
            self.log_error(f"Error processing files: {e}")

        return DataOutput(contracts=contracts, domains=domains)

    def sort_files(self, files: List[UploadFile]) -> dict:
        """Sort files into categories based on their extensions."""
        file_categories = {}

        for file in files:
            filename_lower = file.filename.lower()
            if filename_lower.endswith(".pdf"):
                file_categories.setdefault("pdf", []).append(file)

            elif filename_lower.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                file_categories.setdefault("image", []).append(file)

            elif filename_lower.endswith((".doc", ".docx", ".odt")):
                file_categories.setdefault("doc", []).append(file)

            elif filename_lower.endswith((".csv", ".xls", ".xlsx")):
                file_categories.setdefault("table", []).append(file)

            else:
                self.log_warning(f"Unsupported file type: {file.filename}")

        return file_categories


data_extractor = DocumentDataExtractor()
