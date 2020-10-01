#!/usr/bin/python3

# https://stackoverflow.com/a/6798042
# https://stackoverflow.com/a/17237903

class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ClassA(metaclass=SingletonMetaClass):
    def __init__(self):
        pass


class ClassB(metaclass=SingletonMetaClass):
    def __init__(self):
        pass


def test_singleton():
    inst_a_1 = ClassA()
    inst_b_1 = ClassB()
    inst_a_2 = ClassA()
    inst_b_2 = ClassB()

    print("inst_a_1 %s inst_a_2 %s" % (inst_a_1, inst_a_2))
    print("inst_b_1 %s inst_b_2 %s" % (inst_b_1, inst_b_2))
    assert id(inst_a_1) == id(inst_a_2)
    assert id(inst_b_1) == id(inst_b_2)

    assert id(inst_a_1) != id(inst_b_1)
    assert id(inst_a_1) != id(inst_b_2)
    assert id(inst_a_2) != id(inst_b_1)
    assert id(inst_a_2) != id(inst_b_1)


if __name__ == '__main__':
    test_singleton()
