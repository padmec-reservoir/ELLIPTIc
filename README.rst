.. image:: https://cdn.rawgit.com/gpkc/ELLIPTIc/master/logo.png
    :align: center

|

.. image:: https://img.shields.io/pypi/v/elliptic.svg
    :target: https://pypi.python.org/pypi/elliptic

.. image:: https://travis-ci.org/padmec-reservoir/ELLIPTIc.svg?branch=master
    :target: https://travis-ci.org/padmec-reservoir/ELLIPTIc

.. image:: https://readthedocs.org/projects/elliptic/badge/?version=latest
    :target: http://elliptic.readthedocs.io/en/latest/?badge=latest

.. image:: https://coveralls.io/repos/github/padmec-reservoir/ELLIPTIc/badge.svg?branch=master
    :target: https://coveralls.io/github/padmec-reservoir/ELLIPTIc?branch=master

.. image:: https://api.codacy.com/project/badge/Grade/025660097e6a41fa9fa6fa590ef28148
    :target: https://www.codacy.com/app/gpkc/ELLIPTIc?utm_source=github.com&utm_medium=referral&utm_content=padmec-reservoir/ELLIPTIc&utm_campaign=badger

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/gpkc/ELLIPTIc/master/LICENSE

|

.. image:: https://cdn.rawgit.com/gpkc/ELLIPTIc/master/pic.png
        :width: 500
        :align: center

===========
Description
===========

**ELLIPTIc**, The ExtensibLe LIbrary for Physical simulaTIons, is a library / framework for creating reusable and extensible `Domain Specific Languages (DSL) <https://martinfowler.com/bliki/DomainSpecificLanguage.html>`_ for scientific purposes.

ELLIPTIc's workflow is as follows:

* An ELLIPTIc DSL contract is created to define how the DSL syntax looks like. This DSL contract defines the operations that will be available when using the DSL.
* A DSL implementation is built based on the DSL contract. The DSL implementation tells ELLIPTIc how to generate the corresponding Cython code.
* When using ELLIPTIc-based DSLs, a tree-like intermediate representation is built.
* This intermediate representation is used together with the DSL implementation to generate Cython code.

==========
DSL Syntax
==========

ELLIPTIc-based DSLs use a `Fluent Interface <https://martinfowler.com/bliki/FluentInterface.html>`_ syntax. This allows
for elegant development of algorithms.

Below is an example of how using an ELLIPTIc-based DSL to iterate in a unstructured mesh would look like:

.. code:: python

    dsl = DSL(...)  # Instatiating a DSL object


    with dsl.root() as root:
        all_ents = root.Entities(dim=3).Adjacencies(bridge_dim=2, to_dim=3)  # Operation chaining
        internal_ents = all_ents.Where(boundary=False)  # Continuing an operation chain
        boundary_ents = all_ents.Where(boundary=True)  # Operation branching

        perm_ents = internal_ents.GetField(name="permeability")
        dirichlet = boundary_ents.GetField(name="dirichlet")
        neumann = boundary_ents.GetField(name="neumann")

    dsl.get_built_module().run()  # Run the generated Cython code


It is also possible to export the intermediate representation to a image file, allowing for visual debugging:

.. image:: https://cdn.rawgit.com/gpkc/ELLIPTIc/master/tree_example.png
        :width: 400
        :align: center

=============
Documentation
=============

Please refer to the `documentation page <http://elliptic.readthedocs.io/en/latest/>`_.

=======
Testing
=======

Run `python setup.py test`.

=======================
Building and installing
=======================

Run `python setup.py build` and `python setup.py install`.
