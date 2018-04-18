import time

from elliptic.Kernel.DSL import DSL

from src.DSL import VectorContract
from src.DSLImpl import VectorImplementation, VectorTemplateManager, VectorMeta


dsl = DSL(VectorTemplateManager(),
          VectorContract(VectorImplementation()),
          VectorMeta())


with dsl.root() as root:
    ents = root.Range(start=0, count=100).ScalarSum(5).ScalarMult(2).Sum()


# Result of the above algorithm:
print(dsl.get_built_module().run())

# Result of the equivalent algorithm in pure Python
print(sum(((i+5)*2 for i in range(0, 100))))


# Execution time for the elliptic version:
t0 = time.time()
for i in range(0, 50000):
    dsl.get_built_module().run()
print(time.time() - t0)

# Execution time for the pure
t0 = time.time()
for i in range(0, 50000):
    sum(((i + 5) * 2 for i in range(0, 100)))
print(time.time() - t0)
