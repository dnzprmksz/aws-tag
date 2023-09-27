from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class ElasticBlockStore(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='Elastic Block Store', short_name='ebs')
        self.client = boto3.client('ec2')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 1000
        tag_filters = [
            {'Name': f'tag:{filter.key}', 'Values': [filter.value]}
            for filter in filters if filter.operator == '='
        ]

        response = self.client.describe_volumes(MaxResults=limit, Filters=tag_filters)
        resources = self.__list_response_to_resources(response)
        next_token = response['NextToken'] if 'NextToken' in response else None

        while next_token:
            response = self.client.describe_volumes(MaxResults=limit, Filters=tag_filters, NextToken=next_token)
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
                name=item['VolumeId'],
                tags=[Tag(key=tag['Key'], value=tag['Value']) for tag in item['Tags']] if 'Tags' in item else [],
                description=f"Volume Type: {item['VolumeType']}"
            )
            for item in response['Volumes']
        ]

        for resource in resources:
            if resource.tags:
                maybe_name_tag = next((tag for tag in resource.tags if tag.key == 'Name'), None)
                if maybe_name_tag:
                    resource.description += f', Name Tag: {maybe_name_tag.value}'

        return resources

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

        self.client.create_tags(
            Resources=[resource.name],
            Tags=tags
        )
