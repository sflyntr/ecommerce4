class Test:
    def __init__(self):
        self.__color = "red"

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, clr):
        self.__color = clr


def asterisk_parameter_test(param_a=None, param_b=None):
    # print(f"param_0:{param_0}, param_a:{param_a}, param_b:{param_b}")
    # print(f"param_0:{param_0}, param_a:{param_a}, param_b:{param_b}")
    print(f"param_b:{param_b}")



if __name__ == '__main__':
    t = Test()
    print(t.color)

    asterisk_parameter_test("test", param_b="world")


