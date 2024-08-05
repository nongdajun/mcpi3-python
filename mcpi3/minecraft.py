import time

from mcpi3.connection import Connection, Request
from mcpi3 import commands
from mcpi3.entity import EntityType, Entity
from mcpi3.player import Player
import struct


class CommonCommander:

    def __init__(self, conn: Connection):
        self.conn = conn

    def PING(self):
        req = Request(commands.Common.PING)
        return struct.unpack("<Q", self.conn.send(req))

    def GET_API_VERSION(self):
        req = Request(commands.Common.GET_API_VERSION)
        return struct.unpack("<I", self.conn.send(req))

    def IS_SERVER_READY(self):
        """Checks if server api is ready"""
        req = Request(commands.Common.IS_SERVER_READY)
        return self.conn.send(req) == b'Y'

    def IS_CLIENT_READY(self):
        """Checks if client api is ready"""
        req = Request(commands.Common.IS_CLIENT_READY)
        return self.conn.send(req) == b'Y'

    def SET_ECHO_MODE(self, val):
        req = Request(commands.Common.SET_ECHO_MODE)
        req.arg_int8(1 if val else 0)
        return self.conn.send(req)

    def DEBUG(self, dat: bytes):
        req = Request(commands.Common.DEBUG)
        req.arg_bytes(dat)
        return self.conn.send(req)

    # --- Common command function mapping start---
    ping = PING
    getApiVersion = GET_API_VERSION
    isServerReady = IS_SERVER_READY
    isClientReady = IS_CLIENT_READY
    setEchoMode = SET_ECHO_MODE
    debug = DEBUG
    # --- Common command function mapping end---


