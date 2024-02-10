from abc import ABC, abstractmethod
from array import array

class AbstractEncrypter(ABC):
    @abstractmethod
    def set_password(self, password:str) -> None:
        pass
    
    @abstractmethod
    def encrypt(self, message:bytearray) -> bytearray:
        pass

    @abstractmethod
    def decrypt(self, message:bytearray) -> bytearray:
        pass