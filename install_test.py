from pynput import keyboard
def ddd(e):
    print(e)
lis = keyboard.Listener(on_keypress=ddd)

inx = input("fff")