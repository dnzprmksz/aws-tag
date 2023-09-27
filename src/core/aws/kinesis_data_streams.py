from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class KinesisDataStreams(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='Kinesis Data Streams', short_name='kds')
        self.client = boto3.client('kinesis')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 1000
        response = self.client.list_streams(Limit=limit)
        resources = self.__list_response_to_resources(response)

        while response['HasMoreStreams']:
            response = self.client.list_streams(Limit=limit, ExclusiveStartStreamName=resources[-1].name)
            resources += self.__list_response_to_resources(response)

        return resources

    @staticmethod
    def __list_response_to_resources(response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(name=item['StreamName'], arn=item['StreamARN'])
            for item in response['StreamSummaries']
        ]

        return resources

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags_for_stream(StreamName=resource.name, Limit=50)
        tags = response['Tags']
        tags = [Tag(tag['Key'], tag['Value']) for tag in tags]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = {tag.key: tag.value for tag in tags}
        self.client.add_tags_to_stream(
            StreamName=resource.name,
            Tags=tags
        )
