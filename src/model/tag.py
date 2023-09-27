from dataclasses import dataclass


@dataclass
class Tag:
    key: str
    value: str

    def __str__(self):
        return f"{self.key}: {self.value}"

    def __repr__(self):
        return self.__str__()
