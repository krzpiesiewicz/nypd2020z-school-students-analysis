import numpy as np
from .common import attrs_names
from .stats import FullRecords, group_by, calculate_stats_on_group_by


class StudentsPerTeacherByTheTypeOfSchool(FullRecords):
    def get_stats_in_each_district(self):
        students_per_teacher_grouped_by = group_by(
            df=self,
            drop=[attrs_names["area type"], attrs_names["no."]],
            by=[
                attrs_names["territory code"],
                attrs_names["voivodeship"],
                attrs_names["poviat"],
                attrs_names["district"],
                attrs_names["school type"]
            ]
        )
        return calculate_stats_on_group_by(students_per_teacher_grouped_by,
                                           attrs_names["students per teacher"])

    def get_stats_in_total_for_urban_and_rural_areas(self):
        students_per_teacher_grouped_by = group_by(
            df=self,
            drop=[
                attrs_names["no."],
                attrs_names["territory code"],
                attrs_names["voivodeship"],
                attrs_names["poviat"],
                attrs_names["district"]
            ],
            by=[attrs_names["area type"], attrs_names["school type"]]
        )
        return calculate_stats_on_group_by(
            students_per_teacher_grouped_by,
            attrs_names["students per teacher"]
        ).swaplevel().sort_index()


def students_per_teacher_by_the_type_of_school(schools_df):
    students_per_teacher_df = \
        schools_df[[
            attrs_names["no."],
            attrs_names["territory code"],
            attrs_names["voivodeship"],
            attrs_names["poviat"],
            attrs_names["district"],
            attrs_names["area type"],
            attrs_names["school type"]
        ]].copy()

    students = schools_df[attrs_names["students"]]
    teachers = schools_df[attrs_names["full-time teachers"]] \
               + schools_df[attrs_names["part-time teachers"]]
    students_per_teacher_df[attrs_names["students per teacher"]] = students / teachers

    students_per_teacher_df = \
        students_per_teacher_df.replace([0, np.inf], np.nan) \
            .dropna(axis=0, how="any").reset_index(drop=True)

    return StudentsPerTeacherByTheTypeOfSchool(students_per_teacher_df)
