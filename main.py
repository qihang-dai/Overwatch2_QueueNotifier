from utils import logger
from GUI import QueueWatcherGUI

def main():
    logger.info("start")
    gui = QueueWatcherGUI()
    gui.run()
    

if __name__ == '__main__':
    main()