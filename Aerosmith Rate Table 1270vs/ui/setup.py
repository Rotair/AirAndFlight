from setuptools import setup, find_namespace_packages


packages = [
    'serial==0.0.97'
]

setup(name='rateTableUI', version='0.0.1', packages=find_namespace_packages(), install_requires=packages)
