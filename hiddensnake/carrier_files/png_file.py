import png

from PIL import Image
from array import array
from ..abstract_classes import AbstractFile

img_modes = {
    "RGB":3,
    "RGBA":4
}

class PngFile(AbstractFile):
    def from_bytes(self, bytes: bytearray) -> None:
        pass
    
    def from_file(self, path: str) -> None:
        self.__file = Image.open(path)
        self.__mode = self.__file.mode
        self.__bytes_on_pixel = img_modes[self.__mode]
        self.__file_width = self.__file.width
        self.__file_height = self.__file.height
        self.__data = self.__transform_PIL_data(self.__file.getdata())
        
    
    def save_file(self, path: str) -> None:
        png.from_array(self.__data, mode=self.__mode).save(path)
    
    def get_header(self) -> dict:
        pass
    
    def get_samples(self) -> array:
        flatten = []
        for tab in self.__data:
            flatten += tab
        return bytearray(flatten)
    
    def get_data(self) -> bytearray:
        return self.__data
    
    def change_data(self, data: bytearray) -> None:
        self.__data = self.__flatten_image_conversion(data)

    def set_filename(self, filename: str) -> None:
        self.filename = filename
    
    def __transform_PIL_data(self, PIL_data):
        data = list(PIL_data)
        transformed = []
        buffer = []
        for x in data:
            buffer += x
            if len(buffer) == self.__file_width*self.__bytes_on_pixel:
                transformed.append(buffer.copy())
                buffer = []
        return transformed
    
    def __flatten_image_conversion(self, flatten_image:bytearray):
        image = []
        buffer = []
        for x in flatten_image:
            buffer.append(x)
            if len(buffer) == self.__file_width*self.__bytes_on_pixel:
                image.append(buffer.copy())
                buffer = []
        return image
        
        