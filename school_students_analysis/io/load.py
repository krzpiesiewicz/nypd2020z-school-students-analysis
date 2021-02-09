import pandas as pd
from ..common import attrs_names


def area_type(school):
    # M (Miasto) - city
    # M-Gm (gmina miejsko-wiejska) - urban-rural district
    if school[attrs_names["district type"]] == "M" \
            or (school[attrs_names["district type"]] == "M-Gm"
                and school[attrs_names["district"]] ==
                school[attrs_names["locality"]]):
        return attrs_names["urban"]
    else:
        return attrs_names["rural"]


def excel_engine(path_to_excel_file):
    if str(path_to_excel_file).endswith(".xlsx"):
        return "openpyxl"
    else:
        return None

def load_schools(path_to_excel_file):
    colnames_map = {
        "Lp.": attrs_names["no."],
        "woj": attrs_names["voivodeship_code"],
        "pow": attrs_names["poviat_code"],
        "gm": attrs_names["district_code"],
        "Województwo": attrs_names["voivodeship"],
        "Powiat": attrs_names["poviat"],
        "Gmina": attrs_names["district"],
        "Miejscowość": attrs_names["locality"],
        "Typ gminy": attrs_names["district type"],
        "Nazwa typu": attrs_names["school type"],
        "Uczniowie, wychow., słuchacze": attrs_names["students"],
        "Nauczyciele pełnozatrudnieni": attrs_names["full-time teachers"],
        "Nauczyciele niepełnozatrudnieni (stos.pracy)":
            attrs_names["part-time teachers"],
    }
    schools_df = pd.read_excel(path_to_excel_file,
                               engine=excel_engine(path_to_excel_file),
                               skiprows=[1], usecols=colnames_map.keys())
    schools_df.rename(columns=colnames_map, inplace=True)
    for idx, school in schools_df.iterrows():
        schools_df.loc[idx, attrs_names["territory code"]] = \
            f"{school[attrs_names['voivodeship_code']]:02d}" \
            f"{school[attrs_names['poviat_code']]:02d}" \
            f"{school[attrs_names['district_code']]:02d}"
        schools_df.loc[idx, attrs_names["area type"]] = area_type(school)
    return schools_df


def load_childrens_ages_from_the_sheet(path_to_excel_file, sheet_name):
    terc_colname = "Identyfikator terytorialny\nCode"
    colnames_map = {
        "Wyszczególnienie\nSpecification": attrs_names["entry name"],
        terc_colname: attrs_names["territory code with area type (TERC)"],
        "Miasta  Urban areas": attrs_names["urban"],
        "Wieś   Rural areas": attrs_names["rural"]
    }
    population_df = pd.read_excel(
        path_to_excel_file,
        sheet_name=sheet_name,
        engine=excel_engine(path_to_excel_file),
        skiprows=[0, 1, 2, 3, 4, 6],
        header=0,
        usecols=colnames_map.keys(),
        dtype={terc_colname: str})
    population_df.rename(columns=colnames_map, inplace=True)

    terc_codes = \
        population_df[population_df[
            attrs_names["territory code with area type (TERC)"]
        ].notna()][attrs_names["territory code with area type (TERC)"]]
    ter_codes = terc_codes.apply(lambda terc: terc[:-1])
    assert ter_codes.is_unique, "TERC should be unique for each entry in the " \
                                "population file and the same should be " \
                                "satisfied for its prefix without area type " \
                                "information. It means that each " \
                                "entry should refer to exactly one district " \
                                "with all its areas."

    children_df = pd.DataFrame(
        index=pd.Index(ter_codes, name=attrs_names["territory code"])
    )

    ages = range(0, 20)
    for age in ages:
        children_df[attrs_names["urban"], age] = 0
    for age in ages:
        children_df[attrs_names["rural"], age] = 0

    ter = None
    for _, row in population_df.iterrows():
        if not pd.isna(row[attrs_names["territory code with area type (TERC)"]]):
            ter = row[attrs_names["territory code with area type (TERC)"]][:-1]
        else:
            try:
                age = int(row[attrs_names["entry name"]])
                if age <= 20:
                    colname = age
                    for area_type in (attrs_names["urban"],
                                      attrs_names["rural"]):
                        if row[area_type] != "-":
                            children_df[area_type, colname][ter] = int(row[area_type])
            except:
                pass
    children_df.columns = pd.MultiIndex.from_tuples(
        [(area_type, age) for area_type in
         (attrs_names["urban"], attrs_names["rural"]) for age in ages],
        names=(attrs_names["area type"], attrs_names["age"]))

    return children_df


def load_childrens_ages(path_to_excel_file, sheets_names):
    children_dfs_per_sheet = \
        (load_childrens_ages_from_the_sheet(path_to_excel_file, sheet_name)
         for sheet_name in sheets_names)
    children_df = pd.concat(children_dfs_per_sheet, axis=0)
    return children_df
