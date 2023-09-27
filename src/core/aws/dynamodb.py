from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class DynamoDB(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='DynamoDB', short_name='dynamodb')
        self.client = boto3.client('dynamodb')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 100
        response = self.client.list_tables(Limit=limit)
        resources = self.__list_response_to_resources(response)
        last_table = response['LastEvaluatedTableName'] if 'LastEvaluatedTableName' in response else None

        while last_table:
            response = self.client.list_tables(Limit=limit, ExclusiveStartTableName=last_table)
            resources += self.__list_response_to_resources(response)
            last_table = response['LastEvaluatedTableName'] if 'LastEvaluatedTableName' in response else None

        return resources

    def __list_response_to_resources(self, response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(
                name=table_name,
                arn=self.client.describe_table(TableName=table_name)['Table']['TableArn'],
            )
            for table_name in response['TableNames']
        ]

        return resources

    def get_resource(self, resource_name: str) -> Resource:
        """
        Get a single resource.

        :param resource_name: Name of the resource.
        :return: Resource.
        """
        resource = Resource(
            name=resource_name,
            arn=self.client.describe_table(TableName=resource_name)['Table']['TableArn'],
        )

        return resource

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags_of_resource(ResourceArn=resource.arn)
        tags = [Tag(key=tag['Key'], value=tag['Value']) for tag in response['Tags']]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = [{'Key': tag.key, 'Value': tag.value} for tag in tags]
        self.client.tag_resource(
            ResourceArn=resource.arn,
            Tags=tags
        )
