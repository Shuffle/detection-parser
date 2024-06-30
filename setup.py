from setuptools import setup, find_packages

setup(
    name='shuffle-heimdall',
    version='0.2.2',
    description='An open-source language for email filtering rules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aditya',
    package_data=
    {
        'heimdall': ['lib/binaries/*']
    },
    author_email='aditya@shuffler.io', # pls don't spam me
    packages=['heimdall'],
    # packages=find_packages(),
    install_requires=[],  # Add any dependencies here
)
