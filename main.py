import logging
from QueueWatcher import QueueWatcher

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logging.info('Started')
    # do something
    queueWacher = QueueWatcher()
    # end
    logging.info('Finished')

if __name__ == '__main__':
    main()