from abc import ABC, abstractmethod
from array import array

class AbstractFile(ABC):

    @abstractmethod
    def from_bytes(self, bytes:bytearray) -> None:
        pass

    @abstractmethod
    def from_file(self, path:str) -> None:
        pass

    @abstractmethod
    def save_file(self, path:str) -> None:
        pass
    
    @abstractmethod
    def get_header(self) -> dict:
        pass

    @abstractmethod
    def get_samples(self) -> array:
        pass

    @abstractmethod
    def get_data(self) -> bytearray:
        pass

    @abstractmethod
    def change_data(self, data:bytearray) -> None:
        pass
    
    @abstractmethod
    def set_filename(self, filename:str) -> None:
        pass