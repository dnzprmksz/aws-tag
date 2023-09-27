from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class SNS(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='SNS', short_name='sns')
        self.client = boto3.client('sns')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        response = self.client.list_topics()
        resources = self.__list_response_to_resources(response)
        next_token = response['NextToken'] if 'NextToken' in response else None

        while next_token:
            response = self.client.list_topics(NextToken=next_token)
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
            Resource(
                name=item['TopicArn'].split(':')[-1],
                arn=item['TopicArn']
            ) for item in response['Topics']
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
            arn=self.__get_resource_arn(resource_name)
        )

        return resource

    @staticmethod
    def __get_resource_arn(resource_name: str) -> str:
        """
        Get the ARN for a resource.

        :param resource_name: Name of the resource.
        :return: ARN of the resource.
        """
        aws_account_id = boto3.client('sts').get_caller_identity().get('Account')
        return f"arn:aws:sns:eu-west-1:{aws_account_id}:{resource_name}"

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags_for_resource(ResourceArn=resource.arn)

        if 'Tags' in response:
            tags = [
                Tag(key=item['Key'], value=item['Value']) for item in response['Tags']
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
        tags = [{'Key': tag.key, 'Value': tag.value} for tag in tags]
        self.client.tag_resource(ResourceArn=resource.arn, Tags=tags)
