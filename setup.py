#!/usr/bin/env python3

import setuptools
from setuptools import find_packages

__ver__ = "1.0.0"

install_requires = [
        "humanize",
        "numpy",
        "pillow",
        "pytesseract"]

setuptools.setup(
    name="mates",
    version=__ver__,
    packages=find_packages(
        where='src',
    ),
    package_dir={"": "src"},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'mates = mates.main:run',
        ],
    },
    include_package_data=True,
    )
