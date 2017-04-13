[![Documentation Status](https://readthedocs.org/projects/padpy/badge/?version=latest)](http://padpy.readthedocs.io/en/latest/?badge=latest)
[![Code Health](https://landscape.io/github/gpkc/padpy/master/landscape.svg?style=flat)](https://landscape.io/github/gpkc/padpy/master)
![Coverage](https://cdn.rawgit.com/gpkc/elliptic/master/cov.svg)

<p align="center">
  <img src="https://cdn.rawgit.com/gpkc/ELLIPTIc/master/logo.png"/>
</p>

<p align="center">
  <img src="https://cdn.rawgit.com/gpkc/ELLIPTIc/master/pic.png" width="600"/>
</p>

# ELLIPTIc
ELLIPTIc, the ExtensibLe LIbrary for Physical simulaTIons, is a library / framework for prototyping, testing and running large scale physical simulations.

It is built on top of Python, and uses the [PyMoab](https://bitbucket.org/fathomteam/moab/overview) and [PyTrilinos](https://github.com/trilinos/Trilinos) libraries to handle the internal mesh data structure, and matrix solving, respectively.

Currently, ELLIPTIc only runs on Python 2.7, since PyTrilinos only supports this version. Also, parallelism through MPI4Py is stale for now, since the PyMoab doesn't yet support it.

# Dependencies
* [PyMoab](https://bitbucket.org/fathomteam/moab/overview)
* [PyTrilinos](https://github.com/trilinos/Trilinos)

# Documentation
Please refer to the [documentation page](http://padpy.readthedocs.io/en/latest/).

# Testing
Run `python setup.py test`.

# Building and installing
Run `python setup.py build` and `python setup.py install`.
