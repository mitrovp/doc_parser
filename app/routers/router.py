from typing import List

from fastapi import APIRouter, UploadFile, File

from app.schemas.schemas import DataOutput
from app.services.data_extractor import data_extractor

router = APIRouter(tags=["Parser"])


@router.post("/parse/")
async def extract_documents_data(documents: List[UploadFile] = File(...)) -> DataOutput:
    """
    Extract data from uploaded documents.
    :param documents:
    :return:
    """
    result = await data_extractor.get_data_from_files(documents)
    return result
