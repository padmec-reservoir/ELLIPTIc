from padpy.Solver import ReadOnlyMatrix


class KernelDecorator(object):

    def __init__(self, name="", share=False):
        self.name = name
        self.share = share

    def _set_kernel_name(self, kernel_class):
        if not self.name:
            kernel_class.name = kernel_class.__name__
        else:
            kernel_class.name = self.name

    def _replace_run(self, kernel_class):
        orig_run = kernel_class.run

        @classmethod
        def new_run(cls, mesh, elem, adj):
            vals = orig_run(mesh, elem, adj)
            cls.fill_array(
                vals, mesh.matrix_manager, mesh.id_map)

        kernel_class.run = new_run

    def _define_create_array(self, kernel_class):
        kernel_class.create_array = self.create_array(kernel_class)

    def _define_fill_array(self, kernel_class):
        kernel_class.fill_array = self.fill_array()

    def _define_get_array(self, kernel_class):
        kernel_class.get_array = self.get_array()

    def _set_dependency_vectors_attributes(self, kernel_class):
        @classmethod
        def set_dependency_vectors(cls, mesh):
            for dep in kernel_class.depends:
                ar = dep.get_array(mesh.matrix_manager)
                readonly_ar = ReadOnlyMatrix(ar, mesh.id_map)
                setattr(kernel_class, dep.name + '_array', readonly_ar)

        kernel_class.set_dependency_vectors = set_dependency_vectors

    def __call__(self, kernel_class):
        self._set_kernel_name(kernel_class)
        self._replace_run(kernel_class)
        self._define_create_array(kernel_class)
        self._define_fill_array(kernel_class)
        self._define_get_array(kernel_class)
        self._set_dependency_vectors_attributes(kernel_class)

        return kernel_class


class fill_vector(KernelDecorator):

    def create_array(self, kernel_class):
        @classmethod
        def new_create_array(cls, matrix_manager):
            matrix_manager.create_vector(
                kernel_class.solution_dim, kernel_class.name, self.share)

        return new_create_array

    def fill_array(self):
        @classmethod
        def new_fill_array(cls, vals, matrix_manager, id_map):
            for elem, value in vals:
                row = id_map[elem]
                matrix_manager.fill_vector(cls.name, row, value)

        return new_fill_array

    def get_array(self):
        @classmethod
        def new_get_array(cls, matrix_manager):
            return matrix_manager.get_vector(cls.name)

        return new_get_array


class fill_matrix(KernelDecorator):

    def create_array(self, kernel_class):
        @classmethod
        def new_create_array(cls, matrix_manager):
            matrix_manager.create_matrix(
                kernel_class.solution_dim, kernel_class.name, self.share)

        return new_create_array

    def fill_array(self):
        @classmethod
        def new_fill_array(cls, vals, matrix_manager, id_map):
            set_values = vals['set']
            sum_values = vals['sum']
            for elem, cols, values in set_values:
                row = id_map[elem]
                cols = [id_map[col] for col in cols]
                matrix_manager.fill_matrix(cls.name, row, cols, values)

            for elem, cols, values in sum_values:
                row = id_map[elem]
                cols = [id_map[col] for col in cols]
                matrix_manager.sum_into_matrix(cls.name, row, cols, values)

        return new_fill_array

    def get_array(self):
        @classmethod
        def new_get_array(cls, matrix_manager):
            return matrix_manager.get_matrix(cls.name)

        return new_get_array
