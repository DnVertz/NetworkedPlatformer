#idea load hitbox data into server handle it like clients and transmit the telemtry for the hitbox positions to the clients
import pygame 
import os
import pickle 
pygame.init()
width = 1224
height = 840
screen = pygame.display.set_mode((width, height),pygame.SCALED,vsync = 1 )
messagefont = pygame.font.Font(r'arial.ttf', 20)
objects = []
export = [[[0,0],[0,640]],[[1024,0],[1024,640]],[[0,640],[1024,640]],[[0,0],[1024,0]]]
oldx = None
oldy = None
currentx = None
currenty = None
currentw = None
currenth = None
placed = False
specify = False
counter = 0
roomcounter= 0
while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			os._exit(1)
	pygame.mouse.set_visible(0)
	screen.fill((0,0,0))
	rect = pygame.Rect((100,100,1024,640))
	pygame.draw.rect(screen,(128,128,128),rect)
	for x in objects:
		rect = pygame.Rect((x[0][0],x[0][1],x[1][0],x[1][1]))
		#rect.normalize()
		if x[2][0] == 1:
			
			#rect2 = pygame.Rect((x[0][0],x[0][1],x[2][3]+x[0][0],10))
			#pygame.draw.rect(screen,(255,0,0),rect2)
			pygame.draw.rect(screen,(255,0,0),rect)
		else:
			pygame.draw.rect(screen,(60,60,60),rect)

	
	
	mouseX, mouseY = pygame.mouse.get_pos()
	pygame.draw.line(screen, [255,255,255], (mouseX-10,mouseY), (mouseX+10,mouseY))
	pygame.draw.line(screen, [255,255,255], (mouseX,mouseY-10), (mouseX,mouseY+10))
	textSurf = messagefont.render("x: "+str(mouseX-100)+" y: "+str(mouseY-100), 1, (255,255,255))
	screen.blit(textSurf, (mouseX-60, mouseY-30))
	mouse_buttons = pygame.mouse.get_pressed()
	keys = pygame.key.get_pressed()
	if keys[pygame.K_BACKSPACE] and counter > 10:
		if len(objects) >= 1:
			placed = False
			objects.pop()
			counter = 0

	if keys[pygame.K_RETURN] and counter > 10 and placed == False:
		if roomcounter == 0:

			for x in objects:
				x[0][0] -= 100
				x[0][1] -= 100
				x[2][2] -= 100
				x[2][3] -= 100
				if x[1][0] > 0 and x[1][1] > 0:
					export.append(x)
			pickle.dump(export, open("levels.pkl","wb"))
			roomcounter += 1
		else:

			for x in objects:
				x[0][0] -= 100
				x[0][1] -= 100
				x[2][2] -= 100
				x[2][3] -= 100
				if x[1][0] > 0 and x[1][1] > 0:
					export.append(x)
			pickle.dump(export, open("levels.pkl","ab"))
			roomcounter += 1
		objects = []
		export = [[[0,0],[0,640]],[[1024,0],[1024,640]],[[0,640],[1024,640]],[[0,0],[1024,0]]]
		counter = 0




	counter += 1

	if mouse_buttons[0] == True and specify == False:
		

		if placed == False and counter > 10:
			objects.append([[mouseX,mouseY],[10,10],[0,0,0,0]])
			oldx = mouseX
			oldy = mouseY
			placed = True
			counter = 0

		if placed == True and counter > 10:
			placed = False
			counter = 0

		

	if mouse_buttons[2] == True and placed == True and counter > 10:
		objects.append([[mouseX,mouseY],[10,10],[1,0,0,0]])
		placed = False
		specify = True
		counter = 0

	if  mouse_buttons[2] == True and specify == True and counter > 10:
			specify = False
			objects.pop()
			counter = 0




	if placed == True:

		(objects[len(objects)-1])[1][0] = mouseX-oldx
		(objects[len(objects)-1])[1][1] = mouseY-oldy

	if specify == True:
		
		(objects[len(objects)-1])[1][0] = mouseX-oldx
		(objects[len(objects)-2])[2][0] = 1
		(objects[len(objects)-2])[2][1] = 1
		(objects[len(objects)-2])[2][2] = oldx
		(objects[len(objects)-2])[2][3] = mouseX

	



	pygame.display.flip()
