from unittest import TestCase
from hiddensnake.file_parsers import WavFile
from array import array

class TestWavParser(TestCase):
    def test_can_interpret_bytearray(self):
        # data definition
        data = bytearray([
        0x52, 0x49, 0x46, 0x46, 0x24, 0x08, 0x00, 0x00, 0x57, 0x41, 0x56, 0x45, 0x66, 0x6d, 0x74, 0x20, 0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00,
        0x22, 0x56, 0x00, 0x00, 0x88, 0x58, 0x01, 0x00, 0x04, 0x00, 0x10, 0x00, 0x64, 0x61, 0x74, 0x61, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ])
                                                                                                                                  #little endian
        # initializing
        obj = WavFile()

        # reding bytes
        obj.from_bytes(data)

        # checking if header is parsed correctly
        expected_get_header_result = {
            'chunk_id': 'RIFF',
            'chunk_size': 2084,
            'format': 'WAVE',
            'subchunk1_id': 'fmt ',
            'subchunk1_size': 16,
            'audio_format': 1,
            'num_channels': 2,
            'sample_rate': 22050,
            'byte_rate': 88200,
            'block_align': 4,
            'bits_per_sample': 16,
            'subchunk2_id': 'data',
            'subchunk2_size': 2048
        }
        get_header_result = obj.get_header()
        self.assertDictEqual(expected_get_header_result, get_header_result)

        # checking if samples are parsed correctly
        expected_get_samples_result = array('h', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        get_samples_result = obj.get_samples()
        self.assertEqual(expected_get_samples_result, get_samples_result)
