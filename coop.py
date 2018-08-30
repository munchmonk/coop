#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7



# play with maxwidth and maxheight to affect camera; screenwidth / 2 and screenheight to keep it still


# spawn an item next to each player at the start, in order to win they must collect the other one and enter the same room
# (or spawn it in a random room)




import pygame
import sys
import random
import time

pygame.init()




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




class Prop(pygame.sprite.Sprite):
	img = pygame.image.load('prop1.png')

	def __init__(self, game):
		self.game = game
		self.groups = self.game.props, self.game.allsprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = Prop.img
		self.rect = self.image.get_rect()

		centerx = int(game.screenwidth / 4) + random.randint(-15, 15) * 10
		centery = int(game.screenheight / 2) + random.randint(-15, 15) * 10
		self.rect.center = (centerx, centery)

	def update(self):
		pass

	def draw(self):
		pass






class Tile(pygame.sprite.Sprite):
	img = pygame.image.load('tile.png')

	def __init__(self, x, y, game):
		self.game = game
		self.groups = self.game.tiles, self.game.allsprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = Tile.img
		self.rect = self.image.get_rect(topleft=(x, y))

	def update(self):
		pass

	def draw(self):
		pass


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

	def teleport(self, door):
		self.curr_room = door.destination

		# Center the player, then move it closer to the door
		self.rect.center = (int(self.game.screenwidth / 4), int(self.game.screenheight / 2))

		stepx = int((self.rect.centerx - door.rect.centerx) / 1.5)
		stepy = int((self.rect.centery - door.rect.centery) / 1.5)
		
		self.rect.centerx += stepx
		self.rect.centery += stepy

	def update(self):
		key = pygame.key.get_pressed()

		# Movement - to redo completely in due time
		if self.id == 0:
			if key[pygame.K_w]:
				self.rect.y -= 10
			if key[pygame.K_a]:
				self.rect.x -= 10
			if key[pygame.K_s]:
				self.rect.y += 10
			if key[pygame.K_d]:
				self.rect.x += 10
		else:
			if key[pygame.K_UP]:
				self.rect.y -= 10
			if key[pygame.K_LEFT]:
				self.rect.x -= 10
			if key[pygame.K_DOWN]:
				self.rect.y += 10
			if key[pygame.K_RIGHT]:
				self.rect.x += 10

		# Collide with doors
		for door in self.curr_room.doors:
			if self.rect.colliderect(door.rect):
				self.teleport(door)

		# Collide with hearts
		for heart in self.curr_room.hearts:
			if self.rect.colliderect(heart.rect) and heart.id == self.id:
				self.heart = True
				self.curr_room.hearts.remove(heart)


		# Collide with room walls
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

	def draw(self):
		pass


