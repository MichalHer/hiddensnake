from ..abstract_classes import (
    AbstractHider,
    AbstractEncrypter,
    AbstractFile
)
from copy import deepcopy
from math import ceil
from ..utils import int_to_bytearray

class LSBHider(AbstractHider):
    @property
    def samples_per_byte(self):
        return ceil(8/self.__bits)
    
    @property
    def changed_bits_number(self):
        return self.__bits

    def __init__(self, encrypter:AbstractEncrypter = None, changed_bits_number:int = 1) -> None:
        self.__encrypter = encrypter if encrypter else None
        self.set_changed_bits_number(changed_bits_number)

    def set_changed_bits_number(self, bits_number:int):
        if bits_number < 0 or bits_number > 8: raise ValueError('Bits number should be between 1 and 8.')
        self.__bits = bits_number
        self.__mask = (2**bits_number)-1

    def register_encrypter(self, encrypter:AbstractEncrypter) -> None:
        self.__encrypter = encrypter

    def hide(self, carrier_file:AbstractFile, bytea:bytearray, index:int, total:int, file_extension:str="MSG") -> AbstractFile:
        postfix = bytearray([0x2a, 0x78, 0x2a , index, 0x2f, total, 0x2a, 0x78, 0x2a] + list(bytes(file_extension, encoding="utf-8")) + [0x2a, 0x78, 0x2a])        
        byte_with_eos = bytea.copy()
        byte_with_eos.extend(postfix)
        if self.__encrypter:
            byte_with_eos = self.__encrypter.encrypt(byte_with_eos)
        byte_with_eos_and_prefix = int_to_bytearray(len(byte_with_eos), 8)
        byte_with_eos_and_prefix.extend(byte_with_eos)

        new_file = deepcopy(carrier_file)
        file_samples = carrier_file.get_samples()
        idx = 0
        for b in byte_with_eos_and_prefix:
            bint = int(b)
            current_idx = idx*self.samples_per_byte
            if current_idx + self.samples_per_byte < len(file_samples):
                for x in range(self.samples_per_byte):
                    file_samples[current_idx + x] &= ~self.__mask
                    file_samples[current_idx + x] |= bint & self.__mask
                    bint >>= self.__bits
                idx += 1
        new_file.change_data(bytearray(file_samples))
        return new_file
    
    def reveal(self, carrier_file:AbstractFile) -> bytearray:
        file_samples = carrier_file.get_samples()
        idx = 0
        result = []
        range_start = idx*self.samples_per_byte
        while range_start+self.samples_per_byte <= len(file_samples):
            window = file_samples[range_start : range_start+self.samples_per_byte]
            window.reverse()
            revaled_int = 0
            for x in window:
                revaled_int <<= self.__bits
                revaled_int += x & self.__mask
            result.append(revaled_int)
            idx += 1
            range_start = idx*self.samples_per_byte
        content_len = int.from_bytes(bytearray(result[:8]))
        if self.__encrypter:
            result = self.__encrypter.decrypt(bytearray(result[8:8+content_len]))
        end_idx = bytes(result).find(b'*x*')
        if end_idx == -1: raise Exception('Message not found.')
        file_extension = bytearray(result[end_idx+9:])
        file_extension = file_extension[:file_extension.find(b'*x*')]
        return bytearray(result[:end_idx]), result[end_idx+3], result[end_idx+5], file_extension
    
    def check_capacity(self, carrier_file:AbstractFile, file_extension:str="MSG") -> int:
        postfix_len = len(bytearray(file_extension, encoding="utf-8"))+20
        file_samples = carrier_file.get_samples()
        return int(   ((len(file_samples) - (postfix_len*self.samples_per_byte)) / self.samples_per_byte)    )
    
    