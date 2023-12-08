from unittest import TestCase
from array import array
from stegopy.encryption.cbc_des_encryptor import CBCDESEncryptor

class TestDES(TestCase):
    def test_apply_permutation(self):
        perm_table = array('I', [3,2,5,7,0,1,4,6,
                                 8,10,15,13,14,12,11,9])
        
        test_bytes = int.from_bytes(bytearray([0b10101010, 0b01010101]))
        expected_result = int.from_bytes(bytearray([0b01001011, 0b00110011]))
        e = CBCDESEncryptor()
        permutation = e._CBCDESEncryptor__apply_permutation(test_bytes, perm_table)
        self.assertEqual(permutation, expected_result)

    def test_shift_bytes(self):
        e = CBCDESEncryptor()
        
        self.assertEqual(
            e._CBCDESEncryptor__shift_bytes(bytearray([255,0,0,0,0,0,0,0]), -4),
            bytearray([0b11110000,0,0,0,0,0,0,0b00001111])
        )

        self.assertEqual(
            e._CBCDESEncryptor__shift_bytes(bytearray([255,0,0,0,0,0,0,0]), -8),
            bytearray([0,0,0,0,0,0,0,255])
        )

        self.assertEqual(
            e._CBCDESEncryptor__shift_bytes(bytearray([255,0,0,0,0,0,0,0]), -7),
            bytearray([0b10000000,0,0,0,0,0,0,0b01111111])
        )

        self.assertEqual(
            e._CBCDESEncryptor__shift_bytes(bytearray([255,0,0,0]), -4),
            bytearray([0b11110000,0,0,0b00001111])
        )

    def test_prepare_key(self):
        key = int.from_bytes(bytearray([255,0,0,0,255,0,0,0]))
        e = CBCDESEncryptor()
        result = e._CBCDESEncryptor__prepare_key(key, -4)
        self.assertEqual(
            result,
            int.from_bytes(bytearray([0,0,10,1,1,34,32,135]))
        )