from setuptools import setup, find_packages

setup(
    name="padpy",
    version='0.0.1',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    packages=find_packages(),
    license='LICENSE'
)
