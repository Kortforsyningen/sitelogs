"""
Setup script for the sitelogs package.
"""

import os
import subprocess
from setuptools import setup
from setuptools import find_packages

import sitelog


SHORT_DESCR = "Sitelogs"


def readme():
    """
    Return a properly formatted readme text that can be used as the long
    description for setuptools.setup.
    """
    try:
        with open("README.md") as f:
            readme = f.read()
        return readme
    except:
        return SHORT_DESCR


setup(
    name="sitelogs",
    version=sitelog.__version__,
    description=SHORT_DESCR,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Utilities",
    ],
    packages=find_packages(exclude=["test"]),
    keywords="GNSS sitelog geodesy",
    url="https://github.com/Kortforsyningen/sitelogs",
    author="SDFE / Tanya Pheiffer Sunding",
    author_email="taphs@sdfe.dk",
    license="MIT",
    test_suite="pytest",
    tests_require=["pytest"],
    install_requires=[],
    python_requires=">=3.6",
)
