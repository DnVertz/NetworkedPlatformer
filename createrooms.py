import hitboxes
def create():
	coll = None
	obstacles = None
	colli0 = [[[0,0],[0,640]],[[1024,0],[1024,640]],[[0,640],[1024,640]],[[0,0],[1024,0]],[[0,500],[300,500]],[[800,400],[500,400]],[[500,450],[60,125],[1,1,400,650]]]
	colli1 =[[[-9, 305], [201, 357], [0, 0, -100, -100]], [[113, 499], [911, 170], [0, 0, -100, -100]], [[107, 311], [122, 189], [1, 1, 107, 589]]]
	coll0 = []
	coll1= []
	rooms = []

	for hbox in colli0:
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
	rooms.append(coll1)

	return rooms