from typing import List

import boto3 as boto3

from src.core.aws.base_aws_service import BaseAwsService
from src.helper import filter_helper
from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class ECR(BaseAwsService):

    def __init__(self):
        super().__init__(nice_name='ECR', short_name='ecr')
        self.client = boto3.client('ecr')

    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        name_filter = filter_helper.get_exact_name_filter_value(filters)

        kwargs = {
            'maxResults': 1000,
        }

        if name_filter:
            kwargs['repositoryNames'] = [name_filter] if name_filter else []

        response = self.client.describe_repositories(**kwargs)
        resources = self.__list_response_to_resources(response)
        next_token = response['nextToken'] if 'nextToken' in response else None

        while next_token:
            kwargs['nextToken'] = next_token
            response = self.client.describe_repositories(**kwargs)
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
            Resource(name=item['repositoryName'], arn=item['repositoryArn']) for item in response['repositories']
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
        return f"arn:aws:ecr:eu-west-1:{aws_account_id}:repository/{resource_name}"

    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        response = self.client.list_tags_for_resource(resourceArn=resource.arn)
        tags = [Tag(key=item['Key'], value=item['Value']) for item in response['tags']]

        return tags

    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag the given resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        tags = [{'Key': tag.key, 'Value': tag.value} for tag in tags]
        self.client.tag_resource(resourceArn=resource.arn, tags=tags)
