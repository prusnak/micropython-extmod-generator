import datetime

class Config(object):
    pass

class FuncType(object):
    def __init__(self, name, type, args_min=None, args_max=None):
        self.name = name
        self.type = type
        self.args_min = args_min
        self.args_max = args_max

config = Config()

config.author = 'Pavol Rusnak'
config.module = 'example'
config.functions = [
    FuncType('func0', '0'),
    FuncType('func1', '1'),
    FuncType('func2', '2'),
    FuncType('func3', '3'),
    FuncType('func4', 'var', 3),
    FuncType('func5', 'var_between', 2, 4),
    FuncType('func5', 'kw', 1),
]

config.year = datetime.datetime.now().year
config.MODULE = config.module.upper()
