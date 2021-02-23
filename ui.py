import pygame
#used when rendering the complex buttons in menus
class uistate:
	def __init__(self):
		self.state = ""
		self.blur = 6
	def setState(self, state2):
		self.state = state2
	def setBlur(self, blur):
		self.blur = blur

class button():
	def __init__(self, text, x=0, y=0, w=0, h=0, activeColour=(153,0,0), defaultColour=(41,41,41)):
		self.text = text
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.activeColour = activeColour
		self.defaultColour = defaultColour
		self.colour = defaultColour

	def render(self, screen):
		mouseX, mouseY = pygame.mouse.get_pos()
		image = pygame.Surface([self.w, self.h])
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			self.colour = self.activeColour
			pygame.draw.rect(screen, self.defaultColour, (self.x-10,self.y-10,self.w+20,self.h+20))
		else:
			self.colour = self.defaultColour

			
		pygame.draw.rect(screen, self.colour, (self.x,self.y,self.w,self.h))
		buttonfont = pygame.font.Font(r"arial.ttf", 25)
		textSurf = buttonfont.render(self.text, 1, (255,255,255))
		textRect = textSurf.get_rect()
		textRect.center = ((self.x+(self.w/2)), (self.y+(self.h/2)))
		screen.blit(textSurf, textRect)
	
	def pressed(self,events):
		mouseX, mouseY = pygame.mouse.get_pos()
		if self.x + self.w > mouseX > self.x and self.y + self.h > mouseY > self.y:
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					return True




		
			

					






