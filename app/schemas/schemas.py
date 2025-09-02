from datetime import datetime
from typing import List

from pydantic import BaseModel


class Domains(BaseModel):
    white: set[str]
    banned: set[str]


class Contract(BaseModel):
    seniority: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    industry: str | None = None


class DataOutput(BaseModel):
    domains: Domains | None = None
    contracts: List[Contract] = []
