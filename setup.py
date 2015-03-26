from setuptools import setup
from election_directory import __version__

setup(
    name='election-directory',
    version=__version__,
    description='Library to provide information about assembly constituencies and polling booths of India',
    packages=['election_directory'],
    install_requires=[],
    author='Anand Chitipothu',
    author_email="anandology@gmail.com",
    platforms='any',
    package_data={'election_directory': ['data/*.tsv']}
)

