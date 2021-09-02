from threading import Thread
from threading import Lock
import time
import pygame
import pickle
import uuid, asyncio
import socket
import socketserver
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 8008))
HOSTname = str(s.getsockname()[0])
s.close()
PORT = 8888
HOST = ''
tick = 0
reverse = False
players = []
bullets = []


def broadcast(data):
	for player in players:
		try:
			player.socket.write(data)
		except:
			pass

def sendPlayerInit(player, addr,socket):
	data = "init;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+";"+str(player.name)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendBulletSpawn(x,y,vx,vy,idd,addr,socket,room,size):
	data = "bspawn;"+str(x)+";"+str(y)+";"+str(vx)+";"+str(vy)+";"+str(idd)+";"+str(room)+";"+str(size)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerSpawn(player,addr):
	data = "spawn;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+";"+str(player.name)+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerLeave(player,addr,socket):
	data = "leave;"+str(player.id)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerTick(player,addr,socket,tick,rev):
	data = "tick;"+str(tick)+";"+str(rev)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerPos(player,addr):
	data = "pos;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+";"+str(int(player.room))+";"+str(int(player.activeWeapon))+";"+str(int(player.angle))+";"+str(int(player.hitpoints))+";"+str(int(player.deaths))+";"+str(int(player.timer))+"\n"
	player.socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerMsg(socket,message,addr,name):
	data = "msg;"+str(name)+";"+str(message)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerDie(socket,addr,id):
	data = "die;"+str(id)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)

def sendPlayerKilled(socket,addr,id,id2):
	data = "killed;"+str(id)+";"+str(id2)+"\n"
	socket.sendto(data.encode('UTF-8'),addr)


def timeout():
	clock = pygame.time.Clock() 
	FPS = 120
	
	while True:
		fps = clock.tick(FPS)

		global tick
		global players
		global reverse
		global bullets

		if len(bullets) > 50:
			bullets.remove(bullets[1])

		if tick < 1000:
			tick += 1


		else:
			if reverse == True:
				reverse = False
			else:
				reverse = True

			tick = 0
		for p in players:
			sendPlayerTick(p,p.addr,p.socket,tick,reverse)
			p.timeout += 1
			p.timer += 1
			if p.timeout > 300:
				for x in players:
					sendPlayerLeave(p,x.addr,x.socket)
				players.remove(p)

thr = Thread(target = timeout,args =())
thr.start()

class Player:
	def __init__(self, socket,addr,name):
		self.id = uuid.uuid1()
		self.socket = socket
		self.addr = addr
		self.name = name
		self.x = 0
		self.y = 0
		self.vx = 0
		self.vy = 0
		self.timeout = 0
		self.room = 0
		self.activeWeapon = 1
		self.angle = 0
		self.hitpoints = 100
		self.timer = 0
		self.deaths = 0

class Bullet:
	def __init__(self,x=0,y=0,vx=0,vy=0,idd= 0,room = 0,addr = 0):
		self.id = idd
		self.x = 0
		self.y = 0
		self.vx = 0
		self.vy = 0
		self.addr = addr
		self.room = room




class MyUDPHandler(socketserver.DatagramRequestHandler):
	def handle(self):
		data = self.request[0].strip()
		socket = self.request[1]
		data = data.decode()
		split = data.split(";")



		if split[0] == 'join':
			allow = True
			for x in players:
				if x.name == split[1]:
					msg = "False"
					msg = msg.encode()
					allow = False
					socket.sendto(msg,self.client_address)


			if allow == True:
				rooms2 = []
				with open('levels.pkl', 'rb') as fr:
					try:
						while True:
							rooms2.append(pickle.load(fr))
					except EOFError:
						pass

				msg = "True;"+str(rooms2[0])
				msg = msg.encode()
				socket.sendto(msg,self.client_address)
				player = Player(socket,self.client_address,split[1])
				playerID = player.id
				players.append(player)
				rooms2 = []
				
				

				sendPlayerInit(player, self.client_address,socket) #send init id and pos to player

				for p in players:
					if p is not player:
						sendPlayerSpawn(p,player.addr)
						sendPlayerSpawn(player,p.addr)
					else:		
						sendPlayerSpawn(player,p.addr)
		
		elif split[0] == 'pos':
			for i in range(len(players)):
				if str(players[i].id) == split[1]:
					players[i].x = split[2]
					players[i].y = split[3]
					players[i].room = split[4]
					players[i].timeout = 0
					if len(split) > 5:
						players[i].activeWeapon = split[5]
						players[i].angle = split[6]
						players[i].hitpoints = split[7]

					for p in players:
						#if str(p.id) != str(players[i].id):
						sendPlayerPos(players[i],p.addr)
							
		elif split[0] == 'leave':
			for i in range(len(players)):
				if str(players[i].id) == split[1]:
					for p in players:
						if str(p.id) != str(players[i].id):
							sendPlayerLeave(players[i],p.addr,socket)
					players.remove(players[i])
					break

		elif split[0] == 'msg':
			for p in players:
				p.timeout = 0
				sendPlayerMsg(socket,split[1],p.addr,split[2])

		elif split[0] == 'die':
			for p in players:
				sendPlayerDie(socket,p.addr,split[1])
				if str(p.id) == split[2]:
					p.deaths +=1

		elif split[0] == 'killed':
			for p in players:
				sendPlayerKilled(socket,p.addr,split[1],split[2])
				if p.id == split[2]:
					p.deaths +=1



		elif split[0] == 'joinbullet':
			bullet = Bullet(split[1],split[2],split[3],split[4],split[5],split[6],self.client_address)
			bullets.append(bullet)
			for p in players:
				sendBulletSpawn(split[1],split[2],split[3],split[4],split[5],p.addr,socket,split[6],split[7])


async def main():
    server = socketserver.UDPServer((HOST,8888), MyUDPHandler)
    print(f'Serving on IP: '+str(HOSTname)+" Port: "+str(8888))
    server.serve_forever()
    

asyncio.run(main())
