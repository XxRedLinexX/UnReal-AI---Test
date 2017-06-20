import win32api as wapi
import time



keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'$/\\":
    keyList.append(char)

state_left = wapi.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = wapi.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


def mouse_click():
    a = wapi.GetKeyState(0x01)
    b = wapi.GetKeyState(0x02)
    global state_left
    global state_right
    presses = []
    if a != state_left:  # Button state changed
        state_left = a
        #print(a)
        if a < 0:
            presses.append(1) #([1,0,0,0,0]) #Left Button Pressed
        else:
            presses.append(10) #([0,1,0,0,0]) #Left Button Released

    if b != state_right:  # Button state changed
        state_right = b
        #print(b)
        if b < 0:
            presses.append(2) #([0,0,1,0,0]) #Right Button Pressed
        else:
            presses.append(20) #([0,0,0,1,0]) #Right Button Released
    
    return presses



