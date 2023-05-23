
import pygame

#button class
class Button():
	def __init__(self, x, y, image, scale):
		#values for the button
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
	def draw(self, surface):
		action = False
		#get the position of mouse
		position = pygame.mouse.get_pos()

		#check if mouse is over button and conditions
		if self.rect.collidepoint(position):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draws button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action