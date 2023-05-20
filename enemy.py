import pygame, sys
SCREEN_WIDTH = 1200
screen_height = 640
WINDOW_SIZE = (SCREEN_WIDTH, screen_height)  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE)  # initiate screen
from animation import load_animations

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.mush = []
        self.mush.append(pygame.image.load('data/graphics/images/mushroom_0.png'))
        self.mush.append(pygame.image.load('data/graphics/images/mushroom_1.png'))
        self.mush.append(pygame.image.load('data/graphics/images/mushroom_2.png'))
        self.current_mush = 0
        self.image = self.mush[self.current_mush]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = False
        self.move_direction = 1
        self.move_counter = 0

    def flip_flip(self, boolean):
        if self.flip != boolean:
            self.flip = boolean
    def update(self, scroll):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
            if self.move_direction <= 0:
                self.flip_flip(True)
            if self.move_direction >= 0:
                self.flip_flip(False)
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.current_mush += 0.25
        if int(self.current_mush) >= len(self.mush):
            self.current_mush = 0
        self.image = self.mush[int(self.current_mush)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
class Imposter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.attack_animation = False
        self.reveal = []
        self.reveal.append(pygame.image.load('data/graphics/images/imposter_1.png'))
        self.reveal.append(pygame.image.load('data/graphics/images/imposter_2.png'))
        self.reveal.append(pygame.image.load('data/graphics/images/imposter_3.png'))
        self.reveal.append(pygame.image.load('data/graphics/images/imposter_4.png'))
        self.reveal.append(pygame.image.load('data/graphics/images/tree_attack_1.png'))
        self.reveal.append(pygame.image.load('data/graphics/images/tree_attack_2.png'))
        self.reveal.append(pygame.image.load('data/graphics/images/tree_attack_3.png'))
        self.reveal.append(pygame.image.load('data/graphics/images/tree_attack_4.png'))
        self.current_impos = 0
        self.image = self.reveal[self.current_impos]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def attack(self):
        self.attack_animation = True
    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.attack_animation == True:
            self.current_impos += 0.25
            if int(self.current_impos) >= len(self.reveal):
                self.current_impos = 0
                self.attack_animation = False
        self.image = self.reveal[int(self.current_impos)]
'''class Imposter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.import_animation()
        self.frame = 0
        self.action = ''
        self.flip = False
        self.change_action('idle')
        self.attack_animation = False
        self.reveal = []
        self.image = self.animations[self.action][self.anim[self.frame]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def flip(self, boolean):
        self.flip = boolean
    def attack_begin(self):
        self.attack_animation = True
    def change_action(self, new_action):
        if self.action == new_action:
            pass
        else:
            self.action = new_action
            self.frame = 0
            self.anim = self.animation_frames[self.action]

    def implement_anim(self, loop):
        self.frame += 1
        while self.frame >= len(self.anim):
            if loop:
                self.frame -= len(self.anim)
        image = self.animations[self.action][self.anim[self.frame]]
        self.image = pygame.transform.flip(image, self.flip, False)

    def import_animation(self):
        path = 'data/graphics/'
        self.animations = {'idle': [], 'attack': []}
        animation_data = load_animations(path)
        self.animation_frames = animation_data[0]
        for animation in self.animations.keys():
            self.animations[animation] = animation_data[1]
    def status(self):
        if self.attack_animation == True:
            self.change_action('attack')
        else:
            self.change_action('idle')

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.implement_anim(True)
        self.status()'''
class Swordsman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #swordsman attacking animation
        self.attack_animation = False
        self.pause_running = False
        self.attacking = []
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/swordsman.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/swordman_swordup.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/sword_swong_almost.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/sword_swing.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/sword_fully_swong.png'))
        self.current_frame = 0
        self.attack_image = self.attacking[self.current_frame]
        self.attack_rect = self.attack_image.get_rect()
        # swordsman running animation
        self.running_animation = True
        self.man = []
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_0.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_1.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_2.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_3.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_4.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_5.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_6.png'))
        self.current_sword = 0
        self.image = self.man[self.current_sword]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = False
        self.move_direction = 1
        self.move_counter = 0
        self.health = 10


    def attacking_check(self):
        self.attack_animation = True
        print("attacking")

    def flip_flip(self, boolean):
        if self.flip != boolean:
            self.flip = boolean

    def update(self, scroll):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
            if self.move_direction <= 0:
                self.flip_flip(False)
            if self.move_direction >= 0:
                self.flip_flip(True)
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.current_sword += 0.25
        if int(self.current_sword) >= len(self.man):
            self.current_sword = 0
        self.image = self.man[int(self.current_sword)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
        # attacking animation
        self.current_frame += 0.25
        if self.attack_animation:
            if int(self.current_frame) >= len(self.attacking):
                self.current_frame = 0
            self.attack_image = self.attacking[int(self.current_frame)]
            self.attack_image = pygame.transform.flip(self.attack_image, self.flip, False)
