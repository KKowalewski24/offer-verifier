from nameof import nameof

from module.utils import to_string_class_formatter


class BaseItem:

    def __init__(self, id: str) -> None:
        self.id = id


    def __str__(self) -> str:
        return to_string_class_formatter([self.id], [nameof(self.id)], "\n")
