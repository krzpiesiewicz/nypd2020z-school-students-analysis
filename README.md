# school-student-analysis

It is a simple distribution package for loading and preprocessing data of 
Polish schools and population created by [Statistics Poland](stat.gov.pl).
It also calculate basic statistics like min/average/max number of:
- students per teacher broken down by the type of school (1),
- students per school broken down by their year of birth (2),

in each district (polish ‘gmina’) and in total for cities and rural districts.

(1) number of students divided by the sum of the numbers of full-time
and part-time teachers

(2) number of students with a specific year of birth is estimated by 
proportions of the population age in the district
which the school is located in. 

## How to use it

```python
from students_analysis.io import load_schools, load_childrens_ages

schools_file = "<path to your excel file with schools data>"
schools = load_schools(schools_file)

population_file = "<path to your excel file with population data>"
population_file_sheets_names = ["Dolnośląskie", "Zachodniopomorskie"]
childrens_ages = load_childrens_ages(population_file,
                                     population_file_sheets_names)

from students_analysis import students_per_teacher_by_the_type_of_school

students_per_teacher = students_per_teacher_by_the_type_of_school(schools)
students_per_teacher.get_stats_in_each_district()
students_per_teacher.get_stats_in_total_for_urban_and_rural_areas()

from students_analysis import students_by_year_of_birth

students_by_year_of_birth = students_by_year_of_birth(schools, childrens_ages)
students_by_year_of_birth.get_stats_in_each_district()
students_by_year_of_birth.get_stats_in_total_for_urban_and_rural_areas()
```

## Where to download the data

- [schools](https://dane.gov.pl/pl/dataset/839,wykaz-szko-i-placowek-oswiatowych/resource/16251,wykaz-szkol-i-placowek-wg-stanu-na-30ix-2018-r/table)
- [population](https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/ludnosc-stan-i-struktura-oraz-ruch-naturalny-w-przekroju-terytorialnym-w-2018-r-stan-w-dniu-31-xii,6,25.html)