from typing import Union

from elliptic import Elliptic
from .Expression import StatementRoot


class ExprContext:

    def __init__(self,
                 mci: 'MCI') -> None:
        self._mci = mci
        self.root: StatementRoot = None

    def __enter__(self) -> StatementRoot:
        self.root = StatementRoot()
        return self.root

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._mci.build(self.root)


class MCI:

    def __init__(self, elliptic: Elliptic.Elliptic) -> None:
        self.elliptic = elliptic
        self.built = False
        self.building = False

    def root(self) -> ExprContext:
        if not self.built:
            self.building = True
            return ExprContext(self)
        else:
            raise

    def build(self, root: StatementRoot):
        from elliptic.Backend.DynamicCompiler.TreeBuild import TreeBuild

        template_manager = self.elliptic.get_mesh_template_manager()
        backend_builder = self.elliptic.get_mesh_backend_builder()
        backend_libs = self.elliptic.get_mesh_template_libs()
        include_dirs = self.elliptic.get_mesh_backend_include_dirs()
        tree_builder = TreeBuild(template_manager, backend_builder,
                                 backend_libs, include_dirs)

        built_module = tree_builder.build(root)

        self.building = False
        self.built = True
