import pytest

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.Contract import DSLContract
from elliptic.Kernel.Expression import ExpressionBase
from elliptic.Kernel.TreeBuilder import TemplateManagerBase


class SimpleDSLContract(DSLContract):

    def base_delegate(self, context) -> ContextDelegate:
        class Delegate(ContextDelegate):

            def get_template_file(self):
                return 'base.etp'

            def template_kwargs(self):
                return {'a': self.context.get_value('a'),
                        'b': self.context.get_value('b')}

            def context_enter(self):
                self.context.put_value('a', 'x')
                self.context.put_value('b', 'a')
                self.context.put_value('cur_var', 'base_str')

            def context_exit(self):
                self.context.pop_value('a')
                self.context.pop_value('b')
                self.context.pop_value('cur_var')

        return Delegate(context)

    def expression_delegate(self, context, arg: int) -> ContextDelegate:
        class Delegate(ContextDelegate):

            def get_template_file(self):
                return 'expression.etp'

            def template_kwargs(self):
                return {'append_var': self.context.get_value('cur_var'),
                        'append_val': self.context.get_value('a')}

            def context_enter(self):
                self.context.put_value('a', str(arg))

            def context_exit(self):
                self.context.pop_value('a')

        return Delegate(context)


class Expression(ExpressionBase):

    def __init__(self, arg):
        super().__init__()

        self.arg = arg
        self.name = f"Expression({arg})"

    def get_context_delegate(self, context, dsl_contract: SimpleDSLContract) -> ContextDelegate:
        return dsl_contract.expression_delegate(context=context, arg=self.arg)


@pytest.fixture()
def template_manager():
    template_manager_ = TemplateManagerBase('res', 'templates')

    return template_manager_


@pytest.fixture()
def simple_dsl_contract():
    backend_builder = SimpleDSLContract()

    return backend_builder


@pytest.fixture()
def expression():
    return Expression