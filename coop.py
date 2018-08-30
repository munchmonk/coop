#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7



# play with maxwidth and maxheight to affect camera; screenwidth / 2 and screenheight to keep it still


# medusa - sunglasses!




import pygame
import sys
import random
import time

from room import Room, Door, Heart, Medusa, Antidote
from player import Player
from util import Camera










class Game:
	def __init__(self):
		pygame.init()

		# Window and surfaces
		self.screenwidth = 1200
		self.screenheight = 700
		self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
		self.surf1 = pygame.Surface((int(self.screenwidth / 2), self.screenheight))
		self.surf2 = pygame.Surface((int(self.screenwidth / 2), self.screenheight))

		# Enlarge to have a moving camera
		self.maxwidth = int(self.screenwidth / 2)
		self.maxheight = self.screenheight

		self.gameover = False
		self.clock = pygame.time.Clock()
		self.dt = 0
		self.fps = 45

		self.players = pygame.sprite.Group()
		self.rooms = pygame.sprite.Group()
		self.doors = pygame.sprite.Group()
		self.antidotes = pygame.sprite.Group()
		self.hearts = pygame.sprite.Group()
		self.medusa = None
		self.allsprites = pygame.sprite.Group()

		self.maxrooms = 5
		self.make_rooms()

		# Spawn players
		self.p1 = Player(0, self)
		self.p2 = Player(1, self)

		starting_rooms = self.get_starting_rooms()
		self.p1.curr_room = starting_rooms[0]
		self.p2.curr_room = starting_rooms[1]

		# Spawn hearts
		self.makehearts()

		# Spawn Medusa
		self.spawn_medusa()

		# set cameras
		self.camera = [Camera(self.maxwidth, self.maxheight, int(self.screenwidth / 2), self.screenheight),
						Camera(self.maxwidth, self.maxheight, int(self.screenwidth / 2), self.screenheight)]

		self.play()

	def count_antidotes(self):
		tot = 0
		for room in self.rooms.sprites():
			tot += len(room.antidotes)
		for player in self.players.sprites():
			if player.antidote:
				tot += 1

		return tot


	def spawn_antidote(self):
		room = random.choice(self.rooms.sprites())
		room.antidotes.append(Antidote(self))

	def spawn_medusa(self):
		room = self.p1.curr_room

		while not room.is_empty():
			room = random.choice(self.rooms.sprites())

		self.medusa = Medusa(self, room)
		room.medusa = True



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

			# p1, left screen
			if sprite.is_occupied_by(self.p1):
				# draw room
				self.surf1.blit(sprite.image, self.camera[self.p1.id].apply(sprite))

				# draw doors
				for door in sprite.doors:
					self.surf1.blit(door.image, self.camera[self.p1.id].apply(door))

				# draw antidotes
				for antidote in sprite.antidotes:
					self.surf1.blit(antidote.image, self.camera[self.p1.id].apply(antidote))					

				# draw hearts
				for heart in sprite.hearts:
					self.surf1.blit(heart.image, self.camera[self.p1.id].apply(heart))

				# draw medusa
				if sprite.medusa:
					self.surf1.blit(self.medusa.image, self.camera[self.p1.id].apply(self.medusa))

			# p2, right screen
			if sprite.is_occupied_by(self.p2):
				# draw room
				self.surf2.blit(sprite.image, self.camera[self.p2.id].apply(sprite))

				# draw doors
				for door in sprite.doors:
					self.surf2.blit(door.image, self.camera[self.p2.id].apply(door))

				# draw antidotes
				for antidote in sprite.antidotes:
					self.surf2.blit(antidote.image, self.camera[self.p2.id].apply(antidote))					

				# draw hearts
				for heart in sprite.hearts:
					self.surf2.blit(heart.image, self.camera[self.p2.id].apply(heart))

				# draw medusa
				if sprite.medusa:
					self.surf2.blit(self.medusa.image, self.camera[self.p2.id].apply(self.medusa))

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

	def check_loss(self):
		if self.p1.petrified and self.p2.petrified:
			print("You lose!")
			return True
		return False


	def update(self):
		self.allsprites.update()

		if self.count_antidotes() < 2:
			self.spawn_antidote()

		self.camera[self.p1.id].update(self.p1)
		self.camera[self.p2.id].update(self.p2)

	def play(self):
		while True:
			self.dt = self.clock.tick(self.fps)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if not self.gameover:
				self.update()
				self.draw()
				self.gameover = self.check_win() or self.check_loss()




if __name__ == '__main__':
	Game()