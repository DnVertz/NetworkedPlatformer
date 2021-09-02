# Justification of coding

For this justification I will be focusing on the transfer of data between client and server and back

### Client To Server interaction:

To best illustrate the client to server interaction I will be using the position packet as an example. When a player is connected to a server a position packet transmits for every loop of the main while loop the packet is formatted as such.

`"pos;"+str(clientid)+";"+str(player1.x)+";"+str(player1.y)+";"+str(int(player1.room))+";"+str(int(player1.activeWeapon))+";"+str(int(player1.angle))+";"+str(int(player1.hitpoints))+";"+str(player1.win)+"\n"`

As you can see the packet type is denoted by ``pos`` at the start of the packet it transmits data such as the ID of the client, the clients position,room,activeweapon etc the problem is that this is meant to be a position packet yet transmits allot more data than just the simple position of a client/player this makes both reading the code itself harder as well as understanding the packet structure harder. 

When a packet is sent to the server the server will then split the packet into segments denoted by the ``;`` and update the players paramteres according to the function:

			elif split[0] == 'pos':
				for i in range(len(players)):
					if str(players[i].id) == split[1]:
						players[i].x = split[2]
						players[i].y = split[3]
						players[i].room = split[4]
						players[i].timeout = 0
	          players[i].activeWeapon = split[5]
	          players[i].angle = split[6]
	          players[i].hitpoints = split[7]
	          players[i].win = split[8]
	
					for p in players:
						sendPlayerPos(players[i],p.addr)

This works because whenever a player joins the server the server creates a corresponding class to that player that is then added to the list `players`  in the last 2 lines youll be able to see the server then passing this updated information onto the other clients connected to the server the `sendPlayerPos` function is below.

	def sendPlayerPos(player,addr):
		data = "pos;"+str(player.id)+";"+str(player.x)+";"+str(player.y)+";"+str(int(player.room))+";"+str(int(player.activeWeapon))+";"+str(int(player.angle))+";"+str(int(player.hitpoints))+";"+str(int(player.deaths))+";"+str(int(player.timer))+";"+str(player.win)+"\n"
		
		player.socket.sendto(data.encode('UTF-8'),addr)

like before the position packet is massive and looking back I should have compressed this into many smaller packets, however this has the positive of transferring one big packet every loop this means that the chance of an important piece of information being lost is much lower but as mentioned earlier makes the code harder to read. Focusing again on the program itself this packet is then transferred to many outside clients where they recieve the packet in the function below.

	if split2[0] == "pos":
						for x in multiplays:
							if x.index == split2[1]:
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

this works very similarly to the server side handelling of the position packet where each client will have its own list of the players within the game and when recieving a postion packet from the server they will update the relevant information however this time there is a tiny bit extra logic in the win condition, where the game will end if one players postion packet flips to True. 





