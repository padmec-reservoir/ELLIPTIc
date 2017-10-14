
default_selector = None


DIM = 2

def compute_equiv_diff(mci):
    faces = mci.selector(default_selector)  # .by_ent(DIM-1).where(with_boundary=False)


def compute_2(mci):
    # For each internal face
    ent = mci.by_dim(DIM-1).where(with_boundary=False)

    # Get the adjacent volumes
    ent_adj_vols = ent.by_adj(DIM-1, DIM, 1)

    # For each adjacent volume, get the diffusivity
    D = ent_adj_vols.get_field('Diffusivity')

    # For each adjacent volume, get the centroid
    adj_C = ent_adj_vols.get_field('Centroid')

    # For each internal face, get the centroid
    ent_C = ent.get_field('Centroid')

    # Get the distance between the face and volume centroids
    dx = adj_C.sub(ent_C).norm()

    # By now, dx and D are vectors of two elements, for each internal face


    numerator = D.produtory().times(2)
    denominator = D.dot(dx)

    numerator.over(denominator).store_as('Equiv_Diff')
