import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="school-students-analysis",
    version="0.0.1",
    author="Krzysztof Piesiewicz",
    author_email="krz.piesiewicz@gmail.com",
    description="A package for counting basic statistics on school students from Poland",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krzpiesiewicz/nypd2020z-school-students-analysis",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "numpy", "xlrd", "openpyxl"],
    python_requires='>=3.6',
)
