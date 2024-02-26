import pywhatkit as pwk
import pyautogui 
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()
 
# using Exception Handling to avoid unexpected errors
try:
     # sending message in Whatsapp in India so using Indian dial code (+91)
    pwk.sendwhatmsg_instantly("+917063633765", "Hi, how are you?",tab_close=True)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
 
    print("Message Sent!") #Prints success message in console
 
     # error message
except:
    print("Error in sending the message")