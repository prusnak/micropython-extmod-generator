'''
This is a module help.  Put it into genarated C code.
'''

__author__ = 'Module Author'


# These UPPERCASE variables are treated as constants in C code
CONST1 = 1 + 10 
CONST2 = 2.2 * 2.2
CONST3 = "333" + '444'
ONE_SHOT = False
PERIODIC = True


# We need types to generate proper variable declarations and function result in C code
def func_a():
    pass

def func_b(arg1: int) -> None:
    pass

def func_c(arg1: int, arg2: int) -> int:
    pass

def func_d(arg1: bool, arg2: str, arg3: tuple) -> int:
    pass

def func_e(arg1: list, arg2: dict, arg3, arg4) -> str:
    pass

def func_f(arg1, arg2: int, arg3, arg4, arg5: int=123) -> bytes:
    pass

def func_g(arg1, arg2, arg3: str='test', arg4=None) -> float:
    pass

def func_h(arg1, arg2, arg3, *args) -> bool:
    pass

def func_i(arg1, arg2, **kwargs) -> list:
    pass

def func_j() -> dict:
    pass

def func_k() -> tuple:
    pass

def func_l() -> complex:
    pass

def func_m() -> range:
    pass

def func_n() -> bytearray:
    pass

def func_o() -> memoryview:
    pass

def func_p() -> set:
    pass

def func_q() -> frozenset:
    pass


class Class(object):
    '''
    Class constants are supported
    '''
    CONST1 = 1
    CONST2 = 2.2
    CONST3 = "333"

    ONE_SHOT = False
    PERIODIC = True

    def __init__(self, arg1, arg2):
        pass

    def __del__(self):
        ''' We need destructor too '''
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

    def func_g(self, arg1, arg2, arg3: str='test', arg4=None) -> dict:
        pass

    def func_h(self, arg1, arg2, arg3, *args):
        pass

    def func_i(self, arg1, arg2, **kwargs):
        pass
