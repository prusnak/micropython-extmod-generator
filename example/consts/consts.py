CONST_NONE = None
CONST_INT = 99
CONST_BOOL0 = False
CONST_BOOL1 = True
CONST_FLOAT = 5.5
CONST_STR = '-1aaa'
CONST_TUPLE = (1, (10, 20, 30), '22qq', True, None, False, CONST_BOOL0, 11, 11.11, '33ww', CONST_STR, (1, '22qq44', True, None, False, CONST_BOOL0, 11, '33ww66', CONST_STR, (100, 200, True, None, False)))
CONST_TUPLE_X = (-1, 7.77, (-10, -20, -30))

def test_test():
    pass

class WithConsts():
    ESP_ERR_NO_MEM = 0x101  # Out of memory
    ESP_ERR_INVALID_ARG = 0x102  # Invalid argument
    ESP_ERR_INVALID_STATE = 0x103  # Invalid state
    ESP_ERR_INVALID_SIZE = 0x104  # Invalid size
    ESP_ERR_NOT_FOUND = 0x105  # Requested resource not found
    ESP_ERR_NOT_SUPPORTED = 0x106  # Operation or feature not supported
    ESP_ERR_TIMEOUT = 0x107  # Operation timed out
    ESP_ERR_INVALID_RESPONSE = 0x108  # Received response was invalid
    ESP_ERR_INVALID_CRC = 0x109  # CRC or checksum was invalid
    ESP_ERR_INVALID_VERSION = 0x10A  # Version was invalid
    ESP_ERR_INVALID_MAC = 0x10B  # MAC address was invalid

    ESP_ERR_WIFI_BASE = 0x3000  # Starting number of WiFi error codes
    ESP_ERR_MESH_BASE = 0x4000  # Starting number of MESH error codes
    ESP_ERR_FLASH_BASE = 0x6000  # Starting number of flash error codes

    CONST_NONE = None
    CONST_INT = 99
    CONST_BOOL0 = False
    CONST_BOOL1 = True
    CONST_FLOAT = 5.5
    CONST_STR = '-1aaa'
    CONST_TUPLE = (-1, 1, (10, 20, 30), '22qq', True, None, False, CONST_BOOL0, 11, 11.11, '33ww', CONST_STR, (1, '22qq44', True, None, False, CONST_BOOL0, 11, '33ww66', CONST_STR, (100, 200, True, None, False)))
    CONST_TUPLE_X = (-2, -1, 7.77, (-10, -20, -30))
    
#     def __init__(self):
#         pass

    def test_test(self):
        pass


if __name__ == "__main__":
    print('CONST_INT', CONST_INT)
    CONST_INT += 100
    print('CONST_INT', CONST_INT)

    print(type(CONST_NONE), CONST_NONE)
    CONST_NONE = 'None'
    print(type(CONST_NONE), CONST_NONE)

    print(type(CONST_INT), CONST_INT)
    print(type(CONST_BOOL0), CONST_BOOL0)
    print(type(CONST_BOOL1), CONST_BOOL1)
    print(type(CONST_FLOAT), CONST_FLOAT)
    print(type(CONST_STR), CONST_STR)
    print(type(CONST_TUPLE), CONST_TUPLE)

    print(WithConsts)
    print(dir(WithConsts))
