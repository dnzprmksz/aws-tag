from setuptools import setup, find_packages

setup(
    name='aws-tagger',
    version='23.08.0',
    packages=find_packages(),
    install_requires=[
        'boto3==1.26.47',
        'botocore==1.29.47',
        'jmespath==1.0.1',
        'numpy==1.24.1',
        'pandas==1.5.2',
        'pathvalidate==2.5.2',
        'python-dateutil==2.8.2',
        'pytz==2022.7',
        's3transfer==0.6.0',
        'six==1.16.0',
        'tabulate==0.9.0',
        'urllib3==1.26.13'
    ],
    entry_points={
        "console_scripts": [
            "aws-tagger=src.main:main",
        ]
    }
)
