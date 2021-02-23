import pygame
import ui
#1024*640
def drawStart(screen, titlefont, state,events):
	pygame.draw.rect(screen, (153,0,0), (0,0,250,85))
	pygame.draw.rect(screen, (41,41,41), (0,0,220,70))


	char1 = titlefont.render("Platformer", 1, (255,255,255))
	screen.blit(char1, (10, 10))
	startbutton = ui.button("Start", 370, 185, 300, 75)
	startbutton.render(screen)
	startbutton2 = ui.button("Exit", 370, 285, 300, 75)
	startbutton2.render(screen)




	if startbutton.pressed(events):
		return(0)
	if startbutton2.pressed(events):
		return(1)

	


