# -*- coding: utf-8 -*-
# Copyright (c) Materials Virtual Lab
# Distributed under the terms of the Modified BSD License.
"""
setup: usage: pip install -e .
"""
import os
from setuptools import setup, find_namespace_packages


SETUP_PTH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(SETUP_PTH, "README.rst")) as f:
    desc = f.read()


setup(
    name="pymatgen-io-fleur",
    packages=find_namespace_packages(include=["pymatgen.io.*"]),
    version="0.0.1",
    install_requires=[
        "pymatgen>=2022.0.3",
        "masci-tools @ git+https://github.com/judftteam/masci-tools.git@write_inpgen_files",
    ],
    extras_require={},
    package_data={},
    author="Henning Janssen",
    author_email="he.janssen@fz-juelich.de",
    maintainer="Henning Janssen",
    url="https://github.com/janssenhenning/pymatgen-io-fleur",
    license="BSD",
    description="A pymatgen add-on for IO for the fleur code.",
    long_description=desc,
    keywords=["pymatgen"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
