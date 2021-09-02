#this reads in the levels.pkl file which is a list and transfers it into classes
import hitboxes
import pickle
import json
def create(rooms3):
	rooms2 = []
	rooms = []
	data = [[0,0],[0,640]],[[1024,0],[1024,640]],[[0,640],[1024,640]],[[0,0],[1024,0]]
	rooms2 = json.loads(rooms3)
	for x in rooms2:
		y = []
		for z in data:
			x.append(z)
		for hbox in x:
			if len(hbox) > 2:
				if hbox[2][0] != 2:
					y.append(hitboxes.hitboxes(hbox[0][0],hbox[0][1],hbox[1][0],hbox[1][1],hbox[2][1],hbox[2][2],hbox[2][3]))
			else:
				y.append(hitboxes.hitboxes(hbox[0][0],hbox[0][1],hbox[1][0],hbox[1][1]))
		rooms.append(y)
	return rooms