from setuptools import setup, find_packages, Extension

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    author="Guilherme Caminha",
    author_email='gpkc@cin.ufpe.br',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    description="A tool for building DSLs for scientific purposes.",
    name="ELLIPTIc",
    long_description=readme,
    version='1.0.1',
    url='https://github.com/padmec-reservoir/ELLIPTIc',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-mock', 'pytest-faker',
                   'mypy'],
    install_requires=['colorlog', 'configobj', 'anytree', 'typing_extensions', 'jinja2',
                      'cypyler'],
    extras_require={
        'docs': [
            'sphinx',
            'sphinx_autodoc_typehints',
            'sphinx_rtd_theme']},
    packages=find_packages(),
    license="MIT license",
    zip_safe=False,
    include_package_data=True
)
