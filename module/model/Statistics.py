from typing import List

from nameof import nameof

from module.utils import to_string_class_formatter


class Statistics:

    def __init__(self, silhouette_score: float, calinski_harabasz_score: float,
                 davies_bouldin_score: float, offers_number: int) -> None:
        self.silhouette_score = silhouette_score
        self.calinski_harabasz_score = calinski_harabasz_score
        self.davies_bouldin_score = davies_bouldin_score
        self.offers_number = offers_number


    def to_list(self) -> List[str]:
        properties = [
            self.silhouette_score, self.calinski_harabasz_score,
            self.davies_bouldin_score, self.offers_number
        ]
        return [str(prop) for prop in properties]


    def __str__(self) -> str:
        return to_string_class_formatter(
            [
                self.silhouette_score, self.calinski_harabasz_score,
                self.davies_bouldin_score, self.offers_number
            ],
            [
                nameof(self.silhouette_score), nameof(self.calinski_harabasz_score),
                nameof(self.davies_bouldin_score), nameof(self.offers_number)
            ],
            "\n"
        )
