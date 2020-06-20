import dis

b = 42


def f1():
    b


def f2():
    b
    b = 42


print(f'function {f1}')
dis.dis(f1)
print(f'function {f2}')
dis.dis(f2)
