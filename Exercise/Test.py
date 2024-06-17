import keyboard
import time

"""
こちらはテスト用になります。好きに使ってください。
"""


while True:

    if keyboard.is_pressed('up'):
        print("up pressed")
    if keyboard.is_pressed('esc'):
        print("Exiting...")
        break

    time.sleep(0.01)
