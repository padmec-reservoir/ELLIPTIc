from Source import Kernel, Physical
from elliptic.Mesh.MeshFactory import MOABMeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Solver.Problem import ProblemBase
from elliptic import DefaultLogger
DefaultLogger.init()

NUMBER_STEPS = 30

# Associating physical groups with Physical instances
physical = PhysicalMap()

# Register the physical types that will be used
physical.register(Physical.Saturation)

# Associate each group with a physical type
physical["INITIAL_SATURATION"] = Physical.Saturation
physical["IMPOSED_SATURATION"] = Physical.Saturation

# Reading the mesh
meshfile = 'Meshes/case.h5m'
mf = MOABMeshFactory()
mesh = mf.load_mesh(meshfile)

# Resolve the physical properties
mesh.resolve(physical)

top_level_kernel = Kernel.VelocityField(mesh)

# Creating a problem
pressure_problem = ProblemBase(
    mesh=mesh, kernel=top_level_kernel,
    solution_dim=3)

pressure_problem.run_problem()

top_level_kernel = Kernel.InitialSatField(mesh)

# Creating a problem
saturation_problem = ProblemBase(
    mesh=mesh, kernel=top_level_kernel,
    solution_dim=3)

saturation_problem.run_problem()

fw_kernel = Kernel.WaterFractionalFluxField(mesh)
sat_kernel = Kernel.SatField(mesh)

elems = mesh.moab.get_entities_by_dimension(0, 3)
ms = mesh.moab.create_meshset()
mesh.moab.add_entities(ms, elems)
mesh.moab.write_file('Output/out{0}.vtk'.format(0), [ms])

for i in range(1, NUMBER_STEPS):
    print(i)

    fw_problem = ProblemBase(
        mesh=mesh, kernel=fw_kernel,
        solution_dim=3)

    fw_problem.run_problem()

    saturation_problem = ProblemBase(
        mesh=mesh, kernel=sat_kernel,
        solution_dim=3)

    saturation_problem.run_problem()

    top_level_kernel.set_field_with_field("Sw", "Sw_old")

    mesh.moab.write_file('Output/out{0}.vtk'.format(i), [ms])
