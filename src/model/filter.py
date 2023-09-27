from dataclasses import dataclass
from typing import List

from src.model.tag import Tag


@dataclass
class Filter:
    key: str
    value: str
    operator: str

    def __str__(self):
        return f"{self.key} {self.operator} {self.value}"

    def __repr__(self):
        return self.__str__()

    def match(self, tags: List[Tag]):
        """
        Check if the filter matches the given tags.

        :param tags: Tag list.
        :return: True, if the filter matches the given tags.
        """

        if self.operator == "--":
            tag_keys = [tag.key for tag in tags]
            return self.key not in tag_keys

        for tag in tags:
            if self.key == tag.key:
                if self.operator == "=":
                    return tag.value == self.value
                elif self.operator == "!=":
                    return tag.value != self.value
                elif self.operator == "~":
                    return self.value in tag.value
                elif self.operator == "!~":
                    return self.value not in tag.value
                elif self.operator == "^":
                    return tag.value.startswith(self.value)
                elif self.operator == "!^":
                    return not tag.value.startswith(self.value)
                elif self.operator == "$":
                    return tag.value.endswith(self.value)
                elif self.operator == "!$":
                    return not tag.value.endswith(self.value)
                else:
                    raise ValueError(f"Unknown operator: {self.operator}")

        return False
