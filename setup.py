from setuptools import setup, find_packages

setup(
    name='memjogger',
    version='0.0.1',
    packages=find_packages(),
    install_requires = ['nose', 'requests', 'mock']
)