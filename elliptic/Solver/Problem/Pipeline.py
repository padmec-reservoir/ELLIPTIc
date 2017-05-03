from elliptic.Kernel import KernelBase


class Pipeline(object):
    """Defines a kernel pipeline. A pipeline can be initialized with a
    sequence of kernels, and can be extended using the bitwise or operator with
    both another pipeline, or a single kernel.

    Parameters
    ----------
    kernels: list of elliptic.Kernel.Kernel.Kernel
        List of kernels to compose this pipeline.

    Example
    -------
    >>> kernels = [kernel1, kernel2, kernel3]
    >>> pipeline = Pipeline(kernels)  # Creating a pipeline
    >>> pipeline = pipeline | kernel4  # Extending a pipeline with a kernel

    """
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
