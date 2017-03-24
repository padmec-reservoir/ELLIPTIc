from padpy.Kernel import KernelBase


class Pipeline(object):

    def __init__(self, kernels):
        self.kernels = kernels

    def __or__(self, other):
        if isinstance(other, Pipeline):
            new_p = Pipeline(self.kernels + other.kernels)
            return new_p
        elif isinstance(other, KernelBase):
            new_p = Pipeline(self.kernels + [other])
            return new_p
        else:
            raise TypeError("Must use Pipeline or Kernel objects to extend a "
                            "Pipeline")

    def __iter__(self):
        return iter(self.kernels)
