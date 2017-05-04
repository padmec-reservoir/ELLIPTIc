from CCFVM_Diffusion import Kernel, Physical, Runner
from elliptic.Mesh.MeshFactory import MeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Solver.Problem import Pipeline, LinearProblem


# Associating physical groups with Physical instances
physical = PhysicalMap()
physical[101] = Physical.Dirichlet(1.0)
physical[102] = Physical.Dirichlet(-1.0)
physical[103] = Physical.Symmetric()
physical[50] = Physical.Diffusivity(1.0)

# Reading the mesh
meshfile = 'cube_med.msh'
mf = MeshFactory()
m = mf.load_mesh(meshfile, physical)

# Creating the Kernel pipeline
pipeline = Pipeline([
    Kernel.CCFVMKernel
])

# Creating a problem
problem = LinearProblem(mesh=m, pipeline=pipeline, solution_dim=3)

# Solving the problem
runner = Runner.CCFVMRunner(problem)
runner.run()

# Exporting the solution
problem.export_solution(solution_name="Pressure", file_name="output.vtk")
