import pandas as pd
from .common import attrs_names
from .stats import FullRecords, group_by, calculate_stats_on_group_by


# Schools types and students' ages in 2018:
#
# *(includes only standard types of schools which provide general education
# and have specific age restrictions for the majority of their students.
# School complexes are also omitted due to the impossibility of spliting
# the number of students into individual units)*
#
# Analysis, taking into account the education reform, is based on
# the following sources:
# - https://www.gov.pl/web/edukacja-i-nauka/wdrazanie-reformy
# - http://muzykalnedziecko.pl/kiedy-do-szkoly-muzycznej/
# - https://pl.wikipedia.org/wiki/Og%C3%B3lnokszta%C5%82c%C4%85ca_szko%C5%82a_muzyczna_II_stopnia
# - https://szkoly-branzowe.edubaza.pl/s/4999/80982-zmiany.htm


class StudentsByYearOfBirth(FullRecords):
    def get_stats_in_each_district(self):
        students_grouped_by = group_by(
            df=self,
            drop=[attrs_names["no."], attrs_names["territory code"],
                  attrs_names["area type"]],
            by=[attrs_names["voivodeship"], attrs_names["poviat"],
                attrs_names["district"], attrs_names["year of birth"]]
        )
        return calculate_stats_on_group_by(students_grouped_by,
                                           attrs_names["students"])

    def get_stats_in_total_for_urban_and_rural_areas(self):
        students_grouped_by = group_by(
            df=self,
            drop=[attrs_names["no."], attrs_names["territory code"],
                  attrs_names["voivodeship"], attrs_names["poviat"],
                  attrs_names["district"]],
            by=[attrs_names["area type"], attrs_names["year of birth"]]
        )
        return calculate_stats_on_group_by(students_grouped_by,
                                           attrs_names["students"])


popular_schools_types_and_students_ages = pd.DataFrame([
    ("Szkoła podstawowa", range(7, 15)),
    ("Gimnazjum", range(15, 16)),  # the last year
    ("Liceum ogólnokształcące", range(16, 19)),
    ("Technikum", range(16, 20)),
    ("Czteroletnie liceum plastyczne", range(16, 20)),
    ("Branżowa szkoła I stopnia", range(16, 18)),  # 1st and 2nd years
    ("Ogólnokształcąca szkoła muzyczna I stopnia", range(7, 13)),
    ("Ogólnokształcąca szkoła muzyczna II stopnia", range(13, 19))
], columns=[attrs_names["school type"], attrs_names["age"]])
popular_schools_types_and_students_ages.set_index(
    [attrs_names["school type"]],
    inplace=True
)


def students_by_year_of_birth(schools_df, children_ages_df,
                              year_of_data_compilation=2018):
    schools = schools_df[
        [attrs_names["no."], attrs_names["territory code"],
         attrs_names["voivodeship"], attrs_names["poviat"],
         attrs_names["district"], attrs_names["area type"],
         attrs_names["school type"], attrs_names["students"]]].copy()
    schools = schools[
        (schools[attrs_names["students"]] > 0) \
        & schools[attrs_names["school type"]].isin(
            popular_schools_types_and_students_ages.index
        )
        ]
    multi_index = children_ages_df.columns
    children_ages_df.columns = children_ages_df.columns.to_flat_index()

    schools = schools.join(children_ages_df, how="inner",
                           on=attrs_names["territory code"])
    children_ages_df.columns = multi_index

    students_by_year_of_birth_dicts = []
    for idx, school in schools.iterrows():
        age_range = \
            popular_schools_types_and_students_ages.loc[
                school[attrs_names["school type"]], attrs_names["age"]
            ]
        area_type = school[attrs_names["area type"]]
        children_by_age = school[((area_type, age) for age in age_range)]
        children_total = children_by_age.sum()
        if children_total > 0:
            students = school[attrs_names["students"]]
            students_by_age = children_by_age * students // children_total

            years_of_births_index = pd.Index((year_of_data_compilation - age
                                              for age in age_range))
            students_by_year_of_birth = \
                students_by_age.set_axis(years_of_births_index).sort_index()

            for year_of_birth, students in students_by_year_of_birth.iteritems():
                dct = {attrs_names["year of birth"]: year_of_birth,
                       attrs_names["students"]: students}
                for key in (attrs_names["no."], attrs_names["territory code"],
                            attrs_names["voivodeship"], attrs_names["poviat"],
                            attrs_names["district"], attrs_names["area type"]):
                    dct[key] = school[key]
                students_by_year_of_birth_dicts.append(dct)

    return StudentsByYearOfBirth(pd.DataFrame.from_dict(
        students_by_year_of_birth_dicts
    ))
