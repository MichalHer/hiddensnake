def int_to_bytearray(number:int, arr_len:int):
    result_int = number
    result_bytes = []
    while result_int > 0 or len(result_bytes) < arr_len:
        result_bytes.insert(0, result_int & 255)
        result_int >>= 8
    return bytearray(result_bytes)