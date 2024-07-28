import socket
import select
import sys
from request import Request


class Connection:
    """Connection to Minecraft Pi3 mod"""

    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.call_id = 0
        self.sf = self.socket.makefile("rb")

    def drain(self):
        """Drains the socket of incoming data"""
        while True:
            readable, _, _ = select.select([self.socket], [], [], 0.0)
            if not readable:
                break
            data = self.socket.recv(1500)
            e = "Drained Data: <%s>\n" % data.strip()
            sys.stderr.write(e)

    def send(self, data):
        """Sends data."""
        if isinstance(data, Request):
            data = data.data
        self.call_id += 1
        data_len = len(data) + 3
        if data_len < 0x80:
            data_len_buf = bytes([data_len])
        elif data_len < 0x4000:
            data_len_buf = bytes([(data_len & 0x7F) | 0x80, data_len >> 7])
        else:
            data_len_buf = bytes([(data_len & 0x7F) | 0x80,
                                  ((data_len >> 7) & 0x7F) | 0x80,
                                  ((data_len >> 14) & 0xFF),
                                  (data_len >> 22)])
        print(data_len_buf, data_len, data)
        self.socket.sendall(
            data_len_buf
            + int.to_bytes(self.call_id, 3, "little")
            + data)
        return self.call_id

    def receive(self, call_id):
        """Receives data."""
        while True:
            s = self.sf.read(4)
            assert len(s) == 4, "Receives data error!"
            if s[0] <= 127:
                msg_len = s[0]
                cid = int.from_bytes(s[1:], "little")
            elif s[1] <= 127:
                msg_len = (s[0] & 0x7F) + (s[1] << 7)
                cid = int.from_bytes(s[2:]+self.sf.read(1), "little")
            else:
                msg_len = (s[0] & 0x7F) + ((s[1] & 0x7F) << 7) + (s[2] << 14) + (s[3] << 22)
                cid = int.from_bytes(self.sf.read(3), "little")
            dat = self.sf.read(msg_len - 3)
            if cid == call_id:
                return dat

    def sendReceive(self, data):
        """Sends and receive data"""
        cid = self.send(data)
        return self.receive(cid)
