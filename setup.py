from distutils.core import setup
from setuptools import find_packages
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name='compression',
    # Packages to include into the distribution 
    packages=find_packages(','),
    version='1.0.0',
    license='MIT',
    description='',
    # Long description of your library 
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gustav Ek',
    author_email='gustav.ek@gmail.com',
    # Either the link to your github or to your website 
    url='',
    # Link from which the project can be downloaded 
    download_url='',
    # List of keywords 
    keywords=[],
    # List of packages to install with this one 
    install_requires=['bitarray'],
    # https://pypi.org/classifiers/ 
    classifiers=[]
)
