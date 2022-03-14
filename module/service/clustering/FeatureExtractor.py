from __future__ import annotations

from typing import List

import pandas as pd

from module.model.Offer import Offer


class FeatureExtractor:

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__()
        self.offers = offers


    def extract(self) -> FeatureExtractor:
        # TODO
        return self


    def prepare_dataset(self) -> pd.DataFrame:
        # TODO
        # df: pd.DataFrame = pd.DataFrame(
        #     [offer.get_feature_values() for offer in self.offers],
        #     columns=self.feature_names
        # )
        #
        # label_encoder = LabelEncoder()
        # for name in self.non_numeric_feature_names:
        #     df[name] = label_encoder.fit_transform(df[name])
        #
        # df = df.astype(float)
        # return pd.DataFrame(data=preprocessing.normalize(df), columns=df.columns)
        return pd.DataFrame()
