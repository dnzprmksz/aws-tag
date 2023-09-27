from abc import ABC, abstractmethod
from typing import List

from src.model.filter import Filter
from src.model.resource import Resource
from src.model.tag import Tag


class BaseAwsService(ABC):

    def __init__(self, nice_name: str, short_name: str):
        self.nice_name = nice_name
        self.short_name = short_name

    def list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List all resources that match the given filters.

        :param filters: List of filters to apply to the resources.
        :return: List of resources that match the filters.
        """
        tag_filters = [filter for filter in filters if filter.key != '@name']
        resources = self._list_resources(tag_filters)
        filtered_resources = self.__filter_resources(resources, filters)

        return filtered_resources

    def get_resource(self, resource_name: str) -> Resource:
        """
        Get a single resource.

        :param resource_name: Name of the resource.
        :return: Resource.
        """
        return Resource(name=resource_name)

    def get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.
        Additionally adds the resource name as a tag with the key '@name'.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        tags = self._get_resource_tags(resource)
        tags.append(Tag("@name", resource.name))

        return tags

    def tag_resources(self, resources: List[Resource], tags: List[Tag]) -> None:
        """
        Tag multiple resources with the given tags.

        :param resources: Resources.
        :param tags: List of tags to apply to the resources.
        """
        for resource in resources:
            self.tag_resource(resource, tags)
            print(f"Tagged resource: {resource.name}")

    @abstractmethod
    def tag_resource(self, resource: Resource, tags: List[Tag]) -> None:
        """
        Tag a resource with the given tags.

        :param resource: Resource.
        :param tags: List of tags to apply to the resource.
        """
        raise NotImplementedError()

    @abstractmethod
    def _list_resources(self, filters: List[Filter]) -> List[Resource]:
        """
        List resources for the service.

        :param filters: List of filters to pass to AWS API, if supported.
        :return: List of resources.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_resource_tags(self, resource: Resource) -> List[Tag]:
        """
        Get all tags for the given resource.

        :param resource: Resource.
        :return: List of tags for the resource.
        """
        raise NotImplementedError()

    def __filter_resources(self, resources: List[Resource], filters: List[Filter]) -> List[Resource]:
        """
        Filter the given resources by their tags using the given filters.

        :param resources: List of resources.
        :param filters: List of filters to apply to the resources.
        :return: List of resources that match the filters.
        """
        filtered_resources = []

        maybe_name_filter = [filter for filter in filters if filter.key == '@name']

        if maybe_name_filter:
            name_filter = maybe_name_filter[0]
            filters.remove(name_filter)
            resources = [resource for resource in resources
                         if name_filter.match([Tag(key=name_filter.key, value=resource.name)])]

        if filters:
            for resource in resources:
                try:
                    tags = self.get_resource_tags(resource)
                    all_match = all(filters.match(tags) for filters in filters)

                    if all_match:
                        filtered_resources.append(resource)
                except Exception as exception:
                    print(f"Failed to get tags for resource {resource.name}: {exception}")
        else:
            filtered_resources = resources

        return filtered_resources
