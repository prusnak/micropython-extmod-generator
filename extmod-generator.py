#! /usr/bin/env python3

import argparse
import datetime
import importlib
import inspect
import os
import re
#import sys
import types

import templates

IS_EXTERNAL_MODULE = True # set False if core port module

CONSTANT_TYPES = (type(None), int, bool, float, str, tuple)


class GenericName(object):
    def __init__(self, name, classname=None):
        self.name = name
        self.classname = classname
        if classname:
            self.fullname = classname + '_' + name
        else:
            self.fullname = name


class Value(GenericName):
    def __init__(self, name, value, classname=None):
        super().__init__(name, classname)
        self.value = value


class Function(GenericName):
    def __init__(self, name, func, argspec, classname=None):
        super().__init__(name, classname)
        self.func = func    
        if classname:
            self.dotname = classname + '.' + name
        else:
            self.dotname = name
        self.argspec = argspec
        args = argspec.args

        self.args_min = -1
        self.args_max = -1
        if (argspec.varargs is None) and (argspec.varkw is None) and (argspec.defaults is None):
            if len(args) >= 0 and len(args) <= 3:
                self.type = str(len(args))
            else:
                self.type = 'var_between'
                self.args_min = len(args)
                self.args_max = len(args)
        elif (argspec.varargs is None) and (argspec.varkw is None): # and (argspec.defaults is None):
            self.type = 'var_between'
            self.args_min = len(args) - len(argspec.defaults)
            self.args_max = len(args)
        elif (argspec.varkw is None) and (argspec.defaults is None):
            self.type = 'var'
            self.args_min = len(args)
        elif (argspec.varargs is None) and (argspec.defaults is None):
            self.type = 'kw'
            self.args_min = len(args)
        else:
            raise Exception('Unsupported function type')

    def get_prototype(self):
        def anot(s):
            a = self.argspec.annotations[s]
            if a is None:
                return 'None'
            else:
                return a.__name__

        args = []
        for a in self.argspec.args:
            if a in self.argspec.annotations:
                args.append(a + ': ' + anot(a))
            else:
                args.append(a)
        if self.argspec.defaults:
            l = len(self.argspec.defaults)
            for i in range(l):
                args[-l + i] += '=' + repr(self.argspec.defaults[i])
        if self.argspec.varargs:
            args.append('*args')
        if self.argspec.varkw:
            args.append('**kwargs')
        p = 'def {name}({args})'.format(name=self.dotname, args=', '.join(args))
        if 'return' in self.argspec.annotations:
            p += ' -> {ret}'.format(ret=anot('return'))
        return p


class Class(object):
    def __init__(self, name, class_instance):
        self.name = name
        self.class_instance = class_instance
        self.methods = []
        self.defines = []
        self.vars = []

    def add_method(self, name, func_instance, argspec):
        m = Function(name, func_instance, argspec, classname=self.name)
        self.methods.append(m)


class Module(object):
    def __init__(self, name):
        importlib.invalidate_caches()
        print('Looking for module "{name}":'.format(name=name))
        try:
            self.module = importlib.import_module('{name}.{name}'.format(name=name))
        except:
            self.module = importlib.import_module('{name}'.format(name=name))
        self.path = os.path.split(self.module.__file__)[0]
        print('Found {mod}'.format(mod=self.module))
        self.year = datetime.datetime.now().year
        self.name = name
        self.NAME = name.upper()
        try:
            self.author = self.module.__author__
        except:
            self.author = ''
        self.functions = []
        self.classes = []
        self.defines = []
        self.vars = []
        for n in dir(self.module):
            a = getattr(self.module, n)
            if isinstance(a, types.FunctionType):  # function
                f = Function(n, a, inspect.getfullargspec(a))
                self.functions.append(f)
            elif isinstance(a, CONSTANT_TYPES):
                if (n[0:2] == '__') and (n[-2:] == '__'):  # and (n == n.lower())
                    pass  # '__file__', '__name__', '__package__' etc
                elif n == n.upper():
                    self.defines.append(Value(n, a))
                else:
                    self.vars.append(Value(n, a))
            elif isinstance(a, type):  # class
                c = Class(n, a)
                for m in dir(a):
                    b = getattr(a, m)
                    if isinstance(b, types.FunctionType):  # method
                        c.add_method(m, b, inspect.getfullargspec(b))
                    elif isinstance(b, CONSTANT_TYPES):
                        if (m[0:2] == '__') and (m[-2:] == '__'):  # and (m == m.lower())
                            pass
                        elif m == m.upper():
                            c.defines.append(Value(m, b, classname=c.name))
                        else:
                            c.vars.append(Value(m, b, classname=c.name))
                self.classes.append(c)
        print('Parsed OK ... loaded {f} functions and {c} classes with {m} methods'.format(f=len(self.functions), c=len(self.classes), m=sum([len(c.methods) for c in self.classes])))


