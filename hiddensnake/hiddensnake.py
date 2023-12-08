from .base import (
    BaseFile,
    BaseHider
)

from threading import Thread
import os
from copy import deepcopy

CPU_CORES = os.cpu_count()

class HiddenSnake:
    # hider:BaseHider
    # carrier_files:list[BaseFile]
    # hidden_bytes:bytearray

    def __init__(self, hider:BaseHider = None) -> None:
        self.hider = hider
        self.carrier_files = []
        self.hidden_bytes = None
        self.file_extension = ""
    
    def register_hider(self, hider:BaseHider) -> None:
        self.hider = hider

    def register_carrier_file(self, carrier_file:BaseFile) -> None:
        self.carrier_files.append(carrier_file)

    def register_hidden_bytes(self, hidden_bytes:bytearray, file_extension:str="MSG") -> None:
        self.hidden_bytes = hidden_bytes
        self.file_extension = file_extension

    def can_hide(self, file_extension:str="MSG"):
        self.__check_hidden_bytes_are_specified()
        capacity = self.get_carrier_files_capacity(file_extension)
        if len(self.hidden_bytes) <= capacity: return True
        else: False

    def hide(self) -> list[BaseFile]:
        threads:list[Thread] = []
        self.__check_hidden_bytes_are_specified()
        result = [None for __ in range(len(self.carrier_files))]
        bytea_parts = []
        
        hidden_bytes_len = len(self.hidden_bytes)
        capacity = self.get_carrier_files_capacity(self.file_extension)
        last_hidden_pointer = 0
        for idx, f in enumerate(self.carrier_files):
            part = self.hider.check_capacity(f, self.file_extension)/capacity
            hidden_bytes_part = int(hidden_bytes_len * part)
            bytea_parts.append([last_hidden_pointer, hidden_bytes_part])
            last_hidden_pointer += hidden_bytes_part
        
        while last_hidden_pointer != hidden_bytes_len:
            bytea_parts[-1][-1] += 1
            last_hidden_pointer += 1

        for x in range(min(CPU_CORES, len(self.carrier_files))):
            t = Thread(target=self.__hiding_thread, args=(bytea_parts, result, x, CPU_CORES, len(self.carrier_files)), daemon=True)
            t.start()
            threads.append(t)

        for thd in threads:
            thd.join()
        
        return result
    
    def __hiding_thread(self, bytea_parts:list[tuple], result_list:list, start_pos:int, step:int, total:int):
        idx = start_pos
        hdr:BaseHider = deepcopy(self.hider)
        while idx < total:
            bp = bytea_parts[idx]
            result_list[idx] = hdr.hide(self.carrier_files[idx], self.hidden_bytes[bp[0]:bp[0]+bp[1]], idx+1, total, self.file_extension)
            idx += step

    def reval(self) -> bytearray:
        threads = []
        result = [None for __ in range(len(self.carrier_files))]
        for x in range(min(CPU_CORES, len(self.carrier_files))):
            t = Thread(target = self.__reval_thread, args = (result, x, CPU_CORES, len(self.carrier_files)), daemon=True)
            t.start()
            threads.append(t)

        for thd in threads:
            thd.join()

        return b''.join(result), self.file_extension.decode()
    
    def __reval_thread(self, result_list:list, start_pos:int, step:int, total:int):
        idx = start_pos
        hdr:BaseHider = deepcopy(self.hider)
        while idx < total:
            revaled_bytes = hdr.reval(self.carrier_files[idx])
            if revaled_bytes[2] != total: raise Exception(f'Carrier file content does not fit to revaled data ({revaled_bytes[2]} vs {total}).')
            result_list[revaled_bytes[1]-1] = revaled_bytes[0]
            if idx == 0: self.file_extension = revaled_bytes[3]
            idx += step
    
    def get_carrier_files_capacity(self, file_extension:str="MSG") -> int:
        return int(sum([self.hider.check_capacity(x, file_extension) for x in self.carrier_files]))

    def __check_hidden_bytes_are_specified(self):
        if not self.hidden_bytes: raise Exception('Hidden bytes are not specified.')

    