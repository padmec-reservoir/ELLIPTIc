
class TestGrid:

    def test_grid(self, elliptic_):
        mf = elliptic_.mesh_factory()

        my_grid = mf.grid(nx=1, ny=2, nz=3,
                          dx=3, dy=2, dz=1)
        v0 = my_grid.get_vertex(0, 0, 0)
        v1 = my_grid.get_vertex(1, 0, 0)
        v2 = my_grid.get_vertex(0, 1, 0)

        assert v0.coord() == [0.0, 0.0, 0.0]
        assert v1.coord() == [3.0, 0.0, 0.0]
        assert v2.coord() == [0.0, 4.0, 0.0]

        elliptic_.set_mesh(my_grid)
