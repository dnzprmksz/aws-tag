from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aws-tag=src.main:main",
        ]
    }
)
