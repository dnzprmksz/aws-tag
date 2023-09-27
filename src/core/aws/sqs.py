from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.helper import filter_helper
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class SQS(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='SQS', short_name='sqs')
        self.client = boto3.client('sqs')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 1000
        name_prefix = filter_helper.get_name_prefix_filter_value(filters)

        response = self.client.list_queues(MaxResults=limit, QueueNamePrefix=name_prefix)
        resources = self.__list_response_to_resources(response)
        next_token = response['NextToken'] if 'NextToken' in response else None

        while next_token:
            response = self.client.list_queues(MaxResults=limit, QueueNamePrefix=name_prefix, NextToken=next_token)
            resources += self.__list_response_to_resources(response)
            next_token = response['NextToken'] if 'NextToken' in response else None

        return resources

    @staticmethod
    def __list_response_to_resources(response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(name=item.split('/')[-1]) for item in response['QueueUrls']
        ]

        return resources

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_queue_tags(QueueUrl=resource.name)

        if 'Tags' in response:
            tags = response['Tags']
            tags = [
                Tag(key=key_value[0], value=key_value[1])
                for key_value in list(tags.items())
            ]
        else:
            tags = []

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = {tag.key: tag.value for tag in tags}
        self.client.tag_queue(
            QueueUrl=resource.name,
            Tags=tags
        )
