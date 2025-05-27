from pydantic import BaseModel
from typing import Optional


class processRequest(BaseModel):
    """
    Request model for processing data.
    """
    file_id: str
    chunk_size: Optional[int] = 100
    chunk_overlap: Optional[int] = 100
    do_reset: Optional[int] = 0