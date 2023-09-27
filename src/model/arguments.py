from dataclasses import dataclass
from typing import List

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.operation import Operation
from src.model.tag import Tag


@dataclass
class Arguments:
    operation: Operation
    service: BaseAwsService
    filters: List[Filter]
    tags: List[Tag]
    file_path: str
    export_tags: List[str]
