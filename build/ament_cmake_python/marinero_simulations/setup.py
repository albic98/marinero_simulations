from setuptools import find_packages
from setuptools import setup

setup(
    name='marinero_simulations',
    version='0.0.0',
    packages=find_packages(
        include=('marinero_simulations', 'marinero_simulations.*')),
)
