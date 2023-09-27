from dataclasses import dataclass
from typing import List

from tabulate import tabulate

from src.model.resource import Resource
from src.model.tag import Tag


@dataclass
class ResourceTags:
    resource: Resource
    tags: List[Tag]

    def __str__(self):
        tags_data = [[tag.key, tag.value] for tag in self.tags]
        tags_table = tabulate(tags_data, tablefmt='tsv')
        separator = '-' * len(self.resource.name)
        output = f'{self.resource.name}\n{separator}\n{tags_table}'

        return output

    def __repr__(self):
        return self.__str__()
