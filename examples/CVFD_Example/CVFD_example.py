from CVFD import Kernel, Physical, Runner
from elliptic.Mesh.MeshFactory import MeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Solver.Problem import Pipeline, LinearProblem
from elliptic import DefaultLogger
DefaultLogger.init()

# Associating physical groups with Physical instances
physical = PhysicalMap()

# Register the physical types that will be used
physical.register(Physical.Dirichlet)
physical.register(Physical.Neumann)
physical.register(Physical.Diffusivity)

# Associate each group with a physical type
physical["INLET"] = Physical.Dirichlet
physical["OUTLET"] = Physical.Dirichlet
physical["WALL"] = Physical.Neumann
physical["DIFFUSIVITY"] = Physical.Diffusivity

# Reading the mesh
meshfile = 'Meshes/cube_med.h5m'
mf = MeshFactory()
mesh = mf.load_mesh(meshfile)

# Resolve the physical properties
mesh.resolve(physical)

# Creating the Kernel pipeline
pipeline = Pipeline([
    Kernel.FillBoundary
])

# Creating a problem
problem = LinearProblem(mesh=mesh, pipeline=pipeline, solution_dim=3)

# Solving the problem
runner = Runner.CVFDRunner(problem)
runner.run()

# Exporting the solution
problem.export_solution(solution_name="Pressure", file_name="output.vtk")
