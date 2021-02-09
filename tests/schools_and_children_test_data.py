from final_assignment.school_students_analysis.common import attrs_names


def school_dict(no, ter, voiv, pov, dis, a_t, s_t, students,
                  ft_teachers, pt_teachers):
    return {
        attrs_names["no."]: no,
        attrs_names["territory code"]: ter,
        attrs_names["voivodeship"]: voiv,
        attrs_names["poviat"]: pov,
        attrs_names["district"]: dis,
        attrs_names["area type"]: a_t,
        attrs_names["school type"]: s_t,
        attrs_names["students"]: students,
        attrs_names["full-time teachers"]: ft_teachers,
        attrs_names["part-time teachers"]: pt_teachers,
    }

def children_dict(ter, urban_ages, rural_ages):
    dct = {attrs_names["territory code"]: ter}
    for age, students in enumerate(urban_ages):
        dct[(attrs_names["urban"], age)] = students
    for age, students in enumerate(rural_ages):
        dct[(attrs_names["rural"], age)] = students
    return dct