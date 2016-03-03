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

Example
-------

* input: [example.py](example.py)
* output: [modexample.c](modexample.c)

License
-------

Licensed under MIT License.
