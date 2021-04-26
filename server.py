import threading, uuid, asyncio
import socket


PORT = 8008
#Jank cannot describe this solution
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(("8.8.8.8", 8008))
HOST = str(s.getsockname()[0])
s.close()


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
	for player in players:

		try:
			player.conn.write(data)
			#player.conn.drain()
		except:
			pass

def removePlayer(playerID):
	for player in players:
		if player.id == playerID:
			players.remove(player)

async def sendPlayerInit(player, writer):
	data = "init;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	writer.write(data.encode('UTF-8'))


async def sendPlayerSpawn(player, writer):
	data = "spawn;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	writer.write(data.encode('UTF-8'))

async def sendPlayerJoin(player):
	data = "join;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+"\n"
	broadcast(data.encode('UTF-8'))

async def sendPlayerLeave(playerID):
	data = "leave;"+str(playerID)+"\n"
	broadcast(data.encode('UTF-8'))

class Player:
	def __init__(self, conn):
		self.id = uuid.uuid1()
		self.conn = conn
		self.x = 0
		self.y = 0
		self.vx = 0
		self.vy = 0
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

class VeloUpdate:
	def __init__(self, pid, x: int, y: int):
		self.id = pid
		self.vx = x
		self.vy = y
	async def updatePlayer(self):
		#players_lock.acquire()
		for i in range(len(players)):
			if players[i].id == self.id:
				players[i].vx = self.vx
				players[i].vy = self.vy
				break
		#players_lock.release()
	async def forwardToClients(self):
		data = "velo;"+str(self.id)+";"+str(self.vx)+";"+str(self.vy)+"\n"
		await broadcast(data.encode('UTF-8'))

async def protocolDecode(playerID, data):
	split = data.split(";")
	if split[0] == "pos":
		# decode position update packet
		# position packet structure pos;x;y
		posUpdate = PositionUpdate(playerID, int(split[1]), int(split[2]))
		return posUpdate

	if split[0] == "velo":
		# decode position update packet
		# position packet structure pos;x;y
		veloUpdate = VeloUpdate(playerID, int(split[1]), int(split[2]))
		return veloUpdate

async def handler(reader, writer):
	i = 0

	addr = writer.get_extra_info('peername')
	print(f'Connection from {addr} \n')
	player = Player(writer)
	playerID = player.id
	players.append(player)
	await sendPlayerInit(player, writer) #send init id and pos to player
	for p in players:
		await sendPlayerSpawn(p,writer)

	await sendPlayerJoin(player) #broadcast init id and pos to all players
	while True:
			

			try:
				#raw = await reader.readline()
				raw = await reader.readline()
				if not raw:
					break
			except:
				break

			data = raw.decode()
			"""if not data.endswith("\n"):
				pass"""

			#else:
			packet = await protocolDecode(playerID, data)
			if isinstance(packet, PositionUpdate):
				packet.updatePlayer()
				packet.forwardToClients() #broadcast

			if isinstance(packet, VeloUpdate):
				pass
				#await packet.updatePlayer()
				#await packet.forwardToClients() #broadcast

	writer.close()
	removePlayer(playerID)
	await sendPlayerLeave(playerID)

async def main():
    server = await asyncio.start_server( handler, HOST, PORT)

    #
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    server:
        await server.serve_forever()

asyncio.run(main())