class ServerCommander:

    def __init__(self, conn: Connection):
        self.conn = conn

    def GET_PLAYERS(self):
        req = Request(commands.Server.GET_PLAYERS)
        ret = self.conn.send(req)
        return [Player.createFromStr(a) for a in ret.decode().split("|") if a]

    def ATTACH_PLAYER(self, name: str, id=-1):
        req = Request(commands.Server.ATTACH_PLAYER)
        req.arg_str(name)
        req.arg_int32(id)
        return self.conn.send(req)

    def CURRENT_PLAYER(self):
        req = Request(commands.Server.CURRENT_PLAYER)
        ret = self.conn.send(req)
        if ret:
            return Player.createFromStr(ret.decode())

    def GET_WORLDS(self):
        req = Request(commands.Server.GET_WORLDS)
        ret = self.conn.send(req)
        return [a.decode() for a in ret.split(b"|") if a]

    def ATTACH_WORLD(self, name: str = ""):
        req = Request(commands.Server.ATTACH_WORLD)
        req.arg_str(name)
        return self.conn.send(req)

    def CURRENT_WORLD(self):
        req = Request(commands.Server.CURRENT_WORLD)
        return self.conn.send(req).decode()

    def KILL_PLAYER(self, name: str, id=-1):
        req = Request(commands.Server.KILL_PLAYER)
        req.arg_str(name)
        req.arg_int32(id)
        return self.conn.send(req)

    def GET_GAME_MODE(self):
        req = Request(commands.Server.GET_GAME_MODE)
        return self.conn.send(req).decode()

    def GET_GAME_VERSION(self):
        req = Request(commands.Server.GET_GAME_VERSION)
        return self.conn.send(req).decode()

    def WORLD_GET_NAME(self):
        req = Request(commands.Server.WORLD_GET_NAME)
        return self.conn.send(req).decode()

    def WORLD_GET_BLOCK(self, x: int, y: int, z: int):
        req = Request(commands.Server.WORLD_GET_BLOCK)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        return self.conn.send(req).decode()

    def WORLD_SET_BLOCK(self, x: int, y: int, z: int, t: str):
        req = Request(commands.Server.WORLD_SET_BLOCK)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        req.arg_str(t)
        return self.conn.send(req).decode()

    def WORLD_GET_BLOCK_WITH_DATA(self, x: int, y: int, z: int):
        req = Request(commands.Server.WORLD_GET_BLOCK_WITH_DATA)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        return self.conn.send(req).decode()

    def WORLD_GET_BLOCKS(self, x0, y0, z0, x1, y1, z1):
        req = Request(commands.Server.WORLD_GET_BLOCKS)
        req.arg_int32(x0)
        req.arg_int32(y0)
        req.arg_int32(z0)
        req.arg_int32(x1)
        req.arg_int32(y1)
        req.arg_int32(z1)
        ret = self.conn.send(req)
        if ret:
            return [a.decode() for a in ret.split(b"|") if a]

    def WORLD_SET_BLOCKS(self, x0, y0, z0, x1, y1, z1, t):
        req = Request(commands.Server.WORLD_SET_BLOCKS)
        req.arg_int32(x0)
        req.arg_int32(y0)
        req.arg_int32(z0)
        req.arg_int32(x1)
        req.arg_int32(y1)
        req.arg_int32(z1)
        req.arg_str(t)
        return self.conn.send(req).decode()

    def WORLD_GET_PLAYERS(self):
        req = Request(commands.Server.WORLD_GET_PLAYERS)
        ret = self.conn.send(req)
        if ret:
            return [Player.createFromStr(a) for a in ret.decode().split("|") if a]

    def WORLD_GET_BORDER(self):
        req = Request(commands.Server.WORLD_GET_BORDER)
        ret = self.conn.send(req)
        arr = [float(a) for a in ret.decode().split(",") if a]
        if len(arr) == 8:
            return {"centerXZ": (arr[0], arr[1]),
                    "size": arr[2],
                    "maxRadius": arr[3],
                    "bound_NESW": (arr[4], arr[5], arr[6], arr[7])}

    def WORLD_GET_ENTITY_TYPES(self):
        req = Request(commands.Server.WORLD_GET_ENTITY_TYPES)
        ret = self.conn.send(req)
        if ret:
            return [a.decode() for a in ret.decode().split("|") if a]

    def WORLD_GET_ENTITY(self, id: int):
        req = Request(commands.Server.WORLD_GET_ENTITY)
        req.arg_int32(id)
        ret = self.conn.send(req)
        if ret:
            return Entity.createFromStr(ret.decode())

    def WORLD_GET_ENTITY_BY_TYPE(self, type_name, distance=0.0):
        req = Request(commands.Server.WORLD_GET_ENTITY_BY_TYPE)
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
        ret = self.conn.send(req)
        if ret:
            arr = ret.decode().split("|")
            return [Entity.createFromStr(a) for a in arr if a]

    def WORLD_SPAWN_ENTITY(self, type_name, x, y, z, customName):
        req = Request(commands.Server.WORLD_SPAWN_ENTITY)
        req.arg_str(type_name)
        req.arg_double(x)
        req.arg_double(y)
        req.arg_double(z)
        req.arg_str(customName)
        ret = self.conn.send(req)
        if ret:
            return ret.decode()

    def WORLD_REMOVE_ENTITY(self, id: int):
        req = Request(commands.Server.WORLD_REMOVE_ENTITY)
        req.arg_int32(id)
        return self.conn.send(req)

    def WORLD_REMOVE_ENTITY_BY_TYPE(self, type_name: str, distance=0.0):
        req = Request(commands.Server.WORLD_REMOVE_ENTITY_BY_TYPE)
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
        return self.conn.send(req).decode()

    def WORLD_GET_BLOCK_REGISTRY(self):
        req = Request(commands.Server.WORLD_GET_BLOCK_REGISTRY)
        ret = self.conn.send(req)
        if ret:
            arr = ret.split(b"|")
            return [a.decode() for a in arr if a]

    def WORLD_GET_BLOCK_TYPES(self):
        req = Request(commands.Server.WORLD_GET_BLOCK_TYPES)
        ret = self.conn.send(req)
        if ret:
            arr = ret.split(b"|")
            return [a.decode() for a in arr if a]

    def WORLD_GET_BLOCK_ENTITY_TYPES(self):
        req = Request(commands.Server.WORLD_GET_BLOCK_ENTITY_TYPES)
        ret = self.conn.send(req)
        if ret:
            arr = ret.split(b"|")
            return [a.decode() for a in arr if a]

    def WORLD_GET_INFO(self):
        req = Request(commands.Server.WORLD_GET_INFO)
        return self.conn.send(req).decode()

    def WORLD_GET_IS_RAINING(self):
        req = Request(commands.Server.WORLD_GET_IS_RAINING)
        return self.conn.send(req) == b'Y'

    def WORLD_GET_IS_DAY(self):
        req = Request(commands.Server.WORLD_GET_IS_DAY)
        return self.conn.send(req) == b'Y'

    def WORLD_GET_TIME(self):
        req = Request(commands.Server.WORLD_GET_TIME)
        ret = self.conn.send(req)
        assert len(ret) == 4
        return struct.unpack("<i", ret)

    def PLAYER_GET_NAME(self):
        req = Request(commands.Server.PLAYER_GET_NAME)
        return self.conn.send(req).decode()

    def PLAYER_GET_POS(self):
        req = Request(commands.Server.PLAYER_GET_POS)
        ret = self.conn.send(req)
        if ret:
            return [float(a) for a in ret.decode().split(",") if a]

    def PLAYER_SET_POS(self, x: float, y: float, z: float):
        req = Request(commands.Server.PLAYER_SET_POS)
        req.arg_double(x)
        req.arg_double(y)
        req.arg_double(z)
        return self.conn.send(req)

    def PLAYER_GET_SPAWN_POS(self):
        req = Request(commands.Server.PLAYER_GET_SPAWN_POS)
        ret = self.conn.send(req)
        if ret:
            return [float(a) for a in ret.decode().split(",") if a]

    def PLAYER_SET_SPAWN_POS(self, x: int, y: int, z: int, world_name: str = "", angle: float = 0.0):
        req = Request(commands.Server.PLAYER_GET_SPAWN_POS)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        req.arg_str(world_name)
        req.arg_float(angle)
        return self.conn.send(req).decode()

    def PLAYER_GET_LAST_DEAD_POS(self):
        req = Request(commands.Server.PLAYER_GET_LAST_DEAD_POS)
        ret = self.conn.send(req)
        arr = [a for a in ret.decode().split(",") if a]
        if len(arr) == 4:
            return int(arr[0]), int(arr[1]), int(arr[2]), arr[3]

    def PLAYER_GET_HEALTH(self):
        req = Request(commands.Server.PLAYER_GET_HEALTH)
        return struct.unpack("<f", self.conn.send(req))

    def PLAYER_SET_HEALTH(self, health: float):
        req = Request(commands.Server.PLAYER_SET_HEALTH)
        req.arg_float(health)
        return self.conn.send(req).decode()

    def PLAYER_GET_AIR(self):
        req = Request(commands.Server.PLAYER_GET_AIR)
        return struct.unpack("<i", self.conn.send(req))

    def PLAYER_SET_AIR(self, air: int):
        req = Request(commands.Server.PLAYER_SET_AIR)
        req.arg_int32(air)
        return self.conn.send(req).decode()

    def PLAYER_GET_FOOD_LEVEL(self):
        req = Request(commands.Server.PLAYER_GET_FOOD_LEVEL)
        return struct.unpack("<i", self.conn.send(req))

    def PLAYER_SET_FOOD_LEVEL(self, level: int):
        req = Request(commands.Server.PLAYER_SET_FOOD_LEVEL)
        req.arg_int32(level)
        return self.conn.send(req).decode()

    def PLAYER_GET_MAIN_INVENTORY(self):
        req = Request(commands.Server.PLAYER_GET_MAIN_INVENTORY)
        ret = self.conn.send(req).decode()
        if ret:
            ret_arr = []
            for a in ret.split("|"):
                if a:
                    aa = a.split(",")
                    ret_arr.append((aa[0], int(aa[1])))
                else:
                    ret_arr.append(None)
            return ret_arr

    def PLAYER_GET_ARMOR_INVENTORY(self):
        req = Request(commands.Server.PLAYER_GET_ARMOR_INVENTORY)
        ret = self.conn.send(req).decode()
        if ret:
            ret_arr = []
            for a in ret.split("|"):
                if a:
                    aa = a.split(",")
                    ret_arr.append((aa[0], int(aa[1])))
                else:
                    ret_arr.append(None)
            return ret_arr

    def PLAYER_GET_MAIN_HAND(self):
        req = Request(commands.Server.PLAYER_GET_MAIN_HAND)
        ret = self.conn.send(req).decode()
        if ret:
            arr = ret.split(",")
            return arr[0], int(arr[1])

    def PLAYER_GET_OFF_HAND(self):
        req = Request(commands.Server.PLAYER_GET_OFF_HAND)
        ret = self.conn.send(req).decode()
        if ret:
            arr = ret.split(",")
            return arr[0], int(arr[1])

    def PLAYER_SET_MAIN_HAND(self, item: str):
        req = Request(commands.Server.PLAYER_SET_MAIN_HAND)
        req.arg_str(item)
        return self.conn.send(req).decode()

    def PLAYER_SET_OFF_HAND(self, item: str):
        req = Request(commands.Server.PLAYER_SET_OFF_HAND)
        req.arg_str(item)
        return self.conn.send(req).decode()

    def PLAYER_GET_HOT_BAR_ITEMS(self):
        req = Request(commands.Server.PLAYER_GET_HOT_BAR_ITEMS)
        ret = self.conn.send(req).decode()
        if ret:
            ret_arr = []
            for a in ret.split("|"):
                if a:
                    aa = a.split(",")
                    ret_arr.append((aa[0], int(aa[1])))
                else:
                    ret_arr.append(None)
            return ret_arr

    def PLAYER_SELECT_INVENTORY_SLOT(self, index: int):
        req = Request(commands.Server.PLAYER_SELECT_INVENTORY_SLOT)
        req.arg_int16(index)
        return self.conn.send(req).decode()

    def PLAYER_DROP_ITEM(self, all: bool):
        req = Request(commands.Server.PLAYER_DROP_ITEM)
        req.arg_int8(1 if all else 0)
        return self.conn.send(req).decode()

    def PLAYER_DESTROY_ITEM(self, index: int = -1):
        req = Request(commands.Server.PLAYER_DESTROY_ITEM)
        req.arg_int16(index)
        return self.conn.send(req).decode()

    def PLAYER_SET_INVENTORY_SLOT(self, index: int, name: str, count: int):
        req = Request(commands.Server.PLAYER_SET_INVENTORY_SLOT)
        req.arg_int16(index)
        req.arg_str(name)
        req.arg_int16(count)
        return self.conn.send(req).decode()

    def SEND_MESSAGE(self, msg: str):
        """Post char msg"""
        req = Request(commands.Server.SEND_MESSAGE)
        req.arg_str(msg)
        self.conn.send(req)

    def EXECUTE_COMMAND(self, cmd: str):
        """execute a command"""
        req = Request(commands.Server.EXECUTE_COMMAND)
        req.arg_str(cmd)
        self.conn.send(req)


# --- Server command function mapping start---
    getPlayers = GET_PLAYERS
    attachPlayer = ATTACH_PLAYER
    currentPlayer = CURRENT_PLAYER
    getWorlds = GET_WORLDS
    attachWorld = ATTACH_WORLD
    currentWorld = CURRENT_WORLD
    killPlayer = KILL_PLAYER
    getGameMode = GET_GAME_MODE
    getGameVersion = GET_GAME_VERSION
    worldGetName = WORLD_GET_NAME
    worldGetBlock = WORLD_GET_BLOCK
    worldSetBlock = WORLD_SET_BLOCK
    worldGetBlockWithData = WORLD_GET_BLOCK_WITH_DATA
    worldGetBlocks = WORLD_GET_BLOCKS
    worldSetBlocks = WORLD_SET_BLOCKS
    worldGetPlayers = WORLD_GET_PLAYERS
    worldGetBorder = WORLD_GET_BORDER
    worldGetEntityTypes = WORLD_GET_ENTITY_TYPES
    worldGetEntity = WORLD_GET_ENTITY
    worldGetEntityByType = WORLD_GET_ENTITY_BY_TYPE
    worldSpawnEntity = WORLD_SPAWN_ENTITY
    worldRemoveEntity = WORLD_REMOVE_ENTITY
    worldRemoveEntityByType = WORLD_REMOVE_ENTITY_BY_TYPE
    worldGetBlockRegistry = WORLD_GET_BLOCK_REGISTRY
    worldGetBlockTypes = WORLD_GET_BLOCK_TYPES
    worldGetBlockEntityTypes = WORLD_GET_BLOCK_ENTITY_TYPES
    worldGetInfo = WORLD_GET_INFO
    worldGetIsRaining = WORLD_GET_IS_RAINING
    worldGetIsDay = WORLD_GET_IS_DAY
    worldGetTime = WORLD_GET_TIME
    playerGetName = PLAYER_GET_NAME
    playerGetPos = PLAYER_GET_POS
    playerSetPos = PLAYER_SET_POS
    playerGetSpawnPos = PLAYER_GET_SPAWN_POS
    playerSetSpawnPos = PLAYER_SET_SPAWN_POS
    playerGetLastDeadPos = PLAYER_GET_LAST_DEAD_POS
    playerGetHealth = PLAYER_GET_HEALTH
    playerSetHealth = PLAYER_SET_HEALTH
    playerGetFoodLevel = PLAYER_GET_FOOD_LEVEL
    playerSetFoodLevel = PLAYER_SET_FOOD_LEVEL
    playerGetAir = PLAYER_GET_AIR
    playerSetAir = PLAYER_SET_AIR
    playerGetMainInventory = PLAYER_GET_MAIN_INVENTORY
    playerGetArmorInventory = PLAYER_GET_ARMOR_INVENTORY
    playerGetMainHand = PLAYER_GET_MAIN_HAND
    playerGetOffHand = PLAYER_GET_OFF_HAND
    playerSetMainHand = PLAYER_SET_MAIN_HAND
    playerSetOffHand = PLAYER_SET_OFF_HAND
    playerGetHotBarItems = PLAYER_GET_HOT_BAR_ITEMS
    playerSelectInventorySlot = PLAYER_SELECT_INVENTORY_SLOT
    playerDropItem = PLAYER_DROP_ITEM
    playerDestroyItem = PLAYER_DESTROY_ITEM
    playerSetInventorySlot = PLAYER_SET_INVENTORY_SLOT
    sendMessage = SEND_MESSAGE
    executeCommand = EXECUTE_COMMAND
# --- Server command function mapping end---

class ClientCommander:

    def __init__(self, conn: Connection):
        self.conn = conn

    def PLAYER_MOVE_FORWARD(self, speed: float):
        req = Request(commands.Client.PLAYER_MOVE_FORWARD)
        req.arg_float(speed)
        self.conn.send(req)

    def PLAYER_MOVE_BACKWARD(self, speed: float):
        req = Request(commands.Client.PLAYER_MOVE_FORWARD)
        req.arg_float(speed)
        self.conn.send(req)

    def PLAYER_MOVE_LEFT(self, speed: float):
        req = Request(commands.Client.PLAYER_MOVE_FORWARD)
        req.arg_float(speed)
        self.conn.send(req)

    def PLAYER_MOVE_RIGHT(self, speed: float):
        req = Request(commands.Client.PLAYER_MOVE_FORWARD)
        req.arg_float(speed)
        self.conn.send(req)

    def PLAYER_MOVE_TO(self, dx: float, dy: float, dz: float, speed: float=0.0):
        req = Request(commands.Client.PLAYER_MOVE_TO)
        req.arg_float(dx)
        req.arg_float(dy)
        req.arg_float(dz)
        req.arg_float(speed)
        return self.conn.send(req).decode()

    def PLAYER_JUMP(self):
        req = Request(commands.Client.PLAYER_JUMP)
        return self.conn.send(req).decode()

    def PLAYER_ATTACK(self):
        req = Request(commands.Client.PLAYER_ATTACK)
        self.conn.send(req)

    def PLAYER_ATTACK_ENTITY(self, entity_id: int):
        req = Request(commands.Client.PLAYER_ATTACK_ENTITY)
        req.arg_int32(entity_id)
        return self.conn.send(req).decode()

    def PLAYER_ATTACK_BLOCK(self, x: int, y: int, z: int):
        req = Request(commands.Client.PLAYER_ATTACK_BLOCK)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        return self.conn.send(req).decode()

    def PLAYER_LOOKING_AT(self):
        req = Request(commands.Client.PLAYER_LOOKING_AT)
        ret = self.conn.send(req).decode()
        if ret:
            arr = ret.split(",")
            return (float(arr[0]), float(arr[1]), float(arr[2])), arr[3]

    def PLAYER_SWING_HAND(self, is_off_hand: bool = False):
        req = Request(commands.Client.PLAYER_SWING_HAND)
        req.arg_int8(1 if is_off_hand else 0)
        self.conn.send(req)

    def PLAYER_USE_ITEM(self):
        req = Request(commands.Client.PLAYER_USE_ITEM)
        self.conn.send(req)

    def PLAYER_PICK_ITEM(self):
        req = Request(commands.Client.PLAYER_PICK_ITEM)
        self.conn.send(req)

    def PLAYER_SWAP_HANDS(self):
        req = Request(commands.Client.PLAYER_SWAP_HANDS)
        self.conn.send(req)

    def PLAYER_SET_SNEAK(self, is_sneaking: bool):
        req = Request(commands.Client.PLAYER_SET_SNEAK)
        req.arg_int8(1 if is_sneaking else 0)
        self.conn.send(req)

    def PLAYER_GET_NAME(self):
        req = Request(commands.Client.PLAYER_GET_NAME)
        return self.conn.send(req).decode()

    def PLAYER_GET_POS(self):
        req = Request(commands.Client.PLAYER_GET_POS)
        ret = self.conn.send(req)
        if ret:
            return [float(a) for a in ret.decode().split(",") if a]

    def PLAYER_SET_POS(self, x: float, y: float, z: float):
        req = Request(commands.Client.PLAYER_SET_POS)
        req.arg_double(x)
        req.arg_double(y)
        req.arg_double(z)
        return self.conn.send(req)

    def PLAYER_GET_SPAWN_POS(self):
        req = Request(commands.Client.PLAYER_GET_SPAWN_POS)
        ret = self.conn.send(req)
        if ret:
            return [float(a) for a in ret.decode().split(",") if a]

    def PLAYER_SET_SPAWN_POS(self, x: int, y: int, z: int, world_name: str = "", angle: float = 0.0):
        req = Request(commands.Client.PLAYER_GET_SPAWN_POS)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        req.arg_str(world_name)
        req.arg_float(angle)
        return self.conn.send(req).decode()

    def PLAYER_GET_LAST_DEAD_POS(self):
        req = Request(commands.Client.PLAYER_GET_LAST_DEAD_POS)
        ret = self.conn.send(req)
        arr = [a for a in ret.decode().split(",") if a]
        if len(arr) == 4:
            return int(arr[0]), int(arr[1]), int(arr[2]), arr[3]

    def PLAYER_GET_HEALTH(self):
        req = Request(commands.Client.PLAYER_GET_HEALTH)
        return struct.unpack("<f", self.conn.send(req))

    def PLAYER_GET_AIR(self):
        req = Request(commands.Client.PLAYER_GET_AIR)
        return struct.unpack("<i", self.conn.send(req))

    def PLAYER_GET_FOOD_LEVEL(self):
        req = Request(commands.Client.PLAYER_GET_FOOD_LEVEL)
        return struct.unpack("<i", self.conn.send(req))

    def PLAYER_GET_MAIN_INVENTORY(self):
        req = Request(commands.Client.PLAYER_GET_MAIN_INVENTORY)
        ret = self.conn.send(req).decode()
        if ret:
            ret_arr = []
            for a in ret.split("|"):
                if a:
                    aa = a.split(",")
                    ret_arr.append((aa[0], int(aa[1])))
                else:
                    ret_arr.append(None)
            return ret_arr

    def PLAYER_GET_ARMOR_INVENTORY(self):
        req = Request(commands.Client.PLAYER_GET_ARMOR_INVENTORY)
        ret = self.conn.send(req).decode()
        if ret:
            ret_arr = []
            for a in ret.split("|"):
                if a:
                    aa = a.split(",")
                    ret_arr.append((aa[0], int(aa[1])))
                else:
                    ret_arr.append(None)
            return ret_arr

    def PLAYER_GET_MAIN_HAND(self):
        req = Request(commands.Client.PLAYER_GET_MAIN_HAND)
        ret = self.conn.send(req).decode()
        if ret:
            arr = ret.split(",")
            return arr[0], int(arr[1])

    def PLAYER_GET_OFF_HAND(self):
        req = Request(commands.Client.PLAYER_GET_OFF_HAND)
        ret = self.conn.send(req).decode()
        if ret:
            arr = ret.split(",")
            return arr[0], int(arr[1])

    def PLAYER_GET_HOT_BAR_ITEMS(self):
        req = Request(commands.Client.PLAYER_GET_HOT_BAR_ITEMS)
        ret = self.conn.send(req).decode()
        if ret:
            ret_arr = []
            for a in ret.split("|"):
                if a:
                    aa = a.split(",")
                    ret_arr.append((aa[0], int(aa[1])))
                else:
                    ret_arr.append(None)
            return ret_arr

    def PLAYER_SELECT_INVENTORY_SLOT(self, index: int):
        req = Request(commands.Client.PLAYER_SELECT_INVENTORY_SLOT)
        req.arg_int16(index)
        return self.conn.send(req).decode()

    def PLAYER_DROP_ITEM(self, all: bool):
        req = Request(commands.Client.PLAYER_DROP_ITEM)
        req.arg_int8(1 if all else 0)
        return self.conn.send(req).decode()

    def PLAYER_DESTROY_ITEM(self, index: int = -1):
        req = Request(commands.Client.PLAYER_DESTROY_ITEM)
        req.arg_int16(index)
        return self.conn.send(req).decode()

    def PLAYER_CHANGE_LOOK_DIRECTION(self, dx: float, dy: float):
        """dx, dy the delta angles, [0, 360)"""
        req = Request(commands.Client.PLAYER_CHANGE_LOOK_DIRECTION)
        req.arg_float(dx)
        req.arg_float(dy)
        self.conn.send(req)

    def PLAYER_CHANGE_PERSPECTIVE(self, isFirstPerson: bool):
        req = Request(commands.Client.PLAYER_CHANGE_PERSPECTIVE)
        req.arg_int8(1 if isFirstPerson else 0)
        self.conn.send(req)

    def WORLD_GET_SPAWN_POS(self):
        return self.PLAYER_GET_SPAWN_POS()

    def WORLD_SET_SPAWN_POS(self, *args):
        return self.PLAYER_SET_SPAWN_POS(*args)

    def GET_WORLDS(self):
        req = Request(commands.Client.GET_WORLDS)
        ret = self.conn.send(req)
        if ret:
            return [a.decode() for a in ret.split(b"|") if a]

    def WORLD_GET_NAME(self):
        req = Request(commands.Client.WORLD_GET_NAME)
        return self.conn.send(req).decode()

    def WORLD_GET_BLOCK(self, x: int, y: int, z: int):
        req = Request(commands.Client.WORLD_GET_BLOCK)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        return self.conn.send(req).decode()

    def WORLD_GET_BLOCK_WITH_DATA(self, x: int, y: int, z: int):
        req = Request(commands.Client.WORLD_GET_BLOCK_WITH_DATA)
        req.arg_int32(x)
        req.arg_int32(y)
        req.arg_int32(z)
        return self.conn.send(req).decode()

    def WORLD_GET_BLOCKS(self, x0, y0, z0, x1, y1, z1):
        req = Request(commands.Client.WORLD_GET_BLOCKS)
        req.arg_int32(x0)
        req.arg_int32(y0)
        req.arg_int32(z0)
        req.arg_int32(x1)
        req.arg_int32(y1)
        req.arg_int32(z1)
        ret = self.conn.send(req)
        if ret:
            return [a.decode() for a in ret.split(b"|") if a]

    def WORLD_GET_PLAYERS(self):
        req = Request(commands.Client.WORLD_GET_PLAYERS)
        ret = self.conn.send(req)
        if ret:
            return [Player.createFromStr(a) for a in ret.decode().split("|") if a]

    def WORLD_GET_BORDER(self):
        req = Request(commands.Client.WORLD_GET_BORDER)
        ret = self.conn.send(req)
        arr = [float(a) for a in ret.decode().split(",") if a]
        if len(arr) == 8:
            return {"centerXZ": (arr[0], arr[1]),
                    "size": arr[2],
                    "maxRadius": arr[3],
                    "bound_NESW": (arr[4], arr[5], arr[6], arr[7])}

    def WORLD_GET_ENTITY_TYPES(self):
        req = Request(commands.Client.WORLD_GET_ENTITY_TYPES)
        ret = self.conn.send(req)
        if ret:
            return [a.decode() for a in ret.decode().split("|") if a]

    def WORLD_GET_ENTITY(self, id: int):
        req = Request(commands.Client.WORLD_GET_ENTITY)
        req.arg_int32(id)
        ret = self.conn.send(req)
        if ret:
            return Entity.createFromStr(ret.decode())

    def WORLD_GET_ENTITY_BY_TYPE(self, type_name, distance=0.0):
        req = Request(commands.Client.WORLD_GET_ENTITY_BY_TYPE)
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
        ret = self.conn.send(req)
        if ret:
            arr = ret.decode().split("|")
            return [Entity.createFromStr(a) for a in arr if a]

    def WORLD_GET_BLOCK_REGISTRY(self):
        req = Request(commands.Client.WORLD_GET_BLOCK_REGISTRY)
        ret = self.conn.send(req)
        if ret:
            arr = ret.split(b"|")
            return [a.decode() for a in arr if a]

    def WORLD_GET_BLOCK_TYPES(self):
        req = Request(commands.Client.WORLD_GET_BLOCK_TYPES)
        ret = self.conn.send(req)
        if ret:
            arr = ret.split(b"|")
            return [a.decode() for a in arr if a]

    def WORLD_GET_BLOCK_ENTITY_TYPES(self):
        req = Request(commands.Client.WORLD_GET_BLOCK_ENTITY_TYPES)
        ret = self.conn.send(req)
        if ret:
            arr = ret.split(b"|")
            return [a.decode() for a in arr if a]

    def WORLD_GET_INFO(self):
        req = Request(commands.Client.WORLD_GET_INFO)
        return self.conn.send(req).decode()

    def WORLD_GET_IS_RAINING(self):
        req = Request(commands.Client.WORLD_GET_IS_RAINING)
        return self.conn.send(req) == b'Y'

    def WORLD_GET_IS_DAY(self):
        req = Request(commands.Client.WORLD_GET_IS_DAY)
        return self.conn.send(req) == b'Y'

    def WORLD_GET_TIME(self):
        req = Request(commands.Client.WORLD_GET_TIME)
        ret = self.conn.send(req)
        assert len(ret) == 4
        return struct.unpack("<i", ret)

    def GET_GAME_MODE(self):
        req = Request(commands.Client.GET_GAME_MODE)
        return self.conn.send(req).decode()

    def GET_GAME_VERSION(self):
        req = Request(commands.Client.GET_GAME_VERSION)
        return self.conn.send(req).decode()

    def GET_CLIENT_VERSION(self):
        req = Request(commands.Client.GET_CLIENT_VERSION)
        return self.conn.send(req).decode()

    def SEND_MESSAGE(self, msg: str):
        """Post char msg"""
        req = Request(commands.Client.SEND_MESSAGE)
        req.arg_str(msg)
        self.conn.send(req)

    def EXECUTE_COMMAND(self, cmd: str):
        """execute a command"""
        req = Request(commands.Client.EXECUTE_COMMAND)
        req.arg_str(cmd)
        self.conn.send(req)

# --- Client command function mapping start---
    playerMoveForward = PLAYER_MOVE_FORWARD
    playerMoveBackward = PLAYER_MOVE_BACKWARD
    playerMoveLeft = PLAYER_MOVE_LEFT
    playerMoveRight = PLAYER_MOVE_RIGHT
    playerMoveTo = PLAYER_MOVE_TO
    playerJump = PLAYER_JUMP
    playerAttack = PLAYER_ATTACK
    playerAttackEntity = PLAYER_ATTACK_ENTITY
    playerAttackBlock = PLAYER_ATTACK_BLOCK
    playerLookingAt = PLAYER_LOOKING_AT
    playerSwingHand = PLAYER_SWING_HAND
    playerUseItem = PLAYER_USE_ITEM
    playerPickItem = PLAYER_PICK_ITEM
    playerSwapHands = PLAYER_SWAP_HANDS
    playerSetSneak = PLAYER_SET_SNEAK
    playerGetName = PLAYER_GET_NAME
    playerGetPos = PLAYER_GET_POS
    playerSetPos = PLAYER_SET_POS
    playerGetSpawnPos = PLAYER_GET_SPAWN_POS
    playerSetSpawnPos = PLAYER_SET_SPAWN_POS
    playerGetLastDeadPos = PLAYER_GET_LAST_DEAD_POS
    playerGetHealth = PLAYER_GET_HEALTH
    playerGetAir = PLAYER_GET_AIR
    playerGetFoodLevel = PLAYER_GET_FOOD_LEVEL
    playerGetMainInventory = PLAYER_GET_MAIN_INVENTORY
    playerGetArmorInventory = PLAYER_GET_ARMOR_INVENTORY
    playerGetMainHand = PLAYER_GET_MAIN_HAND
    playerGetOffHand = PLAYER_GET_OFF_HAND
    playerGetHotBarItems = PLAYER_GET_HOT_BAR_ITEMS
    playerSelectInventorySlot = PLAYER_SELECT_INVENTORY_SLOT
    playerDropItem = PLAYER_DROP_ITEM
    playerDestroyItem = PLAYER_DESTROY_ITEM
    playerChangeLookDirection = PLAYER_CHANGE_LOOK_DIRECTION
    playerChangePerspective = PLAYER_CHANGE_PERSPECTIVE
    worldGetSpawnPos = WORLD_GET_SPAWN_POS
    worldSetSpawnPos = WORLD_SET_SPAWN_POS
    getWorlds = GET_WORLDS
    worldGetName = WORLD_GET_NAME
    worldGetBlock = WORLD_GET_BLOCK
    worldGetBlockWithData = WORLD_GET_BLOCK_WITH_DATA
    worldGetBlocks = WORLD_GET_BLOCKS
    worldGetPlayers = WORLD_GET_PLAYERS
    worldGetBorder = WORLD_GET_BORDER
    worldGetEntityTypes = WORLD_GET_ENTITY_TYPES
    worldGetEntity = WORLD_GET_ENTITY
    worldGetEntityByType = WORLD_GET_ENTITY_BY_TYPE
    worldGetBlockRegistry = WORLD_GET_BLOCK_REGISTRY
    worldGetBlockTypes = WORLD_GET_BLOCK_TYPES
    worldGetBlockEntityTypes = WORLD_GET_BLOCK_ENTITY_TYPES
    worldGetInfo = WORLD_GET_INFO
    worldGetIsRaining = WORLD_GET_IS_RAINING
    worldGetIsDay = WORLD_GET_IS_DAY
    worldGetTime = WORLD_GET_TIME
    getGameMode = GET_GAME_MODE
    getGameVersion = GET_GAME_VERSION
    getClientVersion = GET_CLIENT_VERSION
    sendMessage = SEND_MESSAGE
    executeCommand = EXECUTE_COMMAND
# --- Client command function mapping end---


class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi3."""

    def __init__(self, connection):
        self.conn = connection

        self.common = CommonCommander(connection)
        self.server = ServerCommander(connection)
        self.client = ClientCommander(connection)

    @staticmethod
    def connect(address="localhost", port=5647):
        return Minecraft(Connection(address, port))


if __name__ == "__main__":
    mc = Minecraft.connect()
    s = "Hello, Minecraft!"
    print(mc.server.sendMessage(s))
