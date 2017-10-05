from __future__ import absolute_import
import io
import imp
import cython

from distutils.core import Extension
from jinja2 import Environment, FileSystemLoader


env = Environment(
    loader=FileSystemLoader('./Templates')
)

by_ent = env.get_template("by_ent.pyx")
by_ent_pyxbld = env.get_template("pyxbld.py")
by_ent_pyxdep = env.get_template("pyxdep")

by_ent_rendered = by_ent.render(ents=[1, 2, 3])
by_ent_pyxbld_rendered = by_ent_pyxbld.render()

file_hash = "aaaaa"#str(abs(hash(by_ent_rendered)))

module_name = "elliptic_tmp__" + file_hash
fmodule_name = "tmp.elliptic_tmp__" + file_hash
by_ent_fname = "tmp/elliptic_tmp__" + file_hash + ".pyx"
by_ent_pyxbld_fname = "tmp/elliptic_tmp__" + file_hash + ".pyxbld"

with io.open(by_ent_fname, 'w', encoding='utf-8') as f:
    f.write(by_ent_rendered)

with io.open(by_ent_pyxbld_fname, 'w', encoding='utf-8') as f:
    f.write(by_ent_pyxbld_rendered)

import pyximport
pyximport.install(build_dir="tmp/", inplace=True)


modimp = __import__(fmodule_name)

mymod = getattr(modimp, module_name)


from pymoab import core
from pymoab import topo_util
from pymoab import types

mb = core.Core()
mtu = topo_util.MeshTopoUtil(mb)
root_set = mb.get_root_set()

mb.load_file('estruturado_64x64.msh')

mb.tag_get_handle(
    "pydata", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)

mb.tag_get_handle(
    "cydata", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)

def callme():
    mymod.callme(mb)

def pycallme():
    ents = mb.get_entities_by_dimension(0, 2)
    data_tag = mb.tag_get_handle("pydata")

    for ent in ents:
        mb.tag_set_data(data_tag, ent, 1.0)


import timeit
print(timeit.timeit(callme, number=300)/100.0)
print(timeit.timeit(pycallme, number=20)/10.0)

mb.write_file("arquivo.vtk")
