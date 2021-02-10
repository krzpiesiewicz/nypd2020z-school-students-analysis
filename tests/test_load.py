import pandas as pd
import pytest
from .school_students_analysis.common import attrs_names
from .school_students_analysis.io import load_schools, load_childrens_ages


def test_load_nonexisting_file(tmpdir):
    file = tmpdir.join("schools.xls")
    with pytest.raises(FileNotFoundError):
        load_schools(file)
    with pytest.raises(FileNotFoundError):
        load_childrens_ages(file, ["Sheet1"])


def test_load_nonexisting_sheet(tmpdir):
    file = tmpdir.join("children.xls")
    pd.DataFrame([1, 2, 3]).to_excel(file, sheet_name="Sheet1")
    with pytest.raises(Exception):
        pd.read_excel(file, sheet_name="NonexistingSheet")


def test_load_schools_valid():
    schools = load_schools("test_schools_valid.xls")
    assert schools.loc[0, attrs_names["territory code"]] == "010203"
    assert schools.loc[1, attrs_names["area type"]] == attrs_names["urban"]
    assert schools.loc[2, attrs_names["area type"]] == attrs_names["urban"]
    assert schools.loc[3, attrs_names["area type"]] == attrs_names["rural"]
    assert schools.loc[4, attrs_names["area type"]] == attrs_names["rural"]
    assert schools.loc[5, attrs_names["no."]] == 6
    assert schools.loc[5, attrs_names["voivodeship"]] == "mazowieckie"
    assert schools.loc[5, attrs_names["poviat"]] == "Warszawa"
    assert schools.loc[5, attrs_names["district"]] == "Warszawa"
    assert schools.loc[5, attrs_names["district type"]] == "M"
    assert schools.loc[5, attrs_names["locality"]] == "Warszawa"
    assert schools.loc[5, attrs_names["school type"]] == "Szkoła podstawowa"
    assert schools.loc[5, attrs_names["students"]] == 400
    assert schools.loc[5, attrs_names["full-time teachers"]] == 20
    assert schools.loc[5, attrs_names["part-time teachers"]] == 5


def test_load_schools_lacking_columns():
    with pytest.raises(ValueError):
        load_schools("test_schools_invalid_lacking_columns.xls")


def test_load_children():
    children = load_childrens_ages("test_population_valid.xlsx",
                                   ["Dolnośląskie", "Zachodniopomorskie"])
    assert all(
        children.loc["010101", attrs_names["urban"]] == pd.Series([100] * 20)
    )
    assert all(
        children.loc["010101", attrs_names["rural"]] == pd.Series([0] * 20)
    )
    assert all(
        children.loc["010102", attrs_names["urban"]] == pd.Series([0] * 20)
    )
    assert all(
        children.loc["010102", attrs_names["rural"]] == pd.Series(range(20))
    )
    assert all(
        children.loc["020101", attrs_names["urban"]] == pd.Series(
            range(10, 30)
        )
    )
    assert all(
        children.loc["020101", attrs_names["rural"]] == pd.Series(range(20))
    )


def test_load_children_ter_nonunique():
    with pytest.raises(AssertionError):
        load_childrens_ages("test_population_invalid_not_unique_ter.xls",
                            ["Dolnośląskie"])
