from io import BytesIO
from typing import List

import pandas as pd
from fastapi import UploadFile
from starlette.exceptions import HTTPException

from app.services.parsers.abstract import BaseParser


class CSVParser(BaseParser):
    async def parse(self, files: list[UploadFile]) -> dict:
        white_list, banned_list, invalid = [], [], []

        for file in files:
            filename_lower = file.filename.lower()
            extracted_links = await self.extract_links_from_file(file)

            if "white" in filename_lower:
                white_list.extend(extracted_links)
            elif "banned" in filename_lower:
                banned_list.extend(extracted_links)
            else:
                invalid.append(filename_lower)

        if invalid:
            self.log_warning(f"Invalid files found: {[file for file in invalid]}")

        return {"white": set(white_list), "banned": set(banned_list)}

    @staticmethod
    async def extract_links_from_file(file: UploadFile) -> List[str]:
        content = await file.read()
        if file.filename.lower().endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        elif file.filename.lower().endswith((".xls", ".xlsx")):
            df = pd.read_excel(BytesIO(content))
        else:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file type: {file.filename}"
            )

        links_column = df.columns[0]
        links = df[links_column].dropna().astype(str).tolist()
        return links


csv_parser = CSVParser()