class Source(object):
    def __init__(self, module):
        self.module = module
        self.lines = []
        self.lines.append(templates.header(year=self.module.year, author=self.module.author, url='https://github.com/prusnak/micropython-extmod-generator', py_stab_source=module.module.__file__))
        self.qstrdefs = []

    @property
    def csource_filename(self):
        if IS_EXTERNAL_MODULE:
            return os.path.join(self.module.path, '{module}.c'.format(module=self.module.name))
        else:
            return os.path.join(self.module.path, 'mod{module}.c'.format(module=self.module.name))

    @property
    def qstrdefs_filename(self):
        return os.path.join(self.module.path, 'qstrdefs.h')

    def append(self, line, **kwargs):
        kwargs['module'] = self.module.name
        kwargs['MODULE'] = self.module.NAME
        line = line.format(**kwargs)
        self.qstrdefs += re.findall(r'MP_QSTR_[_a-zA-Z0-9]+', line)
        self.lines.append(line)

    def append_str(self, line):
        if line is not None:
            self.lines.append(line)

    def save(self):
        with open(self.csource_filename, 'w') as f:
            f.write('\n'.join(self.lines) + '\n')
        print('Saved source as {fn}'.format(fn=self.csource_filename))
        self.qstrdefs = [x.replace('MP_QSTR_', 'Q(') + ')' for x in sorted(set(self.qstrdefs))]
        if 'Q(__name__)' in self.qstrdefs:
            self.qstrdefs.remove('Q(__name__)')
        with open(self.qstrdefs_filename, 'w') as f:
            if IS_EXTERNAL_MODULE:
                f.write('#if MODULE_{MODULE}_ENABLED\n'.format(MODULE=self.module.NAME))
            else:
                f.write('#if MICROPY_PY_{MODULE}\n'.format(MODULE=self.module.NAME))
            f.write('\n'.join(self.qstrdefs) + '\n')
            f.write('#endif\n')
        print('Saved qstrdefs as {fn}'.format(fn=self.qstrdefs_filename))


python_type_to_c_type = {
    int: "int",
    float: "float",
    bool: "bool",
    str: "char*",
    tuple: "???",
    list: "???",
    dict: "???",
    set: "???",
    # tuple: string_template(
    #     "mp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array({0}_arg, &{0}_len, &{0});"),
    # list: string_template(
    #     "mp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array({0}_arg, &{0}_len, &{0});"),
    # set: string_template(
    #     "mp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array({0}_arg, &{0}_len, &{0});"),
    None: "NULL"
    }


def headers():
    return '''// Include required definitions first.
#include "py/obj.h"
#include "py/objstr.h"
#include "py/objtuple.h"
#include "py/runtime.h"
#include "py/builtin.h"

#include "objfloat.h"

    /*
    // Example exception for any generated function
    if (some_val == 0) {
        mp_raise_ValueError("'some_val' can't be zero!");
    }
    */'''


USE_DEFINE = False


def generate_define(src, d, level, indx):
    if d.value is None:
        if USE_DEFINE:
            src.append('#define {name}\t (MP_ROM_NONE)', name=d.fullname)
        else:
            src.append('STATIC const void *{name} = MP_ROM_NONE;', name=d.fullname)
    elif type(d.value) is bool:
        if USE_DEFINE:
            src.append('#define ' + d.fullname + '\t ' + '(' + ('MP_ROM_TRUE' if d.value else 'MP_ROM_FALSE') + ')')
        else:
            src.append('STATIC const bool *{name} = {value};', name=d.fullname, value='MP_ROM_TRUE' if d.value else 'MP_ROM_FALSE')
    elif type(d.value) is int:
        if USE_DEFINE:
            src.append('#define ' + d.fullname + '\t ' + '(' + str(d.value) + ')')
        else:
            src.append('STATIC const mp_int_t {name} = {value};', name=d.fullname, value=d.value)
    elif type(d.value) is str:
        src.append('STATIC const MP_DEFINE_STR_OBJ({name}_str_obj, "{value}");', name=d.fullname, value=d.value)
    elif type(d.value) is float:
        src.append('STATIC const MP_DEFINE_FLOAT_OBJ({name}_float_obj, {value});', name=d.fullname, value=d.value)
    elif type(d.value) is tuple:
        generate_define_tuple(src, d.fullname, level, indx, d.value)
    else:
        print('generate_define', d.value, type(d.value))
        raise TypeError


