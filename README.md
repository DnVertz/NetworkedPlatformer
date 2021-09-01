NetworkedPlatformer

To run the game:
1.CD into the directory where main.py is present
2.run pip3 install -r requirements.txt to install the required packages
3.run python3 main.py to start a client 
4.either connect to my server at IP:172.105.175.50 and Port:8888 or start your own server by running server.py in a seprate command line window and entering the on screen IP and Port
5.If you decide to run your own server for clients to connect to the server outside of your own computer(eg: running a local client and server on the same computer and connecting that way) you will need to port forward, the default port of the server is 8888. Once that is done just run the server and you will be able to connect via the onscreen IP and Port.

Controls for client(main.py):
A and D to move left and right
Spacebar to jump
Left mouse button to shoot
Mouse to move where you are aiming
1,2 and 3 to select between weapons
Enter to open, send and close the message box 
When in the message box hover over the box and type your message

Controls for level editor(edit.py):
For other players to see changes made within the level editor you must have your own instance of the server running which will then transmit the data of this new level to the clients.
Left click to create an object then just move your mouse to define its shape and size(you cannot define an object where the starting point isnt the top left corner) then left click again to stop defining it
While defining an object you can right click to turn it into a moving obstacle(turning it red) then a line will appear defining its path move your mouse to define this path, when done right click again
Hover within the bounds of an object and press delete to delete it 
Left and right arrow keys to navigate between rooms
Shift to delete a room(pressing this will always delete the last room)
Enter to create a new room(pressing this will alwyas create a room after the last)
After you are happy exit the program as changes are saved automatically



