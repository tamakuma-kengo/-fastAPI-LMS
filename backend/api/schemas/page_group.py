from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class PageGroupCreate(BaseModel):
    flow_id: int
    order: int
    shuffle: Optional[bool] = False
    num_of_show: Optional[int] = None

class PageGroupFlowPagesCreate(BaseModel):
    pagegroup_id: int
    flowpage_id: int
    order: int
