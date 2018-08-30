import pygame


class Camera:
	def __init__(self, width, height, screenwidth, screenheight):
		self.rect = pygame.Rect(0, 0, width, height)
		self.width = width
		self.height = height
		self.screenwidth = screenwidth
		self.screenheight = screenheight

	def apply(self, entity):
		return entity.rect.move(self.rect.topleft)

	def update(self, target):
		x = -target.rect.x + int(self.screenwidth / 2)
		y = -target.rect.y + int(self.screenheight / 2)
		
		x = min(0, x)
		x = max(x, -(self.width - self.screenwidth))

		y = min(0, y)
		y = max(y, -(self.height - self.screenheight))

		self.rect = pygame.Rect(x, y, self.width, self.height)