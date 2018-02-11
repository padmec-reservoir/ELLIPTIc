from .Selector import Selector


class Interface(Selector):

    def __init__(self, to_ent):
        super().__init__()

        self.name = f"Interface({to_ent.unique_id})"