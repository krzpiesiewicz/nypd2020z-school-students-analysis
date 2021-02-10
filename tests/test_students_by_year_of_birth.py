import pandas as pd
import pytest
from .school_students_analysis.common import attrs_names
from .school_students_analysis import students_by_year_of_birth
from .schools_and_children_test_data import school_dict, children_dict

def test_students_by_year():
    schools_df = pd.DataFrame.from_dict([
        school_dict(1, 123, ".", ".", ".", attrs_names["urban"],
                    "School type to be omitted", 100, 10, 0),
        school_dict(2, 123, ".", ".", ".", attrs_names["urban"],
                    "Liceum ogólnokształcące", 100, 10, 0),
        school_dict(3, 123, ".", ".", ".", attrs_names["rural"],
                    "Liceum ogólnokształcące", 100, 10, 0),
        school_dict(4, 124, ".", ".", ".", attrs_names["urban"],
                    "Szkoła podstawowa", 1000, 10, 0),
        school_dict(5, 124, "There is no children in rural area", ".", ".",
                    attrs_names["rural"], "Szkoła podstawowa", 100, 10, 0),
        school_dict(6, 125, "There is no entry in children_ages_df with ",
                    "territory code 02", ".",
                    attrs_names["rural"], "Szkoła podstawowa", 100, 10, 0),
    ])

    children_ages_df = pd.DataFrame.from_dict([
        children_dict(123,
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       100, 150, 50, # Liceum ogólnokształcące
                       0],
                      [100] * 20),
        children_dict(124, range(0, 2000, 100), [0] * 20)
    ])
    children_ages_df = children_ages_df.set_index(attrs_names["territory "
                                                              "code"])
    children_ages_df.columns = pd.MultiIndex.from_tuples(
        [(area_type, age) for area_type in
         (attrs_names["urban"], attrs_names["rural"]) for age in range(20)],
        names=(attrs_names["area type"], attrs_names["age"]))

    students_by_year_of_birth_df = students_by_year_of_birth(schools_df,
                                                             children_ages_df)

    for no in (1, 5, 6):
        assert students_by_year_of_birth_df.query(
            f"`{attrs_names['no.']}` == {no}"
        ).empty

    no2_df = students_by_year_of_birth_df.query(f"`{attrs_names['no.']}` == 2")
    assert all(
        no2_df.loc[:, attrs_names["year of birth"]].values ==
        [2000, 2001, 2002]
    )
    assert all(
        no2_df.loc[:, attrs_names["students"]].values ==
        [int(100 / 6), int(100 / 2), int(100 / 3)]
    )

    no3_df = students_by_year_of_birth_df.query(f"`{attrs_names['no.']}` == 3")
    assert all(
        no3_df.loc[:, attrs_names["year of birth"]].values ==
        [2000, 2001, 2002]
    )
    assert all(
        no3_df.loc[:, attrs_names["students"]].values == [33, 33, 33]
    )

    no4_df = students_by_year_of_birth_df.query(f"`{attrs_names['no.']}` == 4")
    assert all(
        no4_df.loc[:, attrs_names["year of birth"]].values == list(range(2004, 2012))
    )