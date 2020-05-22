#!/usr/bin/env python3

from setuptools import setup, find_packages
from cc.constant import MODULE_NAME, REQUIREMENTS_FILE, VERSION

# Read long_description from README.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

# Read requirements file.
with open(REQUIREMENTS_FILE) as f:
    requirements = f.read().splitlines()

setup(
    name=MODULE_NAME,
    version=VERSION,
    install_requires=requirements,
    author='Brendan Hu',
    author_email='contact@brendanhu.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/mithridatize/ccircle/',
    license='MIT',
    description='Learn to code with Python!',
    long_description=long_description,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Education',
        'Operating System :: MacOS',
        'Topic :: Education :: Software Development',
    ],
)
