from vec3 import Vec3


class EntityType:
    EntityTypeMap = {}

    def __init__(self, name: str, is_summonable: bool):
        self.name = name
        self.is_summonable = is_summonable
        EntityType.EntityTypeMap[name] = self

    def __repr__(self):
        return ('EntityType(name=%s, summonable=%s)'
                % (self.name, self.is_summonable))

class Entity:
    '''Minecraft PI entity description. Can be sent to Minecraft.spawnEntity'''

    def __init__(self, id: int, type: str, x: float, y: float, z: float, customName: str, isAlive: bool,
                 isOnGround: bool):
        self.id = id
        self.type = type
        self.pos = Vec3(x, y, z)
        self.customName = customName
        self.isAlive = isAlive
        self.isOnGround = isOnGround

    def __cmp__(self, rhs):
        return hash(self) - hash(rhs)

    def __eq__(self, rhs):
        return self.id == rhs.id

    def __hash__(self):
        return self.id

    def __iter__(self):
        '''Allows an Entity to be sent whenever id is needed'''
        return iter((self.id,))

    def __repr__(self):
        return ('Entity(id=%d, type=%s, pos=%s, name="%s", alive=%s, ground=%s)'
                % (self.id, self.type, self.pos, self.customName, self.isAlive, self.isOnGround))

    @staticmethod
    def createFromStr(s: str):
        a = s.split(",")
        c = Entity(int(a[0]), a[1],
                   float(a[2]), float(a[3]), float(a[4]),
                   a[5], a[6] != "0", a[7] != "0")
        return c


