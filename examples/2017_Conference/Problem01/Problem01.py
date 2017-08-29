from Source import Kernel, Physical
from elliptic.Mesh.MeshFactory import MOABMeshFactory
from elliptic.Physical.PhysicalMap import PhysicalMap
from elliptic.Solver.Problem import LinearProblem
from elliptic import DefaultLogger
DefaultLogger.init()

MESH_SIZES = (8,)


def create_physical():
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

    return physical


for mesh_size in MESH_SIZES:
    print "Running mesh_size {0}".format(mesh_size)

    # Reading the mesh
    meshfile = 'Meshes/case_{0}x{0}x{0}.h5m'.format(mesh_size)
    mf = MOABMeshFactory()
    mesh = mf.load_mesh(meshfile)

    # Resolve the physical properties
    mesh.resolve(create_physical())

    lhs_kernel = Kernel.CVFDKernel(mesh)
    rhs_kernel = Kernel.BoundaryKernel(mesh)

    # Creating a problem
    problem = LinearProblem(
        mesh=mesh, lhs_kernel=lhs_kernel, rhs_kernel=rhs_kernel,
        solution_name="u")

    problem.run_problem()

    ms = mesh.moab.create_meshset()
    mesh.moab.add_entities(ms, rhs_kernel.get_elements())
    mesh.moab.write_file(
        'Output/steadystate_out_{0}x{0}x{0}.vtk'.format(mesh_size), [ms])
