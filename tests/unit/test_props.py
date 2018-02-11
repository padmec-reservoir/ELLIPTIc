
class TestProps:

    def TestProps(self, elliptic_):
        mf = elliptic_.mesh_factory()

        perm_map = mf.fill_props.perm('perm_map.txt')
        poro_map = mf.fill_props.perm('poro_map.txt')
        perm0 = perm_map.get_prop('perm', i=1, j=2, k=3)
        perm1 = perm_map.get_prop('perm', i=1, j=0, k=0)
        poro0 = poro_map.get_prop('poro', i=0, j=1, k=0)
        poro1 = poro_map.get_prop('poro', i=1, j=1, k=0)


        assert perm0 == [1.0]
        assert perm1 == [0.5]
        assert poro0 == [0.1]
        assert poro1 == [0.9]
