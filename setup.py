from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

requirements = ["numpy>=1", "nibabel==2.1.0", "pillow>=7", "matplotlib>=2"]

setup(
    name="wbplot",
    version="1.0.2",
    author="Joshua Burt",
    author_email="joshua.burt@yale.edu",
    include_package_data=True,
    description="A package for automated plotting of neuroimaging maps using Connectome Workbench.",
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