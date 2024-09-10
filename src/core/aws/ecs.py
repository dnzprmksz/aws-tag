from typing import List

import boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class ECS(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='ECS', short_name='ecs')
        self.client = boto3.client('ecs')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        kwargs = {
            'maxResults': 100,
        }

        response = self.client.list_clusters(**kwargs)
        resources = self.__list_response_to_resources(response)
        next_token = response['nextToken'] if 'nextToken' in response else None

        while next_token:
            kwargs['nextToken'] = next_token
            response = self.client.list_clusters(**kwargs)
            resources += self.__list_response_to_resources(response)
            next_token = response['nextToken'] if 'nextToken' in response else None

        return resources

    @staticmethod
    def __list_response_to_resources(response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(name=item.split('/')[-1], arn=item)
            for item in response['clusterArns']
        ]

        return resources

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags_for_resource(resourceArn=resource.arn)
        tags = [Tag(key=item['key'], value=item['value']) for item in response['tags']]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag the given resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        self.client.tag_resource(
            resourceArn=resource.arn,
            tags=[{'key': tag.key, 'value': tag.value} for tag in tags]
        )
