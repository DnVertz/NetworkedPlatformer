import pygame
import ui
#1024*640
special = [ui.textbutton("IP", 370, 185, 300, 75),ui.textbutton("Port", 370, 285, 300, 75)]
complete = ['None','None']
def drawStart(screen, titlefont, state,events,title):
	global special
	global complete
	if title == "Platformer":
		pygame.draw.rect(screen, (153,0,0), (0,0,250,85))
		pygame.draw.rect(screen, (41,41,41), (0,0,220,70))
	else:
		pygame.draw.rect(screen, (153,0,0), (0,0,350,85))
		pygame.draw.rect(screen, (41,41,41), (0,0,320,70))




	char1 = titlefont.render(title, 1, (255,255,255))
	screen.blit(char1, (10, 10))

	char2 = titlefont.render("IP " + str(complete[0]), 1, (255,255,255))
	screen.blit(char2, (10, 90))

	char3 = titlefont.render("Port " + str(complete[1]), 1, (255,255,255))
	screen.blit(char3, (10, 170))



	for x in special:
		x.render(screen,events)
	"""
	startbutton2 = ui.button("Join", 370, 285, 300, 75)
	startbutton2.render(screen)"""
	startbutton3 = ui.button("Done", 370, 385, 300, 75)
	startbutton3.render(screen)

	"""if startbutton.pressed(events):
		return(0)"""
	ip = special[0].pressed(events)
	port = special[1].pressed(events)

	if ip is not None:
		print(ip)
		complete[0] = ip
	if port is not None:
		print(port)
		complete[1] = port

	"""if startbutton2.pressed(events):
		return(1)"""
	if startbutton3.pressed(events):
		return(complete)
"""
def drawJoin(screen, titlefont, state,events):
	pygame.draw.rect(screen, (153,0,0), (0,0,250,85))
	pygame.draw.rect(screen, (41,41,41), (0,0,220,70))


	char1 = titlefont.render("Platformer", 1, (255,255,255))
	screen.blit(char1, (10, 10))
	startbutton = ui.button("Port", 370, 185, 300, 75)
	startbutton.render(screen)
	startbutton2 = ui.button("IP", 370, 285, 300, 75)
	startbutton2.render(screen)
	startbutton3 = ui.button("Done", 370, 385, 300, 75)
	startbutton3.render(screen)
	
	if startbutton.pressed(events):
		return(0)
	if startbutton2.pressed(events):
		pass"""

	


