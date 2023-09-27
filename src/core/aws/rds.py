from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class RDS(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='RDS', short_name='rds')
        self.client = boto3.client('rds')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 100
        name_filter = [
            {'Name': 'db-instance-id', 'Values': [filter.value]}
            for filter in filters if filter.key == '@name' and filter.operator == '='
        ]

        response = self.client.describe_db_instances(MaxRecords=limit, Filters=name_filter)
        resources = self.__list_response_to_resources(response)
        next_marker = response['Marker'] if 'Marker' in response else None

        while next_marker:
            response = self.client.describe_db_instances(MaxRecords=limit, Filters=name_filter, Marker=next_marker)
            resources += self.__list_response_to_resources(response)
            next_marker = response['Marker'] if 'Marker' in response else None

        return resources

    @staticmethod
    def __list_response_to_resources(response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(
                name=item['DBInstanceIdentifier'],
                arn=item['DBInstanceArn'],
                tags=[Tag(key=tag['Key'], value=tag['Value']) for tag in item['TagList']]
            )
            for item in response['DBInstances']
        ]

        return resources

    def get_resource(self, resource_name: str) -> Resource:
        """
        Get a single resource.

        :param resource_name: Name of the resource.
        :return: Resource.
        """
        resources = self._list_resources([Filter(key='@name', operator='=', value=resource_name)])

        if resources:
            return resources[0]
        else:
            raise Exception(f"Resource '{resource_name}' not found.")

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        if resource.tags:
            return resource.tags
        else:
            return []

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = [{'Key': tag.key, 'Value': tag.value} for tag in tags]
        self.client.add_tags_to_resource(
            ResourceName=resource.arn,
            Tags=tags
        )
