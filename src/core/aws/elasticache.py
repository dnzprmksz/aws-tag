from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.helper import filter_helper
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class ElastiCache(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='ElastiCache', short_name='elasticache')
        self.client = boto3.client('elasticache')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 100
        name_filter = filter_helper.get_exact_name_filter_value(filters)

        response = self.client.describe_cache_clusters(MaxRecords=limit, CacheClusterId=name_filter)
        resources = self.__list_response_to_resources(response)
        marker = response['Marker'] if 'Marker' in response else None

        while marker:
            response = self.client.describe_cache_clusters(MaxRecords=limit, CacheClusterId=name_filter, Marker=marker)
            resources += self.__list_response_to_resources(response)
            marker = response['Marker'] if 'Marker' in response else None

        return resources

    @staticmethod
    def __list_response_to_resources(response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(name=item['CacheClusterId'], arn=item['ARN']) for item in response['CacheClusters']
        ]

        return resources

    def get_resource(self, resource_name: str) -> Resource:
        """
        Get a single resource.

        :param resource_name: Name of the resource.
        :return: Resource.
        """
        response = self._list_resources([Filter(key='@name', operator='=', value=resource_name)])

        if response:
            return response[0]
        else:
            raise Exception(f'Resource {resource_name} not found')

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags_for_resource(ResourceName=resource.arn)
        tags = [Tag(key=tag['Key'], value=tag['Value']) for tag in response['TagList']]

        return tags

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
