class Tile(pygame.sprite.Sprite):
	img = pygame.image.load('TILE.png')

	def __init__(self, x, y, game):
		self.game = game
		self.groups = self.game.TILES, self.game.allsprites

		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = Tile.img
		self.rect = self.image.get_rect(topleft=(x, y))

	def update(self):
		pass

	def draw(self):
		pass