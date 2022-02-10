from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class ContentCreate(BaseModel):
    content: str