class Game:
	def __init__(self):
		self.screenwidth = 1200
		self.screenheight = 700
		self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
		self.surf1 = pygame.Surface((int(self.screenwidth / 2), self.screenheight))
		self.surf2 = pygame.Surface((int(self.screenwidth / 2), self.screenheight))

		# Enlarge to have a moving camera
		self.maxwidth = int(self.screenwidth / 2)
		self.maxheight = self.screenheight

		self.gameover = False

		self.players = pygame.sprite.Group()
		self.tiles = pygame.sprite.Group()
		self.rooms = pygame.sprite.Group()
		self.doors = pygame.sprite.Group()
		self.hearts = pygame.sprite.Group()
		self.allsprites = pygame.sprite.Group()

		self.maxrooms = 4
		self.make_rooms()

		# Spawn players
		self.p1 = Player(0, self)
		self.p2 = Player(1, self)

		starting_rooms = self.get_starting_rooms()
		self.p1.curr_room = starting_rooms[0]
		self.p2.curr_room = starting_rooms[1]

		# Spawn hearts
		self.makehearts()

		# set cameras
		self.camera = [Camera(self.maxwidth, self.maxheight, int(self.screenwidth / 2), self.screenheight),
						Camera(self.maxwidth, self.maxheight, int(self.screenwidth / 2), self.screenheight)]

		self.play()

	def makehearts(self):
		room1 = self.p1.curr_room
		room2 = self.p2.curr_room

		while not room1.is_empty():
			room1 = random.choice(self.rooms.sprites())
		while not room2.is_empty() or room2 == room1:
			room2 = random.choice(self.rooms.sprites())

		room1.make_heart(self.p1.id)
		room2.make_heart(self.p2.id)




	def get_starting_rooms(self):
		room1 = random.choice(self.rooms.sprites())
		room2 = room1
		while room2 == room1:
			room2 = random.choice(self.rooms.sprites())
		return room1, room2


	def sort_rooms_by_unlinked(self):
		unlinked = []
		linked = []

		for room in self.rooms.sprites():
			found = False
			for door in room.doors:
				if door.destination:
					found = True
			if found:
				linked.append(room)
			else:
				unlinked.append(room)

		candidate_rooms = unlinked + linked
		return candidate_rooms

	def make_rooms(self):
		all_rooms_reachable = False

		# DEBUGGING -------
		# attempts = 0

		while not all_rooms_reachable:

			# Empty all rooms every iteration
			self.rooms.empty()

			# Create rooms with doors in random locations
			for i in range(self.maxrooms):
				Room(self)

			# Pair each door with another suitable one in a random room
			for curr_room in self.rooms.sprites():
				for curr_door in curr_room.doors:
					if not curr_door.destination:

						found = False

						# Prioritise links to rooms still unreached
						candidate_rooms = self.sort_rooms_by_unlinked()

						for candidate_room in candidate_rooms:

							if found:
								break

							if candidate_room == curr_room:
								continue
							
							for candidate_door in candidate_room.doors:
								if candidate_door.destination:
									continue
								if ((curr_door.location == 0 and candidate_door.location == 1) or
									(curr_door.location == 1 and candidate_door.location == 0) or
									(curr_door.location == 2 and candidate_door.location == 3) or
									(curr_door.location == 3 and candidate_door.location == 4)):

									curr_door.destination = candidate_room
									candidate_door.destination = curr_room
									found = True

			# Remove all doors left unpaired
			for room in self.rooms.sprites():
				good_doors = []
				for door in room.doors:
					if door.destination:
						good_doors.append(door)
				room.doors = good_doors

			# Check if every room is reachable, if not start again
			all_rooms_reachable = self.check_all_rooms_reachable()

			# DEBUGGING --------	
			# attempts += 1
			# print('attempts', attempts)			

	def check_all_rooms_reachable(self):
		reachable = []
		doors_to_check = []
		start_room = random.choice(self.rooms.sprites())
		reachable.append(start_room)

		for door in start_room.doors:
			doors_to_check.append(door)

		while doors_to_check:
			if doors_to_check[0].destination not in reachable:
				reachable.append(doors_to_check[0].destination)
				for door in doors_to_check[0].destination.doors:
					doors_to_check.append(door)
			doors_to_check.pop(0)

		if len(reachable) == self.maxrooms:
			return True
		print('reachable:', len(reachable), '/', self.maxrooms)
		return False

	def in_the_same_room(self):
		if self.p1.curr_room == self.p2.curr_room:
			return True
		return False

	def draw(self):
		# draw background
		self.surf1.fill((0, 0, 255))
		self.surf2.fill((0, 255, 0))

		# draw sprites
		for sprite in self.rooms:

			if sprite.is_occupied_by(self.p1):
				self.surf1.blit(sprite.image, self.camera[self.p1.id].apply(sprite))
				for door in sprite.doors:
					self.surf1.blit(door.image, self.camera[self.p1.id].apply(door))
				for heart in sprite.hearts:
					self.surf1.blit(heart.image, self.camera[self.p1.id].apply(heart))

			if sprite.is_occupied_by(self.p2):
				self.surf2.blit(sprite.image, self.camera[self.p2.id].apply(sprite))
				for door in sprite.doors:
					self.surf2.blit(door.image, self.camera[self.p2.id].apply(door))
				for heart in sprite.hearts:
					self.surf2.blit(heart.image, self.camera[self.p2.id].apply(heart))

		# players
		if self.in_the_same_room():
			for sprite in self.players:
				self.surf1.blit(sprite.image, self.camera[self.p1.id].apply(sprite))
				self.surf2.blit(sprite.image, self.camera[self.p2.id].apply(sprite))
		else:
			self.surf1.blit(self.p1.image, self.camera[self.p1.id].apply(self.p1))
			self.surf2.blit(self.p2.image, self.camera[self.p2.id].apply(self.p2))

		# print to screen
		self.screen.blit(self.surf1, (0, 0))
		self.screen.blit(self.surf2, (int(self.screenwidth / 2), 0))

		pygame.display.flip()


	def check_win(self):
		if self.in_the_same_room() and self.p1.heart and self.p2.heart:
			print("You win!")
			return True
		return False


	def update(self):
		self.allsprites.update()
		self.camera[self.p1.id].update(self.p1)
		self.camera[self.p2.id].update(self.p2)

	def play(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if not self.gameover:
				self.update()
				self.draw()
				self.gameover = self.check_win()




if __name__ == '__main__':
	Game()