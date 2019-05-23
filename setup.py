import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sortable",
    version="0.0.1",
    author="Charles Brandt",
    author_email="code@charlesbrandt.com",
    description="A module to help sorting collections of objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/charlesbrandt/sortable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
