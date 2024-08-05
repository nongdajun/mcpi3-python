import time

from mcpi3.minecraft import Minecraft

if __name__ == "__main__":
    mc = Minecraft.connect()
    s = "Hello, Minecraft!"
    #types = mc.world.getEntityTypes()
    #print(types)
    #for t in types:
    #    print(t)
    #    print(mc.world.getEntityByType(t.name))
    mc.server.se(s)
    print(mc.common.IS_CLIENT_READY())
    ##print(mc.server.GET_PLAYERS())
    ##print(mc.server.WORLD_GET_BLOCK(510,103, -124))
    #print(mc.server.PLAYER_SET_POS(510, 104, -124))
    ##print(mc.server.WORLD_SET_BLOCK(506,109, -124, "grass_block"))
    #print(mc.server.getBlocks(510,103, -124, 510-10,103-10, -124-10))

    #print(mc.server.WORLD_SPAWN_ENTITY("wolf", 510,107, -124, "XXX"))
    #print(mc.server.WORLD_SET_BLOCKS(506, 109, -124, 506, 109, -124, "grass_block"))
    #print(mc.server.EXECUTE_COMMAND("/time set day"))
    #print(mc.server.WORLD_REMOVE_ENTITY(2320))
    while True:
        time.sleep(1)
        mc.client.playerAttack()
        print("attack")
