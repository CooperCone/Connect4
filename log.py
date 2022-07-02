import logging
import os.path

def setupLogger():
    global handler
    nameBase = 'game.log'
    curExtension = 1
    filename = nameBase + f'.{curExtension}'
    while os.path.exists(filename):
        curExtension += 1
        filename = nameBase + f'.{curExtension}'

    format = logging.Formatter('%(name)s %(message)s')
    handler = logging.FileHandler(filename, mode='w')
    handler.setFormatter(format)

def getLogger(name: str):
    global handler
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
