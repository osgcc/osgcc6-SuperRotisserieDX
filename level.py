
import pygame, os
from pygame.locals import *
from platform import *
from background import *
from enemy import *
from item import *
import copy
import math


class Level():

	def __init__(self, world):
		self.world = world
		platformpath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/OSGCC6/datafiles/level1.dat"
		f = open(platformpath)

		allLines = f.readlines()
		self.platforms = pygame.sprite.Group()
		self.drawGroup = pygame.sprite.Group() #which sprties are in view to draw
		self.movePlatforms = pygame.sprite.Group()
		self.bg1 = Background("background1.png", "background2.png")
		self.bg2 = Background("background_2-1.png", "background_2-2.png")
		self.fg = Background("foreground1.png", "foreground1.png")
		for i in range (1, len(allLines)):
			words = allLines[i].split(" ")

			plat = Platform([(int)(words[0]),(int)(words[1])],(int)(words[2]), (words[3]), (int)(words[4]))
			if plat.moveX or plat.moveY:
				self.movePlatforms.add(plat)
			else:
				self.platforms.add(plat)


		# Add enemies to level
		enemy_dat_path = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/OSGCC6/datafiles/enemy.dat"
		f = open(enemy_dat_path)

		allLines = f.readlines()
		self.enemies = pygame.sprite.Group()

		for i in range (1, len(allLines)):
			words = allLines[i].split(" ")
			x = (int)(words[0])
			y = (int)(words[1])
			height = (int)(words[2])
			width = (int)(words[3])
			enemType = (int)(words[4])
			enem = Enemy([x, y], self.world, pygame.time.Clock(), enemType)
			self.enemies.add(enem)	

		# Add items to level
		item_dat_path = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/OSGCC6/datafiles/item.dat"
		f = open(item_dat_path)

		allLines = f.readlines()
		self.items = pygame.sprite.Group()		

		for i in range (1, len(allLines)):
			words = allLines[i].split(" ")
			x = (int)(words[0])
			y = (int)(words[1])
			ite = Item([x, y], words[2], words[3], (int)(words[4]))
			self.items.add(ite)


	def Update(self):
		for sprite in self.enemies:
			sprite.Update()
		

	#check collisions with objects
	def checkCollision(self, obj, newPos):
		newrect = copy.deepcopy(obj.rect)
		newrect.center = newPos
		for platform in self.platforms:
			newPlat = copy.deepcopy(platform.rect)
			newPlat.center = platform.worldPos
			#print newrect.center
			if newrect.colliderect(newPlat):
				return platform
		return None

	#check collisions with items
	def checkItemCollision(self, obj, newPos):
		newrect = copy.deepcopy(obj.rect)
		newrect.center = newPos		
		for item in self.items:
			newItem = copy.deepcopy(item.rect)
			newItem.center = item.worldPos
			if newItem.colliderect(newrect):
				return item
		return None 


	#check collisions with enemy when shooting beans
	def checkCollisionEnemy(self, obj):
		for enemy in self.enemies:
			if enemy.rect.colliderect(obj.rect):
			#if newRec.colliderect(obj.rect):
				enemy.kill()
				return True
		return None

	def reieveCheckCollisionEnemy(self, player):
		playerrect = copy.deepcopy(player.rect)
		playerrect.center = player.worldPos
		for obj in self.world.enemyObjects:
			newrect = copy.deepcopy(obj.rect)
			newrect.center = obj.worldPos
			if newrect.colliderect(playerrect):
				obj.kill()
				return True
		return False

	#check collision between enemies and player (player may actually be enemy)
	def checkEnemyCollision(self, player, newPos):
		newrect = copy.deepcopy(player.rect)
		newrect.center = newPos		
		for enemy in self.enemies:
			if enemy == player:
				pass
			else:
				enemyrect = copy.deepcopy(enemy.rect)
				enemyrect.center = enemy.worldPos
				if enemyrect.colliderect(newrect):
					return enemy
		return None


	def checkCollisionMoving(self, obj, newPos):
		newrect = copy.deepcopy(obj.rect)
		newrect.center = newPos		
		for plat in self.movePlatforms:
			if plat == obj:
				pass
			else:
				enemyrect = copy.deepcopy(plat.rect)
				enemyrect.center = plat.worldPos
				if enemyrect.colliderect(newrect):
					return plat
		return None



	def Draw(self):
		currentPos = copy.deepcopy(self.world.player.worldPos) #players current worldPos
		self.bg1.Draw(self.world.screen)
		self.bg2.Draw(self.world.screen)
		self.drawGroup.empty()
		#screen = pygame.Rect((currentPos[0] - 800,currentPos[1] + 450),(800,450))
		for platform in self.movePlatforms:
			platform.updatePos()
			if (platform.worldPos[0] >= (currentPos[0] - 1600)) and (platform.worldPos[0] <= (currentPos[0] + 1600)):
				platform.rect.center = [800 -  (currentPos[0] - platform.worldPos[0]), 450  - (currentPos[1] - platform.worldPos[1])]	
			self.drawGroup.add(platform)		
		for platform in self.platforms:
			if platform.gravyVent:
				platform.updatePos()
			if (platform.worldPos[0] >= (currentPos[0] - 1600)) and (platform.worldPos[0] <= (currentPos[0] + 1600)):
				platform.rect.center = [800 -  (currentPos[0] - platform.worldPos[0]), 450  - (currentPos[1] - platform.worldPos[1])]
				#print platform.rect.center[1]
				#print platform.rect.center
				self.drawGroup.add(platform)
		for obj in self.world.objects:
			if (obj.worldPos[0] >= (currentPos[0] - 2000)) and (obj.worldPos[0] <= (currentPos[0] + 2000)):
				obj.rect.center = [800 -  (currentPos[0] - obj.worldPos[0]), 450  - (currentPos[1] - obj.worldPos[1])]	
				self.drawGroup.add(obj)		
		for obj in self.enemies:
			if (obj.worldPos[0] >= (currentPos[0] - 2000)) and (obj.worldPos[0] <= (currentPos[0] + 2000)):
				obj.rect.center = [800 -  (currentPos[0] - obj.worldPos[0]), 450  - (currentPos[1] - obj.worldPos[1])]	
				self.drawGroup.add(obj)	
		for obj in self.items:
			if (obj.worldPos[0] >= (currentPos[0] - 2000)) and (obj.worldPos[0] <= (currentPos[0] + 2000)):
				obj.rect.center = [800 -  (currentPos[0] - obj.worldPos[0]), 450  - (currentPos[1] - obj.worldPos[1])]	
				self.drawGroup.add(obj)
		for obj in self.world.enemyObjects:
			if (obj.worldPos[0] >= (currentPos[0] - 2000)) and (obj.worldPos[0] <= (currentPos[0] + 2000)):
				obj.rect.center = [800 -  (currentPos[0] - obj.worldPos[0]), 450  - (currentPos[1] - obj.worldPos[1])]	
				self.drawGroup.add(obj)		

		self.drawGroup.draw(self.world.screen)

	