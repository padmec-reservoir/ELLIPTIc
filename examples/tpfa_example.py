import numpy as np

from padpy.Kernel import TPFA
from padpy.Mesh.MeshFactory import MeshFactory
from padpy.Physical.PhysicalMap import PhysicalMap
from padpy.Physical import Physical
from padpy.Problem import Pipeline, LinearProblem
from pymoab import types
from PyTrilinos import Epetra, AztecOO


physical = PhysicalMap()
physical[101] = Physical.Dirichlet(1.0)
physical[102] = Physical.Dirichlet(-1.0)
physical[103] = Physical.Symmetric()
physical[50] = TPFA.TPFAPermeability(1.0)

meshfile = 'cube_coarse.msh'
mf = MeshFactory()
m = mf.load_mesh(meshfile, physical)

pipeline = Pipeline([
    TPFA.TPFAKernel
])

problem = LinearProblem(mesh=m, pipeline=pipeline, solution_dim=3)

problem.run_pipeline()
problem.fill_matrices()

problem.setup_linear_problem(A_name='T', b_name='b')
problem.solve()

problem.export_solution(solution_name="Pressure", file_name="output.vtk")
