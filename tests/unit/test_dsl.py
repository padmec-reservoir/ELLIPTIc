import pytest

from elliptic.Kernel.Contract import DSLContract
from elliptic.Kernel.DSL import DSLBuildError, DSLMeta


class TestDSL:

    def test_root(self, dsl, mocker):
        mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')
        assert not dsl.building
        assert not dsl.built

        with dsl.root() as root:
            assert dsl.building
            assert not dsl.built

        assert not dsl.building
        assert dsl.built

    def test_root_raises_MCIBuildError(self, dsl, mocker):
        mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')

        with dsl.root() as root:
            with pytest.raises(DSLBuildError):
                with dsl.root() as root2:
                    pass

    def test_get_built_module(self, dsl, mocker):
        tree_build = mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')
        tree_build.return_value = mocker.sentinel.built_module

        with dsl.root() as root:
            pass

        assert dsl.get_built_module() is mocker.sentinel.built_module

    def test_get_built_module_raises_MCIBuildError(self, dsl, mocker):
        mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')

        with pytest.raises(DSLBuildError):
            dsl.get_built_module()

    def test_build(self, dsl, mocker):
        tree_build = mocker.patch('elliptic.Kernel.TreeBuilder.TreeBuild.build')

        with dsl.root() as root:
            pass

        tree_build.assert_called_once()


class TestDSLContract:

    def test_dsl_contract_raises_TypeError(self):
        with pytest.raises(TypeError):
            DSLContract()


class TestDSLMeta:

    def test_dsl_meta_raises_TypeError(self):
        with pytest.raises(TypeError):
            DSLMeta()