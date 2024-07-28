import time

from connection import Connection
from commands import *
from request import Request
from entity import EntityType, Entity
from player import Player


class OptionCommandHandler:

    def __init__(self, conn: Connection):
        self.conn = conn

    def ping(self):
        req = Request(Option.PING)
        return self.conn.sendReceive(req)

    def hello(self):
        req = Request(Option.HELLO)
        return self.conn.sendReceive(req)

    def ready(self):
        """Checks if server is ready"""
        req = Request(Option.READY)
        return self.conn.sendReceive(req)

    def echo(self, val):
        req = Request(Option.ECHO)
        req.arg_int8(1 if val else 0)
        return self.conn.sendReceive(req)

    def attachPlayer(self, uid=0, name=""):
        req = Request(Option.ATTACH_PLAYER)
        req.arg_int32(uid)
        req.arg_str(name)
        return self.conn.sendReceive(req)

    def currentPlayer(self):
        req = Request(Option.CURRENT_PLAYER)
        return self.conn.sendReceive(req)

    def debug(self, filename: bytes, className: bytes):
        req = Request(Option.DEBUG)
        req.arg_bytes(filename)
        req.arg_bytes(className)
        return self.conn.sendReceive(req)


class WorldCommandHandler:

    def __init__(self, conn: Connection):
        self.conn = conn

    def getBlock(self, x: int, y: int, z: int):
        req = Request(World.GET_BLOCK)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        return self.conn.sendReceive(req).decode()

    def setBlock(self, x, y, z, t):
        req = Request(World.SET_BLOCK)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        req.arg_str(t)
        return self.conn.sendReceive(req)

    def getBlockWithData(self, x: int, y: int, z: int):
        req = Request(World.GET_BLOCK_WITH_DATA)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        return self.conn.sendReceive(req)

    def getBlocks(self, x0, y0, z0, x1, y1, z1):
        req = Request(World.GET_BLOCKS)
        req.arg_int32(x0)
        req.arg_int32(y0)
        req.arg_int32(z0)
        req.arg_int32(x1)
        req.arg_int32(y1)
        req.arg_int32(z1)
        return self.conn.sendReceive(req)

    def setBlocks(self, x0, y0, z0, x1, y1, z1, t):
        req = Request(World.SET_BLOCKS)
        req.arg_int32(x0)
        req.arg_int32(y0)
        req.arg_int32(z0)
        req.arg_int32(x1)
        req.arg_int32(y1)
        req.arg_int32(z1)
        req.arg_str(t)
        return self.conn.sendReceive(req)

    def getPlayers(self):
        req = Request(World.GET_PLAYERS)
        ret = self.conn.sendReceive(req)
        return [Player.createFromStr(a) for a in ret.decode().split("|") if a]

    def getBorder(self):
        req = Request(World.GET_BORDER)
        ret = self.conn.sendReceive(req)
        arr = [float(a) for a in ret.decode().split(",") if a]
        return {"centerXZ": (arr[0], arr[1]),
                "size": arr[2],
                "maxRadius": arr[3],
                "bound_NESW": (arr[4], arr[5], arr[6], arr[7])}

    def getEntityTypes(self):
        req = Request(World.GET_ENTITY_TYPES)
        ret = self.conn.sendReceive(req)
        if ret.startswith(b"ERROR:"):
            raise Exception(ret)
        arr = ret.split(b"|")
        ret_arr = []
        for a in arr:
            aa = a.split(b',')
            ret_arr.append(EntityType(aa[0].decode(), aa[1] != b'0'))
        return ret_arr

    def getEntity(self, id: int):
        req = Request(World.GET_ENTITY)
        req.arg_int32(id)
        ret = self.conn.sendReceive(req)
        if ret:
            return Entity.createFromStr(ret.decode())

    def getEntityByType(self, type_name, distance=0.0):
        req = Request(World.GET_ENTITY_BY_TYPE)
        if not type_name:
            req.arg_int16(0)
        elif isinstance(type_name, list):
            req.arg_int16(len(type_name))
            for a in type_name:
                req.arg_str(a)
        else:
            req.arg_int16(1)
            req.arg_str(type_name)

        req.arg_double(distance)
        ret = self.conn.sendReceive(req)
        if ret.startswith(b"ERROR:"):
            raise Exception(ret)
        arr = ret.decode().split("|")
        return [Entity.createFromStr(a) for a in arr if a]

    def spawnEntity(self, type_name, x, y, z, customName):
        req = Request(World.SPAWN_ENTITY)
        req.arg_str(type_name)
        req.arg_double(x)
        req.arg_double(y)
        req.arg_double(z)
        req.arg_str(customName)
        ret = self.conn.sendReceive(req)
        if ret:
            return int(ret.decode())

    def removeEntity(self, id: int):
        req = Request(World.REMOVE_ENTITY)
        req.arg_int32(id)
        return self.conn.sendReceive(req)

    def removeEntityByType(self, type_name, distance=0.0):
        req = Request(World.GET_ENTITY_BY_TYPE)
        if not type_name:
            req.arg_int16(0)
        elif isinstance(type_name, list):
            req.arg_int16(len(type_name))
            for a in type_name:
                req.arg_str(a)
        else:
            req.arg_int16(1)
            req.arg_str(type_name)

        req.arg_double(distance)
        return self.conn.sendReceive(req)

    def getBlockTypes(self):
        req = Request(World.GET_BLOCK_TYPES)
        ret = self.conn.sendReceive(req)
        if ret.startswith(b"ERROR:"):
            raise Exception(ret)
        arr = ret.split(b"|")
        ret_arr = []
        for a in arr:
            aa = a.split(b',')
            ret_arr.append(aa[0].decode())
        return ret_arr


class MiscCommandHandler:

    def __init__(self, conn: Connection):
        self.conn = conn

    def chat(self, msg: str):
        """Post char msg"""
        req = Request(Misc.CHAT)
        req.arg_str(msg)
        return self.conn.send(req)

    def command(self, cmd: str):
        """Post char msg"""
        req = Request(Misc.COMMAND)
        req.arg_str(cmd)
        return self.conn.send(req)


class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi."""

    def __init__(self, connection):
        self.conn = connection

        self.option = OptionCommandHandler(connection)
        self.world = WorldCommandHandler(connection)
        self.misc = MiscCommandHandler(connection)

    @staticmethod
    def connect(address="localhost", port=5647):
        return Minecraft(Connection(address, port))


if __name__ == "__main__":
    mc = Minecraft.connect()
    s = "Hello, Minecraft!"
    #types = mc.world.getEntityTypes()
    #print(types)
    #for t in types:
    #    print(t)
    #    print(mc.world.getEntityByType(t.name))
    #print(mc.world.getPlayers())
    #print(mc.world.getBlock(510,103, -124))
    #print(mc.world.setBlock(506,109, -124, "grass_block"))
    #print(mc.world.getBlocks(510,103, -124, 510-10,103-10, -124-10))
    #print(mc.world.spawnEntity("wolf", 546,103, -170, "XXX"))
    print(mc.world.setBlocks(506, 109, -124, 506, 109, -124, "grass_block"))
    #print(mc.misc.command("/locate"))
    #print(mc.world.removeEntity(2320))
    #fn = r"D:\Ga\MC\开发\mywork\mcpi3-mod\build\classes\java\main\com\nongdajun\mcpi3\debug\DebugMod.class".encode("gbk")
    #print(mc.option.debug(fn, b"com.nongdajun.mcpi3.debug.DebugMod"))

