import Level_Loader


level_1 = []

level_1.append(Level_Loader.Level("LEVEL_1", "LEVEL_1_0"))
level_1.append(Level_Loader.Level("LEVEL_1", "LEVEL_1_1"))


for sub_level in level_1:
    for sprite in sub_level.all_sprites:
        print(sprite.pos)

    print("===================")
    

