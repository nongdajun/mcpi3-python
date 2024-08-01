import socket
import select
import struct


class Connection:
    """Connection to Minecraft Pi3 mod"""

    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.sf = self.socket.makefile("rb")

    def drain(self):
        """Drains the socket of incoming data"""
        while True:
            readable, _, _ = select.select([self.socket], [], [], 0.0)
            if not readable:
                break
            data = self.socket.recv(1500)

    def _send(self, data):
        """Sends data."""
        if isinstance(data, Request):
            data = data.data
        data_len = len(data)
        if data_len < 0x80:
            data_len_buf = bytes([data_len])
        elif data_len < 0x4000:
            data_len_buf = bytes([(data_len & 0x7F) | 0x80, data_len >> 7])
        else:
            data_len_buf = bytes([(data_len & 0x7F) | 0x80,
                                  ((data_len >> 7) & 0x7F) | 0x80,
                                  ((data_len >> 14) & 0xFF),
                                  (data_len >> 22)])
        #print(data_len_buf, data_len, data)
        self.socket.sendall(data_len_buf + data)

    def _receive(self):
        """Receives data."""
        s = self.sf.read(1)[0]
        if s <= 127:
            msg_len = s
        else:
            msg_len = s & 0x7F
            s = self.sf.read(1)[0]
            if s <= 127:
                msg_len += (s << 7)
            else:
                msg_len += ((s & 0x7F) << 7)
                s2 = self.sf.read(2)
                msg_len += (s2[0] << 14) + (s2[1] << 22)
        #print("recv_msg_len =", msg_len)
        if msg_len or 1:
            dat = self.sf.read(msg_len)
            return dat
        return b''

    def send(self, data):
        """Sends and receive data"""
        self._send(data)
        return self._receive()



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