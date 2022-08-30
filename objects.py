import pygame
from pygame.locals import *
from main import *

config = load_configuration()


class Platform(pygame.sprite.Sprite):
    """
    A class that represents a platform.

    Used for floors, walls, etc, and for collision detection.
    """

    def __init__(self, x, y, width, height, color, ID, draw_layer):
        """
        Platform constructor

        Parameters:
            x (int): x position of the platform (left)
            y (int): y position of the platform (top)
            width (int): width of the platform
            height (int): height of the platform
            color (hex-color): color of the platform
            ID (int): ID of the platform
            draw_layer (int): draw layer of the platform
        """
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.topleft = self.pos


class MovingPlatform(pygame.sprite.Sprite):
    """
    A class that represents a moving platform.

    Used to create movable platforms that can be used to move the player around the map.
    """

    def __init__(self, x1, y1, x2, y2, speed, width, height, color, ID, draw_layer, isActive=True):
        """
        MovingPlatform constructor

        Parameters:
            x1 (int): starting x position of the platform (left)
            y1 (int): starting y position of the platform (top)
            x2 (int): ending x position of the platform (left)
            y2 (int): ending y position of the platform (top)
            speed (int): number of frames it takes to reach goal
            width (int): width of the platform
            height (int): height of the platform
            color (hex-color): color of the platform
            ID (int): ID of the platform
            draw_layer (int): draw layer of the platform
            isActive (bool): whether the platform is active or not
        """
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.start_pos = pygame.math.Vector2(min(x1, x2), min(y1, y2))
        self.end_pos = pygame.math.Vector2(max(x1, x2), max(y1, y2))
        self.pos = pygame.math.Vector2(x1, y1)
        self.rect.topleft = self.pos
        self.speed = speed
        self.direction_x = 1
        self.direction_y = 1
        self.isActive = isActive
        self.ID = ID
        self.draw_layer = draw_layer

    def update(self, collision_group):
        """
        Moves the platform towards the goal

        Parameters:
            collision_group (pygame.sprite.Group): group of sprites that the platform will move along with it
        """
        if self.isActive:
            # Moves the platform towards the goal by
            # the distance of the points divided by the speed multiplied by the direction
            # in order to get the distance-per-frame with direction
            self.pos.x += self.direction_x * \
                abs(self.end_pos.x - self.start_pos.x) / self.speed
            self.pos.y += self.direction_y * \
                abs(self.end_pos.y - self.start_pos.y) / self.speed

            # Moves all entities on the platform along with it
            collides = pygame.sprite.spritecollide(
                self, collision_group, False)
            for entity in collides:
                if entity.rect.bottom == self.rect.top + 1:
                    entity.pos.x += self.direction_x * \
                        abs(self.end_pos.x - self.start_pos.x) / self.speed
                    entity.pos.y += self.direction_y * \
                        abs(self.end_pos.y - self.start_pos.y) / self.speed
                    entity.rect.topleft = entity.pos

            # If the platform reaches the goal, it switches direction
            if self.direction_x == 1:
                if self.pos.x >= self.end_pos.x:
                    self.direction_x = -1
            elif self.direction_x == -1:
                if self.pos.x <= self.start_pos.x:
                    self.direction_x = 1
            if self.direction_y == 1:
                if self.pos.y >= self.end_pos.y:
                    self.direction_y = -1
            elif self.direction_y == -1:
                if self.pos.y <= self.start_pos.y:
                    self.direction_y = 1

            self.rect.topleft = self.pos


