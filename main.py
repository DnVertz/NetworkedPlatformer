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
import signal
import sys

HOST = None
PORT = None
state = ui.uistate()
width = 1024
height = 640
quitol = False
clientid = 1
title = "Platformer"
player1 = None
predict = False

screen = pygame.display.set_mode((width, height),pygame.SCALED,vsync = 1 )
#corner(x,y),(width,height)
#,[(500,10),(1,500)]

coll = [(0,0),(0,640)],[(1024,0),(1024,640)],[(0,640),(1024,640)],[(0,0),(1024,0)],[(0,500),(300,500)],[(500,450),(60,125)],[(800,400),(500,400)]#stores the level hitboxes... can and will be changed into a text file
hitbox = []#loads the hitboxes
multiplays = []#stores the actor class
for x in coll:
	hitbox.append(hitboxes.hitboxes(x[0][0],x[0][1],x[1][0],x[1][1]))

state.state = "start"
pygame.init()
titlefont = pygame.font.Font(r'arial.ttf', 40)
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
			print(server_address)
			msgs = str("join;")
			byte = msgs.encode()
			sock.sendto(byte,server_address)
			break
		except:
			title = "Wrong IP/Port!!!!"
			state.state = "start"

	pygame.display.flip()

initdata,addr = sock.recvfrom(4096)
print(initdata)
initdata = initdata.decode('UTF-8')
split = initdata.split("\n")
for p in split:
	split2 = p.split(";")
	if split2[0] == "init":
		clientid = split2[1]
		multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))
		player1 = actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1])


clock = pygame.time.Clock() 
FPS = 60
fps = clock.tick(FPS)

def networkthread(clientid):
	global predict
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
					
					multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))

			if split2[0] == "join":
				if split2[1] is not clientid:
					multiplays.append(actor.actor(int(split2[2]), int(split2[3]),25 ,50 ,0,hitbox,split2[1]))

			if split2[0] == "pos":
					for x in multiplays:
						if x.index == split2[1]:
							x.setPos(int(split2[2]),int(split2[3]))

			if split2[0] == "leave":
				if split2[1] == clientid:
					os._exit(1)
				else:
					for x in multiplays:
						if x.index == split2[1]:
							multiplays.remove(x)

	os._exit(1)

thr = Thread(target = networkthread,args =(str(clientid),))
thr.start()

def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	data2 = "leave;"+str(clientid)+"\n"
	data2 = data2.encode('UTF-8')
	sock.sendto(data2,server_address)
	os._exit(1)

while True:

	signal.signal(signal.SIGINT, signal_handler)

	screen.fill((128,128,128))

	if quitol == True:
		data2 = "leave;"+str(clientid)+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		break
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			quitol = True
	for x in coll:
		if coll.index(x) >= 4:
			pygame.draw.rect(screen,(60,60,60),(x[0][0],x[0][1],x[1][0],x[1][1]))

	if player1 is not None:
		player1.physicsHandler(fps)
		data2 = "pos;"+str(clientid)+";"+str(int(player1.x))+";"+str(int(player1.y))+"\n"
		data2 = data2.encode('UTF-8')
		sock.sendto(data2,server_address)
		x = inputs.run(state,player1)
		player1.render(screen)

		for p in multiplays:
			if p.index != clientid:
				p.render(screen)
		pygame.display.flip()




sock.close()
