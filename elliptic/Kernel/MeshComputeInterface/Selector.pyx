
class SelectorBase(object):
    """Selectors always act either on a mesh or on entities, and always return new
    entities.
    """
    pass

class EntitySelector(SelectorBase):
    """The EntitySelector class selects entities from the mesh.
    """
    pass

class AdjacencySelector(SelectorBase):
    """The AdjacencySelector class selects adjacent entities from another
    selector.
    """
    pass
