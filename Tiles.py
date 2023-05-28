import pygame
from animation import load_animations

class tiles(pygame.sprite.Sprite):
    def __init__(self, size, loc):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=loc)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

class ground_tile(tiles):
    def __init__(self, size, loc, img):
        super().__init__(size, loc)
        self.image = img
        self.mask = pygame.mask.from_surface(img)

class animated_tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.import_animation('shield')
        self.action = ''
        self.change_action('shield')
        self.anim = self.animation_frames['shield']
        self.image = self.animations[self.action][self.anim[self.frame]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame = 0

    def change_action(self, new_action):
        if self.action == new_action:
            pass
        else:
            self.action = new_action
            self.frame = 0
            self.anim = self.animation_frames[self.action]
    def import_animation(self, type):

        path = '../MergingCopyFatalEcho/data/graphics/'
        self.animations = {'shield': []}
        animation_data = load_animations(path, type)
        self.animation_frames = animation_data[0]
        for animation in self.animations.keys():
            self.animations[animation] = animation_data[1]
    def implement_anim(self, loop):
        self.frame += 1
        while self.frame >= len(self.anim):
            if loop:
                self.frame -= len(self.anim)
            else:
                self.frame = 0
                break
        image = self.animations[self.action][self.anim[self.frame]]
        self.image = pygame.transform.flip(image, False, False)
        self.image = pygame.transform.scale(self.image, (300, 300))

    def update(self):
        self.implement_anim(True)