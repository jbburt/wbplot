from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name="wbplot",
    version="0.0.1",
    author="Joshua Burt",
    author_email="joshua.burt@yale.edu",
    description="A package for automated plotting of neuroimaging maps from Python using Connectome Workbench.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jbburt/wbplot",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)