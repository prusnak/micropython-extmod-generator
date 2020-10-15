
// This is lifted from objfloat.c, because mp_obj_float_t is not exposed there (there is no header file)
typedef struct _mp_obj_float_t {
    mp_obj_base_t base;
    mp_float_t value;
} mp_obj_float_t;

#define MP_DEFINE_FLOAT_OBJ(obj_name, f) mp_obj_float_t obj_name = {{&mp_type_float}, f} 