def generate_define_tuple(src, name, level, indx, d):
    if len(src.lines[-1]) != 0:
        src.append('')

    for i, e in enumerate(d):
        if type(e) is tuple:
            generate_define_tuple(src, name, level + 1, i, e)

    for i, e in enumerate(d):
        if type(e) is str:
            src.append('STATIC const MP_DEFINE_STR_OBJ({name}_{level}_{i}_str_obj, "{value}");', name=name, level=level, i=i, value=e)
        elif type(e) is float:
            src.append('STATIC const MP_DEFINE_FLOAT_OBJ({name}_{level}_{i}_float_obj, {value});', name=name, level=level, i=i, value=e)

    src.append_str('const mp_rom_obj_tuple_t %s_%d_%d_tuple_obj = {{&mp_type_tuple}, %d, {' % (name, level, indx, len(d)))

    for i, e in enumerate(d):
        if e is None:
            src.append('    MP_ROM_NONE,')
        elif type(e) is bool:
            src.append('    ' + ('MP_ROM_TRUE' if e else 'MP_ROM_FALSE') + ',')
        elif type(e) is int:
            src.append('    MP_ROM_INT({value}),', value=e)
        elif type(e) is str:
            src.append('    MP_ROM_PTR(&{name}_{level}_{i}_str_obj),', name=name, level=level, i=i)
        elif type(e) is tuple:
            src.append('    MP_ROM_PTR(&{name}_{level}_{i}_tuple_obj),', name=name, level=level + 1, i=i)
        elif type(e) is float:
            src.append('    MP_ROM_PTR(&{name}_{level}_{i}_float_obj),', name=name, level=level, i=i)
        else:
            raise TypeError

    src.append_str('},};')  # end of tuple

    if level == 0:
        src.append('')


def register_defines(src, defines, classname=None):
    if len(defines):
        src.append('    #define USE_VALUE'+(('_'+classname) if classname else '')+' // Use VALUE from the Python stab code or NAME(aka #define NAME) from include files when this line is commented out')
    for i, d in enumerate(defines):
        if d.value is None:
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), MP_ROM_NONE }},', name=d.name)
        elif type(d.value) is bool:
            src.append('    #ifdef USE_VALUE')
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), ' + ('MP_ROM_TRUE' if d.value else 'MP_ROM_FALSE') + ' }},', name=d.name)
            src.append('    #else')
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), MP_ROM_INT({name}) }},', name=d.name)
            src.append('    #endif')
        elif type(d.value) is int:
            src.append('    #ifdef USE_VALUE')
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), MP_ROM_INT({value}) }},', name=d.name, value=d.value)
            src.append('    #else')
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), MP_ROM_INT({name}) }},', name=d.name)
            src.append('    #endif')
        elif type(d.value) is str:
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), MP_ROM_PTR(&{fullname}_str_obj) }},', name=d.name, fullname=d.fullname, value=d.value)
        elif type(d.value) is float:
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), MP_ROM_PTR(&{fullname}_float_obj) }},', name=d.name, fullname=d.fullname)
        elif type(d.value) is tuple:
            src.append('    {{ MP_ROM_QSTR(MP_QSTR_{name}), MP_ROM_PTR(&{fullname}_0_{i}_tuple_obj) }},', name=d.name, fullname=d.fullname, i=i)
        else:
            raise TypeError


def generate_var(src, v):
    #TODO
    #print(v.fullname, v.value)
    if type(v.value) is str:
        src.append('static ' + python_type_to_c_type[type(v.value)] + ' ' + v.fullname + '\t= ' + '"' + v.value + '";')
    else:
        src.append('static ' + python_type_to_c_type[type(v.value)] + ' ' + v.fullname + '\t= ' + str(v.value) + ';')


