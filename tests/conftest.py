import pytest

from elliptic import Backend, Elliptic


MESH_BACKENDS = [
    Backend.Python
]

SOLVER_BACKENDS = [
    Backend.Python
]

MESH_BACKEND_PARAMS = [
    {
        "output_formats": ['vtk'],
        "report_format": ['txt'],
        "fields": ['field1', 'field2']
    }
]

SOLVER_BACKEND_PARAMS = [
    {
        "solver": None,
        "preconditioner": None
    }
]


@pytest.fixture(params=MESH_BACKENDS)
def mesh_backend_mod(request):
    return request.param.Mesh


@pytest.fixture(params=SOLVER_BACKENDS)
def solver_backend_mod(request):
    meshb = request.param.Solver
    return meshb


@pytest.fixture(params=MESH_BACKEND_PARAMS)
def mesh_backend(request, mesh_backend_mod):
    meshb = mesh_backend_mod.Mesh(**(request.param))
    return meshb


@pytest.fixture(params=SOLVER_BACKEND_PARAMS)
def solver_backend(request, solver_backend_mod):
    solverb = solver_backend_mod.Solver(**(request.param))
    return solverb


@pytest.fixture()
def elliptic_(request, mesh_backend, solver_backend):
    el = Elliptic.Elliptic(mesh_backend=mesh_backend,
                           solver_backend=solver_backend)

    return el
