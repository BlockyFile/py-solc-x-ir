#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="py-solc-x-ir",
    version="1.0.0",  # don't change this manually, use bumpversion instead
    description="Python wrapper and version management tool for the solc Solidity compiler with IR support.",
    long_description_markdown_filename="README.md",
    author="EpicMario71 (forked from py-solc-x by ApeWorX)",
    author_email="info@epicmario71.com",
    url="https://github.com/BlockyFile/py-solc-x-ir",
    include_package_data=True,
    py_modules=["solcxir"],
    setup_requires=["setuptools-markdown"],
    python_requires=">=3.6, <4",
    install_requires=["requests>=2.19.0,<3", "semantic_version>=2.8.1,<3"],
    license="MIT",
    zip_safe=False,
    keywords="ethereum solidity solc",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
