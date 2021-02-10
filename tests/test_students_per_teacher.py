import pandas as pd
import pytest
from .school_students_analysis.common import attrs_names
from .school_students_analysis import students_per_teacher_by_the_type_of_school
from .schools_and_children_test_data import school_dict

def test_in_each_school():
    schools_df = pd.DataFrame.from_dict([
        school_dict(1, 1, "a", "a", "a", "r", "sp", 100, 10, 0),
        school_dict(2, 1, "a", "a", "a", "u", "sp", 50, 10, 0),
        school_dict(3, 2, "a", "a", "b", "r", "sp", 100, 10, 5),
        school_dict(4, 3, "a", "a", "c", "r", "sp", 100, 0, 0),
        school_dict(5, 3, "a", "a", "c", "r", "sp", 0, 0, 0),
        school_dict(6, 1, "a", "a", "a", "r", "sp", 1000, 8, 0),
    ])

    students_per_teacher_df =\
        students_per_teacher_by_the_type_of_school(schools_df)

    assert all(
        students_per_teacher_df[attrs_names["no."]].values == [1, 2, 3, 6]
    )
    assert all(
        students_per_teacher_df[attrs_names["students per teacher"]].values ==
        [10, 5, 100 / 15, 125]
    )