def format_comment(doc):
    lines = doc.splitlines()
    while (len(lines) > 0) and (lines[len(lines)-1].strip() == ''):  # delete the last empty lines
        lines.pop(len(lines)-1)
    while (len(lines) > 0) and (len(lines[0].strip()) == 0):  # delete leading empty lines
        lines.pop(0)
    for i in range(len(lines)):  # truncate spaces lines
        if len(lines[i].strip()) == 0:
            lines[i] = ''
    n = 99999
    for i in range(len(lines)):  # calculate length of leading spaces for remove
        s = lines[i].lstrip()
        if len(s) != 0:
            n = min(n, len(lines[i]) - len(s))
    for i in range(len(lines)):  # remove leading spaces
        lines[i] = lines[i][n:]
    return ''.join(['\n' + line for line in lines])+'\n'


def generate_function(src, f):
    src.append('// ' + f.get_prototype())

    if f.func.__doc__ is not None:
        src.append('/*' + format_comment(f.func.__doc__) + '*/')

    sig = inspect.signature(f.func)

    # special case for constructor
    if f.name == '__init__':
        src.append('STATIC mp_obj_t {module}_{classname}_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {{', classname=f.classname)
        if f.type == '0':
            pass  # should not happen
        elif f.type == '1':
            src.append('    mp_arg_check_num(n_args, n_kw, 0, 0, false);')
        elif f.type == '2':
            src.append('    mp_arg_check_num(n_args, n_kw, 1, 1, false);')
        elif f.type == '3':
            src.append('    mp_arg_check_num(n_args, n_kw, 2, 2, false);')
        elif f.type == 'var':
            src.append('    mp_arg_check_num(n_args, n_kw, {args_min}, 999, false);', args_min=f.args_min - 1)
        elif f.type == 'var_between':
            src.append('    mp_arg_check_num(n_args, n_kw, {args_min}, {args_max}, false);', args_min=f.args_min - 1, args_max=f.args_max - 1)
        elif f.type == 'kw':
            src.append('    mp_arg_check_num(n_args, n_kw, {args_min}, 999, true);', args_min=f.args_min - 1)
        else:
            raise Exception('Unknown function type: {type}'.format(type=f.type))
            
        src.append('    mp_obj_{module}_{classname}_t *self = m_new_obj(mp_obj_{module}_{classname}_t);', classname=f.classname)
        src.append('    self->base.type = &{module}_{classname}_type;', classname=f.classname)
        src.append("")
        src.append_str(parse_params(f, sig.parameters))
        src.append(code(f))
        src.append("")
        src.append('    return MP_OBJ_FROM_PTR(self);')
        src.append('}}')
        src.append('')
        
        src.append('STATIC mp_obj_t {module}_{classname}_print(const mp_print_t *print, mp_obj_t self_obj, mp_print_kind_t kind) {{', classname=f.classname)
        src.append('    {module}_{classname}_obj_t *self = MP_OBJ_TO_PTR(self_obj);', classname=f.classname)

        src.append('    mp_printf(print, "{classname}()");', classname=f.classname)
        src.append("")
        src.append(code(f))
        src.append("")
        src.append('}}')
        src.append('')
        return

#     if f.type == '0':
#         src.append('STATIC mp_obj_t {module}_{function}(void) {{', function=f.fullname)
#     elif f.type == '1':
#         src.append('STATIC mp_obj_t {module}_{function}(mp_obj_t {args[0]}_obj) {{', function=f.fullname, args=f.argspec.args)
#     elif f.type == '2':
#         src.append('STATIC mp_obj_t {module}_{function}(mp_obj_t {args[0]}_obj, mp_obj_t {args[1]}_obj) {{', function=f.fullname, args=f.argspec.args)
#     elif f.type == '3':
#         src.append('STATIC mp_obj_t {module}_{function}(mp_obj_t {args[0]}_obj, mp_obj_t {args[1]}_obj, mp_obj_t {args[2]}_obj) {{', function=f.fullname, args=f.argspec.args)
#     elif f.type == 'var':
#         src.append('STATIC mp_obj_t {module}_{function}(size_t n_args, const mp_obj_t *args) {{', function=f.fullname)
#     elif f.type == 'var_between':
#         src.append('STATIC mp_obj_t {module}_{function}(size_t n_args, const mp_obj_t *args) {{', function=f.fullname)
#     elif f.type == 'kw':
#         src.append('STATIC mp_obj_t {module}_{function}(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {{', function=f.fullname)
#     else:
#         raise Exception('Unknown function type: {type}'.format(type=f.type))

    s = function_init(f"{f.func.__module__}_{f.fullname}")
    s += function_params(f, sig.parameters)
    src.append_str(s)

    src.append_str(parse_params(f, sig.parameters))

    ret_init = ret_val_init(sig)
    if ret_init:
        src.append(ret_init)

