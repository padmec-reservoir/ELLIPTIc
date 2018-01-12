import pytest


@pytest.fixture()
def mesh(request, elliptic_):
    mb = elliptic_.mesh_builder()

    mesh_ = mb.load_file('test.h5m')

    return mesh_


class TestKernel:

    def test_kernel(mesh, kernel):
        mesh.run_kernel(kernel)
