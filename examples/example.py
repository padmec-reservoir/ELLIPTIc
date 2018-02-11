from elliptic import Elliptic, backend, PhysicalMap

from seu_pacote_de_kernels import Kernel1, Kernel2, ...


# Passo 1: Definir os parâmetros do elliptic
mesh_backend = backend.Python.Mesh(
        output_formats=["vtk"],
        report_format={
                "format": "txt",
                "fields": ["field1", "field2"]})

solver_backend = backend.Python.Solver(
        solver="...",
        preconditioner="...")

el = Elliptic(mesh_backend=mesh_backend,
              solver_backend=solver_backend,
              parallel=False)


# Passo 2: Criação da malha
with el.new_mesh() as mesh:
    my_grid = mesh.grid(nx=50, ny=25, nz=10,
                        dx=10, dy=20, dz=5)
    my_grid.get_block(i, j, k)
    # grupos fisicos
    el.set_mesh(my_grid)

    my_mesh = mesh.import_mesh("arquivo.msh")
    my_mesh = mesh.import_mesh("arquivo.h5m")
    My_mesh = mesh.read_dat_file("file_from_imex_or_eclipse.dat")
    el.set_mesh(my_mesh)


# Passo 3: Definição de condições iniciais e de contorno
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


# Passo 4: Resolver o problema e exportar soluções
while el.run_kernel(kernel_keep_running()):
    pressure_field = el.run_kernel(pressure_kernel(initial_conditions))
    velocity_field = el.run_kernel(velocity_kernel(pressure_field))
    saturation_field = el.run_kernel(saturation_kernel(velocity_field))

    problem.export_solution("out.vtk")
    problem.export_report([avr_prop1, avr_prop2,...], 'file_name.txt')
