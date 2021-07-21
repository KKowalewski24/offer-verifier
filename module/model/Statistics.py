from typing import List

from nameof import nameof

from module.utils import to_string_class_formatter


class Statistics:

    def __init__(self, silhouette_score: float, calinski_harabasz_score: float,
                 davies_bouldin_score: float) -> None:
        self.silhouette_score = silhouette_score
        self.calinski_harabasz_score = calinski_harabasz_score
        self.davies_bouldin_score = davies_bouldin_score


    def to_list(self) -> List[float]:
        return [self.silhouette_score, self.calinski_harabasz_score, self.davies_bouldin_score]


    def __str__(self) -> str:
        return to_string_class_formatter(
            [self.silhouette_score, self.calinski_harabasz_score, self.davies_bouldin_score],
            [
                nameof(self.silhouette_score), nameof(self.calinski_harabasz_score),
                nameof(self.davies_bouldin_score)
            ],
            "\n"
        )
