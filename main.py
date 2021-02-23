import pygame 
import ui
import menu
import player
import inputs
import hitboxes
import actor
import random
state = ui.uistate()
#delte this
width = 1024
height = 640
players = 5
#corner(x,y),(width,height)
#,[(500,10),(1,500)]
screen = pygame.display.set_mode((width, height))
coll = [(0,0),(0,640)],[(1024,0),(1024,640)],[(0,640),(1024,640)],[(0,0),(1024,0)],[(0,500),(300,500)],[(500,450),(60,125)],[(800,400),(500,400)]
hitbox = []
rects = []
multiplays = []
for x in coll:
	hitbox.append(hitboxes.hitboxes(x[0][0],x[0][1],x[1][0],x[1][1]))




state.state = "start"
pygame.init()

player = player.player(width/2, height/2, 25, 50,0,hitbox)
for x in range(0,players):
	multiplays.append(actor.actor(width/2, height/2, 25, 50,0,hitbox,x)) 



titlefont = pygame.font.Font(r'arial.ttf', 40)
titlefont2 = pygame.font.Font(r'arial.ttf', 10)
clock = pygame.time.Clock() 
FPS = 70



while True:

	
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	
	if state.state == "start":
		screen.fill((128,128,128))
		start = menu.drawStart(screen, titlefont, state,events)
		if start == 0:
			state.state = "game"
		if start == 1:
			pygame.quit()
	else:
		
		inputs.run(state,player)
		
		
		clock.tick(FPS)
		screen.fill((128,128,128))
		player.render(screen)

		for x in multiplays:
			x.render(screen)
			x.physicsHandler()
			x.setVx(random.randint(-2,2))
			x.jump()
			#x.moveRight(random.randint(0,2))

		player.physicsHandler()
		
		for x in coll:
			if coll.index(x) >= 4:
				pygame.draw.rect(screen,(60,60,60),(x[0][0],x[0][1],x[1][0],x[1][1]))
				textSurf = titlefont2.render("troll face gaming (this is a goomba)", 1, (255,255,255))# and this lol
				textRect = textSurf.get_rect()
				textRect.center = ((x[0][0]+(80)), (x[0][1]+210))
				screen.blit(textSurf, textRect)
		inputs.handleMouse(pygame, player)

		

	pygame.display.flip()