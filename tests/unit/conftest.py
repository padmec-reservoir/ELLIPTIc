import pytest

from elliptic import Elliptic
from elliptic.Kernel.MeshComputeInterface import MCI
from elliptic.Kernel.MeshComputeInterface.BackendBuilder import ContextDelegate


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
    class DelegateStub(ContextDelegate):
        def get_template_file(self):
            pass

        def template_kwargs(self):
            pass

        def context_enter(self):
            self.put_value('a', 10)

        def context_exit(self):
            self.pop_value('a')

    return DelegateStub