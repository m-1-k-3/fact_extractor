'''
This plugin decodes / unpacks Tektronix hex files (.tek)
'''
import binascii
from pathlib import Path

NAME = 'Tektronix HEX'
MIME_PATTERNS = ['firmware/tek']
VERSION = '0.1'


def unpack_function(file_path, tmp_dir):
    '''
    file_path specifies the input file.
    tmp_dir should be used to store the extracted files.
    '''
    target_file = Path(tmp_dir, Path(file_path).name)
    decoded = b''
    try:
        for rec in Path(file_path).read_text().splitlines():
            #  addr = int(rec[1:5], 16)  # information not used by now
            _dlen = int(rec[5:7], 16)
            _crc1 = int(rec[7:9], 16)
            _data = rec[9:9 + _dlen * 2]
            _crc2 = int(rec[-2:], 16)

            expected_crc1 = sum(int(i, 16) for i in rec[1:7]) & 0xff
            expected_crc2 = sum(int(i, 16) for i in _data) & 0xff

            try:
                decoded += binascii.unhexlify(_data)
            except binascii.Error as tek_error:
                return {'output': 'Unknown error in tek record decoding: {}'.format(str(tek_error))}

            if _crc1 != expected_crc1 or _crc2 != expected_crc2:
                return {'output': 'CRC mismatch in tek record: {}'.format(rec)}

        Path(target_file).write_bytes(decoded)

    except FileNotFoundError as fnf_error:
        return {'output': 'Failed to open file: {}'.format(str(fnf_error))}
    except ValueError as v_error:
        return {'output': 'Failed to slice tek record: {}'.format(str(v_error))}

    return {'output': 'Successfully decoded tek file'}


# ----> Do not edit below this line <----
def setup(unpack_tool):
    for item in MIME_PATTERNS:
        unpack_tool.register_plugin(item, (unpack_function, NAME, VERSION))
