import numpy as np
from nameof import nameof

from module.utils import to_string_class_formatter


class Statistics:

    def __init__(self, offers_count: int, confusion_matrix: np.ndarray = np.ndarray([]),
                 execution_time: float = None, dataset_name: str = "") -> None:
        self.offers_count = offers_count
        self.confusion_matrix = confusion_matrix
        self.execution_time = execution_time
        self.dataset_name = dataset_name


    def __str__(self) -> str:
        return to_string_class_formatter(
            [
                self.offers_count, self.confusion_matrix, self.execution_time, self.dataset_name
            ],
            [
                nameof(self.offers_count), nameof(self.confusion_matrix),
                nameof(self.execution_time), nameof(self.dataset_name)
            ],
            "\n"
        )
