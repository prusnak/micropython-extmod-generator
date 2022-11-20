'''
A MODULE COMMENT
'''

CONST_STR = 'QWERTY'
CONST_BYTES = b'ZXCVB'
CONST_INT = 123
CONST_FLOAT = 123.123
CONST_FALSE = False
CONST_TRUE = True
CONST_DICT = {5:'five', 6:'six'}
CONST_LIST = [1, (10, 20, 30), 'asdfg', None, True, False, CONST_FALSE, 123.456, CONST_STR, [1, (10, 20, 30), 'asdfg']]
CONST_TUPLE = (1, (10, 20, 30), 'asdfg', None, True, False, CONST_FALSE, 123.456, CONST_STR, (1, (10, 20, 30), 'asdfg'))
CONST_DICT2 = {1:'one', 2:'two', 3:CONST_LIST, 4:CONST_TUPLE, 5:CONST_DICT}
CONST_SET = {'qux', 'foo', 'bar', 'baz'}
CONST_NONE = None

def test_test():
    pass

class WithConsts():
    '''
    A CLASS COMMENT
    '''

    CONST_STR = 'QWERTY'
    CONST_BYTES = b'ZXCVB'
    CONST_INT = 123
    CONST_FLOAT = 123.123
    CONST_FALSE = False
    CONST_TRUE = True
    CONST_DICT = {5:'five', 6:'six'}
    CONST_LIST = [1, (10, 20, 30), 'asdfg', None, True, False, CONST_FALSE, 123.456, CONST_STR, [1, (10, 20, 30), 'asdfg']]
    CONST_TUPLE = (1, (10, 20, 30), 'asdfg', None, True, False, CONST_FALSE, 123.456, CONST_STR, (1, (10, 20, 30), 'asdfg'))
    CONST_DICT2 = {1:'one', 2:'two', 3:CONST_LIST, 4:CONST_TUPLE, 5:CONST_DICT}
    CONST_SET = {'qux', 'foo', 'bar', 'baz'}
    CONST_NONE = None
    
    def test_test(self):
        pass
