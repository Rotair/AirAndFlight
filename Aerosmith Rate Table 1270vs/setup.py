from setuptools import setup, find_namespace_packages


packages = [
    'pyserial==3.5',
]

setup(name='rateTableControl', version='0.0.1', packages=find_namespace_packages(), install_requires=packages)
