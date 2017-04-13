from elliptic.Kernel import TPFA
from elliptic.Mesh.MeshFactory import MeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Physical import Physical
from elliptic.Problem import Pipeline, LinearProblem


# Associating physical groups with Physical instances
physical = PhysicalMap()
physical[101] = Physical.Dirichlet(1.0)
physical[102] = Physical.Dirichlet(-1.0)
physical[103] = Physical.Symmetric()
physical[50] = TPFA.TPFAPermeability(1.0)

# Reading the mesh
meshfile = 'cube_med.msh'
mf = MeshFactory()
m = mf.load_mesh(meshfile, physical)

# Creating the Kernel pipeline
pipeline = Pipeline([
    TPFA.TPFAKernel
])

# Creating a problem
problem = LinearProblem(mesh=m, pipeline=pipeline, solution_dim=3)

# Solving the problem
runner = TPFA.TPFARunner(problem)
runner.run()

# Exporting the solution
problem.export_solution(solution_name="Pressure", file_name="output.vtk")
