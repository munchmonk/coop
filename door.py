import pygame
import random


class Room(pygame.sprite.Sprite):
	img = pygame.image.load('room.png')
	prop_img = [pygame.image.load('prop1.png'), pygame.image.load('prop2.png')]

	def __init__(self, game):
		self.game = game
		self.groups = self.game.rooms, self.game.allsprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		
		# Makes a copy in order to be able to modify each individual room with props
		self.image = Room.img.copy()
		self.rect = self.image.get_rect(center=(int(game.screenwidth / 4), int(game.screenheight / 2)))

		self.hearts = []
		self.doors = []
		doors_n = random.randint(1, 4)
		for j in range(doors_n):
			self.make_door()

		self.make_props()

	def make_props(self):
		props_n = random.randint(0, 5)
		props = []

		for i in range(props_n):
			prop_collide = True

			while prop_collide:
				prop_collide = False

				prop_type = random.choice(self.prop_img)
				width = prop_type.get_rect().width
				height = prop_type.get_rect().height

				min_x = 0 + width
				max_x = self.rect.width - width * 2
				min_y = height
				max_y = self.rect.height - height * 2

				prop_x = random.randint(min_x, max_x)
				prop_y = random.randint(min_y, max_y)
				prop = pygame.Rect(prop_x, prop_y, width, height)

				for existing in props:
					if existing.colliderect(prop):
						prop_collide = True

				if not prop_collide:
					props.append(prop)
					self.image.blit(prop_type, prop)

	def make_door(self, loc=None, dest=None):
		new_door = Door(self.game, self, loc, dest)
		self.doors.append(new_door)
		return new_door

	def make_heart(self, side):
		self.hearts.append(Heart(self.game, side))


	def is_occupied_by(self, player):
		if player.curr_room == self:
			return True
		return False

	def is_empty(self):
		for player in self.game.players:
			if self.is_occupied_by(player):
				return False
		return True

	def update(self):
		pass

	def draw(self):
		pass


class Door(pygame.sprite.Sprite):
	img = pygame.image.load('door.png')

	def __init__(self, game, room, loc=None, dest=None):
		self.game = game
		self.room = room
		self.groups = self.game.doors, self.game.allsprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = Door.img
		self.rect = self.image.get_rect()

		self.loc = loc
		self.location = self.get_door_spawn_location()
		self.destination = dest

	def is_location_occupied(self, location):
		for door in self.room.doors:
			if door.location == location:
				return True
		return False

	def get_door_spawn_location(self):
		hor_left = int(self.game.maxwidth - Room.img.get_rect().width) / 2
		hor_right = hor_left + Room.img.get_rect().width
		hor_center = int(self.game.maxwidth / 2)

		ver_top = int(self.game.maxheight - Room.img.get_rect().height) / 2
		ver_center = int(self.game.maxheight / 2)
		ver_bottom = ver_top + Room.img.get_rect().height

		location = -1
		if self.loc:
			location = self.loc
		while location == -1 or self.is_location_occupied(location):
			location = random.randint(0, 3)

		# 0 = left
		if location == 0:
			self.rect.midleft = hor_left, ver_center
		# 1 = right
		elif location == 1:
			self.rect.midright = hor_right, ver_center
		# 2 = top
		elif location == 2:
			self.rect.midtop = hor_center, ver_top
		# 3 = bottom
		else:
			self.rect.midbottom = hor_center, ver_bottom

		return location

	def update(self):
		pass

	def draw(self):
		pass


class Heart(pygame.sprite.Sprite):
	img = [pygame.image.load('item1.png'), pygame.image.load('item2.png')]

	def __init__(self, game, side):
		self.game = game
		self.groups = self.game.hearts, self.game.allsprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.id = side
		self.image = Heart.img[side]
		self.rect = self.image.get_rect()

		centerx = int(game.screenwidth / 4) + random.randint(-15, 15) * 10
		centery = int(game.screenheight / 2) + random.randint(-15, 15) * 10
		self.rect.center = (centerx, centery)

	def update(self):
		pass

	def draw(self):
		pass