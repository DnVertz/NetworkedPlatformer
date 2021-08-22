from threading import Thread
import pygame 
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


title = "Platformer"
player1 = None
predict = False
msgbox = False
name = None
msgtimeout = 0
deathmsgtimeout = 0

screen = pygame.display.set_mode((width, height),pygame.SCALED,vsync = 1 )


hitbox = []#loads the hitboxes
rooms = createrooms.create()

#stores the level hitboxes... can and will be changed into a text file

multiplays = []#stores the actor class
messages = []
deathmessages = []

#for x in coll:
	#hitbox.append(hitboxes.hitboxes(x[0][0],x[0][1],x[1][0],x[1][1]))

state.state = "start"
pygame.init()

titlefont = pygame.font.Font(r'arial.ttf', 40)
titlefont2 = pygame.font.Font(r'arial.ttf', 30)
messagefont = pygame.font.Font(r'arial.ttf', 20)

while True:
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

				if initdata2 == "True":
					break
				else:
					title = "Name in use!!!!"
					state.state = "start"

		except:
			title = "Wrong IP/Port!!!!"
			state.state = "start"

	pygame.display.flip()


sock.settimeout(None)
initdata,addr = sock.recvfrom(4096)

initdata = initdata.decode('UTF-8')
split = initdata.split("\n")
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
	global predict
	global messages
	global msgtimeout
	global kicked
	global player1
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
							x.setPos(float(split2[2]),float(split2[3]))
				
							x.setRoom(split2[4])
							if len(split2) > 5:
								x.activeWeapon = int(split2[5])
								x.angle = int(split2[6])
								x.hitpoints = int(split2[7])

			if split2[0] == "leave":

				if split2[1] == clientid:
					os._exit(1)
				for x in multiplays:
					if x.index == split2[1]:
						multiplays.remove(x)

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

				for p in multiplays:

					if str(p.index) == str(split2[2]):
						names = p.name


				messages.append(names +" has killed "+split2[1])
				msgtimeout = 0

	os._exit(1)

thr = Thread(target = networkthread,args =(str(clientid),))
thr.start()

def signal_handler(sig, frame):

	data2 = "leave;"+str(clientid)+"\n"
	data2 = data2.encode('UTF-8')
	sock.sendto(data2,server_address)
	os._exit(1)

def roomcheck(player1):

	global lockout
	if player1.x > 995:
		if player1.room < 1:
			player1.room += 1
			player1.x = 4
			player1.y = 0
			lockout = True
			print(lockout)
			player1.vx = 0
			deathtimeout = 0
			
	elif player1.x < 3:
		if player1.room > 0:
			player1.room -= 1
			player1.x = 993
			player1.y = 0
			lockout = True
			print(lockout)
			player1.vx = 0
			deathtimeout = 0

	if player1.y > 560:
		player1.room = 0
		player1.x = 4
		player1.y = 0
		lockout = True
		print(lockout)
		player1.vx = 0
		player1.hitpoints = 100

		data2 = "die;"+str(player1.name)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)

while True:

	deathtimeout += 1

	signal.signal(signal.SIGINT, signal_handler)
	roomcheck(player1)

	screen.fill((128,128,128))
	roomsg = "Room: "+str(player1.room +1)
	lenofmsg = titlefont2.size(roomsg)
	roomsg2 = "Ammo: "+str(int(player1.maxammo-player1.ammo))
	lenofmsg3 = titlefont2.size(roomsg2)


	
						

	char1 = titlefont2.render("Room: "+str(player1.room +1), 1, (255,255,255))
	screen.blit(char1, (1024-lenofmsg[0] , 10))
	char3 = titlefont2.render((roomsg2), 1, (255,255,255))
	screen.blit(char3, (1020-lenofmsg3[0] , 50))



	if player1.reloading == True:
		lenofmsg2 = titlefont2.size("Reloading")
		char2 = titlefont2.render("Reloading", 1, (255,255,255))
		screen.blit(char2, (315+lenofmsg2[0], 320))

	hitbox = []

	for x in rooms:
		for continuity in x:
			if continuity.move is not None:
				if continuity.upper > continuity.lower:
					continuity.x += continuity.move
					if continuity.x > continuity.upper:
						continuity.move = -continuity.move
					elif continuity.x < continuity.lower:
						continuity.move = -continuity.move
				else:
					continuity.x += continuity.move
					if continuity.x < continuity.upper:
						continuity.move = -continuity.move
					elif continuity.x > continuity.lower:
						continuity.move = -continuity.move

	for hbox in rooms[player1.room]:
		hitbox.append(hitboxes.hitboxes(hbox.x,hbox.y,hbox.w,hbox.h,hbox.move))
		#pygame.draw.rect(screen,(60,60,60),(hbox.x,hbox.y,hbox.w,hbox.h))
		rect = pygame.Rect(hbox.x,hbox.y,hbox.w,hbox.h)
		rect.normalize()
		pygame.draw.rect(screen,(60,60,60),rect)

	print(hitbox)
	if player1.all_bullets is not None:
		#Check if bullets have collided 
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

	if quitol == True:
		data2 = "leave;"+str(clientid)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		break
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			quitol = True
	
			

	for hitbox in hitbox:
		if hitbox.move is not 0:
			if (hitbox.x+5) < (player1.x+player1.w) and hitbox.x-5 + hitbox.w > player1.x:
				if hitbox.y + hitbox.h> player1.y and hitbox.y < (player1.y+player1.h):
					#player1.x += hitbox.move*2
					player1.room = 0
					player1.x = 4
					player1.y = 0
					lockout = True
					print(lockout)
					player1.vx = 0
					player1.hitpoints = 100

					data2 = "die;"+str(player1.name)+"\n"
					data2 = data2.encode('UTF-8')
					sock.sendto(data2,server_address)



	
	if player1 is not None:

		player1.physicsHandler(fps)
		data2 = "pos;"+str(clientid)+";"+str(player1.x)+";"+str(player1.y)+";"+str(int(player1.room))+";"+str(int(player1.activeWeapon))+";"+str(int(player1.angle))+";"+str(int(player1.hitpoints))+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		if len(messages) > 0:
			msgtimeout += 1

		if len(messages) == 7 or (msgtimeout > 350 and len(messages)>0):
			msgtimeout = 0
			messages.remove(messages[0])


		


		player1.render(screen,clientid)
		pygame.mouse.set_visible(0)
		mouseX, mouseY = pygame.mouse.get_pos()
		pygame.draw.line(screen, [0,0,0], (mouseX-10,mouseY), (mouseX+10,mouseY))
		pygame.draw.line(screen, [0,0,0], (mouseX,mouseY-10), (mouseX,mouseY+10))
		textSurf = messagefont.render("x: "+str(mouseX)+" y: "+str(mouseY), 1, (255,255,255))
		screen.blit(textSurf, (mouseX-20, mouseY-20))

		if player1.hitpoints < 100:
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
					p.render(screen,clientid)

		for i in range(len(messages)):
			amount = messagefont.size(messages[i])
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
				#textRect.center = (((100/2)), (60+(60/2)+i*40))
				#textRect.center = (0+amount[0],0+amount[1]+i*40)
				screen.blit(textSurf, textRect)

				


		if msgbox == True:
			start = menu.drawMessage(screen, state,events,title)
			if start != None and start != '' and start != ' ':
				connec = start
				data2 = "msg;"+str(connec)+";"+str(name)+"\n"
				data2 = data2.encode('UTF-8')
				sock.sendto(data2,server_address)

		#if kicked == True:
		if lockout == False:
			x = inputs.run(state,player1,events,msgbox,sock,server_address,clientid,deathtimeout)

		if lockout == True:
			if player1.vy == 0:
				lockout = False
		if x == True:
			if msgbox == True:
				msgbox = False 
			else:
				msgbox = True



		pygame.display.flip()
sock.close()
