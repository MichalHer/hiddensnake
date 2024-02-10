from abc import ABC, abstractmethod
from . import AbstractFile, AbstractEncrypter

class AbstractHider(ABC):
    @abstractmethod
    def hide(self, carrier_file:AbstractFile, hidden_bytes:bytearray, index:int, total:int) -> AbstractFile:
        pass
    
    @abstractmethod
    def reveal(self, carrier_file:AbstractFile) -> bytearray:
        pass
    
    @abstractmethod
    def check_capacity(self, carrier_file:AbstractFile, file_extension:str = "MSG") -> int:
        pass

    @abstractmethod
    def register_encrypter(self, encrypter:AbstractEncrypter) -> None:
        pass
    