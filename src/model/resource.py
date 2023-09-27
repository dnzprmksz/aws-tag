from dataclasses import dataclass
from typing import List, Optional

from src.model.tag import Tag


@dataclass
class Resource:
    name: str
    arn: Optional[str] = None
    tags: Optional[List[Tag]] = None
    description: Optional[str] = None
