import pytest

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.DSL import DSLMeta, DSL


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
def dsl_meta_stub():
    class DSLMetaStub(DSLMeta):
        def libs(self):
            return []

        def include_dirs(self):
            return []

    return DSLMetaStub


@pytest.fixture()
def dsl(mocker, dsl_meta_stub) -> DSL:
    template_manager = mocker.sentinel.template_manager
    dsl_contract = mocker.sentinel.dsl_contract

    dsl_ = DSL(template_manager, dsl_contract, dsl_meta_stub())

    return dsl_


@pytest.fixture()
def delegate_stub():
    class DelegateStub(ContextDelegate):
        def get_template_file(self):
            pass

        def template_kwargs(self):
            pass

        def context_enter(self):
            self.context.put_value('a', '10')

        def context_exit(self):
            self.context.pop_value('a')

    return DelegateStub