#     src.append('    // TODO')
#     src.append('    return mp_const_none;')
    
    src.append("")
    src.append(code(f))
    src.append("")
    src.append_str(ret_val_return(sig.return_annotation))
    
    src.append('}}')

    if f.type == '0':
        src.append('STATIC MP_DEFINE_CONST_FUN_OBJ_0({module}_{function}_obj, {module}_{function});', function=f.fullname)
    elif f.type == '1':
        src.append('STATIC MP_DEFINE_CONST_FUN_OBJ_1({module}_{function}_obj, {module}_{function});', function=f.fullname)
    elif f.type == '2':
        src.append('STATIC MP_DEFINE_CONST_FUN_OBJ_2({module}_{function}_obj, {module}_{function});', function=f.fullname)
    elif f.type == '3':
        src.append('STATIC MP_DEFINE_CONST_FUN_OBJ_3({module}_{function}_obj, {module}_{function});', function=f.fullname)
    elif f.type == 'var':
        src.append('STATIC MP_DEFINE_CONST_FUN_OBJ_VAR({module}_{function}_obj, {args_min}, {module}_{function});', function=f.fullname, args_min=f.args_min)
    elif f.type == 'var_between':
        src.append('STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN({module}_{function}_obj, {args_min}, {args_max}, {module}_{function});', function=f.fullname, args_min=f.args_min, args_max=f.args_max)
    elif f.type == 'kw':
        src.append('STATIC MP_DEFINE_CONST_FUN_OBJ_KW({module}_{function}_obj, {args_min}, {module}_{function});', function=f.fullname, args_min=f.args_min)
    else:
        raise Exception('Unknown function type: {type}'.format(type=f.type))
    src.append('')


def generate_class(src, c):
    parents = ''
    for base in c.class_instance.__bases__:
        parents += (base.__name__ + ', ')
    if parents[-2:] == ', ':
        parents = parents[:-2]
    src.append('// class {classname}({parents}):', classname=c.name, parents=parents)
    if c.class_instance.__doc__ is not None:
        src.append('/*' + format_comment(c.class_instance.__doc__) + '*/')

    if len(c.defines) > 0:
        src.append('// {classname} constants', classname=c.name)
    for indx, d in enumerate(c.defines):
        generate_define(src, d, 0, indx)
    if len(c.defines) > 0:
        src.append('')

    src.append('STATIC const mp_obj_type_t {module}_{classname}_type;', classname=c.name)
    src.append('')
    
    src.append('typedef struct _mp_obj_{module}_{classname}_t {{', classname=c.name)
    src.append('    mp_obj_base_t base;')
    src.append('}} mp_obj_{module}_{classname}_t;', classname=c.name)
    src.append('')
    
    if len(c.methods) > 0:
        src.append('// Defining {classname} methods', classname=c.name)
    for f in c.methods:
        generate_function(src, f)

    src.append('// {classname} stuff', classname=c.name)
    src.append('// Register class methods')
    src.append('STATIC const mp_rom_map_elem_t {module}_{classname}_locals_dict_table[] = {{', classname=c.name)
    for f in c.methods:
        if f.name == '__init__':
            continue
        src.append('    {{ MP_ROM_QSTR(MP_QSTR_{function}), MP_ROM_PTR(&{module}_{classname}_{function}_obj) }},', classname=c.name, function=f.name)
    register_defines(src, c.defines, classname=c.name)
    src.append('}};')

    src.append('STATIC MP_DEFINE_CONST_DICT({module}_{classname}_locals_dict, {module}_{classname}_locals_dict_table);', classname=c.name)
    src.append('')

    src.append('// Create the class-object itself')
    src.append('STATIC const mp_obj_type_t {module}_{classname}_type = {{', classname=c.name)
    src.append('    {{ &mp_type_type }},')
    src.append('    .name = MP_QSTR_{classname},', classname=c.name)
    found = False
    for e in c.methods:
        if e.name == '__init__':
            found = True
            break
    if found:
        src.append('    .make_new = {module}_{classname}_make_new,', classname=c.name)
        src.append('    //.print = {module}_{classname}_print,', classname=c.name)
    src.append('    .locals_dict = (mp_obj_dict_t*)&{module}_{classname}_locals_dict,', classname=c.name)
    src.append('}};')
    src.append('')


