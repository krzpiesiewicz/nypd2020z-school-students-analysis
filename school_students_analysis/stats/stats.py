import pandas as pd
from abc import abstractmethod
from ..common import attrs_names


class FullRecords(pd.DataFrame):
    @abstractmethod
    def get_stats_in_each_district(self):
        pass

    @abstractmethod
    def get_stats_in_total_for_urban_and_rural_areas(self):
        pass


def calculate_stats_on_group_by(grouped_by_obj, top_level_name):
    stat_min = grouped_by_obj.min()
    stat_mean = grouped_by_obj.mean()
    stat_max = grouped_by_obj.max()
    stats_df = pd.concat((stat_min, stat_mean, stat_max), axis=1)
    stats_df.columns = pd.MultiIndex.from_tuples(
        [(top_level_name, attrs_names["min"]),
         (top_level_name, attrs_names["average"]),
         (top_level_name, attrs_names["max"])]
    )
    return stats_df.sort_index()


def group_by(df, by, drop):
    return df.drop(drop, axis=1).groupby(by, sort=False)
