import pandas as pd
import numpy as np
import pytest
from .school_students_analysis.stats import group_by, calculate_stats_on_group_by

def test_calculating_stats_of_sample_data():
    df = pd.DataFrame.from_dict([
        {"A": "a", "B": 1000, "C": 0},
        {"A": "b", "B": 0, "C": 0},
        {"A": "b", "B": 100, "C": pd.NA},
        {"A": "a", "B": 500, "C": 0},
        {"A": "a", "B": np.nan, "C": 0},
        {"A": pd.NA, "B": 10000, "C": 0},
    ])
    gby = group_by(df, by="A", drop="C")
    stats_df = calculate_stats_on_group_by(gby, "B stats")

    assert stats_df.index.size == 2
    assert all(stats_df.loc["a", :].values == [500, 750, 1000])
    assert all(stats_df.loc["b", :].values == [0, 50, 100])