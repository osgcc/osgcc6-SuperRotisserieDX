import pygame


class World():
	size = width, height = 1600, 900
	gravity = .3
	def __init__(self):
		self.screen = pygame.display.set_mode(self.size)
		self.objects = pygame.sprite.Group() #hold random objects/sprites
		self.players = pygame.sprite.Group()
		self.player = None
		self.clock = pygame.time.Clock()

	#gets called by main game loop to do everything
	def Update(self):
		self.getEvents()
		if self.player.dead:
			self.gameOver()
			return

		self.Draw()
		self.level.Update()
		for obj in self.objects:
			if not obj.Update():
				obj.kill()



	def gameOver(self):
		pygame.font.init()
		self.screen.fill(pygame.Color(224,24,13))
		fontobj = pygame.font.Font(None,80)
		msg = fontobj.render("YOU ARE LOSE", 1, (0,0,0))
		self.screen.blit(msg,[700,450], area=None, special_flags=0)

	#do all the drawing
	def Draw(self):
		self.screen.fill(pygame.Color(255,255,255))
		self.level.Draw()
		self.players.draw(self.screen)

		#self.objects.draw(self.screen) now drawn in level

	def getEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.QUIT
				sys.exit()
		keystate =  pygame.key.get_pressed()
		if keystate:
			self.player.Update(keystate)


	def addPlayer(self, player):
		self.players.add(player)
		self.player = player

	def setLevel(self, level):
		self.level = level


	def addObject(self, object):
		self.objects.add(object)

	def checkCollision(self, obj, newPos):
		return self.level.checkCollision(obj, newPos)