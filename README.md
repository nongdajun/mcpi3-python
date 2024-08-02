## mcpi3-python



### 简介

与 minecraft 的 mcpi3-mod  建立连接，并通过接口操纵minecraft游戏里的相关行为，支持Client与Server两方面的操纵，本方案不需要设立额外MC服务器，直接与minecraft 程序通信。



支持的MC版本：

-    1.20.x

支持的Python版本：

-    Python 3.8 及以上



### 当前提供的接口命令

```
# --- Common commands ---
    PING
    GET_API_VERSION
    IS_SERVER_READY
    IS_CLIENT_READY
    SET_ECHO_MODE
    DEBUG

# --- Server commands ---
    GET_PLAYERS
    ATTACH_PLAYER
    CURRENT_PLAYER
    GET_WORLDS
    ATTACH_WORLD
    CURRENT_WORLD
    KILL_PLAYER
    GET_GAME_MODE
    GET_GAME_VERSION
    WORLD_GET_BLOCK
    WORLD_SET_BLOCK
    WORLD_GET_BLOCK_WITH_DATA
    WORLD_GET_BLOCKS
    WORLD_SET_BLOCKS
    WORLD_GET_PLAYERS
    WORLD_GET_BORDER
    WORLD_GET_ENTITY_TYPES
    WORLD_GET_ENTITY
    WORLD_GET_ENTITY_BY_TYPE
    WORLD_SPAWN_ENTITY
    WORLD_REMOVE_ENTITY
    WORLD_REMOVE_ENTITY_BY_TYPE
    WORLD_GET_BLOCK_TYPES
    WORLD_GET_INFO
    WORLD_GET_IS_RAINING
    WORLD_GET_IS_DAY
    WORLD_GET_TIME
    PLAYER_GET_NAME
    PLAYER_GET_POS
    PLAYER_SET_POS
    PLAYER_GET_SPAWN_POS
    PLAYER_SET_SPAWN_POS
    PLAYER_GET_LAST_DEAD_POS
    PLAYER_GET_HEALTH
    PLAYER_SET_HEALTH
    PLAYER_GET_FOOD_LEVEL
    PLAYER_SET_FOOD_LEVEL
    PLAYER_GET_AIR
    PLAYER_SET_AIR
    PLAYER_GET_MAIN_INVENTORY
    PLAYER_GET_ARMOR_INVENTORY
    PLAYER_GET_MAIN_HAND
    PLAYER_GET_OFF_HAND
    PLAYER_SET_MAIN_HAND
    PLAYER_SET_OFF_HAND
    PLAYER_GET_HOT_BAR_ITEMS
    PLAYER_SELECT_INVENTORY_SLOT
    PLAYER_DROP_ITEM
    PLAYER_DESTROY_ITEM
    PLAYER_SET_INVENTORY_SLOT
    SEND_MESSAGE
    EXECUTE_COMMAND

# --- Client commands ---
    PLAYER_MOVE_FORWARD
    PLAYER_MOVE_BACKWARD
    PLAYER_MOVE_LEFT
    PLAYER_MOVE_RIGHT
    PLAYER_MOVE_TO
    PLAYER_JUMP
    PLAYER_ATTACK
    PLAYER_ATTACK_ENTITY
    PLAYER_ATTACK_BLOCK
    PLAYER_LOOKING_AT
    PLAYER_SWING_HAND
    PLAYER_USE_ITEM
    PLAYER_PICK_ITEM
    PLAYER_SWAP_HANDS
    PLAYER_SET_SNEAK
    PLAYER_GET_NAME
    PLAYER_GET_POS
    PLAYER_SET_POS
    PLAYER_GET_SPAWN_POS
    PLAYER_SET_SPAWN_POS
    PLAYER_GET_LAST_DEAD_POS
    PLAYER_GET_HEALTH
    PLAYER_GET_AIR
    PLAYER_GET_FOOD_LEVEL
    PLAYER_GET_MAIN_INVENTORY
    PLAYER_GET_ARMOR_INVENTORY
    PLAYER_GET_MAIN_HAND
    PLAYER_GET_OFF_HAND
    PLAYER_GET_HOT_BAR_ITEMS
    PLAYER_SELECT_INVENTORY_SLOT
    PLAYER_DROP_ITEM
    PLAYER_DESTROY_ITEM
    PLAYER_CHANGE_LOOK_DIRECTION
    PLAYER_CHANGE_PERSPECTIVE
    WORLD_GET_SPAWN_POS
    WORLD_SET_SPAWN_POS
    GET_GAME_MODE
    GET_GAME_VERSION
    GET_CLIENT_VERSION
```
