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

		# sound
		main_sound = pygame.mixer.Sound('audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops=-1)
	
	def run(self):
		while True:
			# Event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR) # Fills the screen with black
			self.level.run()
			pygame.display.update() # Updates the screen
			self.clock.tick(FPS) # Controls the frame rate

if __name__ == '__main__':
	game = Game()
	game.run()