class Button(pygame.sprite.Sprite):
    """
    A class that represents a button.

    Used to create buttons that can be used to trigger events, such as activating a moving platform.
    """

    def __init__(self, x, y, width, height, color, activate_color, activate_actions, deactivate_actions, mode, ID, draw_layer, isActive=False):
        """
        Button constructor

        Parameters:
            x (int): x position of the button (left)
            y (int): y position of the button (top)
            width (int): width of the button
            height (int): height of the button
            color (hex-color): color of the button
            activate_color (hex-color): color of the button when activated
            activate_actions (list): list of actions to be performed when activated
            deactivate_actions (list): list of actions to be performed when deactivated
            mode (str): mode of the button ("BUTTON" or "SWITCH")
            ID (int): ID of the button
            draw_layer (int): draw layer of the button
            isActive (bool): whether the button is activated or not
        """
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.color = color
        self.activate_color = activate_color
        self.pos = pygame.math.Vector2(x, y)
        self.isActive = isActive
        self.activate_actions = activate_actions
        self.deactivate_actions = deactivate_actions
        self.mode = mode
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.topleft = self.pos

    def update(self, collision_group, player, level):
        """
        Checks whther the button needs to change states (activated or deactivated) and calls the appropriate actions if necessary

        Parameters:
            collision_group (pygame.sprite.Group): group of all entities that can activate the button
            level (dict): dictionary of all the levels, used to pass the level to the actions
            player (Player): player object, used to pass the player's position for the switch-mode
        """
        if self.mode == "BUTTON":
            if not self.isActive:
                # Checks if the player is on the button and if so, activates it
                collides = pygame.sprite.spritecollide(
                    self, collision_group, False)
                for entity in collides:
                    if entity.rect.bottom == self.rect.top + 1:
                        self.isActive = True
                        self.surf.fill(self.activate_color)
                        self.activate_button(level)
                        break
            else:
                # Checks if the player is off the button and if so, deactivates it
                collides = pygame.sprite.spritecollide(
                    self, collision_group, False)
                if not collides:
                    self.isActive = False
                    self.surf.fill(self.color)
                    self.deactivate_button(level)

        elif self.mode == "SWITCH":
            if not self.isActive:
                # Checks if the player is in range to activate the switch
                if (self.rect.centerx - player.rect.width < player.rect.centerx and player.rect.centerx < self.rect.centerx + player.rect.width
                        and player.rect.bottom >= self.rect.bottom and player.rect.bottom < self.rect.bottom + player.rect.height):
                    self.isActive = True
                    self.surf.fill(self.activate_color)
                    self.activate_button(level)

            else:
                # Checks if the player is in range to deactivate the switch
                if (self.rect.centerx - player.rect.width < player.rect.centerx and player.rect.centerx < self.rect.centerx + player.rect.width
                        and player.rect.bottom >= self.rect.bottom and player.rect.bottom < self.rect.bottom + player.rect.height):
                    self.isActive = False
                    self.surf.fill(self.color)
                    self.deactivate_button(level)

    def activate_button(self, level):
        """
        Goes through the list of actions to be performed when activated and executes them

        Parameters:
            level (dict): dictionary of all the levels, used to access the sublevels
        """
        for index, do in enumerate(self.activate_actions):
            # If the element is a string, then it's a command, else it's irrelevant
            if type(do) != str:
                continue
            # If the command is "ACTIVATE_OBJECT", then it changes the object's active-state to "true"
            # Uses index + 1 for the sublevel's index
            # Uses index + 2 for the object's ID
            if do == "ACTIVATE_OBJECT":
                for entity in level[self.activate_actions[index + 1]].all_sprites:
                    if entity.ID == self.activate_actions[index + 2]:
                        entity.isActive = True
                        break

            # If the command is "DEACTIVATE_OBJECT", then it changes the object's active-state to "false"
            # Uses index + 1 for the sublevel's index
            # Uses index + 2 for the object's ID
            if do == "DEACTIVATE_OBJECT":
                for entity in level[self.activate_actions[index + 1]].all_sprites:
                    if entity.ID == self.activate_actions[index + 2]:
                        entity.isActive = False
                        break

    def deactivate_button(self, level):
        """
        Goes through the list of actions to be performed when deactivated and executes them

        Parameters:
            level (dict): dictionary of all the levels, used to access the sublevels
        """
        for index, do in enumerate(self.deactivate_actions):
            # If the element is a string, then it's a command, else it's irrelevant
            if type(do) != str:
                continue
            # If the command is "ACTIVATE_OBJECT", then it changes the object's active-state to "true"
            # Uses index + 1 for the sublevel's index
            # Uses index + 2 for the object's ID
            if do == "ACTIVATE_OBJECT":
                for entity in level[self.deactivate_actions[index + 1]].all_sprites:
                    if entity.ID == self.deactivate_actions[index + 2]:
                        entity.isActive = True
                        break

            # If the command is "DEACTIVATE_OBJECT", then it changes the object's active-state to "false"
            # Uses index + 1 for the sublevel's index
            # Uses index + 2 for the object's ID
            if do == "DEACTIVATE_OBJECT":
                for entity in level[self.deactivate_actions[index + 1]].all_sprites:
                    if entity.ID == self.deactivate_actions[index + 2]:
                        entity.isActive = False
                        break


class SwitchingPanel(pygame.sprite.Sprite):
    """
    A class that represents a switching panel.

    Used to switch between sublevels, allowing the player to move between them.
    """

    def __init__(self, x, y, width, height, color, level_ID, ID, draw_layer):
        """
        SwitchingPanel constructor

        Parameters:
            x (int): x position of the switchingPanel (left)
            y (int): y position of the switchingPanel (top)
            width (int): width of the switchingPanel
            height (int): height of the switchingPanel
            color (hex-color): color of the switchingPanel
            level_ID (int): ID of the sublevel to switch to once the panel is activated
            ID (int): ID of the switchingPanel
            draw_layer (int): draw layer of the switchingPanel
        """
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.topleft = self.pos
        self.level_ID = level_ID

    def switch_level(self, player, level):
        """
        Switches the saved current_level to the level_ID of the switchingPanel if the player is in range of the panel

        Parameters:
            player (Player): the player object, used to get player position
            level (dict): the current level object, used to store the level's ID
        """
        if (self.rect.centerx - player.rect.width < player.rect.centerx and player.rect.centerx < self.rect.centerx + player.rect.width
                and player.rect.bottom >= self.rect.bottom and player.rect.bottom < self.rect.bottom + player.rect.height):
            level[-1] = self.level_ID


class FinishGoal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, ID, draw_layer):
        """
        FinishGoal constructor

        Parameters:
            x (int): x position of the FinishGoal (left)
            y (int): y position of the FinishGoal (top)
            width (int): width of the FinishGoal
            height (int): height of the FinishGoal
            color (hex-color): color of the FinishGoal
            ID (int): ID of the FinishGoal
            draw_layer (int): draw layer of the FinishGoal
        """
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.topleft = self.pos

    def update(self, collision_group):
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        for sprite in collides:
            if type(sprite) == Player:
                if self.rect.contains(sprite.rect):
                    return True

                return False

        return False


class Cube(pygame.sprite.Sprite):
    """
    A class that represents a cube.

    Used as a holdable object, allowing the player to step on it, pick it up, and drop it.
    """

    def __init__(self, x, y, width, height, color, ID, draw_layer):
        """
        Cube constructor

        Parameters:
            x (int): x position of the cube (left)
            y (int): y position of the cube (top)
            width (int): width of the cube
            height (int): height of the cube
            color (hex-color): color of the cube
            ID (int): ID of the cube
            draw_layer (int): draw layer of the cube
        """
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.is_held = False
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.topleft = self.pos

    def move(self, collision_group):
        """
        Moves the cube according to the acceleration and velocity

        Parameters:
            collision_group (pygame.sprite.Group): group of sprites that the cube gets pushed by
        """
        # Resets the x acceleration to 0 and gives it the constant downward acceleration (gravity)
        self.acc = pygame.math.Vector2(0, config['PHYSICS']['GRAVITY'])
        # Checks whether the cube is touching any moving objects and adds their acceleration to the cube's acceleration
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        for entity in collides:
            if entity is not self:
                if self.rect.top + 1 < entity.rect.bottom:
                    self.acc.x += entity.acc.x

        # Gives the x acceleration the value of the velocity decreased by the friction (which is negative)
        self.acc.x += self.vel.x * config['PHYSICS']['FRICTION']
        # Updates the velocity according to the acceleration
        self.vel += self.acc
        self.pos += self.vel + config['PHYSICS']['FRICTION'] * self.acc

        # If the cube is out of the screen, it's updated back into the screen
        if self.pos.x > config['WIDTH'] - self.rect.width / 2:
            self.pos.x = config['WIDTH'] - self.rect.width / 2
        if self.pos.x < 0 + self.rect.width / 2:
            self.pos.x = 0 + self.rect.width / 2

        self.rect.topleft = self.pos

    def update(self, collision_group):
        """
        Checks whether the cube is collding with any other objects and updates the cube accordingly

        Parameters:
            collision_group (pygame.sprite.Group): group of all the objects that the cube can collide with
        """
        if not self.is_held:
            collides = pygame.sprite.spritecollide(
                self, collision_group, False)
            # For every entity the cube collides with, it does this using AABB vs AABB collision
            # https://noonat.github.io/intersect/ is a good resource for AABB collision
            for entity in collides:
                if entity is not self:
                    delta_x = entity.rect.centerx - self.rect.centerx
                    gap_x = abs(delta_x) - self.rect.width / \
                        2 - entity.rect.width / 2
                    delta_y = entity.rect.centery - self.rect.centery
                    gap_y = abs(delta_y) - self.rect.height / \
                        2 - entity.rect.height / 2

                    if abs(gap_x) > abs(gap_y):
                        self.vel.y = 0
                        if delta_y < 0:
                            self.pos.y = entity.rect.bottom
                        else:
                            self.pos.y = entity.rect.top - self.rect.height + 1
                            self.is_jumping = False
                    else:
                        self.vel.x = 0
                        if delta_x < 0:
                            self.pos.x = entity.rect.right
                        else:
                            self.pos.x = entity.rect.left - self.rect.width
                    self.rect.topleft = self.pos


