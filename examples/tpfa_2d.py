from elliptic.Kernel import TPFA
from elliptic.Mesh.MeshFactory import MeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Physical import Physical
from elliptic.Problem import Pipeline, LinearProblem
from elliptic.Kernel.kernel_decorators import fill_matrix, fill_vector


@fill_vector()
class EquivPerm(TPFA.EquivPerm.kernel):
    elem_dim = 1
    bridge_dim = 1
    target_dim = 2
    depth = 1
    solution_dim = 1


@fill_matrix(name="T", share=True)
class FillDiag(TPFA.FillDiag.kernel):
    elem_dim = 2
    bridge_dim = 2
    target_dim = 2
    depth = 1
    solution_dim = 2


@fill_vector(name="b")
class FillBoundary(TPFA.FillBoundary.kernel):
    elem_dim = 2
    bridge_dim = 2
    target_dim = 2
    depth = 1
    solution_dim = 2


@fill_matrix(name="T", share=True)
class TPFAKernel2D(TPFA.TPFAKernel.kernel):
    elem_dim = 1
    bridge_dim = 1
    target_dim = 2
    depth = 1
    solution_dim = 2

    depends = [EquivPerm, FillDiag, FillBoundary]


# Associating physical groups with Physical instances
physical = PhysicalMap()
physical[101] = Physical.Dirichlet(1.0)
physical[102] = Physical.Dirichlet(-1.0)
physical[103] = Physical.Symmetric()
physical[50] = TPFA.TPFAPermeability(1.0)

# Reading the mesh
meshfile = 'square.msh'
mf = MeshFactory()
m = mf.load_mesh(meshfile, physical)

# Creating the Kernel pipeline
pipeline = Pipeline([
    TPFAKernel2D
])

# Creating a problem
problem = LinearProblem(mesh=m, pipeline=pipeline, solution_dim=2)

# Solving the problem
runner = TPFA.TPFARunner(problem)
runner.run()

# Exporting the solution
problem.export_solution(solution_name="Pressure", file_name="output_2d.vtk")
