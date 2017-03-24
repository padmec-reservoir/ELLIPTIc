from padpy.Kernel import TPFA
from padpy.Mesh.MeshFactory import MeshFactory
from padpy.Physical.PhysicalMap import PhysicalMap
from padpy.Physical import Physical
from padpy.Problem import Pipeline, LinearProblem


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

runner = TPFA.TPFARunner(problem)
runner.run()

problem.export_solution(solution_name="Pressure", file_name="output.vtk")
