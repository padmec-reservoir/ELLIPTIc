from abc import abstractmethod
from typing import Type

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.Contract import DSLContract, DSLImplementation
from elliptic.Kernel.Expression import Expression


class VectorImplementationBase(DSLImplementation):

    @abstractmethod
    def range_delegate(self, start: int, count: int) -> Type[ContextDelegate]:
        raise NotImplementedError

    @abstractmethod
    def scalar_mult_delegate(self, scalar: float) -> Type[ContextDelegate]:
        raise NotImplementedError

    @abstractmethod
    def scalar_sum_delegate(self, scalar: float) -> Type[ContextDelegate]:
        raise NotImplementedError

    @abstractmethod
    def sum_delegate(self) -> Type[ContextDelegate]:
        raise NotImplementedError


class VectorContract(DSLContract[VectorImplementationBase]):

    def Range(self, start: int, count: int) -> 'VectorContract':
        return self.append_tree(Expression(self.dsl_impl.range_delegate(start, count), "Range"))

    def ScalarMult(self, scalar: int) -> 'VectorContract':
        return self.append_tree(Expression(self.dsl_impl.scalar_mult_delegate(scalar), "ScalarMult"))

    def ScalarSum(self, scalar: int) -> 'VectorContract':
        return self.append_tree(Expression(self.dsl_impl.scalar_sum_delegate(scalar), "ScalarSum"))

    def Sum(self) -> 'VectorContract':
        return self.append_tree(Expression(self.dsl_impl.sum_delegate(), "Sum"))