def generate(module, force=False):
    print('Generating source code:')
    src = Source(module)

    if module.module.__doc__ is not None:
        src.append('/*' + format_comment(module.module.__doc__) + '*/\n')
        
    if IS_EXTERNAL_MODULE:
        src.append('#define MODULE_{MODULE}_ENABLED (1) // you may relocate this line to the mpconfigport.h')
        src.append('#if MODULE_{MODULE}_ENABLED')
        src.append('')
        src.append_str(headers())
    else:
        src.append('#if MICROPY_PY_{MODULE}')
    src.append('')

    if len(module.defines) > 0:
        src.append('/*')
        src.append('// Module constants declarations')
    for indx, d in enumerate(module.defines):
        generate_define(src, d, 0, indx)
    if len(module.defines) > 0:
        src.append('*/')
        src.append('')

    if len(module.vars) > 0:
        src.append('// Module variables declarations')
    for v in module.vars:
        generate_var(src, v)
    if len(module.vars) > 0:
        src.append('')

    if len(module.functions) > 0:
        src.append('// Defining module functions')
    for f in module.functions:
        generate_function(src, f)

    if len(module.classes) > 0:
        src.append('// Defining classes')
    for c in module.classes:
        generate_class(src, c)

    src.append('')
    src.append('// module stuff')
    src.append("// Set up the module properties")
    src.append('STATIC const mp_rom_map_elem_t {module}_globals_table[] = {{')
    src.append('    {{ MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_{module}) }},')

    for f in module.functions:
        src.append('    {{ MP_ROM_QSTR(MP_QSTR_{function}), MP_ROM_PTR(&{module}_{function}_obj) }},', function=f.name)

    for c in module.classes:
        src.append('    {{ MP_ROM_QSTR(MP_QSTR_{classname}), MP_ROM_PTR(&{module}_{classname}_type) }},', classname=c.name)

    register_defines(src, module.defines)

    src.append('}};')
    src.append('STATIC MP_DEFINE_CONST_DICT({module}_globals, {module}_globals_table);')
    src.append('')

    src.append("// Define the module object")
    src.append('const mp_obj_module_t {module}_cmodule = {{')
    src.append('    .base = {{ &mp_type_module }},')
    # src.append('    //.name = MP_QSTR_{module}, // absent')
    src.append('    .globals = (mp_obj_dict_t*)&{module}_globals,')
    src.append('}};')
    if IS_EXTERNAL_MODULE:
        src.append("// Register the module")
        src.append('MP_REGISTER_MODULE(MP_QSTR_{module}, {module}_cmodule, MODULE_{MODULE}_ENABLED);')
        src.append('')
        src.append('#endif // MODULE_{MODULE}_ENABLED')
    else:
        src.append('')
        src.append('#endif // MICROPY_PY_{MODULE}')

    print('Done')

    for fn in (src.csource_filename, src.qstrdefs_filename):
        if os.path.exists(fn) and not force:
            print("Output file '{}' already exists. "
                  "Use option -f to overwrite.".format(fn))
            break
    else:
        src.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--force-overwrite',
        action="store_true",
        help="Force overwriting of output file(s) even if they already exist.")
    parser.add_argument(
        'module',
        nargs='?',
        default='example',
        help="Name of Python source module.")

    args = parser.parse_args()

    module = Module(args.module)
    generate(module, args.force_overwrite)

#= uStubby based ===========================================================================================
def string_template(base_str):
    def string_handle(*args, **kwargs):
        return base_str.format(*args, **kwargs)
    return string_handle
 
