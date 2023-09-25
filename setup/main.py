import pygame, sys
from settings import *
from debug import debug
from level import Level

class Game:
	def __init__(self):
		
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda Like Game') # Sets the screen caption
		self.clock = pygame.time.Clock()

		self.level = Level() # Creates an instance class to run it inside the game
	
	def run(self):
		while True:
			# Event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black') # Fills the screen with black
			self.level.run()
			pygame.display.update() # Updates the screen
			self.clock.tick(FPS) # Controls the frame rate

if __name__ == '__main__':
	game = Game()
	game.run()