from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class KMS(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='KMS', short_name='kms')
        self.client = boto3.client('kms')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        limit = 1000
        response = self.client.list_aliases(Limit=limit)
        resources = self.__list_response_to_resources(response)
        next_marker = response['Marker'] if 'Marker' in response else None

        while next_marker:
            response = self.client.list_aliases(Limit=limit, Marker=next_marker)
            resources += self.__list_response_to_resources(response)
            next_marker = response['Marker'] if 'Marker' in response else None

        return resources

    def __list_response_to_resources(self, response) -> List[Resource]:
        """
        Convert a List API call response to a list of resources.

        :param response: Response from the List API call.
        :return: List of resources.
        """
        resources = [
            Resource(
                name=item['AliasName'].split('alias/')[1],
                arn=self.client.describe_key(KeyId=item['TargetKeyId'])['KeyMetadata']['Arn']
            )
            for item in response['Aliases'] if 'TargetKeyId' in item
        ]

        return resources

    def get_resource(self, resource_name: str) -> Resource:
        """
        Get a single resource.

        :param resource_name: Name of the resource.
        :return: Resource.
        """
        response = self.client.list_aliases(Limit=1000)
        aliases = response['Aliases']

        for alias_item in aliases:
            if alias_item['AliasName'] == f'alias/{resource_name}':
                resource = Resource(
                    name=alias_item['AliasName'].split('alias/')[-1],
                    arn=self.client.describe_key(KeyId=alias_item['TargetKeyId'])['KeyMetadata']['Arn']
                )

                return resource

        raise Exception(f"Alias '{resource_name}' not found.")

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_resource_tags(KeyId=resource.arn, Limit=50)
        tags = [Tag(key=item['TagKey'], value=item['TagValue']) for item in response['Tags']]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = [{'TagKey': tag.key, 'TagValue': tag.value} for tag in tags]
        self.client.tag_resource(
            KeyId=resource.arn,
            Tags=tags
        )
