from abc import ABC, abstractmethod
from contextlib import contextmanager
from types import ModuleType
from typing import List, Iterator

from elliptic.Kernel.Expression import Expression
from .Contract import DSLContract
from .TemplateManager import TemplateManagerBase
from .TreeBuilder import TreeBuild


class DSLMeta(ABC):
    """Class which stores information regarding the DSL compilation.
    """

    @abstractmethod
    def libs(self) -> List[str]:
        """Returns the list of libraries that should be linked against.

        Example:
            ['MOAB', 'Trilinos']
        """
        raise NotImplementedError

    @abstractmethod
    def include_dirs(self) -> List[str]:
        """Returns the list of include directories that should be used when compiling.

        Cypyler adds the numpy includes by default. Any extra include paths should be returned here.

        Example:
            ['/usr/local/include/moab']
        """
        raise NotImplementedError


class DSLException(Exception):
    pass


class DSLBuildError(DSLException):
    """Exception raised when an error related to a DSL build process happens.
    """


class DSL:
    """Defines the interface for interacting with a DSL.

    Parameters:
        template_manager: A `TemplateManagerBase` subinstance.
        dsl_contract: A DSL Contract.
        dsl_meta: A `DSLMeta` instance.
    """

    def __init__(self,
                 template_manager: TemplateManagerBase,
                 dsl_contract: DSLContract,
                 dsl_meta: DSLMeta) -> None:
        self.template_manager = template_manager
        self.dsl_contract = dsl_contract
        self.dsl_meta = dsl_meta

        self.built = False
        self.building = False
        self.built_module: ModuleType = None

    @contextmanager
    def root(self) -> Iterator[DSLContract]:
        """Entry point for building expressions.

        Should be used as a context manager, using the `with` statement.
        """
        if not self.built and not self.building:
            self.building = True

            root_ = self.dsl_contract.Base()
            yield root_
            self._build(root_.expr)
        else:
            raise DSLBuildError("Can't get root while or after building a DSL tree.")

    def get_built_module(self) -> ModuleType:
        """Returns the compiled module that holds the generated code.
        """
        if not self.built:
            raise DSLBuildError("Can't get the built module before finishing building the DSL tree.")
        return self.built_module

    def _build(self, root: Expression):
        """Builds a DSL tree, generating the corresponding code, given the DSL tree root.

        The DSL tree root should always be a StatementRoot instance.

        Parameters:
            root: The DSL tree root.
        """
        tree_builder = TreeBuild(self.template_manager,
                                 self.dsl_meta.libs(), self.dsl_meta.include_dirs())

        self.built_module = tree_builder.build(root)

        self.building = False
        self.built = True
