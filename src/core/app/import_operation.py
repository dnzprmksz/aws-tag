from collections import defaultdict
from typing import List, Dict

import pandas as pd

from src.core.aws.base_aws_service import BaseAwsService
from src.helper import file_helper, input_helper
from src.factory.service_factory import ServiceFactory
from src.model.resource_tags import ResourceTags
from src.model.tag import Tag


def import_tags(file_path: str) -> None:
    """
    Import the resource tags.

    :param service: Service to import resource tags for.
    :param file_path: File path to import resource tags from.
    """
    if not file_path:
        print("No file path was provided. Please use --file option.")
        return

    file_helper.validate_file_exists(file_path)

    df = file_helper.read_csv_to_df(file_path)
    service_resource_tags = __df_to_resource_tags(df)

    print(f"The following services are found.")

    for service in service_resource_tags:
        print(f'- {service.nice_name}')

    for service in service_resource_tags:
        print(f"\nThe following {service.nice_name} resources will be tagged.\n")
        resource_tags_list = service_resource_tags[service]

        for resource_tags in resource_tags_list:
            print(str(resource_tags) + '\n\n')

        answer = input_helper.get_user_input()

        if answer == 'y':
            for resource_tags in resource_tags_list:
                service.tag_resource(resource_tags.resource, resource_tags.tags)

            print(f"\nCompleted tagging {len(resource_tags_list)} resources.")
        else:
            print("\nTagging cancelled.")


def __df_to_resource_tags(df: pd.DataFrame) -> Dict[BaseAwsService, List[ResourceTags]]:
    """
    Convert the given DataFrame to a list of resource tags per service.

    :param df: DataFrame of tags.
    :return: List of resource tags per service.
    """
    resource_names = df['@name'].values.tolist()
    service_names = df['@service'].values.tolist()

    tags_df = df.drop(columns=['@service', '@name']).fillna('')

    cols = tags_df.columns.values.tolist()
    rows = tags_df.values.tolist()

    service_resource_tags = defaultdict(list)

    for service_name, resource_name, row in zip(service_names, resource_names, rows):
        tags = []

        for tag_value, tag_key in zip(row, cols):

            if tag_value:
                tag = Tag(str(tag_key), str(tag_value))
                tags.append(tag)

        service = ServiceFactory().get_service(service_name)
        resource = service.get_resource(resource_name)
        resource_tags = ResourceTags(resource, tags)
        service_resource_tags[service].append(resource_tags)

    return service_resource_tags
