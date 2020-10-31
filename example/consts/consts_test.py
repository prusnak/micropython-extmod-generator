import consts

print(type(consts.CONST_NONE), consts.CONST_NONE)
print(type(consts.CONST_INT), consts.CONST_INT)
print(type(consts.CONST_BOOL0), consts.CONST_BOOL0)
print(type(consts.CONST_BOOL1), consts.CONST_BOOL1)
print(type(consts.CONST_FLOAT), consts.CONST_FLOAT)
print(type(consts.CONST_STR), consts.CONST_STR)
print(type(consts.CONST_TUPLE), consts.CONST_TUPLE)
print(type(consts.CONST_TUPLE_X), consts.CONST_TUPLE_X)
print(type(consts.CONST_TUPLE_X[0]), consts.CONST_TUPLE_X[0])

print(type(consts.CONST_NONE), consts.CONST_NONE)
#consts.CONST_NONE = 'NoneStr'
print(type(consts.CONST_NONE), consts.CONST_NONE)

print('CONST_INT', type(consts.CONST_INT), consts.CONST_INT)
#consts.CONST_INT += 100
print('CONST_INT', type(consts.CONST_INT), consts.CONST_INT)

print('consts.CONST_FLOAT', type(consts.CONST_FLOAT), consts.CONST_FLOAT)
#consts.CONST_FLOAT += 15.15
print('consts.CONST_FLOAT', type(consts.CONST_FLOAT), consts.CONST_FLOAT)

print(dir(consts.WithConsts))
print(consts.WithConsts)
print(consts.WithConsts.CONST_TUPLE)
print(consts.WithConsts.CONST_TUPLE_X)
print(consts.WithConsts.CONST_TUPLE_X[0])
