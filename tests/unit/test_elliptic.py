import pytest

from elliptic.Elliptic import Elliptic


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


class TestElliptic:

    def test_run_kernel(self, elliptic, mocker):
        mci = mocker.Mock()
        mci.get_built_module.return_value = mocker.sentinel.kernel_module

        elliptic.run_kernel(mci)

        elliptic.mesh_backend.run_kernel.assert_called_once_with(
            mocker.sentinel.kernel_module, mocker.sentinel.mesh)

    def test_get_mesh_template_manager(self, elliptic, mocker):
        assert elliptic.get_mesh_template_manager() == mocker.sentinel.template_manager

    def test_get_mesh_backend_libs(self, elliptic, mocker):
        assert elliptic.get_mesh_backend_libs() == mocker.sentinel.libraries

    def test_get_mesh_backend_include_dirs(self, elliptic, mocker):
        assert elliptic.get_mesh_backend_include_dirs() == mocker.sentinel.include_dirs

    def test_mesh_builder(self, elliptic, mocker):
        assert elliptic.mesh_builder() == mocker.sentinel.mesh_builder
