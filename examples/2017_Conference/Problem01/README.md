# Preprocessing

To preprocess the meshes for usage with ELLIPTIc, enter the `Meshes` folder and run `python -m elliptic.Preprocess preprocess.cfg`. The `preprocess.cfg` file contains information for the preprocessor module, such as which mesh file should be used.

Only the 8x8x8 Gmsh mesh is included. In order to run a larger problem, please modify the `mesh_size` variable in the `Meshes/Gmsh/case.geo` file, then generate the mesh using Gmsh. It is necessary to modify the `preprocess.cfg` file to use the generated mesh.


# Running

To run this problem with a preprocessed mesh, use the command `python Problem01.py`. The `Problem01.py` file is configured to search for the preprocessed mesh file under the `Meshes` folder.

In order to run other meshes, the `Problem01.py` file must be changed. If the default naming convention for the meshes is being used, i.e. `case_SxSxS.h5m` where S is the mesh size, only the `MESH_SIZES` tuple needs to be modified with the new mesh sizes.


# Results

The results are exported as VTK files to the `Output` folder by default.