in_type_handler = {
    int: string_template("\tmp_int_t {0} = mp_obj_get_int({0}_obj);"),
    float: string_template("\tmp_float_t {0} = mp_obj_get_float({0}_obj);"),
    bool: string_template("\tbool {0} = mp_obj_is_true({0}_obj);"),
    str: string_template("\tconst char* {0} = mp_obj_str_get_str({0}_obj);"),
    tuple: string_template("\tmp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array({0}_arg, &{0}_len, &{0});"),
    list: string_template("\tmp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array({0}_arg, &{0}_len, &{0});"),
    set: string_template("\tmp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array({0}_arg, &{0}_len, &{0});"),
    object: string_template("\tmp_obj_t {0} args[ARG_{0}].u_obj;"),
    'self': string_template("\tmp_obj_{1}_{2}_t *{0} = MP_OBJ_TO_PTR({0}_obj);"),
    inspect._empty: string_template("??? in_type_handler[inspect._empty]"),
    None: string_template("??? in_type_handler[None]"),
    type(None): string_template("??? in_type_handler[type(None)]")
    }

in_type_handler_arr = {
    int: string_template("\tmp_int_t {0} = mp_obj_get_int(args[{3}]);"),
    float: string_template("\tmp_float_t {0} = mp_obj_get_float(args[{3}]);"),
    bool: string_template("\tbool {0} = mp_obj_is_true(args[{3}]);"),
    str: string_template("\tconst char* {0} = mp_obj_str_get_str(args[{3}]);"),
    tuple: string_template("\tmp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array(args[{3}], &{0}_len, &{0});"),
    list: string_template("\tmp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array(args[{3}], &{0}_len, &{0});"),
    set: string_template("\tmp_obj_t *{0} = NULL;\n\tsize_t {0}_len = 0;\n\tmp_obj_get_array(args[{3}], &{0}_len, &{0});"),
    object: string_template("\tmp_obj_t {0} args[ARG_{0}].u_obj;"),
    'self': string_template("\tmp_obj_{1}_{2}_t *{0} = MP_OBJ_TO_PTR(args[{3}]);"),
    inspect._empty: string_template("??? in_type_handler_arr[inspect._empty]"),
    None: string_template("??? in_type_handler_arr[None]"),
    type(None): string_template("??? in_type_handler_arr[type(None)]")
    }

return_type_handler = {
    int: "\tmp_int_t ret_val;",
    float: "\tmp_float_t ret_val;",
    bool: "\tbool ret_val;",
    str: "",
    bytes: "",
    tuple: "",
    list: "",
    dict: "",
    object: "",
    set: "",
    inspect._empty: "",
    None: ""
    }

return_handler = {
    int: "\treturn mp_obj_new_int(ret_val);",
    float: "\treturn mp_obj_new_float(ret_val);",
    bool: "\treturn mp_obj_new_bool(ret_val);",
    str: """\t// signature: mp_obj_t mp_obj_new_bytes(const char* data, size_t len);
    return mp_obj_new_str("hello", 5);""",
    tuple: '''\t// signature: mp_obj_t mp_obj_new_tuple(size_t n, const mp_obj_t *items);
    mp_obj_t ret_val[] = {
        mp_obj_new_int(123),
        mp_obj_new_float(456.789),
        mp_obj_new_str("hello", 5),
    };
    return mp_obj_new_tuple(3, ret_val);''',
    bytes: '''\t// signature: mp_obj_t mp_obj_new_bytes(const byte* data, size_t len);
    return mp_obj_new_bytes("hello", 5);''',
    list: '''\t// signature: mp_obj_t mp_obj_new_list(size_t n, const mp_obj_t *items);
    mp_obj_t ret_val[] = {
        mp_obj_new_int(123),
        mp_obj_new_float(456.789),
        mp_obj_new_str("hello", 5),
    };
    return mp_obj_new_list(3, ret_val);''',
    dict: '''\tmp_obj_t ret_val = mp_obj_dict(0);
    mp_obj_dict_store(ret_val, mp_obj_new_str("element1", 8), mp_obj_new_int(123));
    mp_obj_dict_store(ret_val, mp_obj_new_str("element2", 8), mp_obj_new_float(456.789));
    mp_obj_dict_store(ret_val, mp_obj_new_str("element3", 8), mp_obj_new_str("hello", 5));
    return ret_val;''',
    object: '''\treturn mp_const_none; // TODO''',
    inspect._empty: "\treturn mp_const_none;",
    None: "\treturn mp_const_none;"
    }

shortened_types = {
    int: "int",
    object: "obj",
    bool: "bool",
    None: "null",
    inspect._empty: 'aaa'
    }

