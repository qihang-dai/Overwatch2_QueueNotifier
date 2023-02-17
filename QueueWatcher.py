import utils
from utils import logger
import win32gui
from PIL import Image
import mss
import time
class QueueWatcher:
    def __init__(self, window_name="Overwatch"):
        self.window_name = window_name
        self.window = win32gui.FindWindow(None, window_name)
        self.position = (-5,-5)
        self.alive = False
        try:
            self.window_position = win32gui.GetWindowRect(self.window)
            top, left, bottom, right = self.window_position
            height, width = bottom - top, right - left
            logger.info("overwatch window size: %s, %s", width, height)
            logger.info("position: %s", self.window_position)
        except Exception as e:
            logger.error(e)
            logger.error("window not found")
            exit()
    
         
    def is_queue_alive(self):
        return self.alive
    
    def set_alive(self):
        self.alive = True
    
    def set_dead(self):
        self.alive = False
    
    def get_position(self):
        return self.position

    def show_window(self):
        win32gui.ShowWindow(self.window, 3)
        win32gui.SetForegroundWindow(self.window)
        time.sleep(1)

    def get_queueing_image(self):        
        # get the position of the overwatch window
        position = self.window_position
        top, left, bottom, right = position
        height, width = bottom - top, right - left
        # take a screenshot of that monitor and save it. it also works with multiple monitors
        with mss.mss() as sct:
            sct_img = sct.grab(position)
            #save the screenshot
            return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    def set_position(self, screenshot,offset_x=0, offset_y=0):
        ''' set the position of the pixel,
        '''
        x , y = self.position
        if offset_x == 0 and offset_x == 0:
            # get the size of the screenshot
            width, height = screenshot.size
            logger.info("screenshot size: %s, %s", width, height)
            # get a pixel from the top of the screenshot, in the middle
            x = width - width // 10 - 20
            y = height // 10 - 40 
        self.position = (x + offset_x, y + offset_y)
        logger.info("pixel position: %s, %s", self.position[0], self.position[1])
        utils.highlight_pixel(screenshot, self.position[0], self.position[1])
        return self.position
    
    
    def run(self, show = False):
        ''' 
        check if the queue is still active
        return True if the queue is finished

        '''
        self.show_window()
        screenshot = self.get_queueing_image()
        x, y = self.set_position(screenshot)
        self.set_alive()
        prev = screenshot.getpixel((x, y))
        start_time = time.time()
        time.sleep(2)

        #logger 
        logger.info("previous pixel: %s", prev)
        logger.info("previous position: %s, %s", x, y)
        logger.info("start queueing time: %s", utils.make_time_readable(start_time))

        while self.is_queue_alive():
            screenshot = self.get_queueing_image()
            cur_pixel = screenshot.getpixel((x, y))

            time_spent = time.time() - start_time
            time_spent = utils.make_time_spent_readable(time_spent)

            utils.print_rgb_color(rgb=cur_pixel)
            utils.print_rgb_color(rgb=prev)
            if show:
                utils.highlight_pixel(screenshot, x, y)

            logger.info("previous pixel: %s", prev)
            logger.info("current pixel: %s", cur_pixel)

            if utils.is_color_different(cur_pixel, prev):
                self.set_dead()
                logger.info("queue finished, queueing time: %s", time_spent)
                screenshot.show()
                return True
            prev = cur_pixel
            time.sleep(5)
            logger.info("queueing time: %s", time_spent)
        logger.info("queue stopped before it finished, queueing time: %s", time_spent)
        return False
    
        
if __name__ == '__main__':
    q = QueueWatcher()
    q.run(show = True)
