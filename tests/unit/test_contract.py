from elliptic.Kernel.Contract import DSLContract
from elliptic.Kernel.Expression import Expression


class DSLStub:
    def base_delegate(self):
        return None


class ContractStub(DSLContract[DSLStub]):

    def Test(self):
        return self.append_tree(Expression(self.dsl_impl.base_delegate(), "Test"))


def test_m():
    m = ContractStub(DSLStub(), None)
    k = m.Base()
    j = k.Test()
    l = j.Test()

    assert m.expr is k.expr
    assert k.expr.children[0] is j.expr
    assert m.expr.children[0].children[0] is l.expr
