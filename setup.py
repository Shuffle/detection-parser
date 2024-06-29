from setuptools import setup, find_packages

setup(
    name='shuffle-email-rules',
    version='0.5',
    description='An open-source language for email filtering rules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aditya',
    package_data=
    {
        'shuffle_email_rules': ['lib/*']
    },
    author_email='aditya@shuffler.io', # pls don't spam me
    packages=['shuffle_email_rules'],
    # packages=find_packages(),
    install_requires=[],  # Add any dependencies here
)