class Player(pygame.sprite.Sprite):
    """
    A class that represents the player.

    Used as the main object that the player controls.
    """

    def __init__(self, x, y, width, height, color, ID, draw_layer):
        """
        Player Constructor

        Parameters:
            x (int): x position of the player (left)
            y (int): y position of the player (left)
            width (int): width of the player
            height (int): height of the player
            color (hex-color): color of the player
            ID (int): ID of the player
            draw_layer (int): draw layer of the player
        """
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.is_jumping = False
        self.direction = 1
        self.is_holding = False
        self.held_object = None
        self.ID = ID
        self.draw_layer = draw_layer
        self.rect.topleft = self.pos

    def move(self):
        """
        Moves the player according to the acceleration and velocity
        """
        # Resets the x acceleration to 0 and gives it the constant downward acceleration (gravity)
        self.acc = pygame.math.Vector2(0, config['PHYSICS']['GRAVITY'])
        # Checks whether the player is holding left or right, and adds acceleration to that direction
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x += -config['PHYSICS']['ACCELERATION']
        if pressed_keys[K_RIGHT]:
            self.acc.x += config['PHYSICS']['ACCELERATION']

        # Gives the x acceleration the value of the velocity decreased by the friction (which is negative)
        self.acc.x += self.vel.x * config['PHYSICS']['FRICTION']
        # Updates the velocity according to the acceleration
        self.vel += self.acc
        self.pos += self.vel + config['PHYSICS']['FRICTION'] * self.acc

        # If the player is out of the screen, it's updated back into the screen
        if self.pos.x + self.rect.width > config['WIDTH']:
            self.pos.x = config['WIDTH'] - self.rect.width
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.topleft = self.pos

    def update(self, collision_group):
        """
        Checks whether the player is collding with any other objects and updates the player accordingly

        Parameters:
            collision_group (pygame.sprite.Group): group of all the objects that the player can collide with
        """
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        # For every entity the player collides with, it does this using AABB vs AABB collision
        # https://noonat.github.io/intersect/ is a good resource for AABB collision
        for entity in collides:
            if entity is not self:
                delta_x = entity.rect.centerx - self.rect.centerx
                gap_x = abs(delta_x) - self.rect.width / \
                    2 - entity.rect.width / 2
                delta_y = entity.rect.centery - self.rect.centery
                gap_y = abs(delta_y) - self.rect.height / \
                    2 - entity.rect.height / 2

                if abs(gap_x) > abs(gap_y):
                    self.vel.y = 0
                    if delta_y < 0:
                        self.pos.y = entity.rect.bottom
                    else:
                        self.pos.y = entity.rect.top - self.rect.height + 1
                        self.is_jumping = False
                else:
                    self.vel.x = 0
                    if delta_x < 0:
                        self.pos.x = entity.rect.right
                    else:
                        self.pos.x = entity.rect.left - self.rect.width
                self.rect.topleft = self.pos
        if self.vel.x > 0:
            self.direction = 1
        elif self.vel.x < 0:
            self.direction = -1

        if self.is_holding:
            self.held_object.pos.x = self.pos.x
            self.held_object.pos.y = self.pos.y
            self.held_object.rect.center = self.rect.center

    def jump(self, collision_group):
        """
        Checks whether the player can jump and if so, it jumps

        Parameters:
            collision_group (pygame.sprite.Group): The group of objects the player can jump on
        """
        collides = pygame.sprite.spritecollide(self, collision_group, False)
        # Removes the player from the collision group so it doesn't collide with itself
        collides.remove(self)
        if collides and not self.is_jumping:
            self.vel.y = -config['PHYSICS']['JUMP_POWER']
            self.is_jumping = True

    def stop_jump(self):
        """
        Checks whether the player is jumping and if so, it stops the jump
        """
        # If the player's jump is ending, we might give it greater velocity than it had, therefore we check to see that we're not doing so
        if self.vel.y < -config['PHYSICS']['SHORT_JUMP_POWER'] and self.is_jumping:
            self.vel.y = -config['PHYSICS']['SHORT_JUMP_POWER']

    def hold_object(self, all_sprites_group, holdable_group) -> bool:
        """
        Checks whether the player can hold/drop an object and if so, it does so

        Parameters:
            all_sprites_group (pygame.sprite.Group): The group containing all the sprites, used to check for collisions when dropping
            holdable_group (pygame.sprite.Group): The group containing all the holdable objects, used to check for objects to hold

        Returns:
            bool: Whether the player managed to hold/drop an object
        """
        if self.is_holding:
            # makes a rectangle that is the held object's size and to the right of the player to check whether it can be dropped there
            collision_sprite = pygame.sprite.Sprite()
            collision_sprite.rect = self.held_object.rect.copy()
            collision_sprite.rect.x += self.rect.width * self.direction
            if pygame.sprite.spritecollide(collision_sprite, all_sprites_group, False):
                # if the player is colliding with something, we can't drop the object there so we check the other direction
                collision_sprite.rect.x -= self.rect.width * self.direction * 2
                if pygame.sprite.spritecollide(collision_sprite, all_sprites_group, False):
                    # if the player is colliding with something, we can't drop the object there so we return False
                    return False
                else:
                    self.held_object.pos = collision_sprite.rect.topleft
                    self.held_object.rect.topleft = self.held_object.pos
                    self.held_object.vel = self.vel.copy()
                    self.held_object.acc = self.acc.copy()
                    self.is_holding = False
                    self.held_object.is_held = False
                    return True
            else:
                self.held_object.pos = collision_sprite.rect.topleft
                self.held_object.rect.topleft = self.held_object.pos
                self.held_object.vel = self.vel.copy()
                self.held_object.acc = self.acc.copy()
                self.is_holding = False
                self.held_object.is_held = False
                return True

        else:
            # Makes a rectangle that's 3x3 the player's size, centered on the player and checks for collisions with the holdable group
            proximity_sprite = pygame.sprite.Sprite()
            proximity_sprite.rect = pygame.Rect(self.rect.left - self.rect.width, self.rect.top -
                                                self.rect.height, self.rect.width * 3, self.rect.height * 3)
            holdable_objects = pygame.sprite.spritecollide(
                proximity_sprite, holdable_group, False)
            for entity in holdable_objects:
                if entity is not self:
                    self.held_object = entity
                    self.is_holding = True
                    self.held_object.vel = pygame.Vector2(0, 0)
                    self.held_object.acc = pygame.Vector2(0, 0)
                    self.held_object.pos.x = self.rect.left
                    self.held_object.pos.y = self.rect.top
                    self.held_object.rect.topleft = self.held_object.pos
                    self.held_object.is_held = True
                    return True
            return False
