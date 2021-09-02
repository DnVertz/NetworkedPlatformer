# Test Data

### Testing main.py line 64-113

This code block aims to check whether or not the user has entered the correct data for IP,Port and Name. To test this we will input a range of data.

1. ``IP:`` ,``Port:`` and ``Name: `` for the first test we will input no data to see whether or not it can handle no data being input without crashing. If it is working properly we will get the message at the top right changing to ``Wrong IP/Port!!!!``
2. ``IP:172.105.175`` ,``Port:8888`` and ``Name:testusr  ``for this test we will input correct data except with the incorrect IP if it is working properly we will get the message at the top right changing to ``Wrong IP/Port!!!!``
3. ``IP:172.105.175.50`` ,``Port:888`` and ``Name:testusr  `` for this test we will input correct data except the incorrect Port if it is working properly we will get the message at the top right changing to ``Wrong IP/Port!!!!``
4. ``IP:172.105.175.50`` ,``Port:8888`` and ``Name:  `` for this test we will input correct data except tha there is no name being input  if it is working properly we will get the message at the top right changing to ``Choose a name``
5. ``IP:172.105.175.50`` ,``Port:8888`` and ``Name:testusr  `` for this test we will have another client connected to the server, it will go under the same name as being input ``testusr``if it is working properly we will get the message at the top right changing to ``Name in use!!!!``
6. ``IP:172.105.175.50`` ,``Port:8888`` and ``Name:testusr  `` for this test we will input correct data if it is working properly we will be let into the controls screen.

## Testing ui.py function at line 150(where self.number = False)

This function aims to both take user input and display it at the same time within a textbox for the case where self.number = False it will have a limit of 6 chars compared to 16 where self.number = True

1. `mouseX:within bounds`,`mouseY:within bounds`,`keypress:a` for this test we will be testing whether or not the textbox will register keypresses and display them when the mouse is within the bounds if it is working correctly we will see `a` displayed textbox
2. `mouseX:within bounds`,`mouseY:within bounds`,`keypress:1` for this test we will be testing whether or not the textbox will register keypresses and display them when the mouse is within the bounds if it is working correctly we will see nothing displayed in the textbox
3. `mouseX:within bounds`,`mouseY:within bounds`,`keypress:aaaaaaaaa` for this test we will be testing whether or not the textbox will limit the amount of keypresses to 6 when inputting into a letter textbox if it is working correctly we will see `aaaaaa` within the textbox
4. `mouseX:out of bounds`,`mouseY:out of bounds`,`keypress:a` for this test we will be testing whether or not the textbox will ignore keypresses outside of its bound if it is working correctly we will see nothing within the textbox
5. `mouseX:in bounds`,`mouseY:out of bounds`,`keypress:a` for this test we will be testing whether or not the textbox will ignore keypresses outside of its bound if it is working correctly we will see nothing within the textbox
6. `mouseX:out of bounds`,`mouseY:in bounds`,`keypress:a` for this test we will be testing whether or not the textbox will ignore keypresses outside of its bound if it is working correctly we will see nothing within the textbox

## Testing ui.py function at line 150(where self.number = True)

This function aims to both take user input and display it at the same time within a textbox for the case where self.number = False it will have a limit of 16 chars compared to 7, this is due to the self.number variable determining whether or not it is intended to be a name or message. Thus we can use the same tests. Except for:

1. `mouseX:within bounds`,`mouseY:within bounds`,`keypress:12345678901234567` for this test we will be testing whether or not the textbox will register keypresses and display them when the mouse is within the bounds as well as testing the limit of 16 chars if it is working correctly we will see `1234567890123456` displayed in the textbox

 





