'''
This is a module help.  Put it into genarated C code.
'''

__author__ = 'Module Author'


# These UPPERCASE Python variables are treated as constants in C code
CONST_NONE = None
CONST_INT = 1 + 1
ONE_BOOL = True
CONST_FLOAT = 2.2 * 2.2
CONST_STR = "333" + '444'
CONST_TUPLE = (None, 1, 2.2, True, 'Hello, world!')

# We need types to generate proper variable declarations and function result in C code
def func_a():
    pass

def func_b(arg1: int) -> None:
    pass

def func_c(arg1: int, arg2: int) -> int:
<<<<<<< HEAD
    pass

def func_d(arg1: bool, arg2: str, arg3: tuple) -> int:
=======
>>>>>>> b213639ff1336ee7bf9d36d406c33989f5e5c093
    pass
func_c.code = "    res = arg1 + arg2;"

def func_d(arg1: bool, arg2: str, arg3: tuple) -> int:
    pass

def func_e(arg1: list, arg2: bool, arg3:int) -> str:
    pass

def func_f(arg1:float, arg2: int, arg3:bool, arg4: int=123) -> bytes:
    pass

def func_g() -> float:
    pass

def func_h() -> bool:
    pass

def func_i() -> list:
    pass

def func_k() -> tuple:
    pass

# def func_j() -> dict:
#     pass
#
# def func_l() -> complex:
#     pass
#
# def func_m() -> range:
#     pass
#
# def func_n() -> bytearray:
#     pass
#
# def func_o() -> memoryview:
#     pass
#
# def func_p() -> set:
#     pass
#
# def func_q() -> frozenset:
#     pass


class ParentClass(object):
    CONST_INT = 100
    pass


class Class(ParentClass, object):
    '''
    Class constants are supported
    '''
    CONST1 = 1
    CONST2 = 2.2
    CONST3 = "333"

    ONE_SHOT = False
    PERIODIC = True

    def __init__(self, arg1:int, arg2:bool):
        pass

    def __del__(self):
        ''' We need destructor too '''
        pass

    def func_a(self):
        pass

    def func_b(self, arg1:str):
        pass

    def func_c(self, arg1:int, arg2:float) -> None:
        pass

    def func_d(self, arg1:bool, arg2:int, arg3:float) -> int:
        pass

    def func_e(self, arg1:str, arg2:int, arg3:int, arg4:int) -> str:
        pass

    def func_f(self, arg1:float, arg2: int, arg3:int, arg4:int, arg5: int=123) -> bytes:
        pass

