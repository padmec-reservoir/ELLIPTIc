from CVFD import Kernel, Physical, Runner
from elliptic.Mesh.MeshFactory import MeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Solver.Problem import Pipeline, LinearProblem
from elliptic import DefaultLogger
DefaultLogger.init()


class EquivDiff(Kernel.EquivDiff):
    entity_dim = 1
    bridge_dim = 1
    target_dim = 2
    depth = 1
    solution_dim = 1


class FillDiag(Kernel.FillDiag):
    entity_dim = 2
    bridge_dim = 2
    target_dim = 2
    depth = 1
    solution_dim = 2


class FillBoundary(Kernel.FillBoundary):
    entity_dim = 2
    bridge_dim = 2
    target_dim = 2
    depth = 1
    solution_dim = 2


class CVFDKernel2D(Kernel.CVFDKernel):
    entity_dim = 1
    bridge_dim = 1
    target_dim = 2
    depth = 1
    solution_dim = 2

    depends = [EquivDiff, FillDiag, FillBoundary]


# Associating physical groups with Physical instances
physical = PhysicalMap()
physical[101] = Physical.Neumann(1.0)
physical[102] = Physical.Dirichlet(0.0)
physical[103] = Physical.Neumann(0.0)
physical[50] = Physical.Diffusivity(1.0)

# Reading the mesh
meshfile = 'Meshes/square.msh'
mf = MeshFactory()
m = mf.load_mesh(meshfile, physical)

# Creating the Kernel pipeline
pipeline = Pipeline([
    CVFDKernel2D
])

# Creating a problem
problem = LinearProblem(mesh=m, pipeline=pipeline, solution_dim=2)

# Solving the problem
runner = Runner.CVFDRunner(problem)
runner.run()

# Exporting the solution
problem.export_solution(solution_name="Pressure", file_name="output_2d.vtk")
