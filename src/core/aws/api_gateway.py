from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class ApiGateway(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='Api Gateway', short_name='agw')
        self.client = boto3.client('apigateway')
        self.all_resources = self._list_resources(filters=[])

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 500
        response = self.client.get_rest_apis(limit=limit)
        resources = self.__list_response_to_resources(response)
        position = response['position'] if 'position' in response else None

        while position:
            response = self.client.get_rest_apis(limit=limit, position=position)
            resources += self.__list_response_to_resources(response)
            position = response['position'] if 'position' in response else None

        return resources

    def __list_response_to_resources(self, response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(
                name=item['name'],
                arn=self.get_resource_arn(item['id']),
                tags=[
                    Tag(key=key_value[0], value=key_value[1])
                    for key_value in list(
                        item['tags'].items() if 'tags' in item else []
                    )
                ]
            )
            for item in response['items']
        ]

        return resources

    def get_resource_arn(self, rest_api_id: str) -> str:
        """
        Get the ARN for a resource.

        :param rest_api_id: ID of the resource.
        :return: ARN of the resource.
        """
        return f"arn:aws:apigateway:{self.client.meta.region_name}::/restapis/{rest_api_id}"

    def get_resource(self, resource_name: str) -> Resource:
        """
        Get a single resource.

        :param resource_name: Name of the resource.
        :return: Resource.
        """
        response = self.all_resources
        resource = next((item for item in response if item.name == resource_name), None)

        if resource:
            return resource
        else:
            raise Exception(f"Resource '{resource_name}' not found")

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
        tags = {tag.key: tag.value for tag in tags}

        self.client.tag_resource(
            resourceArn=resource.arn,
            tags=tags
        )
