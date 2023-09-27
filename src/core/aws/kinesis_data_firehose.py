from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class KinesisDataFirehose(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='Kinesis Data Firehose', short_name='kdf')
        self.client = boto3.client('firehose')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 1000
        response = self.client.list_delivery_streams(Limit=limit)
        resources = self.__list_response_to_resources(response)

        while response['HasMoreDeliveryStreams']:
            response = self.client.list_delivery_streams(Limit=limit,
                                                         ExclusiveStartDeliveryStreamName=resources[-1].name)
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
            Resource(name=stream_name) for stream_name in response['DeliveryStreamNames']
        ]

        return resources

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags_for_delivery_stream(DeliveryStreamName=resource.name, Limit=50)
        tags = response['Tags']
        tags = [Tag(tag['Key'], tag['Value']) for tag in tags]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = [{'Key': tag.key, 'Value': tag.value} for tag in tags]
        self.client.tag_delivery_stream(
            DeliveryStreamName=resource.name,
            Tags=tags
        )
