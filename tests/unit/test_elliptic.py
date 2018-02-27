
class TestElliptic:

    def test_run_kernel(self, elliptic, mocker):
        mci = mocker.Mock()
        mci.get_built_module.return_value = mocker.sentinel.kernel_module

        elliptic.run_kernel(mci)

        elliptic.mesh_backend.run_kernel.assert_called_once_with(
            mocker.sentinel.kernel_module, mocker.sentinel.mesh)

    def test_get_mesh_template_manager(self, elliptic, mocker):
        assert elliptic.get_mesh_template_manager() is mocker.sentinel.template_manager

    def test_get_mesh_backend_libs(self, elliptic, mocker):
        assert elliptic.get_mesh_backend_libs() is mocker.sentinel.libraries

    def test_get_mesh_backend_include_dirs(self, elliptic, mocker):
        assert elliptic.get_mesh_backend_include_dirs() is mocker.sentinel.include_dirs

    def test_mesh_builder(self, elliptic, mocker):
        assert elliptic.mesh_builder() is mocker.sentinel.mesh_builder
