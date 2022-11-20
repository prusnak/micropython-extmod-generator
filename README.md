micropython-extmod-generator
============================

Generator for Micropython external modules written in C

Usage
-----

```
extmod-generator [-f] module
```

Program will look for file named `module/module.py` and generate the following files:

* `module/modmodule.c` - external module source code - to be put in `micropython/extmod`
* `module/qstrdefs.h` - needs to be merged manually with `micropython/py/qstrdefs.h`

If a `module` argument is not provided, the default `example` will be used.

Examples
--------
```
$ python.exe extmod-generator.py
```
[example/example.py](example/example.py) ⇒ [example/modexample.c](example/modexample.c) + [example/qstrdefs.h](example/qstrdefs.h)

```
$ python.exe extmod-generator.py example.consts
```
[example/consts/consts.py](example/consts/consts.py) ⇒ [example/consts/consts.c](example/consts/consts.c) + [example/consts/qstrdefs.h](example/consts/qstrdefs.h)

License
-------

Licensed under MIT License.
