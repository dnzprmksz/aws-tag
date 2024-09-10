from typing import List

import boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class ELB(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='ELB', short_name='elb')
        self.client = boto3.client('elb')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 400
        response = self.client.describe_load_balancers(PageSize=limit)
        resources = self.__list_response_to_resources(response)

        while 'NextMarker' in response:
            response = self.client.describe_load_balancers(Marker=response['NextMarker'])
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
            Resource(name=item['LoadBalancerName'])
            for item in response['LoadBalancerDescriptions']
        ]

        return resources

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.describe_tags(LoadBalancerNames=[resource.name])
        tags = response['TagDescriptions'][0]['Tags']
        tags = [Tag(tag['Key'], tag['Value']) for tag in tags]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag the given resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        self.client.add_tags(
            LoadBalancerNames=[resource.name],
            Tags=[{'Key': tag.key, 'Value': tag.value} for tag in tags]
        )
