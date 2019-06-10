'''
gbm_summarize setup module
'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='gbm_summarize',
    version='0.1.0',
    description='Python command line tool to access cBioPortal',
    author='Shweta Gopaulakrishnan',
    author_email='reshg@channing.harvard.edu',
    keywords='cBioPortal REST client wrapper command line interface',
    packages=find_packages(),
    install_requires=['argparse', 'requests'],
    extras_require={},
    package_data={},
    entry_points={
        'console_scripts': [
            'gbm_summarize=gbm_summarize:__main__',
        ],
    },
)
