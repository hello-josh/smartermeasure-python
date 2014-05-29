from setuptools import setup, find_packages
setup(
    name="SmarterMeasure REST Client",
    version="0.1-pre",
    packages=find_packages(),
    author="Joshua Johnston",
    author_email="johnston.joshua@gmail.com",
    description="Python client for the SmarterMeasure REST API",
    install_requires=[
        'requests'
    ],
    license="PSF",
    keywords="SmarterMeasure API",
    url="https://github.com/Trii/smartermeasure-python"
)
