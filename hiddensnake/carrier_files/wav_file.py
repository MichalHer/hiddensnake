from ..abstract_classes import AbstractFile
from array import array

class WavFile(AbstractFile):

    def from_bytes(self, bytes:bytearray) -> None:
        self._chunk_id = bytes[:4]
        self._chunk_size = bytes[4:8]
        self._format = bytes[8:12]
        self._subchunk1_id = bytes[12:16]
        self._subchunk1_size = bytes[16:20]
        self._audio_format = bytes[20:22]
        self._num_channels = bytes[22:24]
        self._sample_rate = bytes[24:28]
        self._byte_rate = bytes[28:32]
        self._block_align = bytes[32:34]
        self._bits_per_sample = bytes[34:36]
        if bytes[36:40] == b'data':
            self._subchunk2_id = bytes[36:40]
            self._subchunk2_size = bytes[40:44]
            self._data = bytes[44:]
        if bytes[36:40] == b'LIST':
            data_begin = bytes.find(b'data')
            self._list_chunk = bytes[36:data_begin]
            self._subchunk2_id = bytes[data_begin:data_begin+4]
            self._subchunk2_size = bytes[data_begin+4:data_begin+8]
            self._data = bytes[data_begin+8:]

    def set_filename(self, filename:str):
        self.filename = filename

    def from_file(self, path: str) -> None:
        with open(path, 'rb') as f:
            file_bytearr = bytearray(f.read())
        self.from_bytes(file_bytearr)

    def save_file(self, path:str):
        bytea = bytearray(
            self._chunk_id +
            self._chunk_size +
            self._format +
            self._subchunk1_id +
            self._subchunk1_size +
            self._audio_format +
            self._num_channels +
            self._sample_rate +
            self._byte_rate +
            self._block_align +
            self._bits_per_sample +
            self._subchunk2_id +
            self._subchunk2_size +
            self._data
        )
        with open(path, 'wb') as f:
            f.write(bytea)
        
    def get_header(self) -> dict:
        result = {
            "chunk_id" : self._chunk_id.decode('utf-8'),
            "chunk_size" : int.from_bytes(self._chunk_size, byteorder='little'),
            "format" : self._format.decode('utf-8'),
            "subchunk1_id" : self._subchunk1_id.decode('utf-8'),
            "subchunk1_size" : int.from_bytes(self._subchunk1_size, byteorder='little'),
            "audio_format" : int.from_bytes(self._audio_format, byteorder='little'),
            "num_channels" : int.from_bytes(self._num_channels, byteorder='little'),
            "sample_rate" : int.from_bytes(self._sample_rate, byteorder='little'),
            "byte_rate" : int.from_bytes(self._byte_rate, byteorder='little'),
            "block_align" : int.from_bytes(self._block_align, byteorder='little'),
            "bits_per_sample" : int.from_bytes(self._bits_per_sample, byteorder='little'),
            "subchunk2_id" : self._subchunk2_id.decode('utf-8'),
            "subchunk2_size" : int.from_bytes(self._subchunk2_size, byteorder='little'),
        }
        try:
            result['list_chunk'] = self._list_chunk
        except:
            pass
        finally:
            return result 
    
    def get_samples(self) -> array:
        arr = array('h', self._data)
        return arr
    
    def get_data(self) -> bytearray:
        return self._data

    def change_data(self, data: bytearray) -> None:
        self._data = data