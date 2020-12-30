import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Python-METAR-MattBOUCHET", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="matthieu.bouchet@outlook.com",
    description="METAR Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatthieuBOUCHET/Python-METAR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)