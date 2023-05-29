import time, score
import pygame.transform
from player import *
from csv_loader import *
from os import walk
import enemy


SCREEN_WIDTH = 1200
screen_height = 640

rescaled_width = 600
rescaled_height = 320
cooldown_tracker = 0
def logo(img, x, y):
	screen.blit(img, (x,y))
class Tiles(pygame.sprite.Sprite):
	def __init__(self, size, loc):
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.rect = self.image.get_rect(topleft=loc)

	def update(self, scroll):
		self.rect.x -= scroll[0]
		self.rect.y -= scroll[1]


class ground_tile(Tiles):
	def __init__(self, size, loc, img):
		super().__init__(size, loc)
		self.image = img
		self.mask = pygame.mask.from_surface(img)


class Level:
	def __init__(self, game_map, path, surface, name, last_level = False, info = [0, [10, 10], 0]):
		self.game_map = game_map
		self.surface = surface
		self.name = name
		self.path = path
		self.game_map = self.load_map(path)
		self.bg_drawn = False
		self.player_direction = 0
		self.merchant_beside = 0
		self.mushroom_inv = info[0]
		self.mushroom_taken = 0
		self.coin_inv = info[2]
		# used to calcuate final score
		self.final_score = True
		self.last_level = last_level
		self.bad_ending = False
		self.good_ending = False
		self.imposter_kill = False
		self.damage = 10
		self.time_attacked = 0
		self.start_time_attack = time.time()
		self.dead = False
		self.done = False
		self.game_over = False
		self.health = info[1][0]
		self.max_health = info[1][1]
		self.damage_taken = False
		self.tile_size = 16
		self.Simon_tile_size = 32
		# heart images
		self.full_heart = pygame.image.load('data/graphics/bg_images/heart.png').convert_alpha()
		self.half_heart = pygame.image.load('data/graphics/bg_images/half_heart.png').convert_alpha()
		self.empty_heart = pygame.image.load('data/graphics/bg_images/empty_heart.png').convert_alpha()
		#creates the sprite groups of all sprites
		self.player = pygame.sprite.GroupSingle()
		self.tiles = pygame.sprite.Group()
		self.barriers = pygame.sprite.Group()
		self.bg_objects = pygame.sprite.Group()
		self.imposter_group = pygame.sprite.Group()
		self.heart_objects = pygame.sprite.Group()
		self.coin = pygame.sprite.Group()
		self.Death = pygame.sprite.Group()
		self.tree = pygame.sprite.Group()
		self.GoodEnd = pygame.sprite.Group()
		self.BadEnd = pygame.sprite.Group()
		self.orb_group = pygame.sprite.Group()
		self.mushroom_group = pygame.sprite.Group()
		self.blob_group = pygame.sprite.Group()
		self.slopesgroup = pygame.sprite.Group()
		self.headslopesgroup = pygame.sprite.Group()
		self.swordsman_group = pygame.sprite.Group()
		self.wizard_group = pygame.sprite.Group()
		self.merchant_group = pygame.sprite.Group()
		self.platform_group = pygame.sprite.Group()
		self.Spawn = pygame.sprite.GroupSingle()
		self.npc0 = pygame.sprite.Group()
		self.npc1 = pygame.sprite.Group()
		self.npc2 = pygame.sprite.Group()
		self.npc3 = pygame.sprite.Group()
		self.End = pygame.sprite.Group()
		self.merchant_speak = False
		self.merchant_speak1 = False
		self.shoot_cooldown = 0
		self.ammo = 15
		# use to calculate score
		self.score = 0
		self.coin_count = 0
		self.start_time = time.time()
		self.player_on_slope = False
		self.bg_imgs = []
		self.loading_imgs = []
		self.done = False
		self.on_platform = False
		self.level_type = 'Simon'
		#background and loading images added to list
		for i in range(1, 6):
			bg_img = pygame.image.load('data/graphics/bg_images/' + f'forest-{i}.png').convert_alpha()
			self.bg_imgs.append(bg_img)
		for i in range(1, 3):
			loading_img = pygame.image.load('data/graphics/loading_images/'+f'loading{i}.png').convert_alpha()
			self.loading_imgs.append(loading_img)
		#creating and importing the game map files and sprites
		self.terrain_layout = import_csv_files(self.game_map['Grass'])
		self.terrain_sprites = self.create_sprite(self.terrain_layout, 'Grass')
		self.barrier_layout = import_csv_files(self.game_map['Barrier'])
		self.barrier_sprites = self.create_sprite(self.barrier_layout, 'Barrier')
		self.platform_layout = import_csv_files(self.game_map['Platform'])
		self.platform_sprites = self.create_sprite(self.platform_layout, 'Platform')
		self.Gold = import_csv_files(self.game_map['Gold'])
		self.create_sprite(self.Gold, 'Gold')
		self.Mushroom = import_csv_files(self.game_map['Mushroom'])
		self.create_sprite(self.Mushroom, 'Mushroom')
		self.Swordsman = import_csv_files(self.game_map['Swordsman'])
		self.create_sprite(self.Swordsman, 'Swordsman')
		self.Wizard = import_csv_files(self.game_map['Wizard'])
		self.create_sprite(self.Wizard, 'Wizard')
		self.Npc = import_csv_files(self.game_map['Npc'])
		self.create_sprite(self.Npc, 'Npc')
		self.Imposter = import_csv_files(self.game_map['Imposter'])
		self.create_sprite(self.Imposter, 'Imposter')
		self.merchantslayout = import_csv_files(self.game_map['Merchant'])
		self.create_sprite(self.merchantslayout, 'Merchant')
		self.tree_layout = import_csv_files(self.game_map['Trees'])
		self.create_sprite(self.tree_layout, 'Trees')
		self.slope_layout = import_csv_files(self.game_map['Slopes'])
		self.slope_sprites = self.create_sprite(self.slope_layout, 'Slopes')
		self.headslope_layout = import_csv_files(self.game_map['TopSlopes'])
		self.headslope_sprites = self.create_sprite(self.headslope_layout, 'TopSlopes')
		self.spawn = import_csv_files(self.game_map['Spawn'])
		self.create_sprite(self.spawn, 'Spawn')
		self.badending = import_csv_files(self.game_map['BadEnding'])
		self.create_sprite(self.badending, 'BadEnding')
		self.goodending = import_csv_files(self.game_map['GoodEnding'])
		self.create_sprite(self.goodending, 'GoodEnding')
		self.death = import_csv_files(self.game_map['Death'])
		self.create_sprite(self.death, 'Death')

	def armour_trade_check(self):
		if self.coin_inv >= 20:
			return True
		else:
			return False

	def armour_trade(self, boolean):
		if boolean == True:
			self.coin_inv -= 20
			self.health += 2
			self.max_health += 2
			self.health = self.max_health
		elif boolean == False:
			return True

	def mushroom_count(self, int):
		if self.mushroom_inv < int:
			return True
	def coin_counting(self, int):
		if self.coin_inv < int:
			return True
	def mushroom_trade_check(self):
		if self.mushroom_inv >= 1:
			return True
		else:
			return False

	def draw_speech_bubble(self, screen, text, text_colour, bg_colour, pos, size):

		font = pygame.font.SysFont(None, size)
		text_surface = font.render(text, True, text_colour)
		text_rect = text_surface.get_rect(midbottom=pos)

		# background
		bg_rect = text_rect.copy()
		bg_rect.inflate_ip(5, 5)

		# Frame
		frame_rect = bg_rect.copy()
		frame_rect.inflate_ip(2, 2)

		pygame.draw.rect(screen, text_colour, frame_rect)
		pygame.draw.rect(screen, bg_colour, bg_rect)
		screen.blit(text_surface, text_rect)
	def npc_speak(self):
		for npc in self.npc0.sprites():
			player = self.player.sprite
			if abs(player.rect.x - npc.rect.x) < 120:
				self.speaking = True
			else:
				self.speaking = False
			if self.speaking:
				self.draw_speech_bubble(self.surface,"Hello sir, have you heard of the outbreak about 3 leagues west?",(255, 255, 0), (175, 175, 0),npc.rect.midtop, 18)
		for npc in self.npc1.sprites():
				player = self.player.sprite
				if abs(player.rect.x - npc.rect.x) < 120:
					self.speaking = True
				else:
					self.speaking = False
				if self.speaking:
					self.draw_speech_bubble(self.surface,"The infection takes over the mind, controlling the being to do their bidding",
											(255, 255, 0), (175, 175, 0), npc.rect.midtop, 18)
		for npc in self.npc2.sprites():
				player = self.player.sprite
				if abs(player.rect.x - npc.rect.x) < 120:
					self.speaking = True
				else:
					self.speaking = False
				if self.speaking:
					self.draw_speech_bubble(self.surface,
											"Enter the hill, there you will decide your fate, and the fate of the world itself.",
											(255, 255, 0), (175, 175, 0), npc.rect.midtop, 18)
		for npc in self.npc3.sprites():
				player = self.player.sprite
				if abs(player.rect.x - npc.rect.x) < 120:
					self.speaking = True
				else:
					self.speaking = False
				if self.speaking:
					self.draw_speech_bubble(self.surface,
											"For good, on the right, or for evil, on the left. This is what you MUST CHOOSE!", (34, 32, 52), (44, 42, 62), npc.rect.midtop, 18)

	def mushroom_trade(self, boolean):
		if boolean == True:
			self.mushroom_inv -= 1
			self.coin_inv += 5
		elif boolean == False:
			return True

	def load_map(self, path):
		level_data = {}
		f = open(path + 'level', 'r')
		self.level = f.read()
		f.close()
		self.level = self.level.split('\n')
		for name in self.level:
			paths = path.split('/')
			level_name = paths[2]
			level_data[name] = path + level_name + '_' + name + '.csv'
		return (level_data)

	def create_sprite(self, layout, type):
		if self.path == 'data/levels/level_5/':
			row_index = 0
			for row in layout:
				col_index = 0
				for col in row:
					if col != '-1':
						if type == 'Grass':
							terrain_layout = slicing_tiles('data/graphics/FlashbackTerrain/Grass/Grass.png', (32, 32))
							tile = terrain_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							self.tiles.add(sprite)
						if type == 'Platform':
							plat_layout = slicing_tiles('data/graphics/FlashbackTerrain/Platform/moving_platforms.png', (32, 32))
							# tile = plat_layout[int(col)]
							# sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							sprite = enemy.Platform(col_index * 32, row_index * 32)
							self.platform_group.add(sprite)
						if type == 'Npc':
							npc_layout = slicing_tiles('data/graphics/FlashbackTerrain/Npc/npc_1.png', (32, 32))
							# tile = npc_layout[int(col)]
							# sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							if col == '0':
								spritef = enemy.NPC(col_index * 32, row_index * 32, 0)
								self.npc0.add(spritef)
							if col == '1':
								sprites = enemy.NPC(col_index * 32, row_index * 32, 1)
								self.npc1.add(sprites)
							if col == '2':
								sprited = enemy.NPC(col_index * 32, row_index * 32, 2)
								self.npc2.add(sprited)
							if col == '3':
								spriteL = enemy.NPC(col_index * 32, row_index * 32 - 4, 3)
								self.npc3.add(spriteL)
						'''if type == 'UpPlatform':
                            plat_layout = slicing_tiles('data/graphics/SimonTerrain/Platform/moving_platforms.png', (32,32))
                            tile = plat_layout[int(col)]
                            #sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
                            sprite = Platform(col_index * 32, row_index * 32, 0, 1)
                            self.platform_group.add(sprite)'''
						if type == 'Barrier':
							terrain_layout = slicing_tiles('data/graphics/images/barrier.png', (32, 32))
							tile = terrain_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							self.barriers.add(sprite)
						if type == 'Gold':
							gold = slicing_tiles('data/graphics/FlashbackTerrain/Coin/gold_coin.png', (32, 32))
							tiles = gold[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiles)
							self.coin.add(sprite)
						if type == 'Death':
							death = slicing_tiles('data/graphics/SimonTerrain/Death/Death.png', (32, 32))
							tileset = death[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tileset)
							self.Death.add(sprite)
						if type == 'Trees':
							tree_layout = slicing_tiles('data/graphics/FlashbackTerrain/Tree/Tree_tileset.png', (32, 32))
							tiled = tree_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							self.tree.add(sprite)
						if type == 'Merchant':
							tree_layout = slicing_tiles('data/graphics/images/merchant.png', (32, 32))
							tiled = tree_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							self.merchant_group.add(sprite)
						if type == 'Mushroom':
							mush_layout = slicing_tiles('data/graphics/images/mushroom_0.png', (16, 16))
							tiled = mush_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							mushroom = enemy.Mushroom(col_index * 32, row_index * 32 + 18)
							self.mushroom_group.add(mushroom)
						if type == 'Swordsman':
							enemy_layout = slicing_tiles('data/graphics/images/swordsman.png', (32, 32))
							#                         tiled = enemy_layout[int(col)]
							#                       sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							swordsman = enemy.Swordsman(col_index * 32, row_index * 32)
							self.swordsman_group.add(swordsman)
						if type == 'Wizard':
							enemy_layout = slicing_tiles('data/graphics/images/swordsman.png', (32, 32))
							#                         tiled = enemy_layout[int(col)]
							#                       sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							wizard = enemy.Wizard(col_index * 32, row_index * 32 - 8)
							self.wizard_group.add(wizard)
						if type == 'Imposter':
							imposter_layout = slicing_tiles('data/graphics/images/imposter_tree.png', (32, 32))
							tiled = imposter_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							imposter = enemy.Imposter(col_index * 32, row_index * 32 - 32)
							self.imposter_group.add(imposter)
						if type == 'Blobs':
							blob_layout = slicing_tiles('data/graphics/images/blob_img.png', (97, 30))
							tiled = blob_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							blob = enemy.Blob(col_index * 32, row_index * 32 + 15)
							self.blob_group.add(sprite)
						if type == 'Slopes':
							slope_layout = slicing_tiles('data/graphics/FlashbackTerrain/Slopes/Slopes.png', (32, 32))
							ramps = slope_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], ramps)
							self.slopesgroup.add(sprite)
						if type == 'TopSlopes':
							slope_layout = slicing_tiles('data/graphics/FlaskbackTerrain/Grass/Grass.png', (32, 32))
							topramp = slope_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], topramp)
							self.headslopesgroup.add(sprite)
						if type == 'Spawn':
							life = slicing_tiles('data/graphics/FlashbackTerrain/Spawn/spawnportal.png', (32, 64))
							born_set = life[int(col)]
							if col == '0':
								sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], born_set)
								if not self.dead:
									self.Spawn.add(sprite)
								self.dead = True
								player = Player([col_index * 32, row_index * 32])
								self.player.add(player)
								self.dead = False
							if col == '1':
								sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32 - 32], born_set)
								self.End.add(sprite)
						if type == 'GoodEnding':
							end2 = slicing_tiles('data/graphics/FlashbackTerrain/Spawn/light_path.png', (32, 64))
							good_set = end2[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32 - 32], good_set)
							self.GoodEnd.add(sprite)
						if type == 'BadEnding':
							end = slicing_tiles('data/graphics/FlashbackTerrain/Spawn/dark_path.png', (32, 64))
							borned_set = end[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32 - 32],borned_set)
							self.BadEnd.add(sprite)
					col_index += 1
				row_index += 1
			self.tile_sprites = self.tiles.sprites()
			self.barrier_sprites = self.barriers.sprites()
			self.slope_sprite = self.slopesgroup.sprites()
		elif self.path == 'data/levels/level_0/':
			# Used to create sprite_groups to prepare for drawing
			row_index = 0
			for row in layout:
				col_index = 0
				for col in row:
					if col != '-1':
						if type == 'Grass':
							terrain_layout = slicing_tiles('data/graphics/EricTerrain/Grass/Grass.png')
							tile = terrain_layout[int(col)]
							sprite = ground_tile(self.tile_size, [col_index * 16, row_index * 16], tile)
							self.tiles.add(sprite)
						if type == 'Platform':
							plat_layout = slicing_tiles('data/graphics/SimonTerrain/Platform/moving_platforms.png', (32,32))
							tile = plat_layout[int(col)]
							#sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							sprite = enemy.Platform(col_index * 16, row_index * 16)
							self.platform_group.add(sprite)
						if type == 'Barrier':
							terrain_layout = slicing_tiles('data/graphics/images/16barrier.png')
							tile = terrain_layout[int(col)]
							sprite = ground_tile(self.tile_size, [col_index * 16, row_index * 16], tile)
							self.barriers.add(sprite)
						if type == 'Slopes':
							slope_layout = slicing_tiles('data/graphics/EricTerrain/Grass/Slope.png')
							slope = slope_layout[int(col)]
							sprite = ground_tile(self.tile_size, [col_index * 16, row_index * 16], slope)
							self.slopesgroup.add(sprite)
						if type == 'Gold':
							gold = slicing_tiles('data/graphics/EricTerrain/Coin/gold_coin.png')
							tiles = gold[int(col)]
							sprite = ground_tile(self.tile_size, [col_index * 16, row_index * 16], tiles)
							self.coin.add(sprite)
						if type == 'Death':
							death = slicing_tiles('data/graphics/EricTerrain/Death/Death.png')
							tileset = death[int(col)]
							sprite = ground_tile(self.tile_size, [col_index * 16, row_index * 16], tileset)
							self.Death.add(sprite)
						if type == 'Trees':
							if col == '0':
								tree_0 = slicing_tiles('data/graphics/EricTerrain/Tree/Tree_0.png', (64, 64))
								tree_set = tree_0[int(col)]
								sprite = ground_tile(self.tile_size, (col_index * 16, (row_index - 3) * 16.1), tree_set)
							if col == '1':
								tree_1 = slicing_tiles('data/graphics/EricTerrain/Tree/Tree_1.png', (64, 64))
								tree_1_set = tree_1[0]
								sprite = ground_tile(self.tile_size, (col_index * 16, (row_index - 3) * 16.1), tree_1_set)
							self.tree.add(sprite)
						if type == 'Spawn':
							life = slicing_tiles('data/graphics/EricTerrain/Spawn/spawnportal.png', (16,32))
							born_set = life[int(col)]
							if col == '0':
								sprite = ground_tile(self.tile_size, [col_index * 16, row_index * 16], born_set)
								if not self.dead:
									self.Spawn.add(sprite)
								self.dead = True
								player = Player([col_index * 16, row_index * 16])
								self.player.add(player)
								self.dead = False
							if col == '1':
								sprite = ground_tile(self.tile_size, [col_index * 16, row_index * 16 - 16], born_set)
								self.End.add(sprite)
					col_index += 1
				row_index += 1
			self.tile_sprites = self.tiles.sprites()
		elif self.path == 'data/levels/level_1/' or 'data/levels/level_2/' or 'data/levels/level_3/' or 'data/levels/level_4/':
			row_index = 0
			for row in layout:
				col_index = 0
				for col in row:
					if col != '-1':
						if type == 'Grass':
							terrain_layout = slicing_tiles('data/graphics/SimonTerrain/Grass/Grass.png', (32,32))
							tile = terrain_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							self.tiles.add(sprite)
						if type == 'Platform':
							plat_layout = slicing_tiles('data/graphics/SimonTerrain/Platform/moving_platforms.png', (32,32))
							#tile = plat_layout[int(col)]
							#sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							sprite = enemy.Platform(col_index * 32, row_index * 32)
							self.platform_group.add(sprite)
						'''if type == 'UpPlatform':
							plat_layout = slicing_tiles('data/graphics/SimonTerrain/Platform/moving_platforms.png', (32,32))
							tile = plat_layout[int(col)]
							#sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							sprite = Platform(col_index * 32, row_index * 32, 0, 1)
							self.platform_group.add(sprite)'''
						if type == 'Barrier':
							terrain_layout = slicing_tiles('data/graphics/images/barrier.png', (32,32))
							tile = terrain_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tile)
							self.barriers.add(sprite)
						if type == 'Gold':
							gold = slicing_tiles('data/graphics/SimonTerrain/Coin/gold_coin.png', (32,32))
							tiles = gold[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiles)
							self.coin.add(sprite)
						if type == 'Death':
							death = slicing_tiles('data/graphics/SimonTerrain/Death/Death.png', (32,32))
							tileset = death[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tileset)
							self.Death.add(sprite)
						if type == 'Trees':
							tree_layout = slicing_tiles('data/graphics/SimonTerrain/Tree/Tree_tileset.png', (32,32))
							tiled = tree_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							self.tree.add(sprite)
						if type == 'Merchant':
							tree_layout = slicing_tiles('data/graphics/images/merchant.png', (32,32))
							tiled = tree_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							self.merchant_group.add(sprite)
						if type == 'Mushroom':
							mush_layout = slicing_tiles('data/graphics/images/mushroom_0.png', (16, 16))
							tiled = mush_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							mushroom = enemy.Mushroom(col_index * 32, row_index * 32 + 18)
							self.mushroom_group.add(mushroom)
						if type == 'Swordsman':
							enemy_layout = slicing_tiles('data/graphics/images/swordsman.png', (32,32))
	#                         tiled = enemy_layout[int(col)]
	 #                       sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							swordsman = enemy.Swordsman(col_index * 32, row_index * 32)
							self.swordsman_group.add(swordsman)
						if type == 'Wizard':
							enemy_layout = slicing_tiles('data/graphics/wizard/idle/idle_0.png', (32, 32))
							#                         tiled = enemy_layout[int(col)]
							#                       sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							wizard = enemy.Wizard(col_index * 32, row_index * 32 - 8)
							self.wizard_group.add(wizard)
						if type == 'Imposter':
							imposter_layout = slicing_tiles('data/graphics/images/imposter_tree.png', (32,32))
							tiled = imposter_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							imposter = enemy.Imposter(col_index * 32, row_index * 32 - 32)
							self.imposter_group.add(imposter)
						if type == 'Blobs':
							blob_layout = slicing_tiles('data/graphics/images/blob_img.png', (97, 30))
							tiled = blob_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], tiled)
							blob = enemy.Blob(col_index * 32, row_index * 32 + 15)
							self.blob_group.add(sprite)
						if type == 'Slopes':
							slope_layout = slicing_tiles('data/graphics/SimonTerrain/Slopes/Slopes.png', (32,32))
							ramps = slope_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], ramps)
							self.slopesgroup.add(sprite)
						if type == 'TopSlopes':
							slope_layout = slicing_tiles('data/graphics/SimonTerrain/Slopes/Slopes.png', (32,32))
							topramp = slope_layout[int(col)]
							sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], topramp)
							self.headslopesgroup.add(sprite)
						if type == 'Spawn':
							life = slicing_tiles('data/graphics/SimonTerrain/Spawn/spawnportal.png', (32,64))
							born_set = life[int(col)]
							if col == '0':
								sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32], born_set)
								if not self.dead:
									self.Spawn.add(sprite)
								self.dead = True
								player = Player([col_index * 32, row_index * 32])
								self.player.add(player)
								self.dead = False
							if col == '1':
								sprite = ground_tile(self.Simon_tile_size, [col_index * 32, row_index * 32 - 32], born_set)
								self.End.add(sprite)
					col_index += 1
				row_index += 1
			self.tile_sprites = self.tiles.sprites()
			self.platform_sprites = self.platform_group.sprites()
			self.barrier_sprites = self.barriers.sprites()
			self.slope_sprite = self.slopesgroup.sprites()
			self.headslope_sprites = self.headslopesgroup.sprites()

	def scrolling(self):
		spawn = self.Spawn.sprite
		player = self.player.sprite
		true_scroll = [0, 0]
		if self.dead == False:
			true_scroll[0] += (player.rect.x-true_scroll[0] - rescaled_width // 2) // 15
			true_scroll[1] += (player.rect.y-true_scroll[1] - rescaled_height // 2) // 15
			self.scroll = true_scroll.copy()
			self.scroll[0] = int(self.scroll[0])
			self.scroll[1] = int(self.scroll[1])
		else:
			true_scroll[0] += (spawn.rect.x-true_scroll[0])
			true_scroll[1] += (spawn.rect.y-true_scroll[1])
			self.scroll = true_scroll.copy()
			self.scroll[0] = int(self.scroll[0])
			self.scroll[1] = int(self.scroll[1])

	def collision_movement(self):
		if self.dead == False:
			player = self.player.sprite
			player.x = player.rect.x
			player.x += player.movement[0]
			player.rect.x = int(player.x)

			self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
			for tile in self.tiles.sprites():
				if tile.rect.colliderect(player.rect):
					if player.movement[0] > 0:
						player.rect.right = tile.rect.left
						self.collision_types['right'] = True
					if player.movement[0] < 0:
						player.rect.left = tile.rect.right
						self.collision_types['left'] = True
			for platform in self.platform_group.sprites():
				if platform.rect.colliderect(player.rect):
					if player.movement[0] > 0:
						player.rect.right = platform.rect.left
						self.collision_types['right'] = True
					if player.movement[0] < 0:
						player.rect.left = platform.rect.right
						self.collision_types['left'] = True
			for end_tile in self.End.sprites():
				if end_tile.rect.colliderect(player.rect):
					self.end_level()
			for goodending in self.GoodEnd.sprites():
				if goodending.rect.colliderect(player.rect):
					self.end_level()
			for badending in self.BadEnd.sprites():
				if badending.rect.colliderect(player.rect):
					self.end_level()

			player.y = player.rect.y
			player.y += player.movement[1]
			player.rect.y = int(player.y)

			self.slope_collision_from_above(player)
			self.slope_collision_from_below(player)
			self.rectangle_collision(player)
			self.platform_collision(player)
			self.mushroom_collision(player)
			self.merchant_collision(player)
			self.death_collision(player)
			self.coin_collision(player)
			self.attack(player)
			for end_tile in self.End.sprites():
				if end_tile.rect.colliderect(player.rect):
					self.end_level()
			for goodending in self.GoodEnd.sprites():
				if goodending.rect.colliderect(player.rect):
					self.end_level()
			for badending in self.BadEnd.sprites():
				if badending.rect.colliderect(player.rect):
					self.end_level()

			if self.collision_types['bottom']:
				player.collide_bottom = True
				player.air_timer = 0
				player.vertical_momentum = 0
			else:
				player.collide_bottom = False
				player.air_timer += 1

			if self.collision_types['top']:
				player.vertical_momentum = 0

	def rectangle_collision(self, player):
		for tile in self.tiles.sprites():
			if tile.rect.colliderect(player.rect):
				if player.movement[1] > 0:
					player.rect.bottom = tile.rect.top
					self.collision_types['bottom'] = True
				if player.movement[1] < 0:
					player.rect.top = tile.rect.bottom
					self.collision_types['top'] = True
		for barrier in self.barriers.sprites():
			if barrier.rect.colliderect(player.rect):
				if player.movement[0] > 0:
					player.rect.right = barrier.rect.left
					self.collision_types['right'] = True
				if player.movement[0] < 0:
					player.rect.left = barrier.rect.right
					self.collision_types['left'] = True

	def mushroom_collision(self, player):
		for mushroom in self.mushroom_group.sprites():
			mushroom_top = mushroom.rect.top
			player_bottom = player.rect.bottom
			if mushroom_top <= player_bottom:
				if mushroom.rect.colliderect(player.rect):
					self.mushroom_group.remove(mushroom)
					self.mushroom_inv += 1
					self.mushroom_taken += 1

	def getFirstAndLastPointsOfCollision(self, collisionMask):
		firstPoint = None
		lastPoint = None
		for y_pos in range(collisionMask.get_size()[1]):
			for x_pos in range(collisionMask.get_size()[0]):
				position = (x_pos, y_pos)
				if collisionMask.get_at(position):
					if not firstPoint:
						firstPoint = position
					lastPoint = position

		return firstPoint, lastPoint

	def slope_collision_from_below(self, player):
		maxtopVerticalOffset = 0

		for headslope in self.headslopesgroup.sprites():
			if headslope.rect.colliderect(player.rect):
				topoffset = (headslope.rect.left - player.rect.left, headslope.rect.top - player.rect.top + 1)

				collisionMask = player.mask.overlap_mask(headslope.mask, topoffset)
				firstIntersection, lastIntersection = self.getFirstAndLastPointsOfCollision(collisionMask)

				if firstIntersection:
					verticalOffset = lastIntersection[1] - firstIntersection[1]
					if verticalOffset > maxtopVerticalOffset:
						maxtopVerticalOffset = verticalOffset

				if headslope.rect.right == player.rect.right:
					player.rect.x += 1
					player.rect.y += 1

				if headslope.rect.left == player.rect.left:
					player.rect.x -= 1
					player.rect.y += 1

		if maxtopVerticalOffset:
			player.rect.top += maxtopVerticalOffset

	def slope_collision_from_above(self, player):
		maxVerticalOffset = 0  # in cases where player collides with multiple slopes at once, we should move him by maximum required amount, otherwise he'll be moved up next frame. Less jitter
		for slope in self.slopesgroup.sprites():
			if slope.rect.colliderect(player.rect):
				offset = (slope.rect.left - player.rect.left, slope.rect.top - player.rect.top - 1)
				almostCollisionOffset = player.mask.overlap(slope.mask, offset)  # if not None: player is exactly 1 pixel above slope, aka touching the slope, without being inside of it
				realCollisionOffset = pygame.sprite.collide_mask(player, slope)  # if not None: Player has at least 1 pixel inside the slope
				if almostCollisionOffset:
					if almostCollisionOffset[1] > slope.rect.height / 2:
						self.collision_types['bottom'] = True  # remove vertical momentum

						if realCollisionOffset:
							verticalOffset = player.rect.height - realCollisionOffset[1]  # move the player by this amount, and he'll be touching the current ground tile without being inside of it
							if verticalOffset > maxVerticalOffset:
								maxVerticalOffset = verticalOffset

		if maxVerticalOffset:
			player.rect.bottom -= maxVerticalOffset

	def platform_collision(self, player):
		for platform in self.platform_group.sprites():
			if platform.rect.colliderect(pygame.Rect(player.rect.left, player.rect.top, player.rect.width, player.rect.height + 1)):
				self.on_platform = True
				if player.movement[1] > 0:
					player.rect.bottom = platform.rect.top
					player.rect.x += platform.move_x * platform.move_direction
					self.collision_types['bottom'] = True
				if player.movement[1] < 0:
					player.rect.top = platform.rect.bottom
					self.collision_types['top'] = True
			if platform.rect.colliderect(pygame.Rect(player.rect.x - 5, player.rect.top, player.rect.width, player.rect.height)):
				player.rect.left = platform.rect.right - 3
				self.collision_types['left'] = True
			if platform.rect.colliderect(pygame.Rect(player.rect.x + 5, player.rect.top, player.rect.width, player.rect.height)):
				player.rect.right = platform.rect.left + 3
				self.collision_types['right'] = True


	def coin_collision(self, player):
		for coin in self.coin.sprites():
			if coin.rect.colliderect(player.rect):
				self.coin.remove(coin)
				self.coin_inv += 1
				self.coin_count += 1

	def merchant_collision(self, player):
		self.merchant_beside = 0
		for merchant in self.merchant_group.sprites():
			if merchant.rect.colliderect(player.rect):
				self.merchant_beside += 1

	def death_collision(self, player):
		for death in self.Death.sprites():
			if death.rect.colliderect(player.rect):
				self.dead = True
				self.health = 0
				self.player.empty()

	def attack(self, player):
		if self.dead == False:
			self.direction = ''
			if self.time_attacked >= 2:
				player.invincibility = False
			for imposter in self.imposter_group.sprites():
				imposter.attack_animation = False
				if imposter.rect.colliderect(player.rect):
					realCollisionImposter = pygame.sprite.collide_mask(player, imposter)
					if realCollisionImposter:
						imposter.attack_animation = True
						self.imposter_kill = True
			for swordsman in self.swordsman_group.sprites():
				swordsman.attack_animation = False
				if swordsman.rect.colliderect(player.rect):
					realCollisionSwords = pygame.sprite.collide_mask(player, swordsman)
					if realCollisionSwords:
						swordsman.attack_animation = True
						if player.invincibility == False:
							player.invincibility = True
							self.start_time_attack = time.time()
							self.health -= 2
						if player.player_attack:
							swordsman.health -= 10
						if player.rect.x > swordsman.rect.x:
							swordsman.change_flip(True)
							self.direction = 'left'
						elif player.rect.x < swordsman.rect.x:
							swordsman.change_flip(False)
							self.direction = 'right'
				else:
					if self.direction == 'left':
						swordsman.change_flip(False)
						self.direction = ''
					elif self.direction == 'right':
						swordsman.change_flip(True)
						self.direction = ''
				if swordsman.health == 0:
					self.swordsman_group.remove(swordsman)
			for wizard in self.wizard_group.sprites():
				wizard.attack_animation = False
				if abs(player.rect.x - wizard.rect.x) < 200 and player.rect.y - 8 == wizard.rect.y :
					wizard.attack_animation = True
					if player.rect.x > wizard.rect.x:
						wizard.change_flip(True)
						if self.shoot_cooldown == 0 and self.ammo > 0:
							self.shoot_cooldown = 60
							orbs = enemy.Orb(wizard.rect.centerx + 10, wizard.rect.centery - 16, 1)
							self.orb_group.add(orbs)
							self.ammo -= 1
						if self.shoot_cooldown > 0:
							self.shoot_cooldown -= 1
							self.ammo += 1
						self.direction = 'left'
					elif player.rect.x < wizard.rect.x:
						wizard.change_flip(False)
						if self.shoot_cooldown == 0 and self.ammo > 0:
							self.shoot_cooldown = 60
							orbleft = enemy.Orb(wizard.rect.centerx - 20, wizard.rect.centery - 16, -1)
							self.orb_group.add(orbleft)
							self.ammo -= 1
						if player.player_attack:
							wizard.health -= 20
						if self.shoot_cooldown > 0:
							self.shoot_cooldown -= 1
							self.ammo += 1
						self.direction = 'right'
					else:
						if self.direction == 'left':
							wizard.change_flip(False)
							self.direction = ''
						elif self.direction == 'right':
							wizard.change_flip(True)
							self.direction = ''
					if wizard.health == 0:
						self.wizard_group.remove(wizard)
					# check collision with characters
					for orb in self.orb_group.sprites():
						if pygame.Rect.colliderect(orb.rect, player.rect):
							orb.kill()
							if player.invincibility == False:
								player.invincibility = True
								self.start_time_attack = time.time()
								self.health -= 1.5
	def end_level(self):
			loading_imgs = []
			for i in range(1, 4):
				loading_img = pygame.image.load('data/graphics/loading_images/' + f'loading{i}.png').convert_alpha()
				loading_img = pygame.transform.scale(loading_img, (1200, 640))
				loading_imgs.append(loading_img)
			for x in range(240):
				for imgs in loading_imgs:
					logo(imgs, 0, 0)
					pygame.display.update()
			score.score_keeping(self.path, self.score, [self.coin_count, self.time_elasped, self.mushroom_taken])
			n = 0
			final_score = 0
			if self.last_level:
				for _, action, ___ in walk('data/levels/'):
					if n > 5:
						n = 5
					f = open(f'data/levels/level_{n}/score', 'r')
					data = f.read()
					f.close()
					final_score += int(data)
					n += 1
				f = open('data/levels/Final_Score', 'w')
				f.write(str(final_score))
				f.close()
			self.done = True
			if self.last_level and self.done:
				self.game_over = True

	def merchant_check(self):
		if self.merchant_beside != 0:
			return True
		else:
			return False
	def player_swing(self):
		player = self.player.sprite
		if self.player_attack:
			player.player_attack = True
	def player_jump(self):
		player = self.player.sprite
		if player.air_timer < 6:
			player.jump_counter = 0
			player.vertical_momentum = -4
			player.jump_buffer = False
		elif player.air_timer > 6:
			player.jump_held = False
			player.jump_buffer = True

		if player.jump_buffer:
			if player.jump_counter < 1:
				player.vertical_momentum = -3.5
				player.jump_counter += 1
				player.jump_held = False
			else:
				player.jump_held = True

		else:
			player.jump_held = False

	def dying(self):
		self.player.empty()
		self.player = pygame.sprite.GroupSingle()
		if self.scroll[0] == 0 and self.scroll[1] == 0:
			player = Player((0, 0))
			self.player.add(player)
			self.health = self.max_health
			self.dead = False
	def draw_img(self, img, x, y):
		self.surface.blit(img, (x, y))
	def draw_bg(self):
		self.keys = pygame.key.get_pressed()
		player = self.player.sprite
		if self.keys[pygame.K_RIGHT] and self.player_direction < 3000:
			self.player_direction += 1
		elif self.keys[pygame.K_LEFT] and self.player_direction > 0:
			self.player_direction -= 1
		for x in range(40):
			speed = 1
			for i in self.bg_imgs:
				self.surface.blit(i, ((x * 600) - self.player_direction * speed, 0))
				speed += 0.1
	def draw_hearts(self):
		half_hearts_total = self.health / 2
		half_heart_exists = half_hearts_total - int(half_hearts_total) != 0
		for heart in range(int(self.max_health / 2)):
			if int(half_hearts_total) > heart:
				self.surface.blit(self.full_heart, (heart * 30 + 5, 10))
			elif half_heart_exists and int(half_hearts_total) == heart:
				self.surface.blit(self.half_heart, (heart * 30 + 5, 10))
			else:
				self.surface.blit(self.empty_heart, (heart * 30 + 5, 10))
		if self.health <= 0:
			self.dead = True
	def button_held(self):
		player = self.player.sprite
		player.jump_held = True

	def button_released(self):
		player = self.player.sprite
		player.jump_held = False
	def run(self):
		# tiles
		self.time_elasped = time.time() - self.start_time
		self.time_attacked = (time.time() - self.start_time_attack)
		if self.time_attacked > 2:
			self.time_attacked = 2
		if self.imposter_kill == False:
			self.imposter_attacking = 0
			self.scrolling()
		# death
		if self.dead and self.imposter_kill == False:
			self.dying()

		# merchant check
		self.merchant_check()
		#background drawing
		self.tree.update(self.scroll)
		self.tree.draw(self.surface)
		self.blob_group.update(self.scroll)
		self.tiles.update(self.scroll)
		self.tiles.draw(self.surface)
		self.slopesgroup.update(self.scroll)
		self.slopesgroup.draw(self.surface)
		self.headslopesgroup.update(self.scroll)
		self.headslopesgroup.draw(self.surface)
		self.mushroom_group.update(self.scroll)
		self.mushroom_group.draw(self.surface)
		self.imposter_group.update(self.scroll)
		self.imposter_group.draw(self.surface)
		self.platform_group.update(self.scroll)
		self.platform_group.draw(self.surface)


		self.bg_objects.update(self.scroll)
		self.bg_objects.draw(self.surface)
		self.heart_objects.draw(self.surface)
		self.coin.draw(self.surface)
		self.coin.update(self.scroll)
		self.blob_group.draw(self.surface)
		self.npc0.update(self.scroll)
		self.npc0.draw(self.surface)
		self.npc1.update(self.scroll)
		self.npc1.draw(self.surface)
		self.npc2.update(self.scroll)
		self.npc2.draw(self.surface)
		self.npc3.update(self.scroll)
		self.npc3.draw(self.surface)
		self.swordsman_group.update(self.scroll)
		self.swordsman_group.draw(self.surface)
		self.wizard_group.update(self.scroll)
		self.wizard_group.draw(self.surface)
		self.orb_group.update(self.scroll)
		self.orb_group.draw(self.surface)
		self.End.update(self.scroll)
		self.End.draw(self.surface)
		self.BadEnd.update(self.scroll)
		self.BadEnd.draw(self.surface)
		self.GoodEnd.update(self.scroll)
		self.GoodEnd.draw(self.surface)
		self.Death.update(self.scroll)
		self.barriers.update(self.scroll)
		self.Spawn.update(self.scroll)
		self.Spawn.draw(self.surface)
		self.merchant_group.update(self.scroll)
		self.merchant_group.draw(self.surface)
		if self.path == 'data/levels/level_5/':
			self.npc_speak()

		#imposter win
		if self.imposter_kill and self.imposter_attacking >= 5:
			self.surface.fill('black')
			self.health -= 2
			if self.health < 0:
				self.health = 0
			self.player.empty()

		while self.imposter_kill and self.health >= 0:
			self.dead = True
			self.imposter_attacking += 1

			if self.health <= 0:
				self.imposter_kill = False
				time.sleep(0.5)
			time.sleep(0.5)
			break
		# player
		player = self.player.sprite

		self.player.update(self.scroll)
		self.player.draw(self.surface)
		self.collision_movement()