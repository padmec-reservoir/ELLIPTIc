from abc import ABC, abstractmethod


class ContextDelegate(ABC):

    def __init__(self, context):
        self.context = context
        self.child = ""

    def put_value(self, name, value):
        self.context[name].append(value)

    def get_value(self, name):
        return self.context[name][-1]

    def pop_value(self, name):
        self.context[name].pop()

    def clear_values(self, name):
        self.context[name].clear()

    @abstractmethod
    def get_template_file(self):
        pass

    @abstractmethod
    def template_kwargs(self):
        pass

    @abstractmethod
    def context_enter(self):
        pass

    @abstractmethod
    def context_exit(self):
        pass