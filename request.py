import struct


class Request:
    def __init__(self, command: int):
        self.data = int.to_bytes(command, 2, "little")

    def arg_int8(self, value: int, signed=True):
        self.data += int.to_bytes(value, 1, "little", signed=signed)

    def arg_int16(self, value: int, signed=True):
        self.data += int.to_bytes(value, 2, "little", signed=signed)

    def arg_int32(self, value: int, signed=True):
        self.data += int.to_bytes(value, 4, "little", signed=signed)

    def arg_int64(self, value: int, signed=True):
        self.data += int.to_bytes(value, 8, "little", signed=signed)

    def arg_str(self, value: str):
        value = value.encode("utf-8")
        l = len(value)
        assert l <= 35767, "String too long"
        self.data += int.to_bytes(l, 2, "little") + value

    def arg_bytes(self, value: bytes):
        l = len(value)
        assert l <= 35767, "String too long"
        self.data += int.to_bytes(l, 2, "little") + value

    def arg_float(self, value: float):
        self.data += struct.pack("<f", value)

    def arg_double(self, value: float):
        self.data += struct.pack("<d", value)
