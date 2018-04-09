from collections import defaultdict

import pytest

from elliptic.Kernel.Context import ContextDelegate, Context, ContextException


class SimpleContextDelegate(ContextDelegate):
    def get_template_file(self):
        pass

    def template_kwargs(self):
        pass

    def context_enter(self):
        pass

    def context_exit(self):
        pass


class TestContext:
    def setup_method(self, method):
        self.context = Context()

    def test_put_get_value(self):
        self.context.put_value('a', '1')
        self.context.put_value('a', '2')
        self.context.put_value('b', '1')

        assert self.context.get_value('a') == '2'
        assert self.context.get_value('b') == '1'

    def test_pop_value(self):
        self.context.put_value('a', '1')
        self.context.put_value('a', '2')

        assert self.context.get_value('a') == '2'
        self.context.pop_value('a')
        assert self.context.get_value('a') == '1'
        self.context.pop_value('a')

        with pytest.raises(ContextException):
            self.context.get_value('a')

        with pytest.raises(ContextException):
            self.context.pop_value('a')

    def test_clear_vales(self):
        self.context.put_value('a', '1')
        self.context.put_value('a', '2')

        self.context.clear_values('a')

        with pytest.raises(ContextException):
            self.context.get_value('a')



class TestContextDelegate:

    def test_context_delegate_raises_TypeError(self):
        with pytest.raises(TypeError):
            ContextDelegate(Context())
