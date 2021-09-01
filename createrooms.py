import hitboxes
import pickle
import json
def create(rooms3):
	roomcount = 0
	coll = None
	obstacles = None
	colli0 = [[[0,0],[0,640]],[[1024,0],[1024,640]],[[0,640],[1024,640]],[[0,0],[1024,0]],[[0,500],[300,500]],[[800,400],[500,400]],[[500,450],[60,125],[1,1,400,650]]]
	colli1 =[[[0, 0], [0, 640]], [[1024, 0], [1024, 640]], [[0, 640], [1024, 640]], [[0, 0], [1024, 0]], [[-20, 545], [343, 120], [0, 0, -100, -100]], [[160, 425], [320, 221], [0, 0, -100, -100]], [[267, 294], [213, 200], [0, 0, -100, -100]], [[477, -21], [210, 320], [1, 1, 477, 842]], [[457, 473], [573, 171], [0, 0, -100, -100]], [[410, 399], [68, 71], [1, 1, 410, 963]]]
	coll0 = []
	coll1= []
	rooms2 = []
	#rooms2 =list(rooms3)
	rooms = []
	#coll = eval("coll" + str(player1.room))
	#print(rooms2[0])


	data = [[0,0],[0,640]],[[1024,0],[1024,640]],[[0,640],[1024,640]],[[0,0],[1024,0]]
	"""with open('levels.pkl', 'rb') as fr:
		try:
			while True:
				rooms2.append(pickle.load(fr))
		except EOFError:
			pass"""

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



	
	

	"""for hbox in colli0:
		if len(hbox) > 2:
			coll0.append(hitboxes.hitboxes(hbox[0][0],hbox[0][1],hbox[1][0],hbox[1][1],hbox[2][1],hbox[2][2],hbox[2][3]))
		else:
			coll0.append(hitboxes.hitboxes(hbox[0][0],hbox[0][1],hbox[1][0],hbox[1][1]))

	rooms.append(coll0)

	for hbox in colli1:
		if len(hbox) > 2:
			coll1.append(hitboxes.hitboxes(hbox[0][0],hbox[0][1],hbox[1][0],hbox[1][1],hbox[2][1],hbox[2][2],hbox[2][3]))
		else:
			coll1.append(hitboxes.hitboxes(hbox[0][0],hbox[0][1],hbox[1][0],hbox[1][1]))
	rooms.append(coll1)"""

	return rooms