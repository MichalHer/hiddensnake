from abc import ABC, abstractmethod
from . import BaseFile, BaseEncrypter

class BaseHider(ABC):
    @abstractmethod
    def hide(self, carrier_file:BaseFile, hidden_bytes:bytearray, index:int, total:int) -> BaseFile:
        pass
    
    @abstractmethod
    def reval(self, carrier_file:BaseFile) -> bytearray:
        pass
    
    @abstractmethod
    def check_capacity(self, carrier_file:BaseFile, file_extension:str = "MSG") -> int:
        pass

    @abstractmethod
    def register_encrypter(self, encrypter:BaseEncrypter) -> None:
        pass
    