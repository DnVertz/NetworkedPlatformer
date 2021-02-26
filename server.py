import threading, uuid, asyncio
import socket

HOST = '10.0.110.42'
PORT = 8008

players = []
players_lock = threading.Lock()

"""
	Packets

	Inbound (to server)

	Player Pos: sent on player position change, scope: player
		pos;<X>;<Y>
	
	Outbound (to clients)

	Player Init: sent on join, scope: player
		init;<ID>;<X>;<Y>
	Player Join: sent on join, scope: all
		join;<ID>;<X>;<Y>
	Player Pos: sent on player positon change, scope: all
		pos;<ID>;<X>;<Y>

"""

def broadcast(data):
	#players_lock.acquire()
	for player in players:
		player.conn.write(data)
	#players_lock.release()

def removePlayer(playerID):
	players_lock.acquire()
	for player in players:
		if player.id == playerID:
			players.remove(player)
	players_lock.release()

def sendPlayerInit(player, writer):
	data = "init;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	writer.write(data.encode('UTF-8'))

def sendPlayerSpawn(player, writer):
	data = "spawn;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	writer.write(data.encode('UTF-8'))

def sendPlayerJoin(player):
	data = "join;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	broadcast(data.encode('UTF-8'))

def sendPlayerLeave(playerID):
	data = "leave;"+str(playerID)+"\n"
	broadcast(data.encode('UTF-8'))

class Player:
	def __init__(self, conn):
		self.id = uuid.uuid1()
		self.conn = conn
		self.x = 20
		self.y = 0
	def setPosition(self, x, y):
		self.x = x
		self.y = y
	def getPosition(self):
		return (self.x, self.y)

class PositionUpdate:
	def __init__(self, pid, x: int, y: int):
		self.id = pid
		self.x = x
		self.y = y
	def updatePlayer(self):
		#players_lock.acquire()
		for i in range(len(players)):
			if players[i].id == self.id:
				players[i].x = self.x
				players[i].y = self.y
				break
		#players_lock.release()
	def forwardToClients(self):
		data = "pos;"+str(self.id)+";"+str(self.x)+";"+str(self.y)+"\n"
		broadcast(data.encode('UTF-8'))

def protocolDecode(playerID, data):
	split = data.split(";")
	print(split)
	if split[0] == "pos":
		# decode position update packet
		# position packet structure pos;x;y
		posUpdate = PositionUpdate(playerID, int(split[1]), int(split[2]))
		return posUpdate

async def handler(reader, writer):

	addr = writer.get_extra_info('peername')
	print(f'Connection from {addr} \n')
	players_lock.acquire()
	player = Player(writer)
	playerID = player.id
	players.append(player)
	sendPlayerInit(player, writer) #send init id and pos to player
	for p in players:
		sendPlayerSpawn(p,writer)
	players_lock.release()
	sendPlayerJoin(player) #broadcast init id and pos to all players
	while True:

			try:
				raw = await reader.readline()
				if not raw:
					break
			except:
				break

			data = raw.decode()
			packet = protocolDecode(playerID, data)
			if isinstance(packet, PositionUpdate):
				packet.updatePlayer()
				packet.forwardToClients() #broadcast
	writer.close()
	removePlayer(playerID)
	sendPlayerLeave(playerID)

async def main():
    server = await asyncio.start_server(handler, HOST, PORT,limit=30000)
    #
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())