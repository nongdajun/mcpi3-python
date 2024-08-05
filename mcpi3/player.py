from mcpi3.vec3 import Vec3


class Player:

    def __init__(self, id: int, name: str, x: float, y: float, z: float, isMainPlayer: bool, isAlive: bool):
        self.id = id
        self.name = name
        self.pos = Vec3(x, y, z)
        self.isMainPlayer = isMainPlayer
        self.isAlive = isAlive

    def __repr__(self):
        return ('Player(id=%d, name=%s, pos=%s, isMainPlayer=%s, isAlive=%s)'
                % (self.id, self.name, self.pos, self.isMainPlayer, self.isAlive))

    @staticmethod
    def createFromStr(s: str):
        a = s.split(",")
        c = Player(int(a[0]), a[1],
                   float(a[2]), float(a[3]), float(a[4]),
                   a[5] != "0", a[6] != "0")
        return c
