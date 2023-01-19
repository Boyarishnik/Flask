
from time import time_ns


class A:

    def a(self):
        pass

    @staticmethod
    def b():
        pass


obj = A()

a = time_ns()
for _ in range(1000000):
    obj.a()
print(a - time_ns())

a = time_ns()
for _ in range(1000000):
    obj.b()
print(a - time_ns())