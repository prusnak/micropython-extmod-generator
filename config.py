import datetime

class Config(object):
    pass

config = Config()

config.author = 'Pavol Rusnak'
config.module = 'base64'
config.functions = {
    'b64encode': 'b',
    'b64decode': 'b',
}

config.year = datetime.datetime.now().year
config.MODULE = config.module.upper()
