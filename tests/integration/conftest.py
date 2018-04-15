import pytest

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.Contract import DSLContract
from elliptic.Kernel.Expression import Expression
from elliptic.Kernel.TreeBuilder import TemplateManagerBase


class SimpleDSLImpl:

    def base_delegate(self):
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

        return Delegate

    def test_delegate(self, arg: int):
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

        return Delegate


class SimpleDSLContract(DSLContract[SimpleDSLImpl]):

    def Test(self, arg):
        return self.append_tree(Expression(self.dsl_impl.test_delegate(arg), "Test"))


@pytest.fixture()
def template_manager():
    template_manager_ = TemplateManagerBase('res', 'templates')

    return template_manager_


@pytest.fixture()
def simple_dsl_contract():
    dsl_contract = SimpleDSLContract(SimpleDSLImpl())

    return dsl_contract
