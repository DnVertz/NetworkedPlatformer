import pygame
import numpy
import random
import bullet
#import uuid
import socket
class actor:
	def __init__(self, x=0, y=0, w=0, h=0, angle=0,hitboxes=0,index= 0,name = None,predict = False,room=0):
		self.hitboxes = hitboxes
		self.isjump = False
		self.predict = predict
		self.name = name
		self.x = x
		self.y = y
		self.vx = 0
		self.vy = 0
		self.bulletsize = 4
		self.w = w
		self.h = h
		self.angle = 0
		self.spread = 5
		self.index = index 
		self.id = 0
		self.room = 0
		self.ammo = 0
		self.maxammo = 10
		self.reloadtime = 50
		self.reloadprog = 0
		self.reloading = False
		self.all_bullets = []
		self.activeWeapon = 1
		self.ammo1 = 0
		self.ammo2 = 0
		self.ammo3 = 0
		self.shootimeout = 10
		self.weaontimeout = 10
		self.hitpoints = 100
		self.deaths = 0
		self.timer = 0
		numbs = []
		for word in self.index:
			if word.isdigit():
				numbs.append(int(word))
		number = (sum(numbs) / len(numbs))*40
		img_surface = pygame.image.load(r'playerm.png')
		
		img_array = pygame.surfarray.array3d(img_surface)         # Convert it into an 3D array
		colored_img = numpy.array(img_array)                      # Array thing
		colored_img[:, :, 0] = 10*number   # <-- Red
		colored_img[:, :, 1] = 20*number # <-- Green
		colored_img[:, :, 2] = 30*number    # <-- Blue
		img_surface = pygame.surfarray.make_surface(colored_img)
		self.image = img_surface
		self.image2 = pygame.image.load(r'mg.png')
		self.image2 = pygame.transform.scale(self.image2, (112, 37))

	def physicsHandler(self,timedelta):
		# gravity
		g = 1.38
		#wall collision
		if self.inBounds(self.x+self.vx*(timedelta/10), self.y) == False:
			self.x += self.vx*(timedelta/10)
		else:
			self.vx = 0
		#friction
		if self.vx is not 0 and self.vy == 0:
			self.vx *= 0.75
		elif self.vy is not 0:
			self.vx *= 0.95

		#gravity/falling/floor collisons
		if self.inBounds(self.x, self.y+g+self.vy) == False:
			self.vy += g
			self.y += self.vy 
		else:
			self.vy += g
			self.vy *= 0.25 *(timedelta/10)
			if self.inBounds(self.x,self.y+g+self.vy) == True:
				self.isjump = False
				self.vy = 0


		

	def inBounds(self, x, y):
			for hitbox in self.hitboxes:
					if (hitbox.x) < (x+self.w) and hitbox.x + hitbox.w > x:
						if hitbox.y + hitbox.h> y and hitbox.y < (y+self.h):
							return True	
			return False

	

	def setPos(self, x, y):

		self.x = x
		self.y = y

	def setRoom(self, room):

		self.room = room

	def setVx(self,x):
		if self.inBounds(self.x , self.y) == False:
			self.vx = x

	def setVy(self,y):
		if self.inBounds(self.x , self.y) == False:
			self.vy = y

	def jump(self):
		if self.inBounds(self.x, self.y) == False:
			if self.isjump == False and self.vy == 0:
				self.vy += -25
				self.isjump = True

	def moveUp(self):
		if self.inBounds(self.x, self.y) == False:
			if self.isjump == False and self.vy == 0:
				self.vy += -25
				self.isjump = True
				

	def moveLeft(self):
		if self.inBounds(self.x , self.y) == False:
			if self.vy == 0:
				self.vx -= 1.75
			else:
				self.vx -= 0.5



	def moveRight(self):
		if self.inBounds(self.x, self.y) == False:
			if self.vy == 0:
				self.vx += 1.75
			else:
				self.vx += 0.5



	def setAngle(self, Θ=0):
			self.angle = Θ


	def reload(self):
			self.ammo = 0
			self.reloadprog = 0
	def weapon_one(self):
			self.ammo = self.ammo1
			self.maxammo = 10
			self.spread = 5
			self.bulletsize = 4
			self.reloadtime = 50
			self.activeWeapon = 1
			self.weaontimeout = 10
			#self.image2 = pygame.image.load(r'mg.png')
			#self.image2 = pygame.transform.scale(self.image2, (112, 37))

	def weapon_two(self):
			self.ammo = self.ammo2
			self.maxammo = 5
			self.spread = 2
			self.bulletsize = 5
			self.reloadtime = 70
			self.activeWeapon = 2
			self.weaontimeout = 20
			


	def weapon_three(self):
			self.ammo = self.ammo3
			self.maxammo = 2
			self.spread = 2
			self.bulletsize = 10
			self.reloadtime = 30
			self.activeWeapon = 3
			self.weaontimeout = 2
			


	def reload(self):
			self.reloadprog = 0
			self.reloading = True
			

	def shoot(self,sock,server,clientid,deathtimeout):
		if deathtimeout > 100:
			if self.reloading == False and self.shootimeout > self.weaontimeout:
				self.shootimeout = 0
				SPEED = 20
				start = pygame.math.Vector2(self.x+(self.w/2),self.y+(self.h/2))
				mouse = pygame.mouse.get_pos()
				distance = mouse - start
				positions = pygame.math.Vector2(start) 
				aim = mouse - start
				speed = distance.normalize() * SPEED
				newbullet = bullet.bullet(positions,speed)
				newbullet.room = self.room
				newbullet.idd = clientid
				newbullet.size = self.bulletsize
				if self.ammo < self.maxammo:
					self.ammo += 1
					#self.all_bullets.append(newbullet)
					data2 = "joinbullet;"+str(newbullet.position.x)+";"+str(newbullet.position.y+random.randint(-int(self.spread),int(0)))+";"+str(newbullet.speed.x)+";"+str(newbullet.speed.y)+";"+str(newbullet.idd)+";"+str(newbullet.room)+";"+str(newbullet.size)+"\n"
					data2 = data2.encode('UTF-8')
					sock.sendto(data2,server)
			
		#return(all_bullets)

	def render(self, screen,clientid):
		if self.index == clientid:
			start = pygame.math.Vector2(self.x,self.y)
			mouse = pygame.mouse.get_pos() 
			aim = mouse - start
			angles = aim.angle_to(pygame.math.Vector2(1, 0))
			self.angle = int(angles)

		if self.reloading == True:
			self.reloadprog += 1

			if self.reloadprog > self.reloadtime:
				self.reloading = False
				self.ammo = 0


		if self.activeWeapon == 1:
			self.ammo1 = self.ammo
			self.image2 = pygame.image.load(r'mg.png')
			self.image2 = pygame.transform.scale(self.image2, (112, 37))


		if self.activeWeapon == 2:
			self.ammo2 = self.ammo
			self.image2 = pygame.image.load(r'rifle.png')
			self.image2 = pygame.transform.scale(self.image2, (112, 37))



		if self.activeWeapon == 3:
			self.ammo3 = self.ammo
			self.image2 = pygame.image.load(r'shotgun.png')
			self.image2 = pygame.transform.scale(self.image2, (112, 37))


		if self.shootimeout <= self.weaontimeout:
				self.shootimeout += 1

		buttonfont = pygame.font.Font(r"arial.ttf", 25)

		if abs(self.angle) > 90:
			gunrect = pygame.transform.flip(self.image2, False, True)
		else:
			gunrect = self.image2

		rects = pygame.Rect((self.x, self.y), (self.w, self.h))
		rects2 = pygame.Rect((self.x, self.y), (112, 37))
		rects3 = pygame.Rect((self.x-35, self.y-50), (100, 20))
		rects4 = pygame.Rect((self.x-35, self.y-50), (1*self.hitpoints, 20))
		rotated = pygame.transform.rotate(gunrect,self.angle)
		rotatedrect = rotated.get_rect(center=rects.center)
		textSurf = buttonfont.render(self.name, 1, (255,255,255))
		textRect = textSurf.get_rect()
		textRect.center = ((self.x+10, self.y-20))
		screen.blit(textSurf, textRect)

		screen.blit(self.image, rects)
		screen.blit(rotated, rotatedrect)
		pygame.draw.rect(screen,(255, 0, 0),rects3)
		pygame.draw.rect(screen,(0,255,0),rects4)
		

	def remove(self,position,speed):
		self.all_bullets.remove([position, speed])
