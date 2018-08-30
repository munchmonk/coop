import pygame
from room import Room


class Player(pygame.sprite.Sprite):
	img = [pygame.image.load('player1.png'), pygame.image.load('player2.png')]

	def __init__(self, side, game):
		self.game = game
		self.groups = self.game.players, self.game.allsprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.id = side

		self.image = Player.img[self.id]
		self.rect = self.image.get_rect()
		self.rect.center = (int(self.game.screenwidth / 4), int(self.game.screenheight / 2))

		self.curr_room = None
		self.heart = False
		self.speed = 0.3
		self.petrified = False
		self.antidote = False

	def teleport(self, door):
		self.curr_room = door.destination

		# Center the player, then move it closer to the door
		self.rect.center = (int(self.game.screenwidth / 4), int(self.game.screenheight / 2))

		stepx = int((self.rect.centerx - door.rect.centerx) / 1.5)
		stepy = int((self.rect.centery - door.rect.centery) / 1.5)
		
		self.rect.centerx += stepx
		self.rect.centery += stepy

	def get_movement_input(self):
		mx = 0
		my = 0

		key = pygame.key.get_pressed()

		if self.id == 0:
			if key[pygame.K_w]:
				my = -1
			if key[pygame.K_a]:
				mx = -1
			if key[pygame.K_s]:
				my = 1
			if key[pygame.K_d]:
				mx = 1
		else:
			if key[pygame.K_UP]:
				my = -1
			if key[pygame.K_LEFT]:
				mx = -1
			if key[pygame.K_DOWN]:
				my = 1
			if key[pygame.K_RIGHT]:
				mx = 1

		return mx, my

	def move(self, movement):
		mx, my = movement
		step_x = int(mx * self.speed * self.game.dt)
		step_y = int(my * self.speed * self.game.dt)

		if abs(mx) == 1 and abs(my) == 1:
			step_x *= 1 / 2 ** (1/2.0)
			step_y *= 1 / 2 ** (1/2.0)

		self.rect.x += step_x
		self.rect.y += step_y

		self.check_wall_collisions()

	def check_wall_collisions(self):
		left_limit = int((int(self.game.maxwidth) - Room.img.get_rect().width) / 2)
		right_limit = self.game.maxwidth - left_limit
		top_limit = int((int(self.game.maxheight) - Room.img.get_rect().width) / 2)
		bottom_limit = self.game.maxheight - top_limit

		if self.rect.x < left_limit:
			self.rect.x = left_limit
		if self.rect.right > right_limit:
			self.rect.right = right_limit
		if self.rect.y < top_limit:
			self.rect.y = top_limit
		if self.rect.bottom > bottom_limit:
			self.rect.bottom = bottom_limit


	def players_touching(self):
		if not self.game.in_the_same_room():
			return False

		if not self.rect.colliderect(self.get_friend().rect):
			return False

		return True


	def get_friend(self):
		if self.game.p1 == self:
			return self.game.p2
		if self.game.p2 == self:
			return self.game.p1




	def update(self):

		# Movement
		if not self.petrified:
			movement = self.get_movement_input()
			self.move(movement)

		# Collide with doors
		for door in self.curr_room.doors:
			if self.rect.colliderect(door.rect):
				self.teleport(door)

		# Collide with hearts
		for heart in self.curr_room.hearts:
			if self.rect.colliderect(heart.rect) and heart.id == self.id:
				self.heart = True
				self.curr_room.hearts.remove(heart)

		# Collide with antidote
		for antidote in self.curr_room.antidotes:
			if self.rect.colliderect(antidote.rect):
				self.antidote = True
				self.curr_room.antidotes.remove(antidote)

		# Give antidote
		if self.players_touching() and self.get_friend().petrified and self.antidote:
			self.get_friend().petrified = False
			self.antidote = False

		# Check medusa
		if self.curr_room.medusa and not self.heart:
			self.petrified = True


	def draw(self):
		pass