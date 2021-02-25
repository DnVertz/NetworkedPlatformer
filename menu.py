import pygame
import ui
#1024*640
def drawStart(screen, titlefont, state,events):
	pygame.draw.rect(screen, (153,0,0), (0,0,250,85))
	pygame.draw.rect(screen, (41,41,41), (0,0,220,70))


	char1 = titlefont.render("Platformer", 1, (255,255,255))
	screen.blit(char1, (10, 10))
	startbutton = ui.button("Host", 370, 185, 300, 75)
	startbutton.render(screen)
	startbutton2 = ui.button("Join", 370, 285, 300, 75)
	startbutton2.render(screen)
	startbutton3 = ui.button("Exit", 370, 385, 300, 75)
	startbutton3.render(screen)

	if startbutton.pressed(events):
		return(0)
	if startbutton2.pressed(events):
		return(1)
	if startbutton3.pressed(events):
		return(2)

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
		pass

	


