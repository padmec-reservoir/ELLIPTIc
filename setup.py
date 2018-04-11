from setuptools import setup, find_packages, Extension


setup(
    name="ELLIPTIc",
    version='1.0.0',
    url='https://github.com/padmec-reservoir/ELLIPTIc',
    maintainer='Guilherme Caminha',
    maintainer_email='gpkc@cin.ufpe.br',
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
    ext_modules=[]
)
