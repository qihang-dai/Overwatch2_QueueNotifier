from utils import logger
from sendMail import send

def main():
    logger.info("start")
    send()
    

if __name__ == '__main__':
    main()