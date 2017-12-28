from setuptools import setup, find_packages, Extension


USE_CYTHON = False

extensions = []

if USE_CYTHON:
    extensions = [
        Extension("*", ["elliptic/Kernel/MeshComputeInterface/*.pyx"])
    ]
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
    name="ELLIPTIc",
    version='1.0.0',
    url='https://github.com/padmec-reservoir/ELLIPTIc',
    maintainer='Guilherme Caminha',
    maintainer_email='gpkc@cin.ufpe.br',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-mock', 'pytest-faker'],
    install_requires=['numpy', 'colorlog', 'configobj', 'anytree'],
    packages=find_packages(),
    license='LICENSE',
    ext_modules=extensions
)
