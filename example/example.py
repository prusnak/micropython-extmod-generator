__author__ = 'Module Author'


def func_a():
    pass

def func_b(arg1):
    pass

def func_c(arg1, arg2) -> None:
    pass

def func_d(arg1, arg2, arg3) -> int:
    pass

def func_e(arg1, arg2, arg3, arg4) -> str:
    pass

def func_f(arg1, arg2: int, arg3, arg4, arg5: int=123) -> bytes:
    pass

def func_g(arg1, arg2, arg3: str='test', arg4=None):
    pass

def func_h(arg1, arg2, arg3, *args):
    pass

def func_i(arg1, arg2, **kwargs):
    pass


class Class(object):

    def __init__(self, arg1, arg2):
        pass

    def func_a(self):
        pass

    def func_b(self, arg1):
        pass

    def func_c(self, arg1, arg2) -> None:
        pass

    def func_d(self, arg1, arg2, arg3) -> int:
        pass

    def func_e(self, arg1, arg2, arg3, arg4) -> str:
        pass

    def func_f(self, arg1, arg2: int, arg3, arg4, arg5: int=123) -> bytes:
        pass

    def func_g(self, arg1, arg2, arg3: str='test', arg4=None):
        pass

    def func_h(self, arg1, arg2, arg3, *args):
        pass

    def func_i(self, arg1, arg2, **kwargs):
        pass
