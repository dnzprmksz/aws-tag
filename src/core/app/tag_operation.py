from typing import List

from src.core.aws.base_aws_service import BaseAwsService
from src.helper import input_helper
from src.model.filter import Filter
from src.model.tag import Tag


def tag_resources(service: BaseAwsService, filters: List[Filter], tags: List[Tag]) -> None:
    """
    Tag the resources.

    :param service: Service to tag resources for.
    :param filters: Filters to apply to find resources to be tagged.
    :param tags: Tags to apply to resources.
    """
    if not tags:
        print("No tags were provided. Please use --tag option.")
        return

    resources = service.list_resources(filters)

    if not resources:
        print(f"No resources were found for {service.nice_name}.")
        return

    print("The following tags will be applied.")

    for tag in tags:
        print(f'- {tag}')

    print(f"\nThe following {service.nice_name} resources will be tagged.")

    for resource in resources:
        print(f'- {resource.name}')

    print('\n')
    answer = input_helper.get_user_input()

    if answer == 'y':
        service.tag_resources(resources, tags)
        print(f"\nCompleted tagging {len(resources)} resources.")
    else:
        print("\nTagging cancelled.")
