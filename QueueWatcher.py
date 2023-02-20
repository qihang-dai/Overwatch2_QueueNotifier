import utils
from utils import logger
import win32gui
from PIL import ImageGrab
import time
import threading
from sendMail import send
class QueueWatcher:
    def __init__(self, window_name="Overwatch"):
        self.window_name = window_name
        self.window = win32gui.FindWindow(None, window_name)
        self.position = (-5,-5)
        self.alive = threading.Event()
        self.timeInfo = {"start_time": 0, "end_time": 0, "time_spent": 0}
        self.emailInfo = {"email": "", "password": "", "receiver": ""}
    
    def set_email_info(self, email, password, receiver):
        self.emailInfo["email"] = email
        self.emailInfo["password"] = password
        self.emailInfo["receiver"] = receiver
    
    def is_queue_alive(self):
        return self.alive.is_set()
    
    def set_alive(self):
        self.alive.set()
    
    def set_dead(self):
        self.alive.clear()
    
    def get_position(self):
        return self.position
    
    def get_time_info(self):
        return self.timeInfo

    def show_window(self):
        try:
            win32gui.ShowWindow(self.window, 3)
            win32gui.SetForegroundWindow(self.window)
            time.sleep(2)
        except Exception as e:
            logger.error("show window error: %s", e)
            return False

    def get_queueing_image(self):        
        return ImageGrab.grab() #would only grab the main monitor if there are multiple monitors

    def set_position(self, screenshot,offset_x=0, offset_y=0, show = False):
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
        if show:
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
        self.timeInfo["start_time"] = start_time
        time.sleep(2)

        #logger 
        logger.info("previous pixel: %s", prev)
        logger.info("previous position: %s, %s", x, y)
        logger.info("start queueing time: %s", utils.make_time_readable(start_time))
        time_spent = time.time() - start_time
        time_spent = utils.make_time_spent_readable(time_spent)
        while self.is_queue_alive():
            screenshot = self.get_queueing_image()
            cur_pixel = screenshot.getpixel((x, y))

            time_spent = time.time() - start_time
            time_spent = utils.make_time_spent_readable(time_spent)
            self.timeInfo["time_spent"] = time_spent

            utils.print_rgb_color(rgb=cur_pixel)
            utils.print_rgb_color(rgb=prev)
            if show:
                utils.highlight_pixel(screenshot, x, y)

            logger.info("previous pixel: %s", prev)
            logger.info("current pixel: %s", cur_pixel)

            if utils.is_color_different(cur_pixel, prev):
                self.set_dead()
                logger.info("queue finished, queueing time: %s", time_spent)
                send(self.emailInfo["email"], self.emailInfo["password"], self.emailInfo["receiver"])
                return True
            prev = cur_pixel
            time.sleep(5)
            logger.info("queueing time: %s", time_spent)
        logger.info("queue stopped before it finished, queueing time: %s", time_spent)
        return False
    
    def stop(self):
        logger.info("stop queue watcher")
        self.set_dead()
    
    def main(self):
        self.run(show = True)
        self.stop()
    
        
if __name__ == '__main__':
    q = QueueWatcher()
    #run the run function in a thread
    t = threading.Thread(target=q.run, args=(True,))
    t.start()
    #stop the thread after 5 seconds
    time.sleep(5)
    q.stop()
