from typing import Type

from elliptic.Kernel.Context import ContextDelegate
from examples.DSL_Example.src.DSL import VectorImplementationBase


class VectorImplementation(VectorImplementationBase):

    def base_delegate(self) -> Type[ContextDelegate]:
        class BaseDelegate(ContextDelegate):

            def get_template_file(self):
                return 'base.pyx.etp'

            def template_kwargs(self):
                return {'declare_variables': self.context.context['declare_variable']}

            def context_enter(self):
                pass

            def context_exit(self):
                pass

        return BaseDelegate

    def range_delegate(self, start, count) -> Type[ContextDelegate]:
        start = str(start)
        count = str(count)

        class RangeDelegate(ContextDelegate):

            def get_template_file(self):
                return 'range.pyx.etp'

            def template_kwargs(self):
                return {'count': count,
                        'index': self.context.get_value('current_index_name'),
                        'variable': self.context.get_value('current_variable_name'),
                        'counter': self.context.get_value('current_counter_name')}

            def context_enter(self):
                var_type = 'unsigned long int'
                loop_name = 'range' + str(self.unique_id)

                self.context.put_value('declare_variable', (var_type,
                                                            loop_name + 'var',
                                                            '0'))
                self.context.put_value('current_variable_name', loop_name + 'var')

                self.context.put_value('declare_variable', (var_type,
                                                            loop_name + 'counter',
                                                            start))
                self.context.put_value('current_counter_name', loop_name + 'counter')

                self.context.put_value('declare_variable', (var_type,
                                                            loop_name + 'index',
                                                            '0'))
                self.context.put_value('current_index_name', loop_name + 'index')

            def context_exit(self):
                self.context.pop_value('current_variable_name')
                self.context.pop_value('current_counter_name')
                self.context.pop_value('current_index_name')

        return RangeDelegate
