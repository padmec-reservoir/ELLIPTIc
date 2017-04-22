from setuptools import setup, find_packages, Extension


USE_CYTHON = False

extensions = []

if USE_CYTHON:
    extensions = [
        Extension("*", ["elliptic/Kernel/*.py"]),
        Extension("*", ["elliptic/Mesh/*.py"])
    ]
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
    name="ELLIPTIc",
    version='0.2.0',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    packages=find_packages(),
    license='LICENSE',
    ext_modules=extensions
)
