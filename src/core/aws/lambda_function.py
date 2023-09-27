from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class Lambda(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='Lambda', short_name='lambda')
        self.client = boto3.client('lambda')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 50

        response = self.client.list_functions(MaxItems=limit)
        resources = self.__list_response_to_resources(response)
        next_marker = response['NextMarker'] if 'NextMarker' in response else None

        while next_marker:
            response = self.client.list_functions(MaxItems=limit, Marker=next_marker)
            resources += self.__list_response_to_resources(response)
            next_marker = response['NextMarker'] if 'NextMarker' in response else None

        return resources

    @staticmethod
    def __list_response_to_resources(response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(name=item['FunctionName'], arn=item['FunctionArn']) for item in response['Functions']
        ]

        return resources

    def get_resource(self, resource_name: str) -> Resource:
        """
        Get a single resource.

        :param resource_name: Name of the resource.
        :return: Resource.
        """
        response = self.client.get_function(
            FunctionName=resource_name
        )

        function_arn = response['Configuration']['FunctionArn']

        return Resource(name=resource_name, arn=function_arn)

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags(Resource=resource.arn)
        tags = response['Tags']
        tags = [
            Tag(key=key_value[0], value=key_value[1])
            for key_value in list(tags.items())
        ]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = {tag.key: tag.value for tag in tags}
        self.client.tag_resource(
            Resource=resource.arn,
            Tags=tags
        )
