from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dfs",
    version="1.0.0",
    author="Josh Sullivan",
    author_email="sullivanja92@gmail.com",
    description="A daily fantasy football lineup optimization package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sullivanja92/dfs",
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'pandas',
        'pulp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)