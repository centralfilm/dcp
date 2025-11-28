#!/usr/bin/env python3
"""
Setup script for dcp_inspect Python package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dcp-inspect-py",
    version="1.2025.10.28",
    author="Wolfgang Woehl (Python conversion by AI)",
    author_email="",
    description="Digital Cinema Package inspector and validator (Python conversion)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wolfgangw/backports",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dcp-inspect-py=dcp_inspect:main",
        ],
    },
)