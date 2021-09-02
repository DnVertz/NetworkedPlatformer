from threading import Thread
import pygame 
#importing packages/seperate files
import ui
import menu
import inputs
import hitboxes
import actor
import random
import socket
import os
import signal
import sys
import bullet
import createrooms
import pygame.freetype
all_bullets = []

#defining variables
HOST = None
PORT = None
lockout = False
kicked = False
state = ui.uistate()
width = 1024
height = 640
quitol = False
clientid = 1
deathtimeout = 0
regen = 0
servertick = 0
tickreverse = "False"
title = "Platformer"
player1 = None
predict = False
msgbox = False
tabmenu = False
name = None
msgtimeout = 0
deathmsgtimeout = 0
counter = 0
limit = 3
controldisp = True

#setting the screen parameters its important to have vsync as it appears choppy otherwise

screen = pygame.display.set_mode((width, height),pygame.SCALED,vsync = 1 )


hitbox = []#loads the hitboxes
multiplays = []#stores the actor class of the players within the game hence multiplays
messages = []#this stores the messages of when someone sends something
deathmessages = []

state.state = "start"
pygame.init()

titlefont = pygame.font.Font(r'arial.ttf', 40)
titlefont2 = pygame.font.Font(r'arial.ttf', 30)
messagefont = pygame.font.Font(r'arial.ttf', 20)#loading the fonts here because it slows down the program
controls = pygame.image.load(r'controls.png')


while True:
	#this while loop establishes the connection between client and server while also checking if the entered information is correct
	if quitol == True:
		break
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			os._exit(1)

	if state.state == "start":
		screen.fill((128,128,128))
		start = menu.drawStart(screen, titlefont, state,events,title)
		if start is not None:
			connec = start
			state.state = "joincheck"
	else:
		try: 
			sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
			server_address = (str(connec[0]), int(connec[1]))
			name = str(connec[2])

			if not connec[2]:
				title = "Choose a name"
				state.state = "start"

			else:
				msgs = str("join;"+name+"\n")
				byte = msgs.encode()
				sock.sendto(byte,server_address)
				sock.settimeout(0.5)
				initdata2,addr = sock.recvfrom(4096)
				initdata2 = initdata2.decode('UTF-8')
				split = initdata2.split(";")

				if split[0] == "True":

					rooms = createrooms.create(split[1])
						


					break
				else:
					title = "Name in use!!!!"
					state.state = "start"

		except:
			title = "Wrong IP/Port!!!!"
			state.state = "start"

	pygame.display.flip()


#after the loop breaks we finish up the connection 
sock.settimeout(None)
initdata,addr = sock.recvfrom(4096)

initdata = initdata.decode('UTF-8')
split = initdata.split("\n") #recieving our data from the server(the UUID generated for us)
for p in split:
	split2 = p.split(";")
	if split2[0] == "init":
		clientid = split2[1]
		multiplays.append(actor.actor(float(split2[2]), float(split2[3]),25 ,50 ,0,hitbox,split2[1],split2[4]))
		player1 = actor.actor(float(split2[2]), float(split2[3]),25 ,50 ,0,hitbox,split2[1],split2[4])



clock = pygame.time.Clock() 
FPS = 60
fps = clock.tick(FPS)

def networkthread(clientid):
	#this thread handles receiving of packets, the large amount of globals is so that both threads can communicate 
	global predict
	global messages
	global msgtimeout
	global kicked
	global player1
	global servertick
	global tickreverse
	global state

	while True:
		try:
			data,addr2 = sock.recvfrom(4096)
		except:
			break

		data = data.decode('UTF-8')
		split = data.split("\n")

		for p in split:
			split2 = p.split(";")

			if split2[0] == "spawn":

				if split2[1] is not clientid:
					multiplays.append(actor.actor(float(split2[2]), float(split2[3]),25 ,50 ,0,hitbox,split2[1],split2[4]))

			if split2[0] == "join":
				if split2[1] is not clientid:
					multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))

			if split2[0] == "pos":
					for x in multiplays:

						if x.index == split2[1]:
							if clientid != split2[1]:
								x.setPos(float(split2[2]),float(split2[3]))
								x.setRoom(split2[4])
								if len(split2) > 5:
									x.activeWeapon = int(split2[5])
									x.angle = int(split2[6])
									x.hitpoints = int(split2[7])
									x.deaths = split2[8]
									x.timer =split2[9] 
									x.win = split2[10] 
									if x.win == "True":
										state.state = "end"

					if clientid == split2[1]:
						player1.deaths = split2[8]
						player1.timer =split2[9]


			if split2[0] == "leave":

				if split2[1] == clientid:
					os._exit(1)
				for x in multiplays:
					if x.index == split2[1]:
						multiplays.remove(x)
						messages.append(x.name +" has left")

			if split2[0] == "tick":
				#print(split2)
				servertick = int(split2[1])
				tickreverse = split2[2]

			if split2[0] == "msg":
				messages.append(split2[1]+": "+split2[2])
				msgtimeout = 0

			if split2[0] == "bspawn":
				newbul = bullet.bullet(pygame.math.Vector2(int(float(split2[1])),int(float(split2[2]))),pygame.math.Vector2(int(float(split2[3])),int(float(split2[4]))))
				newbul.idd = split2[5]
				newbul.room = split2[6]
				newbul.size = split2[7]
				player1.all_bullets.append(newbul)

			if split2[0] == "die":
				messages.append(split2[1] +" has died")
				msgtimeout = 0

			if split2[0] == "killed":
				names = None
				found = False
				i = 1
				length = len(multiplays)
				while found is False:
					if multiplays[i].index == split2[2]:
						found = True
						
					else:
						i += 1
				
				names = multiplays[i].name
				messages.append(names +" has killed "+split2[1])
				msgtimeout = 0

	os._exit(1)

