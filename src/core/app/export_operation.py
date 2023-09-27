from typing import List

import pandas as pd

from src.core.aws.base_aws_service import BaseAwsService
from src.helper import file_helper, input_helper
from src.model.filter import Filter


def export_tags(service: BaseAwsService, filters: List[Filter], file_path: str, export_tags: List[str]) -> None:
    """
    Export the resource tags.

    :param service: Service to export resource tags for.
    :param filters: Filters to apply to find resources to be exported.
    :param file_path: File path to export resource tags to.
    :param export_tags: List of tags to export. If empty, export all tags.
    """
    if not file_path:
        print("No file path was provided. Please use --file option.")
        return

    resources = service.list_resources(filters)

    if not resources:
        print(f"No resources were found for {service.nice_name}.")
        return

    if export_tags:
        print("The following tags will be exported.")

        for tag in export_tags:
            print(f"- {tag}")

        print('\n')

    print(f"The following {service.nice_name} resources will be exported.")

    for resource in resources:
        text = f"{resource.name} ({resource.description})" if resource.description else resource.name
        print(f"- {text}")

    print('\n')
    answer = input_helper.get_user_input()

    if answer == 'y':
        resource_tags = []

        for resource in resources:
            try:
                tags = service.get_resource_tags(resource)
                tags_dict = {
                    tag.key: tag.value
                    for tag in tags
                    if not export_tags or tag.key in export_tags or tag.key in ['@name', '@service']
                }
                resource_tags.append(tags_dict)
            except Exception as exception:
                print(f"Error while getting tags for resource {resource.name}: {exception}")

        df = pd.DataFrame(resource_tags)
        df = __add_service_column(df, service)
        df = __add_export_tags_columns(df, export_tags)
        df = __order_df_columns(df)
        df = __sort_df(df)
        file_helper.write_df_to_csv(df, file_path)

        print(f"\nCompleted exporting {len(resource_tags)} resources to {file_path}")
    else:
        print("\nExporting cancelled.")


def __add_service_column(df: pd.DataFrame, service: BaseAwsService) -> pd.DataFrame:
    """
    Add a column to the given DataFrame with the service short name.

    :param df: DataFrame to add column to.
    :param service: Service to add column for.
    :return: DataFrame with added column.
    """
    df['@service'] = service.short_name

    return df


def __add_export_tags_columns(df: pd.DataFrame, export_tags: List[str]) -> pd.DataFrame:
    """
    Add columns to the given DataFrame for the given export tags, if not already exists.

    :param df: DataFrame to add columns to.
    :param export_tags: Tags to add columns for.
    :return: DataFrame with added columns.
    """
    for tag in export_tags:
        if tag not in df.columns:
            df[tag] = ''

    return df


def __order_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Order the columns of the given DataFrame to get '@name' column as the first column.

    :param df: DataFrame to order columns of.
    :return: DataFrame with ordered columns.
    """
    cols = df.columns.values.tolist()
    cols.remove('@service')
    cols.remove('@name')
    cols.sort()
    cols.insert(0, '@service')
    cols.insert(1, '@name')
    df = df[cols]

    return df


def __sort_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort the given DataFrame by the '@name' column.

    :param df: DataFrame to sort.
    :return: Sorted DataFrame.
    """
    df = df.sort_values(by=['@name'])

    return df
