#this level editor writes to the levels.pkl file if you want players to see these changes you must run your own instance of the server 
import pygame 
import os
import pickle 
import ui
pygame.init()
width = 1224
height = 840
screen = pygame.display.set_mode((width, height),pygame.SCALED,vsync = 1 )
messagefont = pygame.font.Font(r'arial.ttf', 20)
titlefont = pygame.font.Font(r'arial.ttf', 40)
objects = []
export = []
oldx = None
oldy = None
currentx = None
currenty = None
currentw = None
currenth = None
placed = False
specify = False
counter = 0
save = False
append = False
roomcounter= 0
state = "start"

def save():
	global objects
	global roomcounter
	export = []
	for y in objects:
		for x in y:
			x[0][0] -= 100
			x[0][1] -= 100
			x[2][2] -= 100
			x[2][3] -= 100
			if x[1][0] > 0 and x[1][1] > 0:
				export.append(x)
	pickle.dump(objects, open("levels.pkl","wb"))
	for y in objects:
		for x in y:
			x[0][0] += 100
			x[0][1] += 100
			x[2][2] += 100
			x[2][3] += 100

while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			os._exit(1)
	if state== "start":
		keys = pygame.key.get_pressed()
		screen.fill((128,128,128))
		pygame.draw.rect(screen, (153,0,0), (0,0,350,85))
		pygame.draw.rect(screen, (41,41,41), (0,0,320,70))
		char1 = titlefont.render("Editor", 1, (255,255,255))
		screen.blit(char1, (10, 10))
		startbutton1 = ui.button("Edit Levels", 612-500/2, 285, 500, 100)
		startbutton2 = ui.button("Create New Levels", 612-500/2, 485-50, 500, 100)
		startbutton1.render(screen)
		startbutton2.render(screen)

		if startbutton1.pressed(events):
			state = None
			with open('levels.pkl', 'rb') as fr:
				try:
					while True:
						objects.append(pickle.load(fr))
				except EOFError:
					pass
			objects = objects[0]
			if objects is not []:
				append = True
				for y in objects:
					for x in y:
						x[0][0] += 100
						x[0][1] += 100
						x[2][2] += 100
						x[2][3] += 100

		if startbutton2.pressed(events):
			new =[]
			pickle.dump(new, open("levels.pkl","wb"))	
			with open('levels.pkl', 'rb') as fr:
				try:
					while True:
						objects.append(pickle.load(fr))
				except EOFError:
					pass
			objects = objects[0]
			if objects is not []:
				append = True
				for y in objects:
					for x in y:
						x[0][0] += 100
						x[0][1] += 100
						x[2][2] += 100
						x[2][3] += 100
			state = None

		pygame.display.flip()

	else:
		save()
		pygame.mouse.set_visible(0)
		screen.fill((41,41,41))
		pygame.draw.rect(screen, (153,0,0), (0,0,350,85))
		pygame.draw.rect(screen, (41,41,41), (0,0,320,70))
		char1 = titlefont.render("Room: "+str(roomcounter+1)+"/"+str(len(objects)), 1, (255,255,255))
		screen.blit(char1, (10, 10))
		rect = pygame.Rect((100,100,1024,640))
		pygame.draw.rect(screen,(128,128,128),rect)
		if append == True:
			try:
				for x in objects[roomcounter]:
						rect = pygame.Rect((x[0][0],x[0][1],x[1][0],x[1][1]))
						try:
							if x[2][0] ==1:
								if x[2][1] == 3:
									pygame.draw.rect(screen,(204, 20, 20),rect)
								else:
									pygame.draw.rect(screen,(255, 0, 0),rect)
							elif x[2][0] ==2:
								if x[2][1] == 3:
									pygame.draw.rect(screen,(204, 20, 20),rect)
								else:
									pygame.draw.rect(screen,(255, 0, 0),rect)
							elif x[2][1] == 3:
								pygame.draw.rect(screen,(20, 219, 73),rect)
							else:
								pygame.draw.rect(screen,(60,60,60),rect)
						except:
							pygame.draw.rect(screen,(60,60,60),rect)
			except:
				objects.append([])
						
		mouseX, mouseY = pygame.mouse.get_pos()
		pygame.draw.line(screen, [255,255,255], (mouseX-10,mouseY), (mouseX+10,mouseY))
		pygame.draw.line(screen, [255,255,255], (mouseX,mouseY-10), (mouseX,mouseY+10))
		textSurf = messagefont.render("x: "+str(mouseX-100)+" y: "+str(mouseY-100), 1, (255,255,255))
		screen.blit(textSurf, (mouseX-60, mouseY-30))
		mouse_buttons = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_BACKSPACE] and counter > 10:
			placed = False
			if append == True:
				for hbox in objects[roomcounter]:
					if (hbox[0][0]) < (int(float(mouseX))) and hbox[0][0] + hbox[1][0] > int(float(mouseX)):
						if hbox[0][1] + hbox[1][1]> int(float(mouseY)) and hbox[0][1]< (int(float(mouseY))):
							if len(objects[roomcounter]) >= 1:
								if hbox[2][0] ==1:
									x = objects[roomcounter].index(hbox)

									objects[roomcounter].remove(hbox)
									objects[roomcounter].remove(objects[roomcounter][x])
								elif hbox[2][0] !=2:
									objects[roomcounter].remove(hbox)
								else:
									x = objects[roomcounter].index(hbox) -1
									objects[roomcounter].remove(hbox)
									objects[roomcounter].remove(objects[roomcounter][x])
						counter = 0

			if append == False:
				if len(objects) >= 1:
					objects.pop()
					counter = 0

		if keys[pygame.K_RIGHT] and counter > 10:
			placed = False
			if append == True:
				if roomcounter  <= len(objects)-2:
					roomcounter += 1
					counter = 0


		if keys[pygame.K_LEFT] and counter > 10:
			placed = False
			if append == True:
				if roomcounter - 1 >= 0:
					roomcounter -= 1
					counter = 0

		if keys[pygame.K_RETURN] and counter > 10:
			placed = False
			if append == True:
				roomcounter += 1
				counter = 0

		if keys[pygame.K_RSHIFT] and counter > 10:
			placed = False
			if append == True:
				if len(objects) -1 > 0:
					if roomcounter + 1 == len(objects):
						roomcounter -= 1
					objects.pop()
					counter = 0
		counter += 1

		if mouse_buttons[0] == True and specify == False:
			if append == True:
				if placed == False and counter > 10:
					objects[roomcounter].append([[mouseX,mouseY],[10,10],[0,0,0,0]])
					oldx = mouseX
					oldy = mouseY
					placed = True
					counter = 0
					
				if placed == True and counter > 10:
					placed = False
					counter = 0

		if mouse_buttons[2] == True and placed == True and counter > 10:
			if append == True:
				objects[roomcounter].append([[mouseX,mouseY],[10,10],[1,0,0,0]])
				placed = False
				specify = True
				counter = 0

		if  mouse_buttons[2] == True and specify == True and counter > 10:
				specify = False
				counter = 0

		if placed == True:
			if append == True:

				(objects[roomcounter][len(objects[roomcounter])-1])[1][0] = mouseX-oldx
				(objects[roomcounter][len(objects[roomcounter])-1])[1][1] = mouseY-oldy

		if specify == True:
			if append == True:
				(objects[roomcounter][len(objects[roomcounter])-1])[1][0] = mouseX-oldx
				(objects[roomcounter][len(objects[roomcounter])-1])[2][0] = 2
				(objects[roomcounter][len(objects[roomcounter])-1])[2][1] = 1
				(objects[roomcounter][len(objects[roomcounter])-2])[2][0] = 1
				(objects[roomcounter][len(objects[roomcounter])-2])[2][1] = 1
				(objects[roomcounter][len(objects[roomcounter])-2])[2][2] = oldx
				(objects[roomcounter][len(objects[roomcounter])-2])[2][3] = mouseX

		try:
			for hbox in objects[roomcounter]:
				if (hbox[0][0]) < (int(float(mouseX))) and hbox[0][0] + hbox[1][0] > int(float(mouseX)):
					if hbox[0][1] + hbox[1][1]> int(float(mouseY)) and hbox[0][1]< (int(float(mouseY))):
						if hbox[2][0] ==1:
							x = objects[roomcounter].index(hbox) +1
							hbox[2][1] = 3
							objects[roomcounter][x][2][1]=3
						elif hbox[2][0] ==2:			
							x = objects[roomcounter].index(hbox) -1
							hbox[2][1] = 3
							objects[roomcounter][x][2][1]=3					
						else:
							hbox[2][1] = 3
					else:
						if hbox[2][0] ==1:
							x = objects[roomcounter].index(hbox) +1
							hbox[2][1] = 0
							objects[roomcounter][x][2][1]=0
						elif hbox[2][0] ==2:				
							x = objects[roomcounter].index(hbox) -1
							hbox[2][1] = 1
							objects[roomcounter][x][2][1]=1
						else:
							hbox[2][1] = 0			
				else:
					if hbox[2][0] ==1:
						hbox[2][1] = 1
					else:
						hbox[2][1] = 0
		except:
			pass

		pygame.display.flip()
