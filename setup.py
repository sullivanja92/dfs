import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygskin",  # Replace with your own username
    version="0.0.1",
    author="Josh Sullivan",
    author_email="sullivanja92@gmail.com",
    description="A daily fantasy football lineup optimization package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['pygskin'],
    install_requires=[
        'pandas',
        'scrapy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)