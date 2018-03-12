import numpy as np, cv2 as cv, time, win32api, win32con, win32com.client, threading
import datetime as d
from playsound import playsound
from msvcrt import getch
from PIL import Image, ImageGrab


class SwitcherButton:
    flag = False
    quit = False

    def __init__(self):
        threading.Thread(target=self.OnKeyboardEvent).start()

    def OnKeyboardEvent(self):
        while True:
            ALT     = win32api.GetKeyState(0x12)
            QBTN    = win32api.GetKeyState(0x51)
            ESC     = win32api.GetKeyState(0x1B)

            if ALT < 0 and QBTN<0:
                self.flag = not self.flag

            if ALT<0 and ESC<0:
                self.flag = False
                self.quit = True
                playsound('exit.mp3')
                break

            time.sleep(0.2)

class SoundPlayer():
    in_ = False
    out = False

    def playActivated(self):
        if self.in_:
            return

        threading.Thread(target=self.playAcivated_).start()
        self.in_ = True
        self.out = False

    def playDeactivated(self):
        if self.out:
            return
        threading.Thread(target=self.playDeactivated_).start()
        self.in_ = False
        self.out = True

    def playAcivated_(self):
        playsound('activated.mp3')

    def playDeactivated_(self):
        playsound('deactivated.mp3')

def fishingProcess(img):
    SLICE_Y1 = 655
    SLICE_Y2 = 670
    SLICE_X1 = 571
    SLICE_X2 = 775
    allPixels = (SLICE_Y2 - SLICE_Y1) * (SLICE_X2 - SLICE_X1)
    progressBarInscription = img[SLICE_Y1:SLICE_Y2, SLICE_X1:SLICE_X2]
    quantityWhiteColor = 0

    for line in progressBarInscription:
        for pixel in line:
            if pixel[1] < 15:
                quantityWhiteColor += 1

    if ((quantityWhiteColor / allPixels) > 0.15):
        return True
    else:
        return False


def leftClickM():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)


def rightClickM():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.1)


def pushButton(img):
    SLICE_Y1 = 276
    SLICE_Y2 = 302
    SLICE_X1 = 725
    SLICE_X2 = 835
    allPixels = (SLICE_Y2 - SLICE_Y1) * (SLICE_X2 - SLICE_X1)
    buttonInscription = img[SLICE_Y1:SLICE_Y2, SLICE_X1:SLICE_X2]
    quantityRedColor = 0
    quantityGreenColor = 0
    
    for line in buttonInscription:
        for pixel in line:
            if (pixel[0] < 11 or pixel[0] > 234) and pixel[1] > 100 and pixel[2] > 120:
                quantityRedColor += 1
            elif (pixel[0] > 57 and pixel[0] < 110) and pixel[1] > 100 and pixel[2] > 40:
                quantityGreenColor += 1

    if ((quantityRedColor / allPixels) > 0.15):
        leftClickM()
    elif((quantityGreenColor / allPixels) > 0.15):
        rightClickM()


def sendCommand():
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("{F6}")
    time.sleep(0.5)
    shell.SendKeys("{UP}")
    time.sleep(0.5)
    shell.SendKeys("{ENTER}")

    
if __name__ == "__main__":
    fishing = False
    sendedCommand = False
    inFlag = False
    outFlag = True
    btn = SwitcherButton()
    soundPlayer = SoundPlayer()
    
    while not btn.quit:
        try:
            soundPlayer.playDeactivated()
            while(btn.flag):
                soundPlayer.playActivated()
                screenshot = np.array(ImageGrab.grab().convert("HSV"))
                if(fishingProcess(screenshot)):
                    pushButton(screenshot)
                    sendedCommand = False
                elif(not sendedCommand):
                    sendCommand()
                    sendedCommand = True
                time.sleep(0.2)
            time.sleep(0.2)
        except BaseException:
            btn.quit = True
            break