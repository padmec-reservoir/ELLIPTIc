
class TestGrid:

    def test_grid(self, elliptic_):
        mf = elliptic_.mesh_factory()

        my_grid = mf.grid(nx=1, ny=2, nz=3,
                          dx=3, dy=2, dz=1)
        v0 = my_grid.get_coord(0, 0, 0)
        v1 = my_grid.get_coord(1, 0, 0)
        v2 = my_grid.get_coord(0, 1, 0)

        assert v0 == [0.0, 0.0, 0.0]
        assert v1 == [3.0, 0.0, 0.0]
        assert v2 == [0.0, 2.0, 0.0]
