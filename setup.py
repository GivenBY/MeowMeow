from setuptools import setup, find_packages

setup(
    name="MeowMeow",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyGObject", 
    ],
    entry_points={
        "console_scripts": [
            "meowmeow=main:main",
        ]
    },
    author="GiveBy",
    description="A simple wrapper around Groq with GTK 3 GUI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GivenBY/MeowMeow",
)
