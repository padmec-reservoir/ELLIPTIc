import pytest

from elliptic import Elliptic
from elliptic.Kernel.MeshComputeInterface import MCI


@pytest.fixture()
def mesh_backend(mocker):
    mesh_backend = mocker.Mock()
    mesh_backend.get_template_manager.return_value = mocker.sentinel.template_manager
    mesh_backend.get_backend_builder.return_value = mocker.sentinel.get_backend_builder
    mesh_backend.get_libraries.return_value = mocker.sentinel.libraries
    mesh_backend.get_include_dirs.return_value = mocker.sentinel.include_dirs
    mesh_backend.mesh_builder.return_value = mocker.sentinel.mesh_builder

    return mesh_backend


@pytest.fixture()
def elliptic(mocker, mesh_backend):
    elliptic_ = Elliptic(mesh_backend, mocker.Mock())
    elliptic_.set_mesh(mocker.sentinel.mesh)

    return elliptic_


@pytest.fixture()
def mci(elliptic) -> MCI:
    mci_ = MCI(elliptic)

    return mci_


@pytest.fixture()
def delegate_stub():
    class DelegateStub:
        def get_template_file(self):
            pass

        def template_kwargs(self, _):
            pass

        def context_enter(self, context):
            context[5] = 10

        def context_exit(self, context):
            context[5] = 5

    return DelegateStub