
def preprocess(kernel_class):
    # TODO: Finish me!
    orig_call = kernel_class.__call__

    def __call__(self, adj):
        orig_call(self, adj)

    kernel_class.__call__ = __call__
    return kernel_class


def fill_matrix(kernel_class):
    # TODO: Finish me!
    orig_call = kernel_class.__call__

    def __call__(self, adj):
        orig_call(self, adj)

    kernel_class.__call__ = __call__
    return kernel_class
