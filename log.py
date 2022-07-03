import logging
import os.path

class LoggingStrategy:
    def getLogger(self, name: str):
        pass

class FileLogger(LoggingStrategy):
    def __init__(self):
        nameBase = 'game.log'
        curExtension = 1
        filename = nameBase + f'.{curExtension}'
        while os.path.exists(filename):
            curExtension += 1
            filename = nameBase + f'.{curExtension}'
        
        format = logging.Formatter('%(name)s %(message)s')
        self.handler = logging.FileHandler(filename, mode='w')
        self.handler.setFormatter(format)

    def getLogger(self, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.handler)
        return logger

class NoLogging(LoggingStrategy):
    def getLogger(self, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.CRITICAL)
        return logger