BEE = EntityType('bee', True)
MOOSHROOM = EntityType('mooshroom', True)
SKELETON = EntityType('skeleton', True)
ENDERMAN = EntityType('enderman', True)
CAMEL = EntityType('camel', True)
BREEZE = EntityType('breeze', True)
VILLAGER = EntityType('villager', True)
WITCH = EntityType('witch', True)
HUSK = EntityType('husk', True)
WOLF = EntityType('wolf', True)
SPIDER = EntityType('spider', True)
SHEEP = EntityType('sheep', True)
FISHING_BOBBER = EntityType('fishing_bobber', False)
WIND_CHARGE = EntityType('wind_charge', True)
EVOKER = EntityType('evoker', True)
GLOW_SQUID = EntityType('glow_squid', True)
SMALL_FIREBALL = EntityType('small_fireball', True)
COMMAND_BLOCK_MINECART = EntityType('command_block_minecart', True)
PLAYER = EntityType('player', False)
ARMOR_STAND = EntityType('armor_stand', True)
FOX = EntityType('fox', True)
PIGLIN = EntityType('piglin', True)
TNT_MINECART = EntityType('tnt_minecart', True)
ALLAY = EntityType('allay', True)
FIREBALL = EntityType('fireball', True)
PUFFERFISH = EntityType('pufferfish', True)
COW = EntityType('cow', True)
WARDEN = EntityType('warden', True)
ELDER_GUARDIAN = EntityType('elder_guardian', True)
TROPICAL_FISH = EntityType('tropical_fish', True)
TADPOLE = EntityType('tadpole', True)
ITEM_FRAME = EntityType('item_frame', True)
GIANT = EntityType('giant', True)
MULE = EntityType('mule', True)
ZOGLIN = EntityType('zoglin', True)
IRON_GOLEM = EntityType('iron_golem', True)
WITHER_SKULL = EntityType('wither_skull', True)
PILLAGER = EntityType('pillager', True)
FIREWORK_ROCKET = EntityType('firework_rocket', True)
EXPERIENCE_BOTTLE = EntityType('experience_bottle', True)
HOPPER_MINECART = EntityType('hopper_minecart', True)
POTION = EntityType('potion', True)
WITHER = EntityType('wither', True)
PARROT = EntityType('parrot', True)
BAT = EntityType('bat', True)
SHULKER_BULLET = EntityType('shulker_bullet', True)
BLAZE = EntityType('blaze', True)
RAVAGER = EntityType('ravager', True)
PANDA = EntityType('panda', True)
TNT = EntityType('tnt', True)
HORSE = EntityType('horse', True)
PHANTOM = EntityType('phantom', True)
GLOW_ITEM_FRAME = EntityType('glow_item_frame', True)
ITEM_DISPLAY = EntityType('item_display', True)
SILVERFISH = EntityType('silverfish', True)
STRAY = EntityType('stray', True)
TRADER_LLAMA = EntityType('trader_llama', True)
ZOMBIE = EntityType('zombie', True)
TEXT_DISPLAY = EntityType('text_display', True)
ILLUSIONER = EntityType('illusioner', True)
OCELOT = EntityType('ocelot', True)
POLAR_BEAR = EntityType('polar_bear', True)
ARROW = EntityType('arrow', True)
CREEPER = EntityType('creeper', True)
SHULKER = EntityType('shulker', True)
MARKER = EntityType('marker', True)
DROWNED = EntityType('drowned', True)
END_CRYSTAL = EntityType('end_crystal', True)
EGG = EntityType('egg', True)
ZOMBIE_VILLAGER = EntityType('zombie_villager', True)
AREA_EFFECT_CLOUD = EntityType('area_effect_cloud', True)
PIG = EntityType('pig', True)
ZOMBIE_HORSE = EntityType('zombie_horse', True)
ENDER_PEARL = EntityType('ender_pearl', True)
TRIDENT = EntityType('trident', True)
ITEM = EntityType('item', True)
LEASH_KNOT = EntityType('leash_knot', True)
GHAST = EntityType('ghast', True)
ENDER_DRAGON = EntityType('ender_dragon', True)
HOGLIN = EntityType('hoglin', True)
SNIFFER = EntityType('sniffer', True)
BOAT = EntityType('boat', True)
PAINTING = EntityType('painting', True)
COD = EntityType('cod', True)
MAGMA_CUBE = EntityType('magma_cube', True)
VEX = EntityType('vex', True)
VINDICATOR = EntityType('vindicator', True)
WITHER_SKELETON = EntityType('wither_skeleton', True)
ENDERMITE = EntityType('endermite', True)
DOLPHIN = EntityType('dolphin', True)
DONKEY = EntityType('donkey', True)
SLIME = EntityType('slime', True)
INTERACTION = EntityType('interaction', True)
WANDERING_TRADER = EntityType('wandering_trader', True)
LIGHTNING_BOLT = EntityType('lightning_bolt', True)
EVOKER_FANGS = EntityType('evoker_fangs', True)
FURNACE_MINECART = EntityType('furnace_minecart', True)
LLAMA = EntityType('llama', True)
SALMON = EntityType('salmon', True)
BLOCK_DISPLAY = EntityType('block_display', True)
SQUID = EntityType('squid', True)
SKELETON_HORSE = EntityType('skeleton_horse', True)
SNOW_GOLEM = EntityType('snow_golem', True)
STRIDER = EntityType('strider', True)
EXPERIENCE_ORB = EntityType('experience_orb', True)
RABBIT = EntityType('rabbit', True)
SPAWNER_MINECART = EntityType('spawner_minecart', True)
CHEST_BOAT = EntityType('chest_boat', True)
LLAMA_SPIT = EntityType('llama_spit', True)
TURTLE = EntityType('turtle', True)
CAT = EntityType('cat', True)
PIGLIN_BRUTE = EntityType('piglin_brute', True)
SPECTRAL_ARROW = EntityType('spectral_arrow', True)
FALLING_BLOCK = EntityType('falling_block', True)
MINECART = EntityType('minecart', True)
DRAGON_FIREBALL = EntityType('dragon_fireball', True)
GOAT = EntityType('goat', True)
GUARDIAN = EntityType('guardian', True)
SNOWBALL = EntityType('snowball', True)
CHEST_MINECART = EntityType('chest_minecart', True)
CHICKEN = EntityType('chicken', True)
EYE_OF_ENDER = EntityType('eye_of_ender', True)
AXOLOTL = EntityType('axolotl', True)
CAVE_SPIDER = EntityType('cave_spider', True)
FROG = EntityType('frog', True)
ZOMBIFIED_PIGLIN = EntityType('zombified_piglin', True)
