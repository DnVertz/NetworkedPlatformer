# NetworkedPlatformer

## System Specs: 

### Minimum Hardware Specs:

1. CPU - at least 2 cores and 64bit 
2. RAM-  at least 2GB 
3. GPU - integrated or discrete 
4. Storage - atleast 1mb/s reads and writes with 2mb storage free  
5. A stable internet connection with atleast 1mb/s up and down

### Minimum Software Specs:

1. Language- Python 3
2. Libraries- See requirements.txt for the required libraries 
3. OS- 64bit operating system of Mac OS,Linux or Windows capable of supporting python 3



## To run the game:
1. CD into the directory where main.py is present.
2. run pip3 install -r requirements.txt to install the required packages.
3. run python3 main.py to start a client.(On inital run it will take a few seconds)
4. either connect to my server at IP:172.105.175.50 and Port:8888 or start your own server by running server.py in a seprate command line window however your own server will only accept connections from virtual clients on your own computer(these can be started by running main.py in another command line window) the ip and port to this server is printed to the command line.
5. To connect to a server hover over the IP or Port box and type the respective number(including decimal points with the IP).
6. Choose a name by hovering over the name box and typing what you want to be called(there is a character limit).
7. Enter the game by clicking Done!

Screenshots:

1. Installing required libraries:
	
	![image](images/image.png)

2. Entering the ip and port of a server as well as choosing a name:

   ![image2](images/image2.png)

3. Ingame:

   ![image3](images/image3.png)

## Controls for client(main.py):

1. A and D to move left and right.
2. Spacebar to jump.
3. Left mouse button to shoot.
4. Mouse to move where you are aiming.
5. 1,2 and 3 to select between weapons.
6. Enter to open, send and close the message box.
7. When in the message box hover over the box and type your message.

## Controls for level editor(edit.py):

1. For other players to see changes made within the level editor you must have your own instance of the server running which will then transmit the data of this new level to the clients.
2. Left click to create an object then just move your mouse to define its shape and size(you cannot define an object where the starting point isnt the top left corner) then left click again to stop defining it.
3. While defining an object you can right click to turn it into a moving obstacle(turning it red) then a line will appear defining its path move your mouse to define this path, when done right click again.
4. Hover within the bounds of an object and press delete to delete it.
5. Left and right arrow keys to navigate between rooms.
6. Shift to delete a room(pressing this will always delete the last room).
7. Enter to create a new room(pressing this will alwyas create a room after the last).
8. After you are happy exit the program as changes are saved automatically.

## Trouble Shooting:

When entering into the game there are 3 types of errors you can encounter:

1. Incorrect IP or Port, if you have entered the incorrect IP or Port the client will change the text in the top left to `Wrong IP/Port!!!!`  to fix this error check the provided IP and Port then re enter it into their respective boxes. 

   Example:

   ![image6](images/image6.png)

2. Name in use, if you have entered a name into its respective box that is being used by another person connected to the server the client will change the text in the top left to `Name in use!!!!` to fix this pick another name and enter it into the respective box.

   Example:

   ![image4](images/image4.png)

3. No name entered, if you have not entered a name into its respective box the client will change the text in the top left to `Choose a name`   to fix this pick a name and enter it into the respective box.

   Example:

   ![image5](images/image5.png)

