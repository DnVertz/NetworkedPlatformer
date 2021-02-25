from threading import Thread
import pygame 
import ui
import menu
import player
import inputs
import hitboxes
import actor
import random
import socket
import os


state = ui.uistate()
#delte this
width = 1024
height = 640
players = 20
spawnx= 100
spawny = 100
i = 0
quitol = False
clientid = 1
#corner(x,y),(width,height)
#,[(500,10),(1,500)]
screen = pygame.display.set_mode((width, height))
coll = [(0,0),(0,640)],[(1024,0),(1024,640)],[(0,640),(1024,640)],[(0,0),(1024,0)],[(0,500),(300,500)],[(500,450),(60,125)],[(800,400),(500,400)]#stores the level hitboxes... can and will be changed into a text file
hitbox = []#loads the hitboxes
multiplays = []#stores the actor class
for x in coll:
	hitbox.append(hitboxes.hitboxes(x[0][0],x[0][1],x[1][0],x[1][1]))




state.state = "start"
pygame.init()

player = player.player(width/2, height/2, 25, 50,0,hitbox)
"""
for x in range(0,players):
	multiplays.append(actor.actor(width/2, height/2, 25, 50,0,hitbox,x)) """


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8008)
sock.connect(server_address)
initdata = sock.recv(4096)

initdata = initdata.decode('UTF-8')
split = initdata.split("\n")
for p in split:
	split2 = p.split(";")
	if split2[0] == "init":
		clientid = split2[1]
		multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))




	










titlefont = pygame.font.Font(r'arial.ttf', 40)
titlefont2 = pygame.font.Font(r'arial.ttf', 10)
clock = pygame.time.Clock() 
thrcou = 0
maincou= 0
FPS = 70



def networkthread(clientid):
	buffer = ""

	clock.tick(FPS)
	while True:

		
		try:
			data = sock.recv(4096)
		except:
			break

			
		

		data = data.decode('UTF-8')
		split = data.split("\n")
		for p in split:
			split2 = p.split(";")


			if split2[0] == "spawn":
				if split2[1] is not clientid:
					multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))


			if split2[0] == "join":
				if split2[1] is not clientid:
					multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))

			if split2[0] == "pos":
				if len(split2) == 4:
					if str(split2[1]) != str(clientid):
						for x in multiplays:
							if x.index == split2[1]:
								#print("rundsuhkajdgskj")
								if split2[2].isdigit() and split2[3].isdigit():
									x.setPos(int(split2[2]),int(split2[3]))
				

			

			if split2[0] == "leave":
				for x in multiplays:
					if x.index == split2[1]:
						multiplays.remove(x)
	os._exit(1)








#thr = threading.Thread(target=networkthread)
#thr.start()

thr = Thread(target = networkthread,args =(str(clientid),))
thr.start()

while True:
	if quitol == True:
		break


	
	
	events = pygame.event.get()
	for event in events:

		if event.type == pygame.QUIT:
			#sock.send("poo")
			
			quitol = True
			




	
	if state.state == "start":
		screen.fill((128,128,128))
		start = menu.drawStart(screen, titlefont, state,events)
		if start == 0:
			state.state = "game"
		if start == 1:
			state.state = "join"
		if start == 2:
			pygame.quit()
	elif state.state== "join":
		screen.fill((128,128,128))
		join = menu.drawJoin(screen, titlefont, state,events)

	else:
		
		
		
		
		screen.fill((128,128,128))

		#player.render(screen)

		#player.physicsHandler()
		clock.tick(FPS)

		for p in multiplays:
			if p.index == clientid:
				if inputs.run(state,p) == True:
					data2 = "pos;"+str(int(p.x))+";"+str(int(p.y))+"\n"
					print(data2)
					data2 = data2.encode('UTF-8')
					sock.send(data2)



			
			p.render(screen)
			if p.index == clientid:
				p.physicsHandler()

		
		
		for x in coll:
			if coll.index(x) >= 4:
				pygame.draw.rect(screen,(60,60,60),(x[0][0],x[0][1],x[1][0],x[1][1]))
				"""
				textSurf = titlefont2.render("troll face gaming (this is a goomba)", 1, (255,255,255))# and this lol
				textRect = textSurf.get_rect()
				textRect.center = ((x[0][0]+(80)), (x[0][1]+210))
				screen.blit(textSurf, textRect)"""
		inputs.handleMouse(pygame, player)

		

	pygame.display.flip()
sock.close()






    