def in_type_init(name, _type, default):
    if name == 'self':
        return in_type_handler['self']
    if _type == inspect._empty:
        return in_type_handler_arr[type(default)]
    return in_type_handler[_type]

def in_type_init_arr(name, _type, default):
    if name == 'self':
        return in_type_handler_arr['self']
    if _type == inspect._empty:
        return in_type_handler_arr[type(default)]
    return in_type_handler_arr[_type]

def ret_val_init(sig):
    return return_type_handler[sig.return_annotation]

def ret_val_return(ret_type):
    return return_handler[ret_type]

def kw_enum(params):
    return f"\tenum {{ {', '.join(['ARG_' + k for k in params])} }};"

def kw_allowed_args(f, params):
    args = []
    for name, param in params.items():
        if param.kind in [param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY]:
            arg_type = "MP_ARG_REQUIRED"
        else:
            arg_type = "MP_ARG_KW_ONLY"
        type_txt = shortened_types[param.annotation]
        if param.default is inspect._empty:
            default = ""
        elif param.default is None:
            default = f"{{ .u_{type_txt} = MP_OBJ_NULL }}"
        else:
            default = f"{{ .u_{type_txt} = {param.default} }}"
        args.append(f"{{ MP_QSTR_{name}, {arg_type} | MP_ARG_{type_txt.upper()}, {default} }},")
    args = "\n\t\t".join(args)
    return f"\n\tSTATIC const mp_arg_t {f.__module__}_{f.__name__}_allowed_args[] = {{\n\t\t{args}\n\t}};"

def arg_array(f):
    args = f"{f.__module__}_{f.__name__}_allowed_args"
    return f"\tmp_arg_val_t args[MP_ARRAY_SIZE({args})];\n" \
        f"\tmp_arg_parse_all(n_args - 1, pos_args + 1, kw_args,\n" \
        f"\t\tMP_ARRAY_SIZE({args}), {args}, args);"


def arg_unpack(params):
    return "\n".join(f"\tmp_{shortened_types[param.annotation]}_t {name} = args[ARG_{name}].u_{shortened_types[param.annotation]};" for name, param in params.items())


def function_init(func_name):
    return f"STATIC mp_obj_t {func_name}("


def function_params(f, params):
    if f.type == '0':        
        return "void) {"
    elif f.type in ('1', '2', '3'):
        params = ", ".join([f"mp_obj_t {x}_obj" for x in params])
        return params + ") {"
    elif f.type in ['var', 'var_between']:
        return "size_t n_args, const mp_obj_t *args) {"
    elif f.type == 'kw':
        return "size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {"
    else:
        raise Exception('Unknown function type: {type}'.format(type=f.type))


def ordereddict_to_dict(value):
    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = ordereddict_to_dict(v)
    return dict(value)


def parse_params(f, params):
    """
    :param params: Parameter signature from inspect.signature
    :return: list of strings defining the parsed parameters in c
    """
    if f.type != '0':        
        #for i, e in enumerate(params.items()):
        for e in params.items():
            param, value = e
            if value.annotation == inspect._empty: # and value.default == inspect._empty:
                if (param == 'self'): 
                    pass
                elif value.default != inspect._empty:
                    pass
                else:
                    print('Please annotate type of parameter: File {module}, Line {line}, Function {function}, Parameter {parameter} Type {value}'.format(
                        module=f.func.__code__.co_filename, line=f.func.__code__.co_firstlineno, function=f.func.__name__, parameter=param, value=value.annotation))#__module__
                    # raise TypeError()
                    return None

    if f.type == '0':        
        return None
    elif f.type in ['1', '2', '3']:
        return ''.join([in_type_init(param, value.annotation, value.default)(param, f.func.__module__, f.classname)+'\n' for param, value in params.items()])
    elif f.type in ['var', 'var_between']:
        return ''.join([in_type_init_arr(param, value.annotation, value.default)(param, f.func.__module__, f.classname, ind)+'\n' for ind, (param, value) in enumerate(params.items())])
    elif f.type == 'kw':
        return ''.join([kw_enum(params), kw_allowed_args(f.func, params), "", arg_array(f.func), "", arg_unpack(params)])
    else:
        raise Exception('Unknown function type: {type}'.format(type=f.type))


def code(f):
    try:
        return f.func.code
    except AttributeError:
        return "\t//TODO: Your code here"


if __name__ == "__main__":
    main()
