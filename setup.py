#!/usr/bin/env python3

import setuptools
from setuptools import find_packages

__ver__ = "1.0.1"

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
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'mates = mates.main:run',
            'testmates = mates.tests:tests',
        ],
    },
    package_data={
      "mates": ['*.png', '*.mp3', "./tests/*.png"],
    },
    include_package_data=True,
    include_dirs = ["/storage/emulated/0/Documents/MATES/src/mates/tests/"],
    
    )
