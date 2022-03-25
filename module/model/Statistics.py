from typing import List

from nameof import nameof

from module.utils import to_string_class_formatter


class Statistics:

    def __init__(self, offers_count: int, silhouette_score: float,
                 calinski_harabasz_score: float, davies_bouldin_score: float,
                 execution_time: float) -> None:
        self.offers_count = offers_count
        self.silhouette_score = silhouette_score
        self.calinski_harabasz_score = calinski_harabasz_score
        self.davies_bouldin_score = davies_bouldin_score
        self.execution_time = execution_time


    def to_list(self) -> List[str]:
        properties = [
            self.offers_count, self.silhouette_score,
            self.calinski_harabasz_score, self.davies_bouldin_score,
            self.execution_time
        ]
        return [str(prop) for prop in properties]


    def __str__(self) -> str:
        return to_string_class_formatter(
            [
                self.offers_count, self.silhouette_score,
                self.calinski_harabasz_score, self.davies_bouldin_score,
                self.execution_time
            ],
            [
                nameof(self.offers_count), nameof(self.silhouette_score),
                nameof(self.calinski_harabasz_score), nameof(self.davies_bouldin_score),
                nameof(self.execution_time)
            ],
            "\n"
        )
