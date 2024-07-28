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


ALLAY = EntityType("allay", False)
AREA_EFFECT_CLOUD = EntityType("area_effect_cloud", False)
ARMOR_STAND = EntityType("armor_stand", False)
ARROW = EntityType("arrow", False)
AXOLOTL = EntityType("axolotl", False)
BAT = EntityType("bat", False)
BEE = EntityType("bee", False)
BLAZE = EntityType("blaze", False)
BLOCK_DISPLAY = EntityType("block_display", False)
BOAT = EntityType("boat", False)
BREEZE = EntityType("breeze", False)
CAMEL = EntityType("camel", False)
CAT = EntityType("cat", False)
CAVE_SPIDER = EntityType("cave_spider", False)
CHEST_BOAT = EntityType("chest_boat", False)
CHEST_MINECART = EntityType("chest_minecart", False)
CHICKEN = EntityType("chicken", False)
COD = EntityType("cod", False)
COMMAND_BLOCK_MINECART = EntityType("command_block_minecart", False)
COW = EntityType("cow", False)
CREEPER = EntityType("creeper", False)
DOLPHIN = EntityType("dolphin", False)
DONKEY = EntityType("donkey", False)
DRAGON_FIREBALL = EntityType("dragon_fireball", False)
DROWNED = EntityType("drowned", False)
EGG = EntityType("egg", False)
ELDER_GUARDIAN = EntityType("elder_guardian", False)
END_CRYSTAL = EntityType("end_crystal", False)
ENDER_DRAGON = EntityType("ender_dragon", False)
ENDER_PEARL = EntityType("ender_pearl", False)
ENDERMAN = EntityType("enderman", False)
ENDERMITE = EntityType("endermite", False)
EVOKER = EntityType("evoker", False)
EVOKER_FANGS = EntityType("evoker_fangs", False)
EXPERIENCE_BOTTLE = EntityType("experience_bottle", False)
EXPERIENCE_ORB = EntityType("experience_orb", False)
EYE_OF_ENDER = EntityType("eye_of_ender", False)
FALLING_BLOCK = EntityType("falling_block", False)
FIREWORK_ROCKET = EntityType("firework_rocket", False)
FOX = EntityType("fox", False)
FROG = EntityType("frog", False)
FURNACE_MINECART = EntityType("furnace_minecart", False)
GHAST = EntityType("ghast", False)
GIANT = EntityType("giant", False)
GLOW_ITEM_FRAME = EntityType("glow_item_frame", False)
GLOW_SQUID = EntityType("glow_squid", False)
GOAT = EntityType("goat", False)
GUARDIAN = EntityType("guardian", False)
HOGLIN = EntityType("hoglin", False)
HOPPER_MINECART = EntityType("hopper_minecart", False)
HORSE = EntityType("horse", False)
HUSK = EntityType("husk", False)
ILLUSIONER = EntityType("illusioner", False)
INTERACTION = EntityType("interaction", False)
IRON_GOLEM = EntityType("iron_golem", False)
ITEM = EntityType("item", False)
ITEM_DISPLAY = EntityType("item_display", False)
ITEM_FRAME = EntityType("item_frame", False)
FIREBALL = EntityType("fireball", False)
LEASH_KNOT = EntityType("leash_knot", False)
LIGHTNING_BOLT = EntityType("lightning_bolt", False)
LLAMA = EntityType("llama", False)
LLAMA_SPIT = EntityType("llama_spit", False)
MAGMA_CUBE = EntityType("magma_cube", False)
MARKER = EntityType("marker", False)
MINECART = EntityType("minecart", False)
MOOSHROOM = EntityType("mooshroom", False)
MULE = EntityType("mule", False)
OCELOT = EntityType("ocelot", False)
PAINTING = EntityType("painting", False)
PANDA = EntityType("panda", False)
PARROT = EntityType("parrot", False)
PHANTOM = EntityType("phantom", False)
PIG = EntityType("pig", False)
PIGLIN = EntityType("piglin", False)
PIGLIN_BRUTE = EntityType("piglin_brute", False)
PILLAGER = EntityType("pillager", False)
POLAR_BEAR = EntityType("polar_bear", False)
POTION = EntityType("potion", False)
PUFFERFISH = EntityType("pufferfish", False)
RABBIT = EntityType("rabbit", False)
RAVAGER = EntityType("ravager", False)
SALMON = EntityType("salmon", False)
SHEEP = EntityType("sheep", False)
SHULKER = EntityType("shulker", False)
SHULKER_BULLET = EntityType("shulker_bullet", False)
SILVERFISH = EntityType("silverfish", False)
SKELETON = EntityType("skeleton", False)
SKELETON_HORSE = EntityType("skeleton_horse", False)
SLIME = EntityType("slime", False)
SMALL_FIREBALL = EntityType("small_fireball", False)
SNIFFER = EntityType("sniffer", False)
SNOW_GOLEM = EntityType("snow_golem", False)
SNOWBALL = EntityType("snowball", False)
SPAWNER_MINECART = EntityType("spawner_minecart", False)
SPECTRAL_ARROW = EntityType("spectral_arrow", False)
SPIDER = EntityType("spider", False)
SQUID = EntityType("squid", False)
STRAY = EntityType("stray", False)
STRIDER = EntityType("strider", False)
TADPOLE = EntityType("tadpole", False)
TEXT_DISPLAY = EntityType("text_display", False)
TNT = EntityType("tnt", False)
TNT_MINECART = EntityType("tnt_minecart", False)
TRADER_LLAMA = EntityType("trader_llama", False)
TRIDENT = EntityType("trident", False)
TROPICAL_FISH = EntityType("tropical_fish", False)
TURTLE = EntityType("turtle", False)
VEX = EntityType("vex", False)
VILLAGER = EntityType("villager", False)
VINDICATOR = EntityType("vindicator", False)
WANDERING_TRADER = EntityType("wandering_trader", False)
WARDEN = EntityType("warden", False)
WIND_CHARGE = EntityType("wind_charge", False)
WITCH = EntityType("witch", False)
WITHER = EntityType("wither", False)
WITHER_SKELETON = EntityType("wither_skeleton", False)
WITHER_SKULL = EntityType("wither_skull", False)
WOLF = EntityType("wolf", False)
ZOGLIN = EntityType("zoglin", False)
ZOMBIE = EntityType("zombie", False)
ZOMBIE_HORSE = EntityType("zombie_horse", False)
ZOMBIE_VILLAGER = EntityType("zombie_villager", False)
ZOMBIFIED_PIGLIN = EntityType("zombified_piglin", False)
PLAYER = EntityType("player", False)
FISHING_BOBBER = EntityType("fishing_bobber", False)


