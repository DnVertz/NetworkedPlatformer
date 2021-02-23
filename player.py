
import pygame
class player:
	def __init__(self, x=0, y=0, w=0, h=0, Θ=0,hitboxes=0):
		self.hitboxes = hitboxes
		self.isjump = False
		self.x = x
		self.y = y
		self.vx = 0
		self.vy = 0
		self.w = w
		self.h = h
		self.Θ = Θ

	def physicsHandler(self):

		# gravity
		g = 2
		#friction
		if self.vx is not 0:
			self.vx *= 0.90

		#gravity/falling/floor collisons
		if self.inBounds(self.x, self.y+g+self.vy) == False:
			self.vy += g
			self.y += self.vy
		else:
			self.vy += g
			self.vy *= 0.25
			if self.inBounds(self.x,self.y+g+self.vy) == True:
				self.isjump = False
				self.vy = 0

			self.y += self.vy 
				

		#wall collision
		if self.inBounds(self.x+self.vx, self.y) == False:
			self.x += self.vx
		else:
			self.vx = 0

		
	def inBounds(self, x, y):
			for hitbox in self.hitboxes:
				if (hitbox.x) < (x+self.w) and hitbox.x + hitbox.w > x:
					if hitbox.y + hitbox.h> y and hitbox.y < (y+self.h):
						return True	
			return False


	def render(self, screen):
		rects = pygame.Rect((self.x, self.y), (self.w, self.h))
		#rotated = pygame.transform.rotate(pygame.image.load(r'playerm.png') ,self.Θ)
		pygame.draw.rect(screen,(255,255,255),rects)
		"""

		rect = pygame.Rect((self.x, self.y), (self.w, self.h))
		#rotated = pygame.transform.rotate(pygame.image.load(r'playerm.png') ,self.Θ)
		rotated = pygame.transform.rotate( self.image,0)
		rotatedrect = rotated.get_rect(center=rect.center)
		#screen.blit(rotated, rotatedrect)
		screen.blit(rotated, rotatedrect)"""


	def setPos(self, x, y):
		self.x = x
		self.y = y

	def moveUp(self):
		if self.inBounds(self.x, self.y) == False:
			if self.isjump == False and self.vy == 0:
				self.vy += -25
				self.isjump = True
				

	def moveLeft(self):
		if self.inBounds(self.x , self.y) == False:
			self.vx -= 1.5


	def moveRight(self):
		if self.inBounds(self.x, self.y) == False:
			self.vx += 1.5


	def setAngle(self, Θ=0):
			self.Θ = Θ
	
	