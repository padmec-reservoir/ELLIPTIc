<p align="center">
  <img src="https://cdn.rawgit.com/gpkc/ELLIPTIc/master/logo.png"/>
</p>

---

[![Build Status](https://travis-ci.org/padmec-reservoir/ELLIPTIc.svg?branch=master)](https://travis-ci.org/padmec-reservoir/ELLIPTIc)
[![Documentation Status](https://readthedocs.org/projects/elliptic/badge/?version=latest)](http://elliptic.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/padmec-reservoir/ELLIPTIc/badge.svg?branch=master)](https://coveralls.io/github/padmec-reservoir/ELLIPTIc?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/025660097e6a41fa9fa6fa590ef28148)](https://www.codacy.com/app/gpkc/ELLIPTIc?utm_source=github.com&utm_medium=referral&utm_content=padmec-reservoir/ELLIPTIc&utm_campaign=badger)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gpkc/ELLIPTIc/master/LICENSE)

<p align="center">
  <img src="https://cdn.rawgit.com/gpkc/ELLIPTIc/master/pic.png" width="600"/>
</p>


# Description
**ELLIPTIc**, The ExtensibLe LIbrary for Physical simulaTIons, is a library / framework for prototyping, testing and running large scale physical simulations. Please notice that this package is not yet ready for production. Currently, only Python 3.6 is fully supported.

It is built on top of Python, and uses the [PyMoab](https://bitbucket.org/fathomteam/moab/overview) and [PyTrilinos](https://github.com/trilinos/Trilinos) libraries to handle the internal mesh data structure, and matrix solving, respectively.

Parallelism through MPI is not being developed, since the PyMoab library doesn't yet support it.

# Dependencies
* [PyMoab](https://bitbucket.org/fathomteam/moab/overview)
* [PyTrilinos](https://github.com/trilinos/Trilinos)

# Documentation
Please refer to the [documentation page](http://elliptic.readthedocs.io/en/latest/).

# Testing
Run `python setup.py test`.

# Building and installing
Run `python setup.py build` and `python setup.py install`.
