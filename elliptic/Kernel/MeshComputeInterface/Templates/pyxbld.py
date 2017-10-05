import numpy as np

def make_ext(modname, pyxfilename):
    from distutils.extension import Extension
    ext = Extension(name = modname,
                     sources=[pyxfilename],
                     include_dirs=[np.get_include()],
                     language="c++",
                     libraries = ["MOAB"])
    return ext

#def make_setup_args():
#    return dict(script_args=["--compiler=mingw32"])
