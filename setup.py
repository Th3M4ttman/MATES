#!/usr/bin/env python3

import setuptools

install_requires = [
        "humanize",
        "numpy",
        "pillow",
        "pytesseract"]

setuptools.setup(
    name="mates",
    version="1.1",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'mates = main',
        ],
    },
    include_package_data=True,
    )
