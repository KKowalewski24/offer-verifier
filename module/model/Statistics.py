from typing import List

from nameof import nameof

from module.utils import to_string_class_formatter


class Statistics:

    def __init__(self, offers_number: int, silhouette_score: float,
                 calinski_harabasz_score: float, davies_bouldin_score: float) -> None:
        self.offers_number = offers_number
        self.silhouette_score = silhouette_score
        self.calinski_harabasz_score = calinski_harabasz_score
        self.davies_bouldin_score = davies_bouldin_score


    def to_list(self) -> List[str]:
        properties = [
            self.offers_number, self.silhouette_score,
            self.calinski_harabasz_score, self.davies_bouldin_score
        ]
        return [str(prop) for prop in properties]


    def __str__(self) -> str:
        return to_string_class_formatter(
            [
                self.offers_number, self.silhouette_score,
                self.calinski_harabasz_score, self.davies_bouldin_score,
            ],
            [
                nameof(self.offers_number), nameof(self.silhouette_score),
                nameof(self.calinski_harabasz_score), nameof(self.davies_bouldin_score)
            ],
            "\n"
        )
