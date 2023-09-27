from typing import List

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter


def list_resources(service: BaseAwsService, filters: List[Filter]) -> None:
    """
    List the resources.

    :param service: Service to list resources for.
    :param filters: Filters to apply.
    """
    resources = service.list_resources(filters)

    for resource in resources:
        text = f"{resource.name} ({resource.description})" if resource.description else resource.name
        print(text)
