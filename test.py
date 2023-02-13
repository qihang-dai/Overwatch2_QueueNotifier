import logging, time
import win32gui
import pytesseract
from PIL import Image, ImageGrab
import pyautogui
import mss
from logger import logger


class QueueWatcher:
    def __init__(self):
        self.overwatch_window = win32gui.FindWindow(None, "Overwatch")
        logger.debug("overwatch_window: %s", self.overwatch_window)
        if self.overwatch_window:
            logger.info("detected Overwatch")
        else:
            logger.error("Overwatch not detected")

    def get_queueing_image(self, hide_after_screenshot=False, time_to_wait=2, fullscreen=False, fullscreen_time_to_wait=5):
        ''' take a screenshot of the overwatch_window '''
        # show the overwatch window
        win32gui.ShowWindow(self.overwatch_window, 9)
        win32gui.SetForegroundWindow(self.overwatch_window)
        
        # wait for the window to be shown, else the screenshot will not be correct
        if fullscreen:
            time.sleep(fullscreen_time_to_wait)
        else:
            time.sleep(time_to_wait)

        # get the position of the overwatch window
        position = win32gui.GetWindowRect(self.overwatch_window)
        top, left, bottom, right = position
        height, width = bottom - top, right - left
        logger.info("overwatch window size: %s, %s", width, height)

        # take a screenshot of that monitor and save it. it also works with multiple monitors
        with mss.mss() as sct:
            logger.info("monitor: %s", sct.monitors[1])
            logger.info("position: %s", position)
            sct_img = sct.grab(position)
            #save the screenshot
            screenshot = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            #show the screenshot
            screenshot.show()
            #save the screenshot
            screenshot.save("screenshot.png")

            #grab the entire monitor
            monitor = sct.monitors[1]
            logger.info("monitor: %s", monitor)
            sct_img = sct.grab(monitor)
            #save the screenshot
            screenshot = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            #show the screenshot
            screenshot.show()
        
        # hide the overwatch window again
        if hide_after_screenshot:
            logger.info("hide overwatch window again")
            win32gui.ShowWindow(self.overwatch_window, 6)
        #still cant handle full screen mode
    
    # a method that run all method inside this class
    def run(self):
        # get a screenshot of the queueing screen
        self.get_queueing_image()
        
if __name__ == '__main__':
    q = QueueWatcher()
    q.run()