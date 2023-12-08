from ..base import BaseEncrypter
from math import ceil
from array import array
from ..utils import int_to_bytearray


key_permutation_pc1:array = array("I", [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3])

key_permutation_pc2:array = array("I", [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,33,52,45,41,49,35,28,31])

expansion_permutation:array = array("I", [31,0,1,2,3,4,3,4,5,6,7,8,7,8,9,10,11,12,11,12,13,14,15,16,15,16,17,18,19,20,19,20,21,22,23,24,23,24,25,26,27,28,27,28,29,30,31,0])

shift_table:array = array("I", [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1])

p_permutation:array = array("I", [15,6,19,20,28,11,27,16,
                                       0,14,22,25,4,17,30,9,
                                       1,7,23,13,31,26,2,8,
                                       18,12,29,5,21,10,3,24])

initial_permutation:array = array("I", [57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
                                             61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7,
                                             56,48,40,32,24,16,8,0,58,50,42,34,26,18,10,2,
                                             60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6])

final_permutation:array = array("I", [39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,
                                           37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,
                                           35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,
                                           33,1,41,9,49,17,57,25,32,0,40,8,48,16,56,24])

sboxes:list[list] = [
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    ],
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
    ],
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
    ],
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
    ],
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
    ],
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
    ],
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
    ],
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
    ]
]

class DESEncryptorCBC(BaseEncrypter):

    # _password:str
    # _key:bytearray
    # _vector:bytearray

    def set_password(self, password: str) -> None:
        self._password = password
        key = bytearray(password, encoding='utf-8')
        
        if len(key) == 8:
            self._key = int.from_bytes(key, byteorder='big')

        elif len(key) < 8:
            multiplyer = ceil(8/len(key))-1
            for __ in range(multiplyer):
                key.extend(key)
            self._key = int.from_bytes(key[:8], byteorder='big')

        else:
            shortened_key = [0,0,0,0,0,0,0,0]
            splitted_key = [key[8*i:8*(i+1)] for i in range(ceil(len(key)/8))]
            for x in splitted_key:
                new_key = []
                for y, z in zip(x, shortened_key):
                    new_key.append(z ^ y)
                shortened_key = new_key.copy() + shortened_key[len(new_key):]
            self._key = int.from_bytes(bytearray(shortened_key), byteorder='big')

    def encrypt(self, message:bytearray) -> bytearray:
        return self.__perform(message=message, reverse=False)
    
    def decrypt(self, message:bytearray) -> bytearray:
        return self.__perform(message=message, reverse=True)
    
    def __perform(self, message:bytearray, reverse:bool):
        message_chunks = [message[8*i:8*(i+1)] for i in range(ceil(len(message)/8))]
        chunk_extension = 8 - len(message_chunks[-1])
        message_chunks[-1].extend([0 for __ in range(chunk_extension)])
        keys = self.__create_keys()
        vector = int_to_bytearray(keys[0],8)
        vector.reverse()
        self._vector = int.from_bytes(vector, byteorder='big')
        if reverse == True: keys = keys[::-1]
        

        result = []
        for x in message_chunks:
            result.append(int_to_bytearray(self.__process_chunk(int.from_bytes(x, byteorder='big'), reverse, keys),8))
        result[-1][:8-chunk_extension]
        return bytearray(b''.join(result))
    
    def __process_chunk(self, chunk_int:int, reverse:bool, keys:list[int]):
        if reverse == False: 
            chunk_int ^= self._vector

        chunk = int_to_bytearray(self.__apply_permutation(chunk_int, initial_permutation),8)
        big_part = int.from_bytes(chunk[:4], byteorder='big')
        little_part = int.from_bytes(chunk[4:], byteorder='big')
        for round in range(16):
            key = keys[round]
            feisteled_little = self.__apply_feistels(little_part, key)
            xored_big_part = big_part ^ feisteled_little
            if round != 15:
                big_part = little_part
                little_part = xored_big_part
            else: 
                big_part = xored_big_part
        chunk = big_part
        chunk <<= 4*8
        chunk |= little_part
        chunk = self.__apply_permutation(chunk, final_permutation)

        if reverse == True:
            chunk ^= self._vector
            self._vector = chunk_int
        else:
            self._vector = chunk
        return chunk
    
    def __apply_feistels(self, chunk_int:int, key_int:int):
        expanded_chunk = self.__apply_permutation(chunk_int, expansion_permutation)
        expanded_chunk ^= key_int
        result = bytearray([])
        
        for idx, sbox in enumerate(sboxes):
            bits = expanded_chunk >> idx*6
            bits &= 0b111111
            result.extend([self.__apply_sbox(bits, sbox)])
        result.reverse()
        result = int.from_bytes(result, byteorder='big')
        result = self.__apply_permutation(result, p_permutation)
        return result
    
    def __apply_sbox(self, bits:int, sbox:list[int]):
        if bits not in range(64):
            raise ValueError("Value can not be interpret by sbox. Must be 0-63")
        row = bits >> 5
        row <<= 1
        row += bits & 1

        col = bits & 0b011110
        col >>= 1
        return sbox[row][col]
    
    def __create_keys(self):
        middle_key = self.__apply_permutation(self._key, key_permutation_pc1)
        keys = []
        for round in range(16):
            shift = sum(shift_table[:round+1])
            keys.append(self.__prepare_key(middle_key, -shift))
        return keys

    def __prepare_key(self, key:int, shift:int) -> bytearray:
        key_bytearray = int_to_bytearray(key, 8)
        key_big_part = key_bytearray[:4]
        key_little_part = key_bytearray[4:]
        shifted_key_big_part = self.__shift_bytes(key_big_part, shift)
        shifted_key_little_part = self.__shift_bytes(key_little_part, shift)
        new_key = int.from_bytes(shifted_key_big_part, byteorder='big') << len(shifted_key_big_part)*8
        new_key |= int.from_bytes(shifted_key_little_part, byteorder='big')
        new_key_permutation = self.__apply_permutation(new_key, key_permutation_pc2)
        return new_key_permutation

    def __shift_bytes(self, bytearr:bytearray, shift:int):
        bytearr_int = int.from_bytes(bytearr, byteorder='big')
        if shift < 0:
            mask = (2**(-shift))-1
            mask <<= (8*len(bytearr))+shift
            cutted_part = bytearr_int >> (8*len(bytearr))+shift
            bytearr_int &= ~mask
            bytearr_int <<= -shift
            bytearr_int += cutted_part
        if shift > 0:
            pass
        return int_to_bytearray(bytearr_int, len(bytearr))

    def __apply_permutation(self, chunk_int:int, perm_table:array) -> bytearray:
        result_int = 0
        for x in perm_table:
            result_int <<= 1
            result_int += (chunk_int >> x) & 1
        return result_int