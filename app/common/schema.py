from pydantic import BaseModel
from typing import List


class CandlesWindow(BaseModel):
    updated_time: datetime
    granularity: str
    candle_list: List
