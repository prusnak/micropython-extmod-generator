def includes(**kwargs):
    return """#include <stdio.h>
#include <assert.h>
#include <string.h>

#include "py/nlr.h"
#include "py/runtime.h"
#include "py/binary.h"
#include "mod{module}.h"
""".format(**kwargs)
