micropython-extmod-generator
============================

Generator for Micropython external modules written in C

Usage
-----

```
generate [module]
```

Program will look for file named `module.py` and generate `modmodule.c`.

If an argument is not provided, the default `example` will be used.

Generated file `modmodule-qstrdefs.h` needs to be merged manually with `micropython/py/qstrdefs.h`.

Example
-------

[example.py](example.py) ⇒ [modexample.c](modexample.c) + [modexample-qstrdefs.h](modexample-qstrdefs.h)

License
-------

Licensed under MIT License.