thr = Thread(target = networkthread,args =(str(clientid),))
thr.start()

def signal_handler(sig, frame):
	#this handles the safe quit of a client eg: ctrl+c in that case the leave packet is still sent
	data2 = "leave;"+str(clientid)+"\n"
	data2 = data2.encode('UTF-8')
	sock.sendto(data2,server_address)
	os._exit(1)

def roomcheck(player1):
	#this checks whether or not the player has reached the end of a room
	global rooms
	global lockout
	if player1.x > 995:
		if player1.room < len(rooms)-1:
			player1.room += 1
			player1.x = 4
			player1.y = 0
			lockout = True
			player1.vx = 0
			deathtimeout = 0

		else:
			player1.win = True
			
	elif player1.x < 3:
		if player1.room > 0:
			player1.room -= 1
			player1.x = 993
			player1.y = 0
			lockout = True
			player1.vx = 0
			deathtimeout = 0

	if player1.y > 560:
		player1.room = 0
		player1.x = 4
		player1.y = 0
		lockout = True
		player1.vx = 0
		player1.hitpoints = 100
		data2 = "die;"+str(player1.name)+";"+str(clientid)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)

while True:
	#this is the main thread which handles the transmission of packets + all game logic

	deathtimeout += 1 #this is invincibility for when u spawn after dying
	signal.signal(signal.SIGINT, signal_handler)
	roomcheck(player1)
	screen.fill((128,128,128))
	timer = int(player1.timer)/120
	if player1.reloading == True: #displays "reloading" when you reload
		lenofmsg2 = titlefont2.size("Reloading")
		char2 = titlefont2.render("Reloading", 1, (255,255,255))
		screen.blit(char2, (315+lenofmsg2[0], 320))


	hitbox = []




	for y in rooms: #this handles the syncing of moving objects between clients based off of the server tick
		for continuity in y:
			if continuity.move != 0:
				if tickreverse == "False":
					continuity.x = continuity.upper - (int(((continuity.upper - continuity.lower)/1000)*servertick))

				else:
					continuity.x = continuity.lower + (int(((continuity.upper - continuity.lower)/1000)*servertick))

	
	
	for hbox in rooms[player1.room]: #handles hitboxes of when you enter a new room
		hitbox.append(hitboxes.hitboxes(hbox.x,hbox.y,hbox.w,hbox.h,hbox.move))
		rect = pygame.Rect(hbox.x,hbox.y,hbox.w,hbox.h)
		rect.normalize()
		pygame.draw.rect(screen,(60,60,60),rect)


	if player1.all_bullets is not None:
		#Check if bullets have collided with objects or players
		for z in player1.all_bullets :
			z.position += z.speed
			pos_x = int(z.position.x)
			pos_y = int(z.position.y)

			if int(z.room) == player1.room:
				pygame.draw.circle(screen, (255,255,255), (pos_x, pos_y),int(z.size))

			if (player1.x) < (pos_x+10) and player1.x + player1.w > pos_x:
				if player1.y + player1.h > pos_y and player1.y < (pos_y+10):
					if str(z.idd) != str(clientid):
						if int(z.room) == player1.room:
							if deathtimeout > 100:
								#send bullet id to server 
								player1.hitpoints -= int(z.size)*2
								regen = 0
								if player1.hitpoints <= 0:
	
									player1.room = 0
									player1.x = 4
									player1.y = 0
									player1.hitpoints = 100
									lockout = True

									player1.vx = 0
									data2 = "killed;"+str(player1.name)+";"+str(z.idd)+"\n"
									data2 = data2.encode('UTF-8')
									sock.sendto(data2,server_address)
									deathtimeout = 0

			for hbox in hitbox:
				if (hbox.x) < (int(float(z.position.x))) and hbox.x + hbox.w +10 > int(float(z.position.x)):
					if hbox.y + hbox.h+10> int(float(z.position.y)) and hbox.y< (int(float(z.position.y))) :
						if z in player1.all_bullets:
							player1.all_bullets.remove(z)

	player1.hitboxes = hitbox
	if quitol == True:#same thing as the safe quit earlier however this is for when you press the red X
		data2 = "leave;"+str(clientid)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		break

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			quitol = True
	
	for hitbox in hitbox:
		#if you get stuck inside a hitbox its coded to kill you here 
		if hitbox.move != 0:
			if (hitbox.x+5) < (player1.x+player1.w) and hitbox.x-5 + hitbox.w > player1.x:
				if hitbox.y + hitbox.h> player1.y and hitbox.y < (player1.y+player1.h):
					#player1.x += hitbox.move*2
					player1.room = 0
					player1.x = 4
					player1.y = 0
					lockout = True

					player1.vx = 0
					player1.hitpoints = 100

					data2 = "die;"+str(player1.name)+"\n"
					data2 = data2.encode('UTF-8')
					sock.sendto(data2,server_address)

	if player1 is not None:
		#send your position data to the server
		player1.physicsHandler(fps)
		data2 = "pos;"+str(clientid)+";"+str(player1.x)+";"+str(player1.y)+";"+str(int(player1.room))+";"+str(int(player1.activeWeapon))+";"+str(int(player1.angle))+";"+str(int(player1.hitpoints))+";"+str(player1.win)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		#handle the messages so it doesnt over flow
		if len(messages) > 0:
			msgtimeout += 1

		if len(messages) == 7 or (msgtimeout > 350 and len(messages)>0):
			msgtimeout = 0
			messages.remove(messages[0])

		player1.render(screen,clientid)
		
		mouseX, mouseY = pygame.mouse.get_pos()
		

		if player1.hitpoints < 100: #health regen
			regen += 1
			if regen > 175:
				if player1.hitpoints + 10 > 100:
					player1.hitpoints = 100
				else:
					player1.hitpoints += 10
				regen = 0


		for p in multiplays:
			if p.index != clientid:
				
				if int(p.room) == int(player1.room):
					p.render(screen,clientid)#rendering players only if they are in your room

		for i in range(len(messages)):
			amount = messagefont.size(messages[i]) #more message handling 
			lst = messages[i].split()
			lst2 = list(lst[0])

			if ":" not in lst2:
				if len(lst) <= 3:

					message = lst[0]+" "+lst[1]+" "
					message2 = lst[2]
				else:
					message = lst[0]+" "+lst[1]+" "+lst[2]
					message2 = " "+lst[3]

				
				font = pygame.freetype.Font(None, 50)
				amount2 = messagefont.size(message)
				
				textSurf = messagefont.render(message, 1, (255,255,255))
				textRect = pygame.Rect(0+5,i*40, amount[0], amount[1])
				textSurf2 = messagefont.render(message2, 1, (255,0,0) )
				textRect2 = pygame.Rect((0+5+amount2[0]),i*40, amount[0], amount[1])
				screen.blit(textSurf, textRect)
				screen.blit(textSurf2, textRect2)


			else:
				textSurf = messagefont.render(messages[i], 1, (255,255,255))
				textRect = pygame.Rect(0+5,i*40, amount[0], amount[1])
				screen.blit(textSurf, textRect)

		if msgbox == True:
			#handling the message box 
			start = menu.drawMessage(screen, state,events,title)
			if start != None and start != '' and start != ' ':
				connec = start
				data2 = "msg;"+str(connec)+";"+str(name)+"\n"
				data2 = data2.encode('UTF-8')
				sock.sendto(data2,server_address)

		if tabmenu == True:
			#handling the tab menu
			counter += 1
			for event in events:
				if event.type == pygame.KEYDOWN:
					keys2 = pygame.key.get_pressed()
					if keys2[pygame.K_RIGHT] and counter > 10 and len(multiplays)> limit:
						limit += 3
						counter = 0

					if keys2[pygame.K_LEFT] and counter > 10 and 3 < limit:
						limit -= 3
						counter = 0





			
			rect = pygame.Rect(512-275,320-137.5,550,275)
			pygame.draw.rect(screen,(153,0,0),rect)
			rect = pygame.Rect(512-250,320-125,500,250)
			pygame.draw.rect(screen,(60,60,60),rect)
			offset = 0
			throwaway = list()

			for u in range(limit-3,limit):
				try:
					i = multiplays[u]
					#num = multiplays.index(i)
					throwaway.append(i)
				except:
					break

			
			for x in throwaway:
				#iterating through the list in groups of 3 to be displayed in the tab menu
				
				if x.index == clientid:

					message = "(You)Name: "+ str(x.name)+" Room:"+str(int(player1.room)+1)+" Time: "+str(round(int(player1.timer)/120,2))
					textSurf = messagefont.render(message , 1, (255,255,255))
					textRect = pygame.Rect(512-250,320-125, 500, 20)
					screen.blit(textSurf, textRect)

				else:
					offset += 1
					message = "Name: "+ str(x.name)+" Room: "+str(int(x.room)+1)+" Time: "+str(round(int(x.timer)/120,2))
					textSurf = messagefont.render(message , 1, (255,255,255))
					textRect = pygame.Rect(512-250,320-125+offset*40, 500, 20)
					screen.blit(textSurf, textRect)

				

		x = None
		if lockout == False and controldisp == False:
			x = inputs.run(state,player1,events,msgbox,sock,server_address,clientid,deathtimeout,tabmenu)
			#handling the inputs

		if lockout == True:
			if player1.vy == 0:
				lockout = False

		if x == "RETURN": #pygames keypress event will constantly flip values, this prevents it
			if msgbox == True:
				msgbox = False 
			else:
				msgbox = True
		if x == "TAB": 
			if tabmenu == True:
				tabmenu = False
			else:
				tabmenu = True

		pygame.draw.line(screen, [0,0,0], (mouseX-10,mouseY), (mouseX+10,mouseY))
		pygame.draw.line(screen, [0,0,0], (mouseX,mouseY-10), (mouseX,mouseY+10)) #crosshair


		if controldisp == True: #control menu
			screen.blit(controls, (0, 0))
			pygame.draw.rect(screen, (153,0,0), (0,0,350,85))
			pygame.draw.rect(screen, (41,41,41), (0,0,320,70))
			char1 = titlefont.render("Controls", 1, (255,255,255))
			screen.blit(char1, (10, 10))
			startbutton1 = ui.button("Continue", 620, 555, 300, 75)
			startbutton1.render(screen)
			if startbutton1.pressed(events):
				msgs = str("start;"+player1.name+"\n")
				byte = msgs.encode()
				sock.sendto(byte,server_address)
				controldisp = False
		else: #jank solution
			pygame.mouse.set_visible(0)
				

		roomsg = "Room: "+str(player1.room +1)
		lenofmsg = titlefont2.size(roomsg)
		roomsg2 = "Ammo: "+str(int(player1.maxammo-player1.ammo))
		lenofmsg3 = titlefont2.size(roomsg2)
		char1 = titlefont2.render("Room: "+str(player1.room +1), 1, (255,255,255))
		screen.blit(char1, (1024-lenofmsg[0] , 10))
		char3 = titlefont2.render((roomsg2), 1, (255,255,255))
		screen.blit(char3, (1020-lenofmsg3[0] , 50))
		if state.state == "end" or player1.win == True:
			winner = player1
			pygame.mouse.set_visible(1)
			if player1.win == "False" or player1.win == False:
				for x in multiplays:
					if x.win == "True":
						winner = x

			keys = pygame.key.get_pressed()
			screen.fill((128,128,128))
			pygame.draw.rect(screen, (153,0,0), (0,0,350,85))
			pygame.draw.rect(screen, (41,41,41), (0,0,320,70))
			
			rect = pygame.Rect(370,185, 300, 75)
			char2 = titlefont2.render(str(winner.name)+" has won ", 1, (255,255,255))
			char3 = titlefont2.render("In: "+str(round(int(winner.timer)/120,2))+" Secs", 1, (255,255,255))
			
			pygame.draw.rect(screen,(60,60,60),rect)
			screen.blit(char2, (370,185))
			screen.blit(char3, (370,225))
			char1 = titlefont.render("The End", 1, (255,255,255))
			screen.blit(char1, (10, 10))
			
			startbutton1 = ui.button("Exit", 370, 285, 300, 75)
			startbutton1.render(screen)
			if startbutton1.pressed(events):
				os._exit(1)



		pygame.display.flip()
sock.close()
