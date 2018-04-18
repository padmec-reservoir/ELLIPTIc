from typing import Type, Dict, Any, List

from elliptic.Kernel.Context import ContextDelegate
from elliptic.Kernel.TemplateManager import TemplateManagerBase
from elliptic.Kernel.DSL import DSLMeta

from examples.DSL_Example.src.DSL import VectorImplementationBase



class VectorTemplateManager(TemplateManagerBase):

    def __init__(self) -> None:
        super().__init__(__package__, 'Templates')


class VectorMeta(DSLMeta):

    def include_dirs(self) -> List[str]:
        return []

    def libs(self) -> List[str]:
        return []


class VectorImplementation(VectorImplementationBase):

    def base_delegate(self) -> Type[ContextDelegate]:
        class BaseDelegate(ContextDelegate):

            def get_template_file(self):
                return 'base.pyx.etp'

            def template_kwargs(self):
                return {'declare_variables': self.context.context['declare_variable'],
                        'return_variable': self.context.get_value('return_variable')}

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

    def scalar_mult_delegate(self, scalar: int) -> Type[ContextDelegate]:
        scalar = str(scalar)

        class ScalarMulDelegate(ContextDelegate):
            def get_template_file(self) -> str:
                return 'scalarmult.pyx.etp'

            def template_kwargs(self) -> Dict[str, Any]:
                return {'scalar': scalar,
                        'variable': self.context.get_value('current_variable_name')}

            def context_enter(self) -> None:
                pass

            def context_exit(self) -> None:
                pass

        return ScalarMulDelegate

    def scalar_sum_delegate(self, scalar: int) -> Type[ContextDelegate]:
        scalar = str(scalar)

        class ScalarSumDelegate(ContextDelegate):
            def get_template_file(self) -> str:
                return 'scalarsum.pyx.etp'

            def template_kwargs(self) -> Dict[str, Any]:
                return {'scalar': scalar,
                        'variable': self.context.get_value('current_variable_name')}

            def context_enter(self) -> None:
                pass

            def context_exit(self) -> None:
                pass

        return ScalarSumDelegate

    def sum_delegate(self) -> Type[ContextDelegate]:

        class SumDelegate(ContextDelegate):
            def get_template_file(self) -> str:
                return 'sum.pyx.etp'

            def template_kwargs(self) -> Dict[str, Any]:
                return {'variable': self.context.get_value('current_variable_name'),
                        'acc_variable': self.context.get_value('acc_variable_name')}

            def context_enter(self) -> None:
                self.context.put_value('declare_variable', ('int',
                                                            'acc' + str(self.unique_id),
                                                            '0'))
                self.context.put_value('acc_variable_name', 'acc' + str(self.unique_id))
                self.context.put_value('return_variable', 'acc' + str(self.unique_id))

            def context_exit(self) -> None:
                self.context.pop_value('acc_variable_name')

        return SumDelegate